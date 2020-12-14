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

# Purposes:
#   a.  provide brief nicknames for te args;
#   b.  provide te args' defaults.

from _usability import *
from _preferences import *
from _common import *
from _formatting_aids import *


"""
**Should** be definitive, but is far from: due to some combination of [a] stdc++
templates all having been instantiated and expanded w/o leaving records
accessible to GDB; and [b] my not invoking GDB's Python API correctly.
"""
def could_custom_teArg_beA (custom_teArg, teArgNickname):
	from gdb.types import get_basic_type
	from gdb import lookup_type
	if not isinstance(custom_teArg,gdb.Type):
		return False
	t = get_basic_type(custom_teArg)
	s = str(t)
	if 'ALLO' == teArgNickname:
		x = sprintf('%s::size_type',s)
		try:
			gdb.lookup_type(x)
		except BaseException as e:
			return False
	"""
	# A few things that **should** work; examples, not exhaustive listing.
	#
	if 'EQ' == teArgNickname or 'CMP' == teArgNickname:
		x = sprintf('bool %s::operator()(const %s &, const %s &) const',
					s, 'float', 'float') # Using "float" as example; not
		# bothering to pass in actual values because doesn't work anyway.
		#
		# And yes, for real would also check for "()(%s,%s)" in case type
		# is primitive and small and hence is just passed by value.
		#
		# And also yes, for real woul check for standalone hasher func too.
		#
		# Approach 1
		syrv = gdb.lookup_symbol(x)
		if None==syrv or None==syrv[0] or ! syrv[0].is_valid():
			return False
		#
		# Approach 2
		sy = gdb.lookup_global_symbol(x)
		if None==sy or ! sy.is_valid():
			return False
		#
		# Approach 3
		try:
			gdb.parse_and_eval('&' + x)
		except BaseException as e:
			return False
		#
	if 'HASH' == teArgNickname:
		x = sprintf('std::size_t %s::operator()(const %s &) const',
					s, 'float') # Same caveats as above.
		# Approach 1, etc.
	"""
	return True


