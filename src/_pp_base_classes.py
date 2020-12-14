#                                          Copyright 2020 Vainstein K.
# --------------------------------------------------------------------
# This file is part of PrCxx.
# 
# PrCxx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# PrCxx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PrCxx.  If not, see <https://www.gnu.org/licenses/>.

import math

from gdb import *
from gdb.printing import *
from gdb.types import *

from _usability import *
from _codes_stringified import *
from _common import die
from _common import eIteratorStanding
from _common import prAddr
from _common import getValueAtAddress
from _common import debug_stringify_gdbValue
from _common import isStringform
from _common import extractString_from_gdbValue


class PPFault (Exception):
	def __init__ (self, msg):
		self.msg = msg


class BasePP (gdb.printing.PrettyPrinter):
	"""
		miscInfo         : string[]
		traitsInfo       : {collectionName,traitName,traitValue}[]
		sz_used__objProper  : uint
	"""
	@staticmethod
	def isKnownSTL ( ): #Extending non-STL classes *MUST* return False here, instead.
		return True
	def __init__ (self):
		self.miscInfo = []
		self.traitsInfo = []
		self.sz_used__objProper = -1
		pass
	def __call__ (self, _):
		return self.to_string()
	def display_hint (self):
		raise PPFault('display_hint undef by %s; BUG!' %  (self.__class__.__name__))
	def noteMisc (self, miscCharacteristic):
		self.miscInfo.append(assert_string(miscCharacteristic))
	def noteTrait (self, collectionName,traitName,traitValue):
		assert_string(collectionName)
		assert_string(traitName)
		self.traitsInfo.append( (collectionName,traitName,traitValue) )
	def moreInfo (self):
		for x in self.miscInfo:
			printf('%s\n', x)
		#		
		if len(self.traitsInfo):
			printf('traits: {\n')
			for x in self.traitsInfo:
				printf('\t/%s/ %30s = %s\n', x[0], x[1], str(x[2]))
			printf('}\n')
		#
		assert_uint(self.sz_used__objProper)
		printf('sz_used__objProper=%u\n', self.sz_used__objProper)


class ScalarPP (BasePP):
	"""
		scalar : string
	"""
	def __init__ (self, scalar):
		BasePP.__init__(self)
		self.scalar = scalar
	def display_hint (self):
		return 'string'
	def to_string (self):
		return self.scalar


class ScalarHolderPP (ScalarPP):
	"""
		sizeof_payload  : uint
		sizeof_total    : uint
	"""
	def __init__ (self, scalar):
		ScalarPP.__init__(self, scalar)
		self.sizeof_payload = scalar.type.sizeof
		self.sizeof_total = -1


# Any object that contains/wraps a pointer or reference.
class IndirectorPP (BasePP):
	"""
		targetType       : gdb.Type
		targetAddr       : ulong ...uintptr_t, to be precise.
		targetVal        : anyStringifiableType
		sz_overhead      : uint
		empty            : bool
		ownerInfo        : string[]
	"""
	def __init__ (self, targetType):
		assert (isinstance(targetType, gdb.Type))
		BasePP.__init__(self)
		self.targetType = targetType
		self.targetAddr = None
		self.targetVal = None
		self.sz_overhead = -1 # Overhead: anything over 1 word for the pointer.
		self.empty = None
		self.ownerInfo = []
	def figureVal (self):
		if self.targetVal != None:
			return
		assert (self.targetType != None)
		if self.targetAddr==None:
			self.targetVal = gdb.Value('<Empty indirector>')
			return
		if not int(self.targetAddr):
			self.targetVal = gdb.Value('<NULL indirector>')
			return
		self.targetVal = getValueAtAddress(self.targetAddr, self.targetType)
		if self.targetVal==None:
			self.targetVal = gdb.Value('<Bad indirector>')
	def moreInfo (self):
		#
		if self.empty==None:
			printf('empty:N/A\n')
		else:
			assert_bool(self.empty)
			printf('empty:%s\n', str(self.empty))
		#
		if self.targetAddr!=None: # Yes, via s-target-addr will also show this.
			printf('targetAddr=%s\n', prAddr(self.targetAddr))
		#
		assert_uint(self.sz_overhead)
		printf('sz_overhead=%u\n', self.sz_overhead)
		#
		if len(self.ownerInfo):
			printf('ownership: {\n')
			for x in self.ownerInfo:
				printf('\t%s\n', x)
			printf('}\n')
		#
		BasePP.moreInfo(self)
	def display_hint (self):
		self.figureVal()
		return 'string'
	def to_string (self):
		self.figureVal()
		return self.targetVal
	def getTargetAddress (self):
		if None==self.targetAddr:
			die('Object points to/manages nothing.')
		return self.targetAddr