class TeArgs_Rule:
	"""
Rule for generating default te args of an STL type, given the actual te args
from the declaration of an instance of said STL type.  Also assigns a static
nickname to each te param; those nicknames, #-delimited, appear in output of
q-whatis, q-precis, p-afar, and p-type.

Examples of a string pair comprising componentNicknames abound in code; just
search down for \<componentNicknames\>.

Example of string pair comprising elementalCompositions is

	"std::basic_string<char, std::char_traits<char>, std::allocator<char> >"
	&
	"std::basic_string<char, #'TRAITS#, #'ALLO#>"

; that one occurs when we are figuring out concise type designation of
	std::vector<std::string>>
, for example.  The 2nd part of an elementalCompositions pair may be None
; that occurs when the corresponding te arg is not, itself, a templated type.

(NB: *elemental* is what we call a te param without a defaults.  As example
, of the te params of std::set<K,CMP,ALLO> only the first one is elemental.)
________
		componentNicknames     : pair<strExpectedExpansion,strNickname>[]
		elementalCompositions  : pair<strExpectedExpansion,strComposition>[]
	"""
	@staticmethod
	def dump (tar, actual_teArgs, tag=None):
		assert tar!=None
		assert isinstance(tar, TeArgs_Rule)
		nickList = tar.nicknames()
		dtaList = tar.defaultStrings # "dta" = "default te arg"
		printf('%s%s%s\n', FONTmagenta,
			   listCallers(8,omitInnermost=False,stairwise=True) ,resetFONT)
		tagPrefix=''
		if tag !=None:
			tagPrefix = sprintf('/%s%s%s%s/ ',
								FONTyellowBackgd,boldFONT,tag,resetFONT)
		printf('%sDumping teArgsRule [%s]: {{{\n',
			   tagPrefix, tar.__class__.__name__)
		for i in range(max(len(nickList),len(dtaList),len(actual_teArgs))):
			s_nick='----'
			if i < len(nickList):
				s_nick = nickList[i]
			s_dta='----'
			if i < len(dtaList):
				if dtaList[i]:
					s_dta = sprintf('"%s"', dtaList[i])
				else:
					s_dta = '/*None*/'
			s_actual='----'
			if i < len(actual_teArgs):
				s_actual = sprintf('"%s"', actual_teArgs[i])
			widthAdj=int(10) #<<< Only adjust *this* number.
			blueStripe = sprintf('%s%s%s', FONTblue,
								 ''.rjust(max(0,widthAdj-len(s_nick)),'_'),
								 resetFONT)
			printf('    %2u=i  nick=%s %s def=%s\n%*sactu=%s\n',
				   i, s_nick, blueStripe, s_dta, widthAdj+16, '', s_actual)

			if 0 == i: continue
			atea_ty = actual_teArgs[i].strip_typedefs()
			printf('\t\t\t atea_ty:  %s  %s\n',type_codeToStr[atea_ty.code], str(atea_ty))
			ateaA_ty_s = sprintf('%s::size_type',str(atea_ty))
			try:
				gdb.lookup_type(ateaA_ty_s)
				printf('%s have!A\n',ateaA_ty_s)
			except BaseException as whatev:
				printf('%s lack!A\n',ateaA_ty_s)

		if BOTHERwithCOMPONENTS and (len(tar.componentNicknames)):
			printf('___________\n')
			for cN in tar.componentNicknames:
				printf('  & component,  %s%s%s  ==> "%s%s%s"\n',
					   FONTblue,cN[0],resetFONT , boldFONT,cN[1],resetFONT)
		printf('}}} n_elementalTeParams=%u.\n', tar.n_elementalTeParams())
	#
	def __init__ (self):
		self.componentNicknames = [] # Concrete subclasses may populate.
		self.elementalCompositions = [] # Concrete subclasses may populate.
	#
	def str_elementalCompositions (self):
		s=''
		if 0 == len(self.elementalCompositions):
			s += sprintf('%s%s{ }%s', boldFONT,italicFONT,resetFONT)
			return s
		s += sprintf('%s%s{%s\n', boldFONT,italicFONT,resetFONT)
		for i in range(len(self.elementalCompositions)):
			if i > 0:
				s += sprintf('\t%s\n', ''.rjust(70,'-'))
			eC = self.elementalCompositions[i]
			s += sprintf('%u\t%s%s%s\n\t%s%s%s\n', i,
						 FONTblue,eC[0],resetFONT,
						 FONTred ,eC[1],resetFONT)
		s += sprintf('%s%s}%s', boldFONT,italicFONT,resetFONT)
		return s
	#
	def composeElementals (self, inputStrings, outputStrings):
		printf('Time to die;  %s\n', listCallers(6,omitInnermost=False))
		die('%s ! implements composeElementals(); should it?',
			self.__class__.__name__)
	#
	@returns(int)
	def n_elementalTeParams (self): # See class-level comment re "elemental".
		i = int(0)
		for x in self.defaultStrings:
			if None==x: i += int(1)
#		printf('(%s) n_eleme=%u\n',str(self.__class__),i)
		return i


class heterogenous_container (TeArgs_Rule):
	"""
Even twistier than fixedSize_container; here, the # of elems is fixed at
compiletime, and is also the # of types!  Type std::tuple is one.
	"""
	@staticmethod
	def nicknames ( ):
		return ( )
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		cardTypes = len(actual_teArgs)
		tmp_list = []
		for i in range(cardTypes):
			tmp_list.append(None)
		self.defaultStrings = tuple(tmp_list)
	def composeElementals (self, inputStrings, outputStrings):
		tmp_list = []
		for i in range(min(len(inputStrings), len(outputStrings))):
			tmp_list.append( (inputStrings[i],outputStrings[i]) ,)
		self.elementalCompositions = tuple(tmp_list)
		# Here, *every* te param is an elemental.
	def n_elementalTeParams (self):
		return len(self.defaultStrings)


class fixedSize_container (TeArgs_Rule):
	"""
For cases where # of elems is fixed at compiletime, *but* is not given as a
size_t non-type te arg.  Type std::integer_sequence is one.
	"""
	@staticmethod
	def nicknames ( ):
		return ('E')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 1)
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		strE = normalizeTypename(str(typE))
		self.defaultStrings = (None,)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		# Populate elementalCompositions; have no defaultStrings to re-generate.
		self.elementalCompositions = ( (inputStrings[0],strE) ,)

class fixedKnownSize_container (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('E', 'N')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 1)
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		self.defaultStrings = (None,)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		# Populate elementalCompositions; have no defaultStrings to re-generate.
		self.elementalCompositions = ( (inputStrings[0],strE) ,)


class simple_container (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('E', 'ALLO')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert len(actual_teArgs) >= 1
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		strE = normalizeTypename(str(typE))
		self.synthesize(strE)
	def synthesize (self, strE):
		strALLO = fixBroketSpacing(sprintf('std::allocator<%s>', strE))
		self.defaultStrings = (None, strALLO)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		# Read & validate
		strE = outputStrings[0]
		# Populate elementalCompositions, and re-generate defaultStrings.
		self.elementalCompositions = ( (inputStrings[0],strE) ,)
		if strE != None:
			self.synthesize(strE)


class std__deque (simple_container):
	# Superclass defined nicknames(), so we needn't.
	@staticmethod
	def str_componentITER (strE):
		return sprintf('std::_Deque_iterator<%s, %s&, %s*>', strE, strE, strE)
	def __init__ (self, actual_teArgs):
		simple_container.__init__(self, actual_teArgs)
		# Superclass validated param, so we can dispense with assert()s.
		typE = actual_teArgs[0]
		strE = normalizeTypename(str(typE))
		self.synthesize(strE)
	def synthesize (self, strE):
		simple_container.synthesize(self, strE)
#		self.componentNicknames = ( (std__deque.str_componentITER(strE),'ITER') ,)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strE) ,)
		if strE != None:
			self.synthesize(strE)


class helperHASHTABLE:
	def __init__ (self, keysOnly, strK, strKV,
				  actualHASH=None, actualEQ=None, actualALLO=None):
		trait_cacheHashcode=False
		trait_constantIterators=False
		trait_uniqueKeys=True
		if keysOnly:
			self.strEXTRACT_K = 'std::__detail::_Identity'
		else:
			self.strEXTRACT_K = 'std::__detail::_Select1st'
		#
		self.strALLO = nonNull(actualALLO, sprintf('std::allocator<%s >', strKV))
		self.strEQ = nonNull(actualEQ, sprintf('std::equal_to<%s>', strK))
		self.strHASH = nonNull(actualHASH, sprintf('std::hash<%s>', strK))
		#
		self.strRANGE_HASHING = 'std::__detail::_Mod_range_hashing'
		self.strRANGED_HASH = 'std::__detail::_Default_ranged_hash'
		self.strPOL__REHASH = 'std::__detail::_Prime_rehash_policy'
		self.strTRAITS = sprintf('std::__detail::_Hashtable_traits<%s, %s, %s>',
								 ternary(trait_cacheHashcode,'true','false'),
								 ternary(trait_constantIterators,'true','false'),
								 ternary(trait_uniqueKeys,'true','false'))
		#
		toplevFmt = 'std::_Hashtable<%s, %s, %s, %s, %s, %s, %s, %s, %s, %s >'
		self.canonicalFmtToplev = sprintf(toplevFmt,
										  strK, strKV,
										  self.strALLO, self.strEXTRACT_K,
										  self.strEQ, self.strHASH,
										  self.strRANGE_HASHING,
										  self.strRANGED_HASH,
										  self.strPOL__REHASH, self.strTRAITS)
#
class std__Hashtable (TeArgs_Rule): # A *component* of STL container types.
	@staticmethod
	def nicknames ( ):
		return ('K', 'KV', 'ALLO', 'EXTRACT_K', 'EQ', 'HASH',
				'RANGE_HASHING', 'RANGED_HASH', 'POL__REHASH', 'TRAITS')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 2)
		typK = actual_teArgs[0]
		assert isinstance(typK, gdb.Type)
		strK = normalizeTypename(str(typK))
		typKV = actual_teArgs[1]
		assert isinstance(typKV, gdb.Type)
		strKV = normalizeTypename(str(typKV))
		ht = helperHASHTABLE(False, strK, strKV)
		self.defaultStrings = (None, None,
							   ht.strALLO, ht.strEXTRACT_K,
							   ht.strEQ, ht.strHASH,
							   ht.strRANGE_HASHING, ht.strRANGED_HASH,
							   ht.strPOL__REHASH, ht.strTRAITS)