class IteratorPP (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return None
	def __init__ (self, targetType):
		IndirectorPP.__init__(self, targetType)



class AggregatePP (BasePP):
	"""
		elementType            : gdb.Type
		printablesPopulated    : bool
		printables             : anyStringifiableType[]
		elemAddrs              : ulong[]
		nElements              : uint
		nElements_allocated    : uint
		sizeof_element         : uint
		sizeof_node            : uint
		sz_overhead        : uint
		rbTree_height          : uint
		nBuckets               : uint
		bucketLoadStats        : pair<string,string>[]
		hasConventionalElements              : bool
		smallObjectOptimization              : bool
		sz_interstitial_traversal : uint
	"""
	def __init__ (self):
		BasePP.__init__(self)
		self.elementType = None
		self.printablesPopulated = False
		self.printables = []
		self.elemAddrs = []
		### Initialize to -1, so could easily know when not populated.
		self.nElements = -1 # how many valid, legally referenceable, elements.
		self.nElements_allocated = -1
		self.sizeof_element = -1
		self.sizeof_node = -1
		self.sz_overhead = -1 # Overhead: anything except "payload" elements.
		self.rbTree_height = None
		self.nBuckets = None
		self.bucketLoadStats = []
		self.hasConventionalElements = True # conventional: homogenous, size in bytes.
		self.smallObjectOptimization = None
		self.sz_interstitial_traversal = -1
		# Total size = sz_overhead + nElements_allocated * sizeof(elementType)
	def populatePrintables (self):
		raise PPFault('Not yet implemented by %s !!' % (self.__class__.__name__))
	def ensure_printablesPopulated(self):
		if not self.printablesPopulated: self.populatePrintables()
	def children (self):
		self.ensure_printablesPopulated()
		return self.printables
	def display_hint (self):
		pass
	def to_string (self):
		pass
	@returns(int)
	def countElements (self):
		assert_uint(self.nElements)
		return self.nElements
	@returns(bool)
	def hasElement (self, lookupBy):
		raise PPFault('Not yet implemented by %s !!' % (self.__class__.__name__))
	def getElement (self, lookupBy):
		raise PPFault(sprintf('Not yet impld by %s !!', self.__class__.__name__))
	@returns(int)
	def getElementAddress (self, lookupBy):
		raise PPFault(sprintf('Not yet impld by %s !!', self.__class__.__name__))
	def moreInfo (self):
		self.ensure_printablesPopulated()
		#
		if self.hasConventionalElements:
			assert self.elementType!=None
			printf('elementType= %s\n', str(self.elementType))
		#
		if self.sizeof_element < 0 and self.elementType != None:
			self.sizeof_element = int(self.elementType.sizeof)
		if self.hasConventionalElements:
			assert_uint(self.sizeof_element)
			printf('sizeof_element=%u\n', self.sizeof_element)
		#
		assert_uint(self.nElements)
		printf('nElements_valid=%u\n', self.nElements)
		#
		assert_uint(self.nElements_allocated)
		printf('nElements_allocated=%u\n', self.nElements_allocated)
		#
		if self.hasConventionalElements: # and self.sizeof_node >= 0:
			assert_uint(self.sizeof_node)
			printf('sizeof_node=%u\n', self.sizeof_node)
		#
		assert_uint(self.sz_overhead)
		printf('sz_overhead=%u\n', self.sz_overhead)
		#
		if self.elementType != None and self.hasConventionalElements:
			elemSz = self.elementType.sizeof
			totSz = self.sz_overhead + self.nElements_allocated * elemSz
			printf('sz_used__total=%u\n', totSz)
			printf('sz_used__outsideObj=%u\n', totSz - self.sz_used__objProper)
		#
		assert_uint(self.sz_interstitial_traversal)
		printf('sz_interstitial_traversal=%d\n', self.sz_interstitial_traversal)
		#
		if self.smallObjectOptimization != None:
			printf('smallObjectOptimization:%s\n',
				   str(self.smallObjectOptimization))
		#
		if self.rbTree_height != None:
			printf('rbTree_height=%u\n', self.rbTree_height)
		#
		if self.nBuckets != None:
			printf('nBuckets=%u\n', self.nBuckets)
			if self.nBuckets > 0:
				self.reckon_bucketLoadStats()
		if len(self.bucketLoadStats):
			printf('bucketLoadStats: {\n')
			for x in self.bucketLoadStats:
				printf('\t%30s = %s\n', x[0], x[1])
			printf('}\n')
		#
		BasePP.moreInfo(self)
	def relateIter (self, it):
		assert isinstance(it, IteratorPP)
		self.ensure_printablesPopulated()
		s = self.iterStanding(it)
		printf('%s\n', str(s).replace('eIteratorStanding.', ''))
	@returns(eIteratorStanding)
	def iterStanding (self, it):
		pass


class SequencePP (AggregatePP):
	def display_hint (self):
		return 'array'
	def __init__ (self):
		AggregatePP.__init__(self)
	def addElem (self, elem, elemAddr=None):
		assert_uint_orNone(elemAddr)
		i = len(self.printables)
		self.printables.append((str(i),elem))
		if elemAddr:
			self.elemAddrs.append(elemAddr)
	@returns(int)
	def indexAlternatively (self, lookupBy): # Subclasses may override.
		die('Asked to lookup by other than nonnegative integer.')
	def hasElement (self, lookupBy):
		s = str(lookupBy)
		if s.isdecimal(): i = int(lookupBy)
		else:             i = self.indexAlternatively(s)
		assert_uint(i)
		return i < self.nElements
	def getElement (self, lookupBy):
		s = str(lookupBy)
		if s.isdecimal(): i = int(lookupBy)
		else:             i = self.indexAlternatively(s)
		assert_uint(i)
		if i >= self.nElements:
			die('Out-of-bounds: =[=%u=]= >= =[=%u=]= = size.'%(i, self.nElements))
		return self.printables[i]
	def getElementAddress (self, lookupBy):
		s = str(lookupBy)
		if s.isdecimal(): i = int(lookupBy)
		else:             i = self.indexAlternatively(s)
		assert_uint(i)
		if i >= self.nElements:
			die('Out-of-bounds: =[=%u=]= >= =[=%u=]= = size.'%(i, self.nElements))
		if 0 == len(self.elemAddrs):
			raise PPFault('Elem addresses not collected; BUG?')
		return self.elemAddrs[i]



class AssociativePP (AggregatePP): # a.k.a. "KeyedLookup"
	"""
		keysOnly       : bool
		keyAddrs       : ulong[]
		nodeAddrs      : ulong[]     // For "iterator standing" questions.
		stringformKeys : bool
	"""
	def __init__ (self, keysOnly):
		assert_bool(keysOnly)
		AggregatePP.__init__(self)
		self.keysOnly = keysOnly # None # elemType is K if keysOnly, else std::pair<K,V>
		self.keyAddrs = []
		self.nodeAddrs = []
		self.stringformKeys=None
	def decide_whether_stringformKeys (self, kType):
		self.stringformKeys = isStringform(kType)
	def display_hint (self):
		if self.keysOnly:
			return 'array'
		else:
			return 'map'
	def addElem_Key (self, key, keyAddr=None,
					 nodeAddr=None):
		assert(self.keysOnly == True)
		assert_uint_orNone(keyAddr)
		assert_uint_orNone(nodeAddr)
		i = len(self.printables)
		self.printables.append((str(i),key))
		if keyAddr:
			self.keyAddrs.append(keyAddr)
			self.elemAddrs.append(keyAddr)
		if nodeAddr:
			self.nodeAddrs.append(nodeAddr)
	def addElem_KeyVal (self, key, val, keyAddr=None, valAddr=None,
						nodeAddr=None):
		assert(self.keysOnly == False)
		assert_uint_orNone(keyAddr)
		assert_uint_orNone(valAddr)
		assert_uint_orNone(nodeAddr)
		assert(0 == (len(self.printables) % 2))
		i = len(self.printables) / 2
		self.printables.append((str(int(2 * i)), key))
		self.printables.append((str(int(2 * i + 1)), val))
		if keyAddr:
			self.keyAddrs.append(keyAddr)
		if valAddr:
			self.elemAddrs.append(valAddr)
		if nodeAddr:
			self.nodeAddrs.append(nodeAddr)
	@returns(bool)
	def sameAs (self, key, printables_gdbValue):
		if self.stringformKeys:
			comparandA = key
#			printf('compA = [%s]\n', comparandA)
			comparandB = extractString_from_gdbValue(printables_gdbValue)
#			printf('compB = [%s]\n', comparandB)
			return comparandA == comparandB
		elif key.isdigit():
			return int(key) == int(printables_gdbValue)
		else: # Hope for the best!
			return key == printables_gdbValue
	def hasElement (self, key):
		assert self.stringformKeys!=None
#		printf('repr(key) = %s; len=%u\n', repr(key), len(key))
#		printf('str? %s\n', str(isinstance(key,str)))
#		printf('int? %s\n', str(isinstance(key,numbers.Integral)))
		if self.keysOnly:
			for i in range(0, self.nElements, 1):
				if self.sameAs(key, self.printables[i][1]): return True
		else:
			for i in range(0, self.nElements, 2):
				if self.sameAs(key, self.printables[i][1]): return True
		return False
	def getElement (self, key):
		assert self.stringformKeys!=None
		if self.keysOnly:
			for i in range(0, self.nElements, 1):
				if self.sameAs(key, self.printables[i][1]): return self.printables[i]
		else:
			for i in range(0, self.nElements, 2):
				if self.sameAs(key, self.printables[i][1]): return self.printables[i+1]
		die('Found no element keyed by =[=%s=]=', str(key))
	def getElementAddress (self, key):
		assert self.stringformKeys!=None
		if self.keysOnly:
			for i in range(0, self.nElements, 1):
				if self.sameAs(key, self.printables[i][1]): return self.elemAddrs[i]
		else:
			for i in range(0, self.nElements, 2): # Must use "//" when dividing integers.
				if self.sameAs(key, self.printables[i][1]): return self.elemAddrs[i//2]
		die('Found no element keyed by =[=%s=]=' % (str(key)))
	def getElementKeyAddress (self, key):
		assert self.stringformKeys!=None
		if self.keysOnly:
			for i in range(0, self.nElements, 1):
				if self.sameAs(key, self.printables[i][1]): return self.keyAddrs[i]
		else:
			for i in range(0, self.nElements, 2): # Must use "//" when dividing integers.
				if self.sameAs(key, self.printables[i][1]): return self.keyAddrs[i//2]
		die('Found no element keyed by =[=%s=]=' % (str(key)))



from _formatting_aids import *

def dump_ppObj_internalLookups (ppObj):
	ppClass = ppObj.__class__
	isScalar = issubclass(ppClass, ScalarPP)
	isAssoc = issubclass(ppClass, AssociativePP)
	eachElem_isKVPair = isAssoc and not getattr(ppObj,'keysOnly',False)
	if issubclass(ppClass, AggregatePP):
		ppObj.ensure_printablesPopulated()
	#
	len_printables = -1
	len_elemAddrs = -1
	len_keyAddrs = -1
	len_nodeAddrs = -1
	if hasattr(ppObj,'printables'):
		len_printables = len(getattr(ppObj,'printables'))
	if hasattr(ppObj,'elemAddrs'):
		len_elemAddrs = len(getattr(ppObj,'elemAddrs'))
	if hasattr(ppObj,'keyAddrs'):
		len_keyAddrs = len(getattr(ppObj,'keyAddrs'))
	if hasattr(ppObj,'nodeAddrs'):
		len_nodeAddrs = len(getattr(ppObj,'nodeAddrs'))
	#
	printf('|printables|=%d nElements=%d ',
		   len_printables, getattr(ppObj,'nElements',-1))
	printf('isAssoc:%c keysOnly:%c amMulti:%c stringformKeys:%c\n\n',
		   bool_to_char(isAssoc),
		   boolOrNone_to_char(getattr(ppObj,'keysOnly',None)),
		   boolOrNone_to_char(getattr(ppObj,'amMulti',None)),
		   boolOrNone_to_char(getattr(ppObj,'stringformKeys',None)))
	#
	if isScalar:
		printf('Scalar.\n____________________\n%s\n', debug_stringify_gdbValue(ppObj.scalar))
		return
	sep = '  '
	printf(' i %s elemAddr %s  keyAddr %s nodeAddr %s %s\n',
		   sep,sep,sep,sep, ternary(eachElem_isKVPair,'vKey --> vValue','vElem'))
	printf('___%s__________%s__________%s__________%s________________________\n',
		   sep,sep,sep,sep)
	i = 0
	while True:
		s = ''
		#
		s += sep
		if i < len_elemAddrs:
			s += prAddr(ppObj.elemAddrs[i])
		else:
			s += ''.rjust(10)
		#
		s += sep
		if i < len_keyAddrs:
			s += prAddr(ppObj.keyAddrs[i])
		else:
			s += ''.rjust(10)
		#
		s += sep
		if i < len_nodeAddrs:
			s += prAddr(ppObj.nodeAddrs[i])
		else:
			s += ''.rjust(10)
		#
		s += sep
		if eachElem_isKVPair and (i*2 +1) < len_printables:
			s += sprintf('%s[%s] --> %s[%s]',
						 ppObj.printables[i*2][0],
						 debug_stringify_gdbValue(ppObj.printables[i*2][1]),
						 ppObj.printables[i*2 +1][0],
						 debug_stringify_gdbValue(ppObj.printables[i*2 +1][1]))
		elif not eachElem_isKVPair and i < len_printables:
			s += sprintf('%s[%s]',
						 ppObj.printables[i][0],
						 debug_stringify_gdbValue(ppObj.printables[i][1]))
		#
		if s.isspace(): # If all-spaces, we've run out lookup entries to print.
			break
		printf('%s%3u%s%s\n', FONTmagenta,i,resetFONT, s)
		i += 1


import _indent_spec

def dump_ppObj_pythonClassDerivation (ppObj):
	indents = _indent_spec.IndentSpec(0)
	ppClass = ppObj.__class__
	while True:
		indents.incrIndent(2)
		printf('%s', ppClass.__name__)
		if 'BasePP' == ppClass.__name__:
			break
		indents.newLine_misc()
		printf('\\_  ')
		ppClass = ppClass.__bases__[0]
	printf('\n')