class std__unordered_map (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('K', 'V', 'HASH', 'EQ', 'ALLO')
	def __init__ (self, actual_teArgs):
		assert (len(actual_teArgs) >= 2)
		TeArgs_Rule.__init__(self)
		typK = actual_teArgs[0]
		assert isinstance(typK, gdb.Type)
		typV = actual_teArgs[1]
		assert isinstance(typV, gdb.Type)
		strK = normalizeTypename(str(typK))
		strV = normalizeTypename(str(typV))
		self.synthesize(strK, strV, actual_teArgs)
	def synthesize (self, strK, strV, actual_teArgs=None):
		strHASH = fixBroketSpacing(sprintf('std::hash<%s>', strK))
		strEQ =   fixBroketSpacing(sprintf('std::equal_to<%s>', strK))
		strKV =      fixBroketSpacing(sprintf('std::pair<%s const, %s>', strK, strV))
		strALLO =    fixBroketSpacing(sprintf('std::allocator<%s>', strKV))
		self.defaultStrings = (None, None,
							   strHASH, strEQ, strALLO)
		if None == actual_teArgs: return
		actualHASH = normalizeTypename(str(actual_teArgs[2]))
		actualEQ = normalizeTypename(str(actual_teArgs[3]))
		actualALLO = normalizeTypename(str(actual_teArgs[4]))
		ht = helperHASHTABLE(False, strK, strKV,
							 actualHASH, actualEQ, actualALLO)
		self.componentNicknames = ( (ht.canonicalFmtToplev,'HASHTABLE') ,)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 2 and len(outputStrings) >= 2
		strK = outputStrings[0]
		strV = outputStrings[1]
		self.elementalCompositions = ( (inputStrings[0],strK) ,
									   (inputStrings[1],strV) )
		if strK != None or strV != None:
			self.synthesize(nonNull(strK,inputStrings[0]),
							nonNull(strV,inputStrings[1]))


class std__unordered_set (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('E','HASH','EQ','ALLO')
	def __init__ (self, actual_teArgs):
		assert (len(actual_teArgs) >= 1)
		TeArgs_Rule.__init__(self)
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		strE = normalizeTypename(str(typE))
		self.synthesize(strE, actual_teArgs)
	def synthesize (self, strE, actual_teArgs=None):
		strHASH = fixBroketSpacing(sprintf('std::hash<%s>', strE))
		strEQ = fixBroketSpacing(sprintf('std::equal_to<%s>', strE))
		strALLO = fixBroketSpacing(sprintf('std::allocator<%s>', strE))
		self.defaultStrings = (None, strHASH, strEQ, strALLO)
		if None == actual_teArgs: return
		actualHASH = normalizeTypename(str(actual_teArgs[1]))
		actualEQ = normalizeTypename(str(actual_teArgs[2]))
		actualALLO = normalizeTypename(str(actual_teArgs[3]))
		ht = helperHASHTABLE(True, strE, strE,
							 actualHASH, actualEQ, actualALLO)
		self.componentNicknames = ( (ht.canonicalFmtToplev,'HASHTABLE') ,)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strE) ,)
		if strE != None:
			self.synthesize(strE)


class helperRB_TREE:
	def __init__ (self, strK, strKV):
		self.strEXTRACT_K = sprintf('std::_Select1st<%s >', strKV)
		self.strCMP = sprintf('std::less<%s>', strK)
		self.strALLO = sprintf('std::allocator<%s >', strKV)
		#
		toplevFmt = 'std::_Rb_tree<%s, %s, %s, %s, %s >'
		self.canonicalFmtToplev = sprintf(toplevFmt,
										  strK, strKV,
										  self.strEXTRACT_K, self.strCMP,
										  self.strALLO)
#
class std__Rb_tree (TeArgs_Rule): # A *component* of STL container types.
	@staticmethod
	def nicknames ( ):
		return ('K', 'KV', 'EXTRACT_K', 'CMP', 'ALLO')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		printf('WTF %s\n%u\n', str(actual_teArgs), len(actual_teArgs))
		assert (len(actual_teArgs) >= 2)
		typK = actual_teArgs[0]
		assert isinstance(typK, gdb.Type)
		strK = normalizeTypename(str(typK))
		typKV = actual_teArgs[1]
		assert isinstance(typKV, gdb.Type)
		strKV = normalizeTypename(str(typKV))
		ht = helperRB_TREE(strK, strKV)
		self.defaultStrings = (None, None,
							   ht.strEXTRACT_K, ht.strCMP,
							   ht.strALLO)

class std__map (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('K','V','CMP','ALLO')
	def __init__ (self, actual_teArgs):
		assert (len(actual_teArgs) >= 2)
		TeArgs_Rule.__init__(self)
		#
		typK = actual_teArgs[0]
		assert isinstance(typK, gdb.Type)
		strK = normalizeTypename(str(typK))
		#
		typV = actual_teArgs[1]
		assert isinstance(typV, gdb.Type)
		strV = normalizeTypename(str(typV))
		#
		self.synthesize(strK, strV)
	def synthesize (self, strK, strV):
		strCMP = fixBroketSpacing(sprintf('std::less<%s>', strK))
		strKV = fixBroketSpacing(sprintf('std::pair<%s const, %s>', strK, strV))
		strALLO = fixBroketSpacing(sprintf('std::allocator<%s>', strKV))
		self.defaultStrings = (None, None, strCMP, strALLO)
		rbt = helperRB_TREE(strK, strKV)
		self.componentNicknames = ( (rbt.canonicalFmtToplev,'RB_TREE') ,)
	def composeElementals (self, inputStrings, outputStrings):
#		printf('cE: |inputs|=%u |outputs|=%u\n', len(inputStrings), len(outputStrings))
		assert len(inputStrings) >= 2 and len(outputStrings) >= 2
		if PREF_Debug:
			printf('Given K  %s  ==>  %s\n', inputStrings[0], outputStrings[0])
			printf('Given V  %s  ==>  %s\n', inputStrings[1], outputStrings[1])
		# Read & validate
		strK = outputStrings[0]
		strV = outputStrings[1]
		self.elementalCompositions = ( (inputStrings[0],strK) ,
									   (inputStrings[1],strV) )
		if strK != None or strV != None:
			self.synthesize(nonNull(strK,inputStrings[0]),
							nonNull(strV,inputStrings[1]))


class std__set (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('E','CMP','ALLO')
	def __init__ (self, actual_teArgs):
		assert (len(actual_teArgs) >= 1)
		TeArgs_Rule.__init__(self)
		#
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		strE = normalizeTypename(str(typE))
		self.synthesize(strE)
	def synthesize (self, strE):
		strCMP = fixBroketSpacing(sprintf('std::less<%s>', strE))
		strALLO = fixBroketSpacing(sprintf('std::allocator<%s>', strE))
		self.defaultStrings = (None, strCMP, strALLO)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strE) ,)
		if strE != None:
			self.synthesize(strE)


class simple_sequence_adapter (TeArgs_Rule): # std__queue or std__stack
	@staticmethod
	def nicknames ( ):
		return ('E','CONT')
	def __init__ (self, actual_teArgs):
		assert (len(actual_teArgs) >= 2)
		TeArgs_Rule.__init__(self)
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		strE = normalizeTypename(str(typE))
		self.synthesize(strE)
		#
		typCONT = actual_teArgs[1]
		if str(typCONT).startswith('std::deque<'):
			self.componentNicknames = ( (std__deque.str_componentITER(strE),
										 'DEQUE_ITER') ,)
		#
	def synthesize (self, strE):
		strCONT = fixBroketSpacing(sprintf('std::deque<%s, std::allocator<%s>>',
										   strE,strE))
		self.defaultStrings = (None, strCONT)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strE) ,)
		if strE != None:
			self.synthesize(strE)


class std__priority_queue (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('E','CONT','CMP')
	def __init__ (self, actual_teArgs):
		assert (len(actual_teArgs) >= 2)
		TeArgs_Rule.__init__(self)
		typE = actual_teArgs[0]
		assert isinstance(typE, gdb.Type)
		strE = normalizeTypename(str(typE))
		self.synthesize(strE)
		#
		typCONT = actual_teArgs[1]
		if str(typCONT).startswith('std::deque<'):
			self.componentNicknames = ( (std__deque.str_componentITER(strE),
										 'DEQUE_ITER') ,)
		#
	def synthesize (self, strE):
		strCONT = fixBroketSpacing(sprintf('std::vector<%s, std::allocator<%s>>',
										   strE,strE))
		strCMP = fixBroketSpacing(sprintf('std::less<%s>', strE))
		self.defaultStrings = (None, strCONT, strCMP)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strE = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strE) ,)
		if strE != None:
			self.synthesize(strE)


class std__pair (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('K','V')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 2)
		self.defaultStrings = (None, None)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 2 and len(outputStrings) >= 2
		strK = outputStrings[0]
		strV = outputStrings[1]
		self.elementalCompositions = ( (inputStrings[0],strK) ,
									   (inputStrings[1],strV) )


class std__basic_string (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('CH','TRAITS','ALLO')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 1)
		#
		typCH = actual_teArgs[0]
		assert isinstance(typCH, gdb.Type)
		strCH = normalizeTypename(str(typCH))
		#
		strTRAITS = sprintf('std::char_traits<%s>', strCH)
		strALLO = sprintf('std::allocator<%s>', strCH)
		self.defaultStrings = (None, strTRAITS, strALLO)
	def composeElementals (self, inputStrings, outputStrings):
		pass # 'CH' will not be templated, so that is end of conversation.

class std__basic_string_view (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('CH','TRAITS')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 1)
		#
		typCH = actual_teArgs[0]
		assert isinstance(typCH, gdb.Type)
		strCH = normalizeTypename(str(typCH))
		#
		strTRAITS = sprintf('std::char_traits<%s>', strCH)
		self.defaultStrings = (None, strTRAITS)
	def composeElementals (self, inputStrings, outputStrings):
		pass # 'CH' will not be templated, so that is end of conversation.


class std__unique_ptr (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('T','T_DEL')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 1)
		#
		typT = actual_teArgs[0]
		assert isinstance(typT, gdb.Type)
		strT = normalizeTypename(str(typT))
		self.synthesize(strT)
	def synthesize (self, strT):
		strT_DEL = fixBroketSpacing(sprintf('std::default_delete<%s>', strT))
		self.defaultStrings = (None, strT_DEL)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strT = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strT) ,)
		if strT != None:
			self.synthesize(strT)


class simple_pointer_wrapper (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('T')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 1)
		#
		self.defaultStrings = (None,)
	def composeElementals (self, inputStrings, outputStrings):
		assert len(inputStrings) >= 1 and len(outputStrings) >= 1
		strT = outputStrings[0]
		self.elementalCompositions = ( (inputStrings[0],strT) ,)


class std__ratio (TeArgs_Rule):
	@staticmethod
	def nicknames ( ):
		return ('NUMER', 'DENOM')
	def __init__ (self, actual_teArgs):
		TeArgs_Rule.__init__(self)
		assert (len(actual_teArgs) >= 2)
		strNUMER = str(actual_teArgs[0])
		strDENOM = str(actual_teArgs[1])
		self.defaultStrings = (None,'1')
