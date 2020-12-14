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

import copy
import functools

from _usability import *
from _preferences import *
from _codes_stringified import *
from _common import *
from _formatting_aids import *
import _indent_spec
import _te_arg_profile
from _te_arg_profile import eActualTeArgKind, TeArg_Profile__Deck
from _te_args_rules import *

import _stl_iterators

from gdb import *
from gdb.printing import *
from gdb.types import *

def addrcStorageCategory (addrc):
	if addrc and (addrc in addr_classToStr):
		if not addrc in (gdb.SYMBOL_LOC_TYPEDEF, gdb.SYMBOL_LOC_BLOCK):
			return addr_classToStr[addrc]
	return None


def simplifyTypename__substTeArgNicknames (tyNameShow,
										   teArgs_strList__concise, teArgs_strList):
	import copy
	cfid = next_callFrameId()
	s = copy.deepcopy(tyNameShow)

	if PREF_Debug:
		printf('%s suTeArgNi-0 "%s%s%s%s"\n\t teArgs_strList__concise= %s\n\t teArgs_strList= %s\n',
			   cfid, boldFONT,FONTmagenta,tyNameShow,resetFONT,
			   toOnelineStr_aList(teArgs_strList__concise,FONTblue),
			   toOnelineStr_aList(teArgs_strList,FONTblue))
	if len(teArgs_strList__concise) > len(teArgs_strList):
		if PREF_Debug:
			printf('%s suTeArgNi-1  No-op, because |teArgs_strList__concise| > |teArgs_strList|\n',cfid)
		return s
	teArgsConcise = '<' + ', '.join(teArgs_strList__concise) + '>'
	teArgsConcise = fixBroketSpacing(teArgsConcise)
	i_teArgList_start = s.find('<')
	if i_teArgList_start >= 0:
		exchangeTo = s[:i_teArgList_start] + teArgsConcise
		if s == exchangeTo:
			if PREF_Debug:
				printf('%s suTeArgNi-4  No-op, because same.\n', cfid)
			return s
		traceExchg('suR-bst', s,True,exchangeTo  , traceSuccess=SUBST_Debug)
		s = exchangeTo
		if PREF_Debug:
			printf('%s suTeArgNi-2  Exchanged into "%s%s%s%s"\n', cfid, boldFONT,FONTmagenta,s,resetFONT)
	else:
		if PREF_Debug:
			printf('%s suTeArgNi-3  No-op, because not found "<"\n', cfid)
	return s


@accepts(gdb.Frame)
def blockOfFrame (fr):
	b = None
	if fr and hasattr(fr,'block'):
		try:
			b = fr.block()
		except BaseException as whatev: None
	return b

def blockFromAddr (a):
	b = None
	try:
		return gdb.block_for_pc(int(a))
	except BaseException as err:
#		printf('\nCannot blockFromAddr(%s): %s\n', prAddr(a), str(err))
		return None

@accepts(gdb.Block)
def blockValid (blo):
	return (blo!=None) and hasattr(blo,'is_valid') and blo.is_valid()

def nameTypeConcisely_S (s):
	s = s.replace('unsigned ', 'u_')
	return s

def sprintfAltName (label, nameStr):
	return sprintf('%s%s%s="%s%s%s"',
				   underscFONT,label,resetFONT, FONTmagenta,nameStr,resetFONT)


class UnravelDepth:
	"""
		dElab   : uint
		dTempl  : uint
	"""
	def __init__ (self):
		self.dElab  = int(0)
		self.dTempl = int(0)
	def __str__ (self):
		return sprintf('d{Elab=%d,Templ=%d}', self.dElab, self.dTempl)
	def mkIncr_dElab (self):
		ud = UnravelDepth()
		ud.dElab  = self.dElab + 1
		ud.dTempl = self.dTempl
		return ud
	def mkIncr_dTempl (self):
		ud = UnravelDepth()
		ud.dElab  = self.dElab
		ud.dTempl = self.dTempl + 1
		return ud
	def dbgIndent (self):
		return ''.ljust(4 * (self.dElab + self.dTempl))


class Elaboration:
	# A single obj can combine is_rvalRef + is_ptr, but not is_lvalRef + is_ptr !
	def __init__ (self):
		self.targetType_isConst = False # only if: ptr or lvalRef.
		self.targetType_isVolatile = False # only if: ptr or lvalRef.
		self.is_rvalRef = False
		self.is_lvalRef = False
		self.is_ptr = False
		self.objItself_isConst = False # only if: neither lval nor rval, depth 0.
		self.objItself_isVolatile = False # only if: not rval, depth 0.
		self.arrayDimensions = '' # E.g.  "[][100][3]"
	def __str__ (self):
		emphBeg = boldFONT + FONTyellowBackgd # Emphasize elab elements this instance has.
		s = sprintf('%s%s<<%s', FONTblue,boldFONT,resetFONT)
		s += ' '
		s += sprintf('%stypNam%s', italicFONT,resetFONT)
		s += ' '
		if self.targetType_isConst:     s += sprintf('%sC%s', emphBeg,resetFONT)
		else:                           s += sprintf('%sC%s', italicFONT,resetFONT)
		if self.targetType_isVolatile:  s += sprintf('%sV%s', emphBeg,resetFONT)
		else:                           s += sprintf('%sV%s', italicFONT,resetFONT)
		s += ' '
		if self.is_ptr:                 s += sprintf('%s*%s', emphBeg,resetFONT)
		else:                           s += sprintf('%s*%s', italicFONT,resetFONT)
		s += ' '
		if self.objItself_isConst:      s += sprintf('%sC%s', emphBeg,resetFONT)
		else:                           s += sprintf('%sC%s', italicFONT,resetFONT)
		if self.objItself_isVolatile:   s += sprintf('%sV%s', emphBeg,resetFONT)
		else:                           s += sprintf('%sV%s', italicFONT,resetFONT)
		s += ' '
		if self.is_rvalRef:             s += sprintf('%s&&%s', emphBeg,resetFONT)
		elif self.is_lvalRef:           s += sprintf('%s&%s',  emphBeg,resetFONT)
		else:                           s += sprintf('%s&%s', italicFONT,resetFONT)
		s += ' '
		s += sprintf('%sobjNam%s', italicFONT,resetFONT)
		s += ' '
		if len(self.arrayDimensions): s += sprintf('%s%s%s', emphBeg,
												   self.arrayDimensions,resetFONT)
		else:                         s += sprintf('%s[]%s', italicFONT,resetFONT)
		s += ' '
		s += sprintf('%s%s>>%s', FONTblue,boldFONT,resetFONT)
		return s
	@returns(bool)
	def validate (self, ud):
		depth = ud.dElab
		inconsistencies = []
		if self.is_lvalRef and self.is_rvalRef:
			inconsistencies.append('both lvalRef and rvalRef')
		if self.is_lvalRef and self.is_ptr:
			inconsistencies.append('both lvalRef and ptr')
		if self.targetType_isConst and self.is_rvalRef:
			inconsistencies.append('targetType_isConst and yet rvalRef')
		if self.targetType_isConst and not self.is_ptr and not self.is_lvalRef:
			inconsistencies.append('targetType_isConst but is not indirector')
		if self.is_rvalRef and self.objItself_isConst:
			inconsistencies.append('rvalRref and objItself_isConst')
		if depth and self.objItself_isConst:
			inconsistencies.append('depth>0 and objItself_isConst')
		if depth and self.objItself_isVolatile:
			inconsistencies.append('depth>0 and objItself_isVolatile')
		if len(inconsistencies):
			printf('\nElab inconsistencies: %s%s{%s%s\n%s%s}%s\n',
				   FONTred,boldFONT,resetFONT,
				   '\n,\t'.join(inconsistencies),
				   FONTred,boldFONT,resetFONT)
		return not len(inconsistencies)
	@returns(bool)
	def trivial (self):
		return (not self.targetType_isConst and
				not self.is_rvalRef and
				not self.is_lvalRef and
				not self.is_ptr and
				not self.objItself_isConst and
				not self.objItself_isVolatile and
				0 == len(self.arrayDimensions))
	@staticmethod
	def diptychCandV (isC,isV):
		if isC and isV:
			return 'CV'
		elif isC:
			return 'C '
		elif isV:
			return ' V'
		else:
			return '  '
	@staticmethod
	def extract_CandV__objItself (t, elab):
		s = str(t)
		if ELAB_Debug: printf('\tchk CandV__objItself %s%s%s //%s//\n',
							  FONTblue,s,resetFONT, type_codeToStr[t.code])
		if s.endswith(' const volatile') or s.endswith(' volatile const'):
			elab.objItself_isConst=True
			elab.objItself_isVolatile=True
		else:
			elab.objItself_isConst    = t == t.const()
			elab.objItself_isVolatile = t == t.volatile()
		if ELAB_Debug:
			printf('\tdecided ...objItself [%s]\n', Elaboration.diptychCandV(
				elab.objItself_isConst, elab.objItself_isVolatile))
	@staticmethod
	def extract_CandV__targetType (t, elab):
		s = str(t)
		if ELAB_Debug: printf('\tchk CandV__targetType %s%s%s //%s//\n',
							  FONTblue,s,resetFONT, type_codeToStr[t.code])
		if s.startswith('const volatile ') or s.startswith('volatile const '):
			elab.targetType_isConst=True
			elab.targetType_isVolatile=True
		else:
			elab.targetType_isConst    = t == t.const()
			elab.targetType_isVolatile = t == t.volatile()
		if ELAB_Debug:
			printf('\tdecided ...targetType [%s]\n', Elaboration.diptychCandV(
				elab.targetType_isConst, elab.targetType_isVolatile))
	@staticmethod
	def extract (tMaybeElaborate, ud):
		assert isinstance(tMaybeElaborate, gdb.Type)
		assert isinstance(ud, UnravelDepth)
		elab = Elaboration()
		t = tMaybeElaborate
		if ELAB_Debug: printf('\n/00/ %s  //%s\n', str(t), type_codeToStr[t.code])
		# Must remember to keep calling strip_typedefs(), because code of a
		# typedef'd type is TYPE_CODE_TYPEDEF and not TYPE_CODE_whatReallyIs.
		t = t.strip_typedefs()
		if ELAB_Debug: printf('/20/ %s\n', str(t))
		#
		# Unwrap CV-qualifiers of obj itself.
		if 0 == ud.dElab and t.unqualified().strip_typedefs() != t:
			Elaboration.extract_CandV__objItself(t,elab)
			t = t.unqualified().strip_typedefs()
			if ELAB_Debug: printf('/30/ %s\n', str(t))
		#
		# Unwrap lvalueRef.
		if t.code == TYPE_CODE_REF:
			assert(not elab.is_ptr)
			elab.is_lvalRef = True
			t = t.target().strip_typedefs()
			if ELAB_Debug: printf('/40/ %s\n', str(t))
			# Unwrap CV-qualifiers of targetType, if target is *lvalueReferred-to*.
			# You'd think so, but actually no!!
			Elaboration.extract_CandV__objItself(t,elab)
			t = t.unqualified().strip_typedefs()
			if ELAB_Debug: printf('/44/ %s\n', str(t))
		#
		# Unwrap rvalueRef.
		if t.code == TYPE_CODE_RVALUE_REF:
			assert(not elab.is_lvalRef)
			elab.is_rvalRef = True
			t = t.target().strip_typedefs()
			if ELAB_Debug: printf('/50/ %s\n', str(t))
		#
		# Unwrap array-ness.
		while hasattr(t,'code') and TYPE_CODE_ARRAY == t.code:
			dimensionWrapper = invoke_nothrow(gdb.Type.range,t)
			if dimensionWrapper and 2 == len(dimensionWrapper):
				elab.arrayDimensions += sprintf('[%u]', dimensionWrapper[1] + 1)
			else:
				printf('\n%sERR!%s t=%s arrDim=%s ; %s\n', FONTred, resetFONT,
					   str(t), elab.arrayDimensions,str(dimensionWrapper))
				elab.arrayDimensions=''
				break
			t = t.target().strip_typedefs() # Get type of elements
			if ELAB_Debug: printf('/60/ %s\n', str(t))
		#
		if len(elab.arrayDimensions):
			# Unwrap CV-qualifiers of the array elements themselves.
			Elaboration.extract_CandV__objItself(t,elab)
			t = t.unqualified().strip_typedefs()
			if ELAB_Debug: printf('/70/ %s\n', str(t))
		#
		# Unwrap ptr.
		if t.code == TYPE_CODE_PTR:
			elab.is_ptr = True
			t = t.target().strip_typedefs()
			if ELAB_Debug: printf('/80/ %s\n', str(t))
			# Unwrap CV-qualifiers of targetType, if target is *pointed-to*.
			Elaboration.extract_CandV__targetType(t,elab)
			t = t.unqualified().strip_typedefs()
			if ELAB_Debug: printf('/88/ %s\n', str(t))
		#
		if ELAB_Debug: printf('/99/ %s\n\t; elab is  %s\n', str(t), str(elab))
		return (t,elab)
	@staticmethod
	@returns(str)
	def decorate (tStr, elab): # For simple display of type not associated w an obj
		assert_string(tStr)
		assert isinstance(elab,Elaboration)
		s = tStr
		if elab.targetType_isVolatile: s = 'volatile ' + s
		if elab.targetType_isConst:    s = 'const ' + s
		if elab.is_rvalRef: s += '&& '
		if elab.is_lvalRef: s += '& '
		if elab.is_ptr:     s += ' *'
		if elab.objItself_isConst:    s += ' const'
		if elab.objItself_isVolatile: s += ' volatile'
		if len(elab.arrayDimensions): s += (' ' + elab.arrayDimensions)
		return s


class DeepField:
	"""
		depth                  : uint
		tToplev                : gdb.Type
		offsParent_fromToplev  : uint
		isKnownSTL             : bool
		effStatic              : bool
		vThis                   : gdb.Value
		fThis                   : gdb.Field
		fParent                 : gdb.Field
		fAncest                 : gdb.Field // a field of the top-lev type.
	"""
	def __init__ (self, depth, tToplev, offsParent_fromToplev, # in bytes!
				  isKnownSTL, effStatic, vThis, fThis, fParent, fAncest,
				  fVirtualBase):
		assert isinstance(tToplev, gdb.Type)
		assert ((None==vThis) or isinstance(vThis, gdb.Value))
		assert isinstance(fThis, gdb.Field)
		assert ((not fParent) or isinstance(fParent, gdb.Field))
		assert ((not fAncest) or isinstance(fAncest, gdb.Field))
		assert ((not fVirtualBase) or isinstance(fVirtualBase, gdb.Field))
		self.depth                   = assert_uint(depth)
		self.tToplev                 = tToplev
		self.offsParent_fromToplev   = -999999 # Patently bogus.
		if offsParent_fromToplev >= 0:
			self.offsParent_fromToplev   = offsParent_fromToplev
		self.isKnownSTL              = isKnownSTL
		self.effStatic               = assert_bool(effStatic)
		self.vThis                   = vThis
		self.fThis                   = fThis
		self.fParent                 = fParent
		self.fAncest                 = fAncest
		#
		if isVirtualBase(self.fThis): ### Is this a virtual base?
			# A virtual base will always have same offset *from end* as it
			# did in the original virtual deriver class; in other words.
			virtDeriver = self.fThis.parent_type
			offsBase_fromEndOf_virtDeriver = ((virtDeriver.sizeof * 8) +
											  self.fThis.bitpos)
			offsBase_fromEndOf_ourToplev = offsBase_fromEndOf_virtDeriver
			self.offsTot_fromToplev = ((self.tToplev.sizeof * 8) -
									   offsBase_fromEndOf_ourToplev)
		elif fVirtualBase !=None: ### Have we a virtual base ancestor (any level)?
			virtDeriver = fVirtualBase.parent_type
			offsBase_fromEndOf_virtDeriver = ((virtDeriver.sizeof * 8) +
											  fVirtualBase.bitpos)
			offsBase_fromEndOf_ourToplev = offsBase_fromEndOf_virtDeriver
			self.offsTot_fromToplev = ((self.tToplev.sizeof * 8) -
									   offsBase_fromEndOf_ourToplev +
									   self.offsThis_fromParent())
		else:
			self.offsTot_fromToplev = ((self.offsParent_fromToplev * 8) +
									   self.offsThis_fromParent())
		#
		if FIELD_Debug:
			printf('\n%s\n',str(self))
	#
	def isToplev (self):
		return None == self.fParent
	def isLeaf (self):
		fType = get_basic_type(self.fThis.type)
		if not couldHaveFields(fType):
			return True
		for f in self.fThis.type.fields():
			if not hasattr(f,'bitpos'): continue # static?
			return False
		return True
	#
	def isStatic_inParent (self):
		return not hasattr(self.fThis,'bitpos')
	def offsThis_fromParent (self): ## In bits!
		if self.isStatic_inParent():
			return 0
		return abs(int(self.fThis.bitpos))
	def absoluteAddrSize_bytes (self, v_toplev):
		if v_toplev==None:
			return (None,None)
		if not hasattr(v_toplev,'address'):
			return (None,None)
		toplevAddr = int(v_toplev.address)
		if self.isStatic_inParent(): # In this case, use .address
			return (None,None) # of the field's gdb.Value if can.
		absAddr_bytes = toplevAddr + int(self.offsTot_fromToplev) / 8
		return (absAddr_bytes , self.fThis.type.sizeof)
	def isWaferthinNonleafBase (self):
		if not self.fThis.is_base_class: return False
		card_layoutContributingIvars = int(0)
		couldBeLeaf = True
		couldBeWaferthin = True
		for f in self.fThis.type.fields():
			if f.is_base_class:
				continue
			if couldHaveFields(f.type):
				couldBeLeaf = False
				continue
			if hasattr(f,'bitpos'):
				couldBeWaferthin = False
				continue # not static?
		return couldBeWaferthin and couldBeLeaf
	def getBitsize_countingTowardTotal (self):          ## In bits, like it says.
		assert (not self.effStatic)
		if self.fThis.is_base_class:
			return 0
		if self.fThis.bitsize:
			return self.fThis.bitsize
		assert (self.fThis.type)
		return self.fThis.type.sizeof * 8
	def __str__ (self):
		fParent_name = '??'
		fAncest_name = '??'
		if self.fParent: fParent_name = self.fParent.name
		if self.fAncest: fAncest_name = self.fAncest.name
		offs = ''
		if self.isStatic_inParent():
			offs = 'N/A(static)'
		else:
			offs = sprintf('{tot=%d toplevToPar=%d parToMe=%d}',
						   self.offsTot_fromToplev,
						   self.offsParent_fromToplev,
						   int(self.fThis.bitpos))
			if self.fThis.bitpos < 0:
				offs += sprintf('(asGiven=%d)', self.fThis.bitpos)
		thisTypeName = ''
		fTypeSimple = self.fThis.type#.strip_typedefs()
		if fTypeSimple.name:
			thisTypeName = nameTypeConcisely_S(fTypeSimple.name)
		else:
			fTypeSimple = fTypeSimple.strip_typedefs()
			if fTypeSimple.name:
				thisTypeName = nameTypeConcisely_S(fTypeSimple.name)
			else:
				thisTypeName = nameTypeConcisely_S(str(fTypeSimple))
		s = sprintf('%s%s%s "%s%s%s"\n\\______dep=%u,leaf?%c offs:%s '\
					'Par"%s" Anc"%s" %s',
					boldFONT,thisTypeName,resetFONT,
					FONTred,nonNull(self.fThis.name,'??'),resetFONT,
					self.depth, bool_to_char(self.isLeaf()), offs,
					fParent_name,
					fAncest_name, type_codeToStr[fTypeSimple.code])
		return s

def cmp_deepFields (x, y):
	# Statics go first
	if x.effStatic and not y.effStatic:
		return -1
	if not x.effStatic and y.effStatic:
		return 1
	if x.effStatic and y.effStatic:
		return x.fThis.name < y.fThis.name
	# Everyone else, by offset from toplev type; or ...
	x__offsTot = x.offsTot_fromToplev
	y__offsTot = y.offsTot_fromToplev
	if x__offsTot < y__offsTot:
		return -1
	if x__offsTot > y__offsTot:
		return 1
	# ... if offset-from-toplev same, by depth (so bases sort first!); ...
	if x.depth < y.depth:
		return -1
	if x.depth > y.depth:
		return 1
	# ... if depth same, by name (so plain bases sort before virtual!).
	return x.fThis.name < y.fThis.name


def dump_listed_deepFields (dfList, tag):
	printf('\n_____________________________________ Dumping %s:\n', tag)
	for df in dfList:
		printf('\t%s\n', str(df))
	printf('...done dumping %s______________________________.\n', tag)


def nameTypeConcisely (cxxType): # Caller responsible to strip_typedefs() beforehand.
	if TYPE_CODE_ARRAY == cxxType.code:
		cxxType_ofElements = cxxType.target().strip_typedefs()
		arrayBoundaryIndices = invoke_nothrow(gdb.Type.range,cxxType)
		nElementsDescriptor='??'
		if arrayBoundaryIndices and len(arrayBoundaryIndices) > 1:
			nElementsDescriptor = sprintf('%u', arrayBoundaryIndices[1] + 1)
		return sprintf('%s[%s]',
					   nameTypeConcisely(cxxType_ofElements), nElementsDescriptor)
	else:
		s = cxxType.name
		constQualifier = ''
		if cxxType == cxxType.const():
			constQualifier = ' const'
		if s:
			return sprintf('%s%s', nameTypeConcisely_S(s), constQualifier)
		else:
			return nameTypeConcisely_S(str(cxxType)) # '???'


def list_deepFields (results, tParent, depth, tToplev, offsParent_fromToplev # in bytes!!
					 , effStatic, vParent, tToplev_isKnownSTL, fParent=None, fAncest=None
					 , fVirtualBase=None):
	par_isStruOrUni = get_basic_type(tParent).code in (TYPE_CODE_STRUCT, TYPE_CODE_UNION)
	if PREF_Debug:
		(fParent_name,fAncest_name) = ( getattr(fParent,'name','??') , getattr(fAncest,'name','??') )
		printf('\nIn l_dF();  %2u=|res| %u=dep %3d=offsPar_Toplev effSta=%c ' \
			   'tPar=%s, fPar=%s fAnc=%s; tToplev_isKnownSTL=%c\n',
			   len(results), depth, offsParent_fromToplev, bool_to_char(effStatic),
			   tParent.name, fParent_name, fAncest_name, bool_to_char(tToplev_isKnownSTL))
	pass__fVirtualBase = None
	if fParent!=None and isVirtualBase(fParent):  pass__fVirtualBase = fParent
	else:                                         pass__fVirtualBase = fVirtualBase

	for name,fThis in deep_items(tParent):
		tcod = ternary(fThis.type, type_codeToStr[fThis.type.code], '??')
		pass__effStatic = effStatic
		fThis_offs = 0 # Offset of this field from its immediate-parent type.
		if hasattr(fThis,'bitpos'): # If fThis isn't static
			assert(0 == (fThis.bitpos % 8)) # XXX Deal with
			fThis_offs = int(fThis.bitpos / 8)
		else:
			pass__effStatic = True
		isBase = fThis.is_base_class
		tThis = fThis.type
		if tThis:
			tThis = tThis.unqualified()
			fund_tThis = tThis.strip_typedefs()
			tThis_isKnownSTL = couldHaveFields(fund_tThis) and (gdbType_to_ppClass(fund_tThis,False)[0] !=None)
		else:
			tThis_isKnownSTL = False
		if FIELD_Debug: printf('\ndep=%u %s%s%s tThis=%s isKnownSTL:%s\n', depth,
							   FONTcyanBackgd,fThis.name,resetFONT, str(tThis), str(tThis_isKnownSTL))
		if PREF_Debug: printf('\n\tname[%s] f.name[%s]; isBase:%c, fThis_offs=%u sizeof=%u tcod[%s]\n',
							  name, fThis.name, bool_to_char(isBase), fThis_offs, tThis.sizeof, tcod)

		if isBase: assert(tThis) # TODO rm later
		vThis = None
		if par_isStruOrUni and fThis_offs >= 0:
			if vParent and fThis.name and tParent.has_key(name): #assert tParent.has_key(name) #yes??
				try: vThis = vParent[fThis.name]
				except BaseException as whatev: None
			if (None==vThis) and (vParent and vParent.address and tThis):
				aThis = int(vParent.address) + int(fThis_offs)
				vThis = getValueAtAddress(aThis, tThis)
				if False: printf('\n%s%s: not via vParent[x]! pa=%s fThis_offs=%u a=%s%s\n',
								 FONTmagenta, name,prAddr(vParent.address), fThis_offs,prAddr(aThis), resetFONT)
				assert vThis != None

		if tThis and tThis.code in (TYPE_CODE_STRUCT, TYPE_CODE_UNION):
			### Want more than fundamental "leaves"? ###
			effectivelyLeaf = tThis_isKnownSTL and not tToplev_isKnownSTL #effectivelyLeaf ==> ! descend into.
			if isBase and isPREF(eBaseClasses.flatten):
				if FIELD_Debug: printf('\n%swhyM-field%s not append-to-results [%s]\n', FONTred,resetFONT,name)
			elif not effectivelyLeaf and not isBase and isPREF(eNestedDatamemb.flatten):
				if FIELD_Debug: printf('\n%swhyN-field%s not append-to-results [%s]\n', FONTred,resetFONT,name)
			else:
				if FIELD_Debug: printf('\n%sYes%s append-to-results [%s]\n', FONTred,resetFONT,name)
				dfNonleaf = DeepField(depth, tToplev, offsParent_fromToplev, tThis_isKnownSTL,
									  pass__effStatic, vParent, fThis, fParent, fAncest, pass__fVirtualBase)
				results.append(dfNonleaf)

			### Want to go deeper than top-level? ###
			if tThis_isKnownSTL and not tToplev_isKnownSTL:
				if FIELD_Debug: printf('\n%swhyR-field%s not descend into [%s]\n', FONTred,resetFONT,name)
			elif isBase and isPREF(eBaseClasses.omit):
				if FIELD_Debug: printf('\n%swhyS-field%s not descend into [%s]\n', FONTred,resetFONT,name)
			elif not isBase and isPREF(eNestedDatamemb.omit):
				if FIELD_Debug: printf('\n%swhyT-field%s not descend into [%s]\n', FONTred,resetFONT,name)
			else:
				if FIELD_Debug: printf('\n%sYes%s descend into [%s]\n', FONTred,resetFONT,name)
				pass__fAncest = nonNull(fAncest,fThis)
				list_deepFields(results, tThis, depth+1, tToplev, offsParent_fromToplev + fThis_offs,
								pass__effStatic, vThis, tToplev_isKnownSTL, fThis, pass__fAncest,
								pass__fVirtualBase)
		else:
			if FIELD_Debug: printf('\n%sYes%s append-to-results not-struct [%s]\n', FONTred,resetFONT,name)
			dfLeaf = DeepField(depth, tToplev, offsParent_fromToplev, tThis_isKnownSTL,
							   pass__effStatic, vThis, fThis, fParent, fAncest, pass__fVirtualBase)
			results.append(dfLeaf)


def lookupTeArgs_Rule (ppClass, templateArgs):
	if ppClass!=None:
		tarClass = ppClass.getTeArgs_Rule()
		if tarClass:
			tarObj = tarClass(templateArgs)
			if PREF_Debug: TeArgs_Rule.dump(tarObj, templateArgs)
			return tarObj
	return None


class ToplevKnowns:
	"""
Collects some of the arguments passed to simplifyTypename(); specifically,
those arguments which stay same in all the simplifyTypename() invocations
done for a particular toplev type.
________
		gdbType                  : gdb.Type
		isKnownSTL               : bool
		tapDeck                  : TeArg_Profile__Deck
		strName                  : string // gdbType.name
		baseClasses_list         : gdb.Type[] // infer i for "@i@" from position in list.
		ppClass                  : BasePP, the class not an obj  // requires non-null tapDeck
		tar                      : TeArgs_Rule // requires non-null ppClass
	"""
	def __init__ (self, gdbType, isKnownSTL, tapDeck,
				  baseClasses_list=None, ppClass=None, tar=None):
		assert gdbType!=None and isinstance(gdbType, gdb.Type)
		self.gdbType          = gdbType
		self.strName          = gdbType.name
		self.isKnownSTL       = assert_bool(isKnownSTL)
		assert tapDeck!=None and isinstance(tapDeck,TeArg_Profile__Deck)
		self.tapDeck          = tapDeck
		self.baseClasses_list = baseClasses_list
		self.ppClass          = ppClass
		assert (not tar) or isinstance(tar,TeArgs_Rule)
		self.tar              = tar

	def __str__ (self):
		s = self.strName
		s += sprintf(' %s', type_codeToStr[self.gdbType.code])
		s += sprintf(' isKnSTL:%s', bool_to_char(self.isKnownSTL))
		s += sprintf(' |tapDeck|%u', len(self.tapDeck.tapDeck))
		if self.baseClasses_list!=None: s += sprintf(' |baseCl|%u', len(self.baseClasses_list))
		if self.ppClass!=None:  s += sprintf(' ppClass[%s]', self.ppClass.__name__)
		if self.tar!=None: s += sprintf(' tar(%s),|cN|%u,|eC|%u', self.tar.__class__.__name__,
										len(self.tar.componentNicknames),
										len(self.tar.elementalCompositions))
		return s

@enum.unique
class eSimplifFocus (Enum):
	aType_toplev = 1,
	aType_solo = 2,
	aTeArg = 3,
	aBaseClass = 4,
	aField = 5

def simplifyTypename (focus_kind, focus_gdbType, focus_strName, toplevKn,
					  df=None, # Required, if focus_kind == aField
					  teArg_depth=None, # Required, if focus_kind == aTeArg
					  cardTeArgsAlreadyParsed=None, # Required, if focus_kind == aTeArg
					  trimRuleToFitActual=False,
					  recv_nicknumberLookup_tapDeck=None):
	cfid = next_callFrameId()
	assert focus_kind!=None and isinstance(focus_kind,eSimplifFocus)
	assert focus_gdbType!=None and isinstance(focus_gdbType,gdb.Type)
	assert_string(focus_strName)

	assert toplevKn!=None and isinstance(toplevKn,ToplevKnowns)
	if focus_kind == eSimplifFocus.aTeArg:
		assert_uint(teArg_depth)
		assert cardTeArgsAlreadyParsed!=None
		assert_uint(cardTeArgsAlreadyParsed)
		assert toplevKn.tapDeck!=None
		#assert toplevKn.tapDeck.max_tap_card > 0

	if UNRAVEL_Debug:
		sOut=''
		if teArg_depth!=None:
			sOut = ''.ljust(4 * (teArg_depth + teArg_depth + 1))
		sOut += sprintf('%s %sSIMPL%s', FONTwhiteRUDE,resetFONT, cfid)
		sOut += sprintf('  %s%sFoc%s"%s"',
						boldFONT,italicFONT,resetFONT, sAbbr(60,cmpPrep(focus_strName)))
		if focus_gdbType.name != focus_strName:
			sOut += sprintf('  !=%s%stypFoc%s"%s"',
							boldFONT,italicFONT,resetFONT, sAbbr(60,cmpPrep(focus_gdbType.name)))
		printf('%s\n', sOut)

	#================================================================================#
	depthGauge=''
	if teArg_depth!=None:
		depthGauge = ''.rjust(teArg_depth, "'")

	teArgs_strList=None
	if toplevKn.tapDeck!=None:
		teArgs_strList = toplevKn.tapDeck.mk_listOf__strFinal()
	#================================================================================#

	###
	focusTag=''
	#
	tapCurr_kind=None
	if focus_kind == eSimplifFocus.aTeArg and toplevKn.tapDeck.max_tap_card > 0:
		tapCurr_kind = toplevKn.tapDeck.tapDeck[-1].kind
		if tapCurr_kind !=None:
			focusTag += tapCurr_kind.name[:11]
		else:
			focusTag += '?kind?'
		focusTag += sprintf(';%u/%uN',
							cardTeArgsAlreadyParsed+1, toplevKn.tapDeck.max_tap_card)
	elif focus_kind == eSimplifFocus.aField and df !=None:
		focusTag += sprintf('"%s"', df.fThis.name)
	if len(focusTag):
		focusTag = sprintf('%s(%s%s%s%s%s)%s', italicFONT,resetFONT,
						   boldFONT,focusTag,resetFONT,italicFONT,resetFONT)
	###
	argsNotes=[]
	#
	if teArg_depth!=None:
		argsNotes.append( sprintf('dep=%s%s%u%s',
								  FONTred,boldFONT,teArg_depth,resetFONT) )
	argsNotes.append( sprintf('toplevSTL:%c', bool_to_char(toplevKn.isKnownSTL)) )
#	if cardTeArgsAlreadyParsed!=None and len(toplevKn.tapDeck.tapDeck):
#		argsNotes.append( sprintf('i_teArg=%u', toplevKn.tapDeck.tapDeck[-1].i_teArg) )
	if toplevKn.ppClass!=None:
		argsNotes.append( sprintf('pp=%s', toplevKn.ppClass.__name__) )
	else:
		argsNotes.append( 'NOpp' )
	if toplevKn.tar!=None:
		argsNotes.append( sprintf('tar=%s', toplevKn.tar.__class__.__name__) )
	else:
		argsNotes.append( 'NOtar' )
	if teArgs_strList!=None:
		argsNotes.append( sprintf('teArgs=%s',toOnelineStr_aList(teArgs_strList)) )
	if toplevKn.baseClasses_list!=None and len(toplevKn.baseClasses_list):
		argsNotes.append( sprintf('|baseCl|=%u',len(toplevKn.baseClasses_list)) )
	if cardTeArgsAlreadyParsed !=None:
		argsNotes.append( sprintf('cardTAAP=%d', cardTeArgsAlreadyParsed) )
	if recv_nicknumberLookup_tapDeck != None:
		argsNotes.append( 'haveRecvExtrTapd' )
	###
	if SUBST_Debug: printf('%s%s\n%s Focus{%s%s%s%s %s%s%s %s}\n\t%s\n',
						   mkBoldStripe('='),
						   listCallers(omitInnermost=False,stairwise=True),
						   cfid, FONTcyanBackgd, focus_kind.name, resetFONT,
						   focusTag,
						   FONTyellowBackgd, focus_strName, resetFONT,
						   type_codeToStr[focus_gdbType.code],
						   '  '.join(argsNotes))
	if SUBST_Debug and toplevKn.tar!=None:
		printf('%s%selementalCompositions%s= %s\n', boldFONT,underscFONT,
			   resetFONT, toplevKn.tar.str_elementalCompositions())

	#================================================================================#
	result = focus_strName
	#================================================================================#

	#____________________________________________________________________________#
	sav = result
	result = strip__cxx11(result)
	traceSubst('suB-bst', sav, 'cxx11-with','cxx11-sans' ,result  ,False)

	if focus_kind == eSimplifFocus.aField:
		field_matched_toplev=False
		#____________________________________________________________________________#
		if not field_matched_toplev:
			exchangeTo = '@TOPLEV@'
			cond = focus_gdbType == toplevKn.gdbType
			(eqLHS,eqRHS) = (str(focus_gdbType), str(toplevKn.gdbType))
			traceExchg('suHA-bst:toplev,full', result,cond,exchangeTo ,SUBST_Debug, eqLHS,eqRHS)
			if cond:
				result = exchangeTo
				field_matched_toplev=True

		if not field_matched_toplev and PREF_HeurAbbr:
			exchangeTo = '@TOPLEV@'
			(eqLHS,eqRHS) = (cmpPrep(result),toplevKn.strName)
			cond = eqLHS == eqRHS
			traceExchg('suHB-bst:toplev,full',  result,cond,exchangeTo  ,SUBST_Debug, eqLHS,eqRHS)
			if cond:
				result = exchangeTo
				field_matched_toplev=True

		if not field_matched_toplev and PREF_HeurAbbr:
			iRmostRbroket = result.rfind('>')
			iRmostDoubleColon = result.rfind('::')
			if iRmostDoubleColon>=0 and (iRmostRbroket<0 or iRmostRbroket<iRmostDoubleColon):
				split_atRmostNQ = splitTypename_atRmostNameQualifier(result)
				replaceWhat = toplevKn.strName
				replaceWith = '@TOPLEV@'
				sav = result
				if replaceWhat == cmpPrep(split_atRmostNQ[0]):
					result = replaceWith + split_atRmostNQ[1]
					field_matched_toplev=True
				traceSubst('suHC-bst:toplev,part',
						   sav, replaceWhat,replaceWith ,result  ,SUBST_Debug)

		if not field_matched_toplev and not isPREF(eTemplateArgs.omit) and PREF_HeurAbbr and toplevKn.tapDeck!=None:
			list_strOriginal = toplevKn.tapDeck.mk_listOf__strOriginal()
			for i in range(len(list_strOriginal)):
				exchangeTo = sprintf('#%u#',i)
				(eqLHS,eqRHS) = (cmpPrep(focus_strName), cmpPrep(list_strOriginal[i]))
				cond = eqLHS == eqRHS
				traceExchg(sprintf('suHD-bst:toplev,full[%u]',i),
						   result,cond,exchangeTo  ,SUBST_Debug ,eqLHS,eqRHS)
				if cond:
					result = exchangeTo
					field_matched_toplev=True
					break
#		if not field_matched_toplev and PREF_HeurAbbr and toplevKn.tapDeck!=None:
#			list_strBest = toplevKn.tapDeck.mk_listOf__strBest()

		if field_matched_toplev:
			if SUBST_Debug: printf('%s =========== Ret|b  %s%s%s%s\n\n', cfid,
								   FONTyellowBackgd,boldFONT,exchangeTo,resetFONT)
			return result


	if focus_kind in (eSimplifFocus.aBaseClass, eSimplifFocus.aField):
		#____________________________________________________________________________#
		if focus_gdbType.code == TYPE_CODE_STRUCT:
			(focus_ppClass,dummy) = gdbType_to_ppClass(focus_gdbType, False)
			if focus_ppClass and focus_ppClass.isKnownSTL():
				send_nicknumberLookup_tapDeck=None
				if focus_kind == eSimplifFocus.aField and df !=None:
					if not toplevKn.isKnownSTL and toplevKn.tapDeck.max_tap_card > 0:
						# So could subst "#num#" for an elemental te arg, later down the line.
						send_nicknumberLookup_tapDeck = toplevKn.tapDeck
				exchangeTo = impl__type_nameOnly(focus_gdbType, send_nicknumberLookup_tapDeck)
				traceExchg('suZ-bst:isSTL!',  result,True,exchangeTo  ,SUBST_Debug)
				if SUBST_Debug: printf('%s =========== Ret|c  %s%s%s%s\n\n',
									   cfid, FONTyellowBackgd,boldFONT,exchangeTo,resetFONT)
				return exchangeTo

	if toplevKn.tar!=None:
		#____________________________________________________________________________#
		# # # If field of templated non-STL type, maybe subst nicknumber of earlier teArg,
		# in order to simplify the field's (itself templated) type?
		if recv_nicknumberLookup_tapDeck !=None and (focus_kind == eSimplifFocus.aTeArg):
			highest_index_of_elementalTeArg = toplevKn.tar.n_elementalTeParams() - 1
			if PREF_HeurAbbr and (cardTeArgsAlreadyParsed <= highest_index_of_elementalTeArg):
				for j in range(highest_index_of_elementalTeArg + 1):
					if j >= recv_nicknumberLookup_tapDeck.max_tap_card:
						break
					jth_strFinal = recv_nicknumberLookup_tapDeck.tapDeck[j].strFinal
					(eqLHS,eqRHS) = (focus_strName, jth_strFinal)
					cond = eqLHS == eqRHS
					exchangeTo = sprintf('#%u#',j)
					traceExchg(sprintf('suJ-bst[j=%u]',j),
							   result,cond,exchangeTo  ,SUBST_Debug  ,eqLHS,eqRHS)
					if cond:
						if SUBST_Debug: printf('%s =========== Ret|j  %s%s%s%s\n\n', cfid,
											   FONTyellowBackgd,boldFONT,exchangeTo,resetFONT)
						return exchangeTo

		#____________________________________________________________________________#
		for eC in toplevKn.tar.elementalCompositions:
			if None==eC[1]: continue
			sav = result
			result = result.replace(eC[0], eC[1])
			traceSubst('suA-bst:eC',  sav, eC[0],eC[1] ,result  ,SUBST_Debug)

		if (focus_kind == eSimplifFocus.aTeArg) and (0 == len(teArgs_strList)):
			if SUBST_Debug: printf('%s =========== Ret|d  %s%s%s%s\n\n',
								   cfid, FONTyellowBackgd,boldFONT,result,resetFONT)
			return result

		#____________________________________________________________________________#
		for cN in toplevKn.tar.componentNicknames: # look to match component expansions.
			replaceWith = sprintf('#ext%s#',cN[1])
			sav = result
			result = result.replace(cN[0], replaceWith)
			traceSubst('suC-bst:cponentNi',  sav, cN[0],replaceWith ,result  ,SUBST_Debug)


	if toplevKn.tar!=None and teArgs_strList!=None and len(teArgs_strList):
		if SUBST_Debug:
			printf('%s Have tar; teArgs_strList= %s\n',
				   cfid,toOnelineStr_aList(teArgs_strList, FONTmagenta))
		dtaList = toplevKn.tar.defaultStrings
		nickList = toplevKn.tar.nicknames()

		if trimRuleToFitActual: # Still building te args list?  If so, "trim to len of actual".
			actuN = len(teArgs_strList) #cardTeArgsAlreadyParsed+1
			#
			if len(dtaList) > actuN:
				if SUBST_Debug:
					printf('%s Trimming from dtaList:  %s\n',cfid, str(dtaList[(actuN):]))
			dtaList = dtaList[:actuN]
			#
			if len(nickList) > actuN:
				if SUBST_Debug:
					printf('%s Trimming from nickList: %s\n',cfid,str(nickList[(actuN):]))
			nickList = nickList[:actuN]

		if SUBST_Debug:
			printf('%s dtaList= %s\n',cfid,toOnelineStr_aList(dtaList))
			printf('%s nickList= %s\n',cfid,toOnelineStr_aList(nickList))

		#____________________________________________________________________________#
		# # # Look for a complete match of a *default* te arg.
		if focus_kind == eSimplifFocus.aTeArg and PREF_HeurAbbr:
			for i in range(len(dtaList)):
				(eqLHS,eqRHS) = (focus_strName, dtaList[i])
				if eqLHS == eqRHS: # This is the "cond".
					exchangeTo = sprintf('#%s%s#', depthGauge,nickList[i])
					traceExchg(sprintf('suD-bst:dta[%u],full',i),
							   result,True,exchangeTo  ,SUBST_Debug  ,eqLHS,eqRHS)
					if SUBST_Debug: printf('%s =========== Ret|e  %s%s%s%s\n\n', cfid,
										   FONTyellowBackgd,boldFONT,exchangeTo,resetFONT)
					# ======== Examp ========
					# Overall input   std::list<float>
					# +Now+           #ALLO#
					# -Was-           std::allocator<float>
					# Ret|e           #ALLO#
					return exchangeTo

		#____________________________________________________________________________#
		# # # Failing that, look for a partial match.
		result = cmpPrep(result)
		if (focus_kind == eSimplifFocus.aTeArg) and PREF_HeurAbbr:
			indices = list(range(len(nickList)))
			indices.reverse() # On assumption that te args start with the simpler types.
			for i in indices:
				if (i < len(dtaList)) and dtaList[i]:
					replaceWhat = cmpPrep(dtaList[i])
					replaceWith = sprintf(' #%s%s# ', depthGauge,nickList[i])
					sav = result
#					result = result.replace(replaceWhat,replaceWith)
					result = replace_atTokenBoundaries(replaceWhat,replaceWith,result)
					traceSubst(sprintf('suE-bst:dta[%u],part',i),
							   sav, replaceWhat,replaceWith ,result   ,SUBST_Debug)

		#____________________________________________________________________________#
		# # # Then look for a complete match of an *actual* te arg.
		if focus_kind!=eSimplifFocus.aType_solo and PREF_HeurAbbr:
			highest_index_of_elementalTeArg = toplevKn.tar.n_elementalTeParams() - 1
			indices = list(range(min(len(teArgs_strList),len(nickList))))
			indices.reverse() # On assumption that te args start with the simpler types.
			for i in indices:
#				printf('%s In F- loop, i=%d highest_index_of_elementalTeArg=%d\n',cfid,
#					   i, highest_index_of_elementalTeArg)
				if i <= highest_index_of_elementalTeArg: # Don't render "std::map<float,float>"
					break                                # as "std::map<float,#K#>" !!
				replaceWhat = cmpPrep(strip__cxx11(teArgs_strList[i]))
				# XXX Que chingada??? nickList can't be None here, pendejo!
				if nickList!=None: replaceWith = sprintf(' #%s%s# ', depthGauge,nickList[i])
				else:              replaceWith = sprintf(' #%s%u# ', depthGauge,i)
				replaceWith = strip__cxx11(replaceWith)
				sav = result
				result = replace_atTokenBoundaries(replaceWhat, replaceWith, cmpPrep(result))
				traceSubst(sprintf('suF-bst:actu[%u],tokBound',i),
						   sav, replaceWhat,replaceWith ,result  ,SUBST_Debug)

		#____________________________________________________________________________#
		# # # If a custom te arg, maybe subst nickname of an elemental te arg?
		if (focus_kind == eSimplifFocus.aTeArg) and PREF_HeurAbbr:
			assert tapCurr_kind!=None
			if tapCurr_kind == eActualTeArgKind.not_sameAs_knownDefault:
#				printf('Feh  print the normal tapdeck,%s\n',str(toplevKn.tapDeck))
				indices = list(range(min(len(teArgs_strList),len(nickList))))
				for i in indices:
#					printf('%s In G- loop, i=%d highest_index_of_elementalTeArg=%d\n',cfid,
#						   i, highest_index_of_elementalTeArg)
					if i > highest_index_of_elementalTeArg:
						break
					custom_teArg = toplevKn.tapDeck.tapDeck[i].actual_teArg
					if not could_custom_teArg_beA(custom_teArg, nickList[i]):
						if True or SUBST_Debug:
							printf('Says never could be a %s .\n', nickList[i])
						continue
					# Gaaaaaaaaaaah!  The suJ-bst simplification is interfering with us.
					if recv_nicknumberLookup_tapDeck !=None:
						replaceWhat = toplevKn.tapDeck.tapDeck[i].strBest
					else:
						replaceWhat = teArgs_strList[i]
					replaceWith = sprintf('#%s#', nickList[i])
					# Elemental te args have nest depth of 0, hence depthGa would be ''.
					sav = result
					result = replace_atTokenBoundaries(replaceWhat,replaceWith,result)
					traceSubst(sprintf('suG-bst:nick[%u]',i),
							   sav, replaceWhat,replaceWith ,result   ,SUBST_Debug)

	#____________________________________________________________________________#
	# # # If field of templated non-STL type, maybe subst nicknumber of earlier teArg,
	# in order to simplify the field's (itself templated) type?

	if (focus_kind == eSimplifFocus.aField) and PREF_HeurAbbr and (teArgs_strList!=None):
		if (teArgs_strList!=None) and not toplevKn.isKnownSTL:
			# Field is of non-STL type, hence all of T's te args are up for play.
			for j in range(toplevKn.tapDeck.max_tap_card):
				replaceWhat = teArgs_strList[j]
				replaceWith = sprintf('#%u#', j)
				sav = result
				result = replace_atTokenBoundaries(replaceWhat,replaceWith,result)
				traceSubst(sprintf('suK-bst[j=%u]',j),
						   sav, replaceWhat,replaceWith ,result   ,SUBST_Debug)

	if (focus_kind == eSimplifFocus.aField) and PREF_HeurAbbr and (teArgs_strList!=None):
		indices = list(range(len(teArgs_strList)))
		indices.reverse() # On assumption that te args start with the simpler types.
		#____________________________________________________________________________#
		matched_actu_full=False
		for i in indices:
			(eqLHS,eqRHS) = (result, cmpPrep(strip__cxx11(teArgs_strList[i])))
			cond = eqLHS == eqRHS
			exchangeTo = sprintf('#%u#',i)
			traceExchg(sprintf('suV-bst:actuTe[%u],full',i),
					   result,cond,exchangeTo  ,SUBST_Debug ,eqLHS,eqRHS)
			if cond:
				result = exchangeTo
				matched_actu_full = True
				break
		#____________________________________________________________________________#
		split_atRmostNQ = splitTypename_atRmostNameQualifier(result)
		if (not matched_actu_full) and split_atRmostNQ!=None:
			for i in indices:
				replaceWhat = teArgs_strList[i]
				replaceWith = sprintf('#%u#',i)
				sav = result
				if replaceWhat == split_atRmostNQ[0]:
					result = replaceWith + split_atRmostNQ[1]
				traceSubst(sprintf('suW-bst:actu[%u],part',i),
						   sav, replaceWhat,replaceWith ,result  ,SUBST_Debug)
				if result != sav: break

	#____________________________________________________________________________#
	# # # Base classes: not for aTeArg, nor aType_solo (in which case unavail anyway)
	if focus_kind == eSimplifFocus.aField and (toplevKn.baseClasses_list!=None) \
	   and (PREF_HeurAbbr or (df!=None and df.fThis.is_base_class)):
		#____________________________________________________________________________#
		for i in range(len(toplevKn.baseClasses_list)):
			#TOOD: Also try toplevKn.baseClasses_list[i].name, if that's different?
			baseCl_strName = str(get_basic_type(toplevKn.baseClasses_list[i]))
			exchangeTo = sprintf('@%u@',i)
			(eqLHS,eqRHS) = (result, baseCl_strName)
			cond = eqLHS == eqRHS
			traceExchg(sprintf('suS-bst:baseCl[%u],full',i),
					   result,cond,exchangeTo  ,SUBST_Debug ,eqLHS,eqRHS)
			if cond: result = exchangeTo
			if cond: break
		#____________________________________________________________________________#
		split_atRmostNQ = splitTypename_atRmostNameQualifier(result)
		if split_atRmostNQ!=None:
			for i in range(len(toplevKn.baseClasses_list)):
				#TOOD: Also try toplevKn.baseClasses_list[i].name, if that's different?
				replaceWhat = str(get_basic_type(toplevKn.baseClasses_list[i]))
				replaceWith = sprintf('@%u@',i)
				sav = result
				if replaceWhat == split_atRmostNQ[0]:
					result = replaceWith + split_atRmostNQ[1]
				traceSubst(sprintf('suT-bst:baseCl[%u],full',i),
						   sav, replaceWhat,replaceWith ,result  ,SUBST_Debug)
				if result != sav: break

	#____________________________________________________________________________#
	if focus_kind == eSimplifFocus.aType_solo:
		assert toplevKn.tapDeck!= None
		teArgs_strList__concise = toplevKn.tapDeck.mk_listOf__strBest__concise()
		teArgs_strList             = toplevKn.tapDeck.mk_listOf__strBest()
		result = simplifyTypename__substTeArgNicknames(result,
													   teArgs_strList__concise,
													   teArgs_strList)

	#____________________________________________________________________________#
	if 'std::basic_string<char>' == result:
		exchangeTo = 'std::string'
		traceExchg('suM-bst',   result,True,exchangeTo   ,SUBST_Debug)
		result = exchangeTo
	#____________________________________________________________________________#
	elif 'std::basic_string<wchar_t>' == result:
		exchangeTo = 'std::wstring'
		traceExchg('suM-bst',   result,True,exchangeTo   ,SUBST_Debug)
		result = exchangeTo
	#____________________________________________________________________________#
	elif 'std::basic_string_view<char>' == result:
		exchangeTo = 'std::string_view'
		traceExchg('suM-bst',   result,True,exchangeTo   ,SUBST_Debug)
		result = exchangeTo
	#____________________________________________________________________________#
	elif 'std::basic_string_view<wchar_t>' == result:
		exchangeTo = 'std::wstring_view'
		traceExchg('suM-bst',   result,True,exchangeTo   ,SUBST_Debug)
		result = exchangeTo

	#================================================================================#
	if SUBST_Debug: printf('%s =========== Ret|f  %s%s%s%s\n\n', cfid,
						   FONTyellowBackgd,boldFONT,result,resetFONT)
	return result



@accepts(gdb.Block)
@returns(str)
def scopeOfBlock (b):
	b__fu = b.function
	if b__fu:
		if b__fu.is_valid():
			s = b__fu.print_name
			if b__fu.symtab and b__fu.symtab.filename:
				s += sprintf('  // %s', prettyPath(b__fu.symtab.filename))
			return s
		else:
			return '??unk_func??'
	elif b.is_static:
		return 'file-static' # "translation unit-static", if you insist.
	elif b.is_global:
		return 'global'
	else:
		return sprintf('??[%u,%u]??', b.start, b.end)


def describeScopeGivenAddr (addr, frame):
	blocksSoFar = []
	currBlock = blockOfFrame(frame)
	while currBlock and currBlock.is_valid():
#		iterdump_Block(currBlock)
#		stal = gdb.find_pc_line(currBlock.start)
		if PREF_Debug:
			currFunc = currBlock.function
			printf('\tblock: PCrange[%12x - %12x]; static=%c global=%c ; f=  %s\n',
				   currBlock.start, currBlock.end,
				   ternary(currBlock.is_static,'Y','N'),
				   ternary(currBlock.is_global,'Y','N'),
				   safe_ivar(currFunc,'print_name'))
		for prevBlock in blocksSoFar:
			if prevBlock == currBlock: # Better safe than infinitely looping.
				return None
		blocksSoFar.append(currBlock)
		if currBlock.start <= addr and addr <= currBlock.end:
			return scopeOfBlock(currBlock)
		currBlock = currBlock.superblock
	return None


def stringifyActualTeArgKind (kind):
	assert (None==kind) or isinstance(kind,eActualTeArgKind)
	if (None==kind) or (kind == eActualTeArgKind.noDefaultKnown):
		return '         '
	elif kind == eActualTeArgKind.sameAs_knownDefault:
		return '/default/'
	else:
		return ' /custom/'


#________________________________________
### ### ### stringifyType__ * ### ### ###

@accepts(gdb.Type)
@returns(str)
def stringifyType__align (t):
	assert t and isinstance(t, gdb.Type)
	s = ''
	if safe_ivar(t,'alignof'): # Missing in gdb 8.x ??
		s += sprintf('%2X', t.alignof)
		return sprintf('  %s=align', s.rjust(2))
	else:
		return ''

@returns(str)
def stringifyType__size (t):
	assert t and isinstance(t, gdb.Type)
	s = ''
	if t.sizeof != None:
		s += sprintf('%3u', t.sizeof)
	else:
		s += '??'
	return sprintf('%s=sz', s.rjust(3))

def stringify__isConst (isConst):
	assert_bool(isConst)
	return ternary(isConst, FONTyellowBackgd+'C'+resetFONT, ' ')
#
def stringify__isVolatile (isVolatile):
	assert_bool(isVolatile)
	return ternary(isVolatile, FONTyellowBackgd+'V'+resetFONT, ' ')

def stringify__isReference (isLvalRef, isRvalRef):
	assert_bool(isLvalRef)
	assert_bool(isRvalRef)
	if   isLvalRef:
		return '&'
	elif isRvalRef:
		return '&&'
	else:
		return ' '
#
def stringifyType__referenceTag (t):
	assert t and isinstance(t, gdb.Type)
	return stringify__isReference(TYPE_CODE_REF == t.code, TYPE_CODE_RVALUE_REF == t.code)

def stringify__isPointer (isPointer):
	assert_bool(isPointer)
	return ternary(isPointer, '*', ' ')
#
def stringifyType__pointerTag (t):
	assert t and isinstance(t, gdb.Type)
	return stringify__isPointer(isPointer(t))


#_________________________________________
### ### ### stringifyValue__ * ### ### ###

def stringifyValue__dynTyp (v):
	assert (v != None) and isinstance(v, gdb.Value)
	if v.dynamic_type:
		staticTyp = get_basic_type(v.type)
		if staticTyp:
			dynTyp = get_basic_type(v.dynamic_type)
			if dynTyp and dynTyp != staticTyp:
				return sprintf('/dynTyp=%s', str(dynTyp))
	return None


#		z = int.from_bytes(bytearray(rawBytes), sys.byteorder) #, False)
#		printf('\nBut z = 0x%08X\n', z)
@returns(str)
def stringifyValue__whatHolds (v, t, a, sizeof):
	assert (v !=None) and isinstance(v, gdb.Value)
	assert t and isinstance(t, gdb.Type)
	s = ''

	bytes_spacer_period = 4 # (Insert a space between groups of this many bytes.)
	max_grab_sizeof = 12
	max_hexString_printWidth = ((max_grab_sizeof * 2) # 1 char/nybble, 2 chars/byte
								+ (int(max_grab_sizeof / bytes_spacer_period) - 1) #Spacers
								+ 3) # 3 = strlen('...')
	infProcess = gdb.selected_inferior()
	if a!=None and sizeof and infProcess and infProcess.is_valid():
		grab_sizeof = min(sizeof, max_grab_sizeof)
		rawBytes = infProcess.read_memory(a, grab_sizeof)
		hexChars = rawBytes.hex().lower()
		hexString = string_to_groupOfSubstrings(hexChars, bytes_spacer_period * 2)
		s += FONTblue + italicFONT
		s += hexString.rjust(max_hexString_printWidth - 3)
		if sizeof > grab_sizeof: s += '...'
		else:                    s += '   '
		s += resetFONT
	else:
		s += ''.ljust(max_hexString_printWidth)

	s += '   '
	s += FONTblue

	t_code = t.code
	tbas_code = get_basic_type(t).code

	if tbas_code == TYPE_CODE_ARRAY and not isScalar(t.target().strip_typedefs()):
		pass
	elif a!=None and t_code == TYPE_CODE_ARRAY:
		s += gdb.execute(sprintf('output/x (%s)* 0x%x', str(t), int(a)), to_string=True)
	elif not tbas_code in (TYPE_CODE_FUNC, TYPE_CODE_STRUCT):
		s += str(v)

#	if v.is_lazy:                 //Seems arbitrary; not helpful.
#		s += '  /lazyEh?'

	# If optimized out, GDB will have printed "<optimized out>".
#	if v.is_optimized_out:
#		s += '  /optimzdOut'

#	if not a:                   //Don't say it's constexpr, when it's just static const.
#		s += '  /constexpr??'

	s += resetFONT
	return s


#_________________________________________
### ### ### stringifyField__ * ### ### ###  For fields of structs or unions, *only*.

def stringifyField__name (df):
	assert df and isinstance(df, DeepField)
	f = df.fThis
	assert f and isinstance(f, gdb.Field)
	s = ''
	if isVirtualBase(f):
		s += '/Virtual Base/'
	elif f.is_base_class:
		s += '/Base/'
	elif f.name:
		if f.type and f.name == str(f.type.strip_typedefs()):
			s += '/EBO/'   #XXX sure about this??????  Fishy!
		else:
			s += f.name
	else:
		s += '/Anon/'
		if f.artificial:
			s += '/Artif/'
	return s.rjust(PREF_PrintWidth_MemberName)

def stringifyField__size (f):
	assert f and isinstance(f, gdb.Field)
	s = ''
	if f.bitsize:
		s += sprintf(',%u', f.bitsize)
	elif f.type:
		s += sprintf('%u', f.type.sizeof)
	else:
		s += '??'
	return s.rjust(3) + '=sz'

def stringifyField__isStatic (df): # NB: takes a DeepField, not a gdb.Field !
	assert df and isinstance(df, DeepField)
	return ternary(df.effStatic, '|S', '  ')

def stringifyField__offset (df): # NB: takes a DeepField, not a gdb.Field !
	assert df and isinstance(df, DeepField)
	if df.effStatic:
		return 'static'.ljust(3 + 2 + 4)
	else:
		bitpos = df.offsTot_fromToplev
		s = sprintf('%3u', int(bitpos / 8))   # 3 chars
		if 0 != (bitpos % 8):
			s += sprintf('%s,%u%s', FONTred, bitpos % 8, resetFONT)      # 2 chars
		else:
			s += '__'
		s += '=off'                                     # 4 chars
		return        s.rjust(3 + 2 + 4)


def valueProper (v, oride__t=None, oride__addr=None, oride__sizeof=None):
	assert isinstance(v, gdb.Value)
	t      = nonNull(oride__t,      v.type)
	a      = nonNull(oride__addr,   v.address)
	sizeof = nonNull(oride__sizeof, t.sizeof)
	#
	if not v.is_optimized_out:
		dynTyp = stringifyValue__dynTyp(v) #could be None
		if dynTyp:
			printf('%s  ', dynTyp)
	#
	whatHolds = stringifyValue__whatHolds(v, t, a, sizeof)
	if whatHolds and len(whatHolds):
		printf('%s', whatHolds)


def wrap__valueProper (v, indents, oride__t=None, oride__addr=None, oride__sizeof=None):
	valueProper(v, oride__t, oride__addr, oride__sizeof)

	isRawPtr=False
	return #XXX get this-all to work, willya??
	if performsIndirection(v.type):
		indents.incrIndent(1)
		indents.newLine_misc()
		if v.type.code == TYPE_CODE_REF:
			printf('Lvalue ref to:')
		elif v.type.code == TYPE_CODE_RVALUE_REF:
			printf('Rvalue ref to:')
		else:
			printf('Pointer to:')
			isRawPtr=True

		targ__v = v.referenced_value()

		if (targ__v==None):
			printf(' //nothing')
		elif (v.type.code == TYPE_CODE_PTR) and targ__v.address == v.address:
			printf(' //self') # Common enough with e.g. linked list
		else:
			uncannyMem=False
#			if targ__v.is_lazy: printf('\nis_lazy')
			targ__notes = []
			# For target we want not whole shebang, but just a very few key facts, viz.:
			targ__a = targ__v.address
			if targ__a:
				targ__b = blockFromAddr(int(targ__a))
				if targ__b:
					printf('\ntarg__b = %s\n', str(targ__b))
				if blockValid(targ__b):
					targ__notes.append(sprintf('scope=%s', scopeOfBlock(targ__b)))  ## Scope
					targ__fu = targ__b.function
					if targ__fu:
						if targ__fu.name:
							targ__notes.append(sprintf('"%s"', targ__fu.name))       ## Name
						targ__storCat = addrcStorageCategory(targ__fu.addr_class)
						if targ__storCat:
							targ__notes.append(sprintf('/%s/', targ__storCat)) ## Addr class
				else:
					targ__notes.append('??? mem')
					uncannyMem=True
				if not isRawPtr: # If isRawPtr, we already printed the address.
					targ__notes.append(prAddr(targ__a))                          ## Addr
			if len(targ__notes):
				printf(' %s', '; '.join(targ__notes))
			if not uncannyMem:
				valueProper(targ__v)
#		indents.decrIndent()


def printfPad__size (actual_bitpos, expected_bitpos):
	delta_bitpos = int(actual_bitpos) - int(expected_bitpos)
	if FIELD_Debug:
		printf('\n%sGiven actual_bitpos=%d expected_bitpos=%d, delta_bitpos=%d%s\n',
			   FONTblue,actual_bitpos, expected_bitpos, delta_bitpos, resetFONT)
	if 0 == (delta_bitpos % 8):
		printf('Pad|      %4u=sz', int(delta_bitpos / 8))
	else:
		printf('Pad|    %4u,%u=sz', int(delta_bitpos / 8), int(delta_bitpos % 8))


def decideTeArg__tag (nickname_raw, i_teArg):
	if len(nickname_raw):
		return nickname_raw
	else:
		return str(i_teArg)

def sprintfTeArg__tag (nickname_raw, i_teArg):
	s = decideTeArg__tag(nickname_raw, i_teArg)
	return sprintfBrightDelimitedTag(s, '#')

def sprintfBaseClass__tag (i_baseClass):
	s = str(i_baseClass)
	return sprintfBrightDelimitedTag(s, '@')


def impl__type (cxxType, v=None):
	from _stl_iterators import isCanonicalIterType
	cfid = next_callFrameId()
	"""
		Ivar render fomat is         |S typName CV * CV & ivarName [arrBounds] ;
	"""
	assert cxxType and isinstance(cxxType, gdb.Type)
	assert ((v==None) or isinstance(v, gdb.Value))
	tyName_asDeclaredInProgram = cxxType.name
	indents = _indent_spec.IndentSpec(0)

	# # # Figure out the "real" type and name; ppClass, if we have it.
	ty = get_basic_type(cxxType) # Go with this one simplification, for now.
	tyStr = str(ty)
	if isUnexpected(ty):
		die('Unexpected ty.code = %s; tyStr = "%s"', type_codeToStr[ty.code], tyStr)

	(ppClass,if_iterHusk) = gdbType_to_ppClass(ty, try__unwrap_iteratorType=(None==v))
	tToplev_isKnownSTL = (ppClass != None) and ppClass.isKnownSTL()

	# # # template args # # #
	tar = None
	teArgs = list_templateArgs(ty) # Rets list of gdb.Type (and/or gdb.Value?)
	if PREF_Debug: dump_templateArgs(teArgs)

	tapDeck = _te_arg_profile.TeArg_Profile__Deck(len(teArgs))
	ud = UnravelDepth()
	if len(teArgs):
		tar = lookupTeArgs_Rule(ppClass, teArgs)
		for i_teArg in range(len(teArgs)):
			teArg = teArgs[i_teArg]
			tapCurr = tapDeck.add__TeArg_Profile(tar, teArg)
			tapCurr.set__strBest(strip__cxx11(tapCurr.strBest))
			nickname_raw = ''
			if tar:
				tapCurr.decide_kind()
				nickname_raw = tar.nicknames()[i_teArg]
			descript = ''
			if PREF_Debug: descript += tapCurr.generateDebugTag()
			descript += '  '
			descript += stringifyActualTeArgKind(tapCurr.kind)
			descript += sprintf('%s', ''.ljust(20 - len(nickname_raw)))
			descript += sprintfTeArg__tag(nickname_raw, i_teArg)
			if isinstance(teArg,gdb.Type):
				toplevKn_partial = ToplevKnowns(ty, tToplev_isKnownSTL, tapDeck,
												ppClass=ppClass,tar=tar)
				use_strFinal = simplifyTypename(eSimplifFocus.aTeArg,
												ternary(isinstance(teArg,gdb.Type),teArg,None),
												tapCurr.strBest, toplevKn_partial,
												teArg_depth=0,
												cardTeArgsAlreadyParsed=i_teArg,
												trimRuleToFitActual=True)
				tapCurr.set__strFinal(use_strFinal)
			else:
				tapCurr.set__strFinal(str(teArg))
			if tapCurr.strFinal == tapCurr.strBest:
				if isinstance(teArg,gdb.Type):
					tapCurr.set__strFinal(impl__type_nameOnly(teArg))
				else: # If not a gdb.Type, will be a gdb.Value with TYPE_CODE_INT code.
					tapCurr.set__strFinal(str(teArg))
				if PREF_Debug:
					printf('Owrote [%s] to [%s]',tapCurr.strBest,tapCurr.strFinal)
			descript += sprintf('    %s', tapCurr.strFinal)
			if not isPREF(eTemplateArgs.omit) and tapCurr.printThis_teArg:
				if 0 == i_teArg: indents.sameLine_beginList('<')
				else:            indents.newLine_nextItem(',')
				printf('%s', descript)

		if not isPREF(eTemplateArgs.omit):
			if 1 == len(teArgs):   indents.sameLine_endList('>')
			else:                  indents.newLine_endList('>')
			printf('\n')
	teArgs_strList = tapDeck.mk_listOf__strBest()
	if PREF_Debug: dump_aList(teArgs_strList, 'teArgs_strList')
	teArgs_strList__concise = tapDeck.mk_listOf__strFinal()

	if PREF_Underly and tar:
		for cN in tar.componentNicknames:
			printf('%s%s    %s\n', ''.ljust(15),
				   sprintfTeArg__tag('ext'+cN[1],99),
				   sprintfAltName('Underly component',cN[0]))

	# # # scalar attributes of type itself # # #
	toplevKn = ToplevKnowns(ty, tToplev_isKnownSTL, tapDeck, ppClass=ppClass,tar=tar)
	if PREF_Debug:
		printf('%s impl__type %sbig-kahuna tapDeck%s =\n\t%s%s%s\n',cfid,
			   FONTred,resetFONT, boldFONT,str(tapDeck),resetFONT)
	tyNameShow = simplifyTypename(eSimplifFocus.aType_toplev, ty, tyStr, toplevKn)
	toplevKn.strName = tyNameShow # Now that have tyNameShow, use *it*.

	tyNameShow = simplifyTypename__substTeArgNicknames(tyNameShow,
													   teArgs_strList__concise, teArgs_strList)
	tyNameShow_C_V = tyNameShow
	zty = cxxType.strip_typedefs()
	if zty.code in (TYPE_CODE_PTR, TYPE_CODE_REF):
		if zty == zty.const(): tyNameShow_C_V += ' const'
		if zty == zty.volatile(): tyNameShow_C_V += ' volatile'
	printf('%s', tyNameShow_C_V)

	if len(tyNameShow_C_V) > 75: printf('\n')
	else:                    printf('          ')
	printf('// %sTot;%s %s.', stringifyType__size(cxxType),
		   stringifyType__align(cxxType), type_codeToStr[cxxType.code])
	if PREF_Underly:
		if tyNameShow != tyName_asDeclaredInProgram:
			printf('   /%s', sprintfAltName('DeclAs',tyName_asDeclaredInProgram))
		tyNameUnderly = simplifyTypename(eSimplifFocus.aType_toplev, ty,
										 nameTypeConcisely(ty), toplevKn)
		if tyNameShow != tyNameUnderly:
			printf('   /%s', sprintfAltName('ext',tyNameUnderly))
	if ty.code not in (TYPE_CODE_STRUCT, TYPE_CODE_UNION):
		printf('\n')
	if isTypeNativelyPrintable(ty):
		return

	# # # method/func params, if the toplev type itself is a func # # #
	if ty.code in (TYPE_CODE_FUNC, TYPE_CODE_METHOD, TYPE_CODE_INTERNAL_FUNCTION):
		indents.sameLine_beginList('(')
		params = ty.fields()
		for i in range(len(params)):
			if i: indents.newLine_nextItem(',')
			printf('%s %s', nameTypeConcisely(params[i].type), nonNull(params[i].name,''))
		indents.newLine_endList(')')
		printf('\n')
		return

	if ty.code not in (TYPE_CODE_STRUCT, TYPE_CODE_UNION):
		die('Unexp type!!! %s', type_codeToStr[ty.code])

	# # # list and sort subordinate gdb.Field objects # # #
	unsorted_deepFields = []
	list_deepFields(unsorted_deepFields, ty, 0, ty, 0, False, v, tToplev_isKnownSTL)
	if PREF_Debug: dump_listed_deepFields(unsorted_deepFields, 'unsorted_deepFields')
	sorted_deepFields = sorted(unsorted_deepFields,
							   key=functools.cmp_to_key(cmp_deepFields))
	if PREF_Debug: dump_listed_deepFields(sorted_deepFields, 'sorted_deepFields')

	# # # base classes # # #
	toplev_baseType_fields = {} #Each elem is: pair<gdb.Field, btTag>
	toplev_baseTypes = [] # Each elem is a gdb.Type
	if not isPREF(eBaseClasses.omit):
		btTag = int(0)
		for df in sorted_deepFields:
			if df.depth == 0 and df.fThis.is_base_class:
				if isPREF(eBaseClasses.skipIfEmpty) and df.isWaferthinNonleafBase():
					continue
				if btTag:   indents.newLine_nextItem(',')
				else:       indents.newLine_beginList(':')
				if not isPREF(eLayout.omit):
					printf('%s   ', stringifyField__size(df.fThis))
				printf('%s    ', sprintfBaseClass__tag(btTag))
				ty_baseCl_strName = simplifyTypename(eSimplifFocus.aBaseClass, df.fThis.type,
											  str(df.fThis.type), toplevKn, df=df)
				printf('%s', ty_baseCl_strName)
				if PREF_Underly and ty_baseCl_strName != df.fThis.type.name:
					printf('   /%s', sprintfAltName('DeclAs',df.fThis.type.name))
				toplev_baseTypes.append(df.fThis.type)
				toplev_baseType_fields[df.fThis] = btTag
				btTag += int(1)
	toplevKn.baseClasses_list = toplev_baseTypes
#	for k,v in toplev_baseType_fields.items(): printf('\t[%s] --> %u\n', k.__repr__(), v)
	if 0 == len(sorted_deepFields):
		printf(' { }\n')
		return

	# # # static and instance vars # # #
	indents.newLine_beginList('{')
	expected_bitpos = 0
	printStatics = gdb.parameter('print static-members')

	for df in sorted_deepFields:
		nameRoughly = nonNull(df.fThis.name, '?no-name?')
		# Look for reasons to not print this field.
		if FIELD_Debug:
			printf('\nFld %s%s%s  ', FONTyellowBackgd,nameRoughly,resetFONT)
		if df.effStatic and not printStatics:
			if FIELD_Debug: printf('%swhyA%s not print\n',FONTred,resetFONT)
			continue
		if isPREF(eNestedDatamemb.omit) and not df.isToplev():
			if FIELD_Debug: printf('%swhyB%s not print\n',FONTred,resetFONT)
			continue
		if isPREF(eNestedDatamemb.flatten) and not df.fThis.is_base_class and not df.isLeaf() and not df.isKnownSTL:
			if FIELD_Debug: printf('%swhyC%s not print\n',FONTred,resetFONT)
			continue
		if isPREF(eBaseClasses.omit) and df.fThis.is_base_class:
			if FIELD_Debug: printf('%swhyD%s not print\n',FONTred,resetFONT)
			continue
		if isPREF(eBaseClasses.skipIfEmpty) and df.isWaferthinNonleafBase():
			if FIELD_Debug: printf('%swhyE%s not print\n',FONTred,resetFONT)
			continue
		else:
			if FIELD_Debug: printf('%sYes%s print\n',FONTred,resetFONT)

		indents.newLine_nextItem(' ')

		if not df.effStatic:
			actual_bitpos = df.offsTot_fromToplev
			if actual_bitpos > expected_bitpos and isPREF(eLayout.full):
				printfPad__size(actual_bitpos, expected_bitpos)
				indents.newLine_nextItem(' ')
			expected_bitpos = actual_bitpos + df.getBitsize_countingTowardTotal()
		fType = df.fThis.type
		fAbsAddr,fSize_bytes = df.absoluteAddrSize_bytes(v)

		fLine = ''
		if isPREF(eLayout.full):
			fLine += ' '  + stringifyField__offset(df)
		else:
			fLine += ' '  + stringifyField__isStatic(df)
		if isPREFin((eLayout.onlySize, eLayout.full)):
			fLine += ' ' + stringifyField__size(df.fThis)

		if SUBST_Debug and toplevKn.tapDeck!=None:
			printf('%s%s%sHave tapDeck=%s    %s\n',
				   FONTred,boldFONT,italicFONT,resetFONT,str(toplevKn.tapDeck))
		if SUBST_Debug and toplevKn.baseClasses_list!=None:
			printf('%s%s%sHave baseClasses_list=%s   %s\n', FONTred,boldFONT,
				   italicFONT,resetFONT,stringify_aList(toplevKn.baseClasses_list))

		fTypeBareStr=None
		candidateA=None # Because don't trust Python to manage scope; clear explictly.
		candidateB=None
		candidateC=None
		(fType_noElab,fElab) = Elaboration.extract(fType, UnravelDepth())
		if TYPEnameCHOICE_Debug:
			printf('%s%s%s// fType "%s", fType_noElab "%s"\n',
				   FONTyellowRUDE,nameRoughly,resetFONT, str(fType), str(fType_noElab))

		if isFundamental(fType_noElab) and 0==len(teArgs) and 0==len(toplev_baseTypes):
			fTypeBareStr=str(fType_noElab)
			if TYPEnameCHOICE_Debug:
				printf('Chose: as-was "%s%s%s"\n',FONTblue,fTypeBareStr,resetFONT)
			if SUBST_Debug: printf('Accepted as-was, elab=(%s)\n', str(fElab))

		if isCanonicalIterType(fType):
			fTypeBareStr = impl__type_nameOnly(fType)
			if TYPEnameCHOICE_Debug:
				printf('Chose: direct nameOnly "%s%s%s"\n',FONTblue,fTypeBareStr,resetFONT)
			# If control reached here, we need to strip certain elaborations which no
			# longer make sense *now that we know this is an iterator*.
			fElab.is_ptr = False
			fElab.targetType_isConst = False

		if None==fTypeBareStr:
			if SUBST_Debug: printf('%s%s############## BEGIN simplifTry-A%s for "%s"\n',
								   boldFONT,FONTmagenta,resetFONT, nameRoughly)
			candidateA = simplifyTypename(eSimplifFocus.aField, fType_noElab,
										  str(fType_noElab), toplevKn, df=df)
			if SUBST_Debug: printf('%s%s############## END simplifTry-A%s ==>   "%s"  (%s)\n',
								   boldFONT,FONTmagenta,resetFONT, candidateA, str(fElab))
			if '#' in candidateA or '@' in candidateA:
				fTypeBareStr = candidateA
				if TYPEnameCHOICE_Debug:
					printf('Chose: candidateA "%s%s%s"\n',FONTblue,fTypeBareStr,resetFONT)

		if None==fTypeBareStr:
			if SUBST_Debug: printf('%s%s############## BEGIN simplifTry-B%s for "%s"\n',
								   boldFONT,FONTmagenta,resetFONT, nameRoughly)
			(candidateB,fElabB) = unravelElab_noDecorate(fType, toplevKn)
			if SUBST_Debug: printf('%s%s############## END simplifTry-B%s ==>   "%s"  (%s)\n',
								   boldFONT,FONTmagenta,resetFONT, candidateB, str(fElabB))

		if None==fTypeBareStr and \
		   (candidateA.find('<') >= 0) and (cmpPrep(candidateA) == cmpPrep(candidateB)):
			if SUBST_Debug: printf('%s%s############## BEGIN simplifTry-C%s for "%s"\n',
								   boldFONT,FONTmagenta,resetFONT, nameRoughly)
			(candidateC,fElabC) = unravelElab_noDecorate(fType)
			if SUBST_Debug: printf('%s%s############## END simplifTry-C%s ==>   "%s"  (%s)\n',
								   boldFONT,FONTmagenta,resetFONT, candidateC, str(fElabC))
			if (candidateC.find('<')<0 and candidateB.find('<')>=0) or \
			   (len(candidateC) < len(candidateB)):
				fTypeBareStr = candidateC
				if TYPEnameCHOICE_Debug:
					printf('Chose: candidateC "%s%s%s"\n',FONTblue,fTypeBareStr,resetFONT)

		if None==fTypeBareStr:
			fTypeBareStr = candidateB
			if TYPEnameCHOICE_Debug:
				printf('Chose: candidateB "%s%s%s"\n',FONTblue,fTypeBareStr,resetFONT)

		fTypeSumptuousStr = fTypeBareStr.rjust(PREF_PrintWidth_MemberType).replace('@',sprintf('%s%s@%s%s',resetFONT,FONTgreen,resetFONT,boldFONT)).replace('#',sprintf('%s%s#%s%s',resetFONT,FONTgreen,resetFONT,boldFONT))
		fLine += '  '
		fLine += (boldFONT + fTypeSumptuousStr + resetFONT)
		fLine += ' '
		fLine += stringify__isConst(fElab.targetType_isConst)
		fLine += stringify__isVolatile(fElab.targetType_isVolatile)
		fLine += ' '
		fLine += stringify__isPointer(fElab.is_ptr)
		fLine += ' '
		fLine += stringify__isConst(fElab.objItself_isConst)
		fLine += stringify__isVolatile(fElab.objItself_isVolatile)
		fLine += ' '
		fLine += stringify__isReference(fElab.is_lvalRef, fElab.is_rvalRef)
		fLine += ' '
		fLine += (boldFONT + FONTred + stringifyField__name(df) + resetFONT)
		if len(fElab.arrayDimensions):
			fLine += (' ' + fElab.arrayDimensions)
		if not isCallable(fType): fLine += ' ;'
		printf('%s', fLine)

		fLine = ''
		fLine += FONTmagenta
		#
		printComposeRelations = isPREF(eNestedDatamemb.full) and PREF_Relations
		printInheritRelations = isPREF(eBaseClasses.full) and PREF_Relations
		fTagAnc=''
		if df.fAncest:
			if df.fAncest.is_base_class:
				if printInheritRelations:
					if df.fAncest not in toplev_baseType_fields:
						die('?anc[%s]  %s', df.fAncest.name, df.fAncest.__repr__())
					btTag = toplev_baseType_fields[df.fAncest]
					fTagAnc = sprintf('/inhAnc=@%u@', btTag) # "inh" ==> inheritance
			else:
				if printComposeRelations:
					fTagAnc = sprintf('/comAnc=%s', df.fAncest.name) # "com" ==> composition
		if len(fTagAnc): fTagAnc += '  '
		#
		if df.fParent:
			if df.fParent.is_base_class:
				if printInheritRelations:
					ty_inhPar_strName = simplifyTypename(eSimplifFocus.aField, df.fParent.type,
														 df.fParent.name, toplevKn)
					fLine += sprintf('  %u=dep  %s/inhPar=%s',
									 df.depth, fTagAnc, ty_inhPar_strName)
			else:
				if printComposeRelations:
					fLine += sprintf('  %u=dep  %s/comPar=%s',
									 df.depth, fTagAnc, df.fParent.name)
		else:
			if printInheritRelations or printComposeRelations:
				fLine += sprintf('  %u=dep', 0)
		#
		fLine += resetFONT
		if PREF_Underly:
			fTypeDecoratedStr = Elaboration.decorate(fTypeBareStr, fElab)
			fType_basic = fType.unqualified()
			fLine += sprintf('   %s%s%s',
							 italicFONT,type_codeToStr[fType_basic.code], resetFONT)
			underly_ty_f_strName = simplifyTypename(eSimplifFocus.aField, fType_basic,
													nameTypeConcisely(fType_basic),
													toplevKn, df=df)
			if strip__spaces(underly_ty_f_strName) != strip__spaces(fTypeDecoratedStr):
				fLine += sprintf('   %s', sprintfAltName('Underly',underly_ty_f_strName))
		#
		fLine = fLine.lstrip()
		if (len(fLine) - len(FONTmagenta) - len(resetFONT)) > 0:
			printf('\n%s%s', ''.ljust(30), fLine)

		if df.vThis != None:
			assert v != None # TODO rm later
			saved_nestLev = indents.nestLev
			indents.incrIndent(3)
			indents.newLine_misc()
			wrap__valueProper(df.vThis, indents, fType, fAbsAddr, fSize_bytes)
			indents.nestLev = saved_nestLev

		if isCallable(fType):
			indents.incrIndent()
			indents.newLine_beginList('(')
			params = fType.fields()
			for i in range(len(params)):
				if i: indents.sameLine_nextItem(',')
				printf('%s%s%s',
					   impl__type_nameOnly(params[i].type),
					   stringifyType__referenceTag(params[i].type).strip(),
					   stringifyType__pointerTag(params[i].type).strip())
			indents.sameLine_endList(');')
			indents.decrIndent()

	actual_bitpos = ty.sizeof * 8
	if actual_bitpos > expected_bitpos and isPREF(eLayout.full):
		indents.newLine_nextItem(' ')
		printfPad__size(actual_bitpos, expected_bitpos)

	indents.newLine_endList('}')
	printf('\n')


def unravelElab_noDecorate (cxxType, toplevKn_override=None):
	cfid = next_callFrameId()
	assert cxxType and isinstance(cxxType, gdb.Type)
	tA = cxxType.strip_typedefs() # But don't strip CV-qualifiers.
	ud = UnravelDepth()

	(tB,elab) = Elaboration.extract(tA, ud)
	if isPlain(tB):
		sC = unravelTempl_recurs(tB, ud.mkIncr_dElab(), False, toplevKn_override)
	else:
		sC =  unravelElab_recurs(tB, ud.mkIncr_dElab(), False, toplevKn_override)
#	sD = Elaboration.decorate(sC, elab)
	if SUBST_Debug or UNRAVEL_Debug:
		printf('%s zRet "%s"  %s\n', cfid, sC, listCallers(5,omitInnermost=False))
	return (sC, elab) # Caller will decorate, we don't need to.


def unravelElab_recurs (cxxType, ud, decorateAfter,
						toplevKn_override=None, extra_nicknumberLookup_tapDeck=None):
	cfid = next_callFrameId()
	assert cxxType and isinstance(cxxType, gdb.Type)
	assert isinstance(ud, UnravelDepth)
	assert_bool(decorateAfter)
	if UNRAVEL_Debug:
		printf('%s%s %sBEG-Elab%s %s%s%s "%s%s%s" %s%s%s%s\n' ,ud.dbgIndent(),cfid,
			   FONTcyanRUDE,resetFONT , FONTgreen,str(ud),resetFONT ,
			   boldFONT,cmpPrep(str(cxxType)),resetFONT ,
			   FONTmagenta,italicFONT,immedCaller(1),resetFONT)
	tA = cxxType
	(tB,elab) = Elaboration.extract(tA, ud)
	if isPlain(tB):
		sC = unravelTempl_recurs(tB, ud.mkIncr_dElab(), decorateAfter,
								 toplevKn_override, extra_nicknumberLookup_tapDeck)
	else:
		sC =  unravelElab_recurs(tB, ud.mkIncr_dElab(), decorateAfter,
								 toplevKn_override, extra_nicknumberLookup_tapDeck)
	if decorateAfter:
		sD = Elaboration.decorate(sC, elab)
	else:
		sD = sC
	if UNRAVEL_Debug:
		printf('%s%s %sEND-Elab%s %s%s%s "%s%s%s%s"\n' ,ud.dbgIndent(),cfid,
			   FONTcyanRUDE,resetFONT , FONTgreen,str(ud),resetFONT ,
			   FONTblue,boldFONT,sD,resetFONT)
	return sD


# If passed a "toplevKn_override" arg, that means invoker is impl__type(), asking about a field.
#
def unravelTempl_recurs (cxxType, ud, decorateAfter,
						 toplevKn_override=None, extra_nicknumberLookup_tapDeck=None):
	cfid = next_callFrameId()
	assert cxxType and isinstance(cxxType, gdb.Type)
	assert isinstance(ud, UnravelDepth)

	assert_bool(decorateAfter)
	ty = get_basic_type(cxxType) # Go with this one simplification, for now.
	tyStr = str(ty)
	if SUBST_Debug:
		printf('%s %s ty="%s"\n', cfid, str(ud), tyStr)
	if UNRAVEL_Debug:
		printf('%s %s%sBEG-Tmpl%s %s%s%s "%s%s%s"\n',
			   cfid, ud.dbgIndent(),
			   FONTyellowRUDE,resetFONT , FONTgreen,str(ud),resetFONT ,
			   boldFONT,cmpPrep(tyStr),resetFONT)
	teArgs = list_templateArgs(ty)
	if PREF_Debug: dump_templateArgs(teArgs)
	(ppClass,if_iterHusk) = gdbType_to_ppClass(ty, try__unwrap_iteratorType=True)
	if if_iterHusk !=None and if_iterHusk.coreType !=None:
		ty = get_basic_type(if_iterHusk.coreType)
		if UNRAVEL_Debug or LOOKUPppCLASS_Debug:
			printf('%s Unwrap "%s" from "%s"\n', cfid, str(ty), tyStr)
		tyStr = str(ty)
		teArgs = list_templateArgs(ty)
		assert len(teArgs) > 0
	tToplev_isKnownSTL = (ppClass != None) and ppClass.isKnownSTL()
	if (ppClass != None) and 0 == len(teArgs): # Can happen if no such *objects* found.
		if toplevKn_override!=None:
			tyNameShow = simplifyTypename(eSimplifFocus.aType_solo, ty, tyStr,
										  toplevKn_override, teArg_depth=ud.dTempl)
			return tyNameShow
		else:
			return tyStr
	tar = lookupTeArgs_Rule(ppClass, teArgs)
	if SUBST_Debug and tar: TeArgs_Rule.dump(tar, teArgs)
	tapDeck = _te_arg_profile.TeArg_Profile__Deck(len(teArgs))
	if UNRAVEL_Debug:
		ppStr='None'
		if ppClass!=None: ppStr = ppClass.__name__
		tarStr='None'
		if tar!=None: tarStr = tar.__class__.__name__
		printf('%s %s%s%s%u=%s|teArgs| ppClass%s=%s%s tar%s=%s%s\n',
			   cfid, ud.dbgIndent(), boldFONT,FONTred,len(teArgs),resetFONT,
			   FONTred,ppStr,resetFONT, FONTred,tarStr,resetFONT)
	for i_teArg in range(len(teArgs)):
		teArg = teArgs[i_teArg]
		tapCurr = tapDeck.add__TeArg_Profile(tar, teArg)
		if tar:
			if tapCurr.want_derElementals:
				teArg_str_simplif = unravelElab_recurs(teArg, ud.mkIncr_dTempl(), decorateAfter)
				tapCurr.set__derElementals(teArg_str_simplif)
			tapDeck.composeElementals_maybe(i_teArg)
			tapCurr.decide_kind()
		#
		if isinstance(teArg,gdb.Type):
			toplevKn_partial = ToplevKnowns(ty, tToplev_isKnownSTL, tapDeck,
											ppClass=ppClass,tar=tar)
			use_strFinal = simplifyTypename(eSimplifFocus.aTeArg,
											ternary(isinstance(teArg,gdb.Type),teArg,None),
											tapCurr.strBest,
											nonNull(toplevKn_override,toplevKn_partial),
											teArg_depth=ud.dTempl,
											cardTeArgsAlreadyParsed=i_teArg,
											recv_nicknumberLookup_tapDeck=
											extra_nicknumberLookup_tapDeck)
			tapCurr.set__strFinal(use_strFinal)
		else:
			tapCurr.set__strFinal(str(teArg))
		if UNRAVEL_Debug:
			printf('%s %si%s=%u%s  %s%sOrig{%s%s%s%s}  Best{%s%s%s%s}  Final{%s%s%s%s}%s\n',
				   cfid, ud.dbgIndent(), FONTred,i_teArg,resetFONT , boldFONT,italicFONT,
				   resetFONT,cmpPrep(tapCurr.strOriginal),boldFONT,italicFONT,
				   resetFONT,cmpPrep(tapCurr.strBest),boldFONT,italicFONT,
				   resetFONT,cmpPrep(tapCurr.strFinal),boldFONT,italicFONT,resetFONT)

	if SUBST_Debug:
		printf('%s%s%s%s\n%s %s  ty="%s%s%s%s"\nUltimately, tapDeck =\n%s%s\n\n',
			   mkBoldStripe('_'),
			   FONTgreen,listCallers(omitInnermost=False,stairwise=True),resetFONT,
			   cfid, str(ud),
			   FONTblue,boldFONT,tyStr,resetFONT,
			   str(tapDeck), mkBoldStripe('_'))
	if toplevKn_override !=None:
		save__tapDeck = toplevKn_override.tapDeck
		toplevKn_override.tapDeck = tapDeck
		tyNameShow = simplifyTypename(eSimplifFocus.aField, ty, tyStr,
									  toplevKn_override, teArg_depth=ud.dTempl)
		toplevKn_override.tapDeck = save__tapDeck

	else:
		toplevKn = ToplevKnowns(ty, tToplev_isKnownSTL, tapDeck, ppClass=ppClass,tar=tar)
		if PREF_Debug: printf('%s %sbig-kahuna toplevKn%s =\n\t%s%s%s\n',cfid,
							  FONTred,resetFONT, boldFONT,str(toplevKn),resetFONT)
		tyNameShow = simplifyTypename(eSimplifFocus.aType_solo, ty, tyStr,
									  toplevKn, teArg_depth=ud.dTempl)
	if UNRAVEL_Debug:
		printf('%s%s %sEND-Tmpl%s %s%s%s "%s%s%s%s"\n' ,ud.dbgIndent(), cfid,
			   FONTyellowRUDE,resetFONT , FONTgreen,str(ud),resetFONT ,
			   FONTblue,boldFONT,tyNameShow,resetFONT)
	return tyNameShow


def impl__type_nameOnly (cxxType, extra_nicknumberLookup_tapDeck=None):
	from _stl_iterators import iterTypenameSuffix, getPP, primitive__typeOfContainer
	cfid = next_callFrameId()
	assert cxxType and isinstance(cxxType, gdb.Type)
	assert ((None==extra_nicknumberLookup_tapDeck)
			or
			isinstance(extra_nicknumberLookup_tapDeck, _te_arg_profile.TeArg_Profile__Deck))
	#
	t = cxxType
	s_tOrig = str(t)
	if TYPEnameCHOICE_Debug or PREF_Debug:
		printf('%s %s%sOrig, %s%s,  "%s%s%s"\n\t%s%s%s%s\n',cfid,
			   FONTmagenta,boldFONT,type_codeToStr[t.code],resetFONT,
			   FONTmagenta,s_tOrig,resetFONT,
			   FONTgreen,italicFONT,listCallers(4,omitInnermost=False),resetFONT)

	if 'iterator' in s_tOrig:
		proceed_withUnraveling_tCont=False
		primitiveMode=False

		if t.code == TYPE_CODE_TYPEDEF:
			(tCont,isConstIter,
			 markIterReverse) = _stl_iterators.primitive__typeOfContainer(t)
			if tCont!=None:
				if TYPEnameCHOICE_Debug:
					printf('%s primitive__typeOfContainer success\n',cfid)
				proceed_withUnraveling_tCont=True
				primitiveMode=True
			elif TYPEnameCHOICE_Debug:
				printf('%s primitive__typeOfContainer(t) ret None.\n',cfid)

		if not proceed_withUnraveling_tCont:
			(iterppClass,iterHusk) = _stl_iterators.getPP(t,True)
			if iterppClass:
				proceed_withUnraveling_tCont=True
				if TYPEnameCHOICE_Debug: printf('iterppClass = %s\n', iterppClass.__name__)
				tIter = t
				coreMost_tIter = t
				if None==iterHusk.coreType:
					if TYPEnameCHOICE_Debug: printf('coreType is None.\n')
				else:
					if TYPEnameCHOICE_Debug: printf('coreType  "%s"\n', str(iterHusk.coreType))
					coreMost_tIter = iterHusk.coreType
				(tCont,isConstIter) = iterppClass.typeOfContainer(tIter,
																  iterHusk.coreType)
				markIterReverse = iterHusk.any_reverseWrappers
			elif TYPEnameCHOICE_Debug:
				printf('_stl_iterators.getPP(t) ret None.\n')

		if proceed_withUnraveling_tCont:
			if TYPEnameCHOICE_Debug: printf('tCont  "%s"\n', str(tCont))
			s=None
			if tCont!=None:
				t = tCont.strip_typedefs()
				if TYPEnameCHOICE_Debug or PREF_Debug:
					printf('%s Aft strip_typedefs, %stCont of iter%s:\n\t%s%s%s\n',cfid,
						   FONTred,resetFONT, boldFONT,str(tCont),resetFONT)
				s = unravelElab_recurs(t, UnravelDepth(), True)
			elif not primitiveMode:
				(s,isConstIter) = iterppClass.appx_typenameOfContainer(coreMost_tIter)
			if s!=None:
				s += _stl_iterators.iterTypenameSuffix(isConstIter,markIterReverse)
				if TYPEnameCHOICE_Debug or SUBST_Debug or PREF_Debug:
					printf('%s Returning iter "%s"\n', cfid, s)
				return s

	t = t.strip_typedefs()
	if TYPEnameCHOICE_Debug or PREF_Debug:
		printf('%s Aft strip_typedefs, %st of non-iter%s\n\t%s%s%s\n',
			   cfid, FONTred,resetFONT, boldFONT,str(t),resetFONT)
	s = unravelElab_recurs(t, UnravelDepth(), True,
						   extra_nicknumberLookup_tapDeck=extra_nicknumberLookup_tapDeck)
	if TYPEnameCHOICE_Debug or SUBST_Debug or PREF_Debug:
		printf('%s Returning non-iter "%s"\n', cfid, s)
	return s


def extract_filesSpec (stab, sline):
	srcfileSpec = ''
	objfileSpec = ''
	if stab and stab.is_valid():
		if hasattr(stab,'objfile'):
			objf = stab.objfile
			if objf and objf.filename:
				objfileSpec = prettyPath(objf.filename)
			srcfileSpec = prettyPath(stab.fullname())
			if 0 == len(srcfileSpec): srcfileSpec = prettyPath(stab.filename)
	if sline: srcfileSpec += sprintf(':%u', sline)
	return (srcfileSpec,objfileSpec)


def impl__afar (v, symb_lookup_rv, fr, b):
	symb = None
	if symb_lookup_rv:
		symb = symb_lookup_rv[0]
	assert((v==None)or isinstance(v, gdb.Value))
	assert(not symb or isinstance(symb, gdb.Symbol))
	assert(not fr   or isinstance(fr, gdb.Frame))
	assert(not b    or isinstance(b, gdb.Block))

	main__srcfileSpec=''
	main__objfileSpec=''
	scope_perAddr = None
	scope_perBlock = None
	basic_notes = []
	scope_notes = []
	storage_notes = []
	unusual_notes = []

	if (v!=None): #___________________________________ what we can get from *v*
		if v.type:
			indents = _indent_spec.IndentSpec(0)
			focusType = get_basic_type(v.type)
			tyNameShow = impl__type_nameOnly(focusType)
			basic_notes.append(tyNameShow) #str(focusType))
			basic_notes.append(type_codeToStr[focusType.code])
			basic_notes.append(stringifyType__size(focusType).strip())

		if v.address:
			basic_notes.append(prAddr(v.address))

			if fr:
				scope_perAddr = describeScopeGivenAddr(v.address, fr)

		if v.is_optimized_out:
			unusual_notes.append('Optimized out')

		if v.is_lazy:
			unusual_notes.append('Lazy -- XXX, fetch?')

	if symb: #_____________________________ what we can get from *symb*
		if symb_lookup_rv[1]:
			basic_notes.append('An ivar')

		sname = symb.name
#		notes.append(sprintf('Symb name = "%s"', sname))

		if PREF_Debug and symb.linkage_name and symb.linkage_name != sname:
			storage_notes.append(sprintf('Diff linkage_name = "%s"', symb.linkage_name))

		if symb.print_name and symb.print_name != sname:
			storage_notes.append(sprintf('Diff print_name = "%s"', symb.print_name))

		storCat = addrcStorageCategory(symb.addr_class)
		if storCat:
			basic_notes.append(storCat)

		if symb.is_argument: basic_notes.append('An argument')
#		if symb.is_variable: notes.append('a variable') # Absence of "a constant" enough.
		if symb.is_constant: basic_notes.append('A constant')
		if symb.is_function: basic_notes.append('A function')

		sline = symb.line
		stab = symb.symtab
		if (not stab or not stab.is_valid()) and fr:
			stab_and_line = fr.find_sal()
			if stab_and_line:
				sline = nonNull(sline, stab_and_line.line)
				stab = stab_and_line.symtab
		(main__srcfileSpec,main__objfileSpec) = extract_filesSpec(stab, sline)
		if len(main__srcfileSpec): scope_notes.append('Def at= ' + main__srcfileSpec)
#		if len(main__objfileSpec): storage_notes.append(main__objfileSpec)

	if fr: #_________________________________ what we can get from *fr*
		if fr.type() and (fr.type() in frame_typeToStr):
			if fr.type() != gdb.NORMAL_FRAME:
				unusual_notes.append(sprintf('Frame: %s', frame_typeToStr[fr.type()]))

		fr__stal = fr.find_sal()
		if fr__stal and fr__stal.is_valid():
			fr__stab = fr__stal.symtab
			if fr__stab and fr__stab.is_valid():
				fr__lt = fr__stab.linetable()
				if fr__lt and fr__lt.is_valid():
					pass #iterdump_LineTable(fr__lt)

# There's more, but sadly it's all utterly uninteresting.
#		fr__notes = []
#		fr__pc = fr.pc()
#		fr__notes.append(sprintf('name= %s', fr.name()))
#		if fr.type() and fr.type() in frame_typeToStr:
#			fr__notes.append(sprintf('type= %s', frame_typeToStr[fr.type()]))
#		fr__stab_and_line = fr.find_sal()
#		if fr__stab_and_line:
#			fr__line = fr__stab_and_line.line
#			if fr__line: fr__notes.append(sprintf('line= %u', fr__line))
#			fr__pc = nonNull(fr__pc, fr__stab_and_line.pc)
#		if fr__pc: fr__notes.append(sprintf('pc= 0x%X', fr__pc))
#		if len(fr__notes): notes.append(sprintf('Frame: %s', '; '.join(fr__notes)))

	fu__name = ''
	if b: #___________________________________ what we can get from *b*
		fu = b.function
		if not fu and fr:
			fu = fr.function() # Yes indeed: Block.function, but Frame.function()
		if fu and (None==v or (not v.is_optimized_out and not isCallable(v.type))):
			fu__name = getattr(fu,'name',None)

			fu__storCat = addrcStorageCategory(fu.addr_class)
			if fu__storCat:
				storage_notes.append(sprintf('Storage category: %s', fu__storCat))

			fu__stab = fu.symtab
			(fu__srcfileSpec,fu__objfileSpec) = extract_filesSpec(fu__stab, fu.line)
			# TODO: use fu__objfileSpec, if differ from main__objfileSpec
			if len(fu__srcfileSpec):
				scope_notes.append(sprintf('scope began= %s', fu__srcfileSpec))

		scope_perBlock = scopeOfBlock(b)

	if fu__name:
		scope_notes.append(sprintf('scope= "%s"', fu__name))
	elif scope_perAddr or scope_perBlock:
		scope_notes.append(sprintf('scope= %s', nonNull(scope_perBlock, scope_perAddr)))
		# They shouldn't differ, but if did, the from-Block one would be more specific?

	notesAll = []
	if len(basic_notes):   notesAll.append(              ' | '.join(basic_notes))
	if len(scope_notes):   notesAll.append(              ' | '.join(scope_notes))
	if len(storage_notes): notesAll.append('Storage: ' + ' | '.join(storage_notes))
	if len(unusual_notes): notesAll.append(              ' | '.join(unusual_notes))
	if len(notesAll):
		printf('%s', '\n'.join(notesAll))


@accepts(str)
def parseAndEval (s):
	try:
		return gdb.parse_and_eval(s)
	except BaseException as whatev:
		printf('%s%s%s\n', FONTmagenta, str(whatev), resetFONT)
		return None


@accepts(str)
def find_ValueSymbolFrameBlock (s):
	v = None
	symb_lookup_rv = None
	b = None
	fr = gdb.selected_frame()
	if fr and not fr.is_valid(): fr=None
	if fr:
		try: v = fr.read_var(s)
		except BaseException as whatev: None
		#if (v!=None): printf('vOK! frame.read_var(name)\n')
		if (v==None):
			blocksToTry = []
			fr__b = blockOfFrame(fr)
			if fr__b:
				if blockValid(fr__b):
					blocksToTry.append(fr__b)
				if fr__b.global_block and blockValid(fr__b.global_block):
					blocksToTry.append(fr__b.global_block)
				if fr__b.static_block and blockValid(fr__b.static_block):
					blocksToTry.append(fr__b.static_block)
			for xb in blocksToTry:
				b = xb
				symb_lookup_rv = gdb.lookup_symbol(s, block=b)
				assert symb_lookup_rv # XXX If assumption violated, do as in find_Symbol()??
				symb = symb_lookup_rv[0]
				if symb and symb.is_valid():
					try: v = symb.value(fr)
					except BaseException as whatev: None
					#if (v!=None): printf('vOK! lookup_symbol().value(fr)\n')
					break
	if not b and fr:
		b = blockOfFrame(fr)
		if not blockValid(b): b=None
	if (v==None) and b and fr and symb_lookup_rv and symb_lookup_rv[0]:
		try: v = fr.read_var(symb_lookup_rv[0], b)
		except BaseException as whatev: None
		#if (v!=None): printf('vOK! frame.read_var(symb,b)\n')
	if not symb_lookup_rv or not symb_lookup_rv[0]:
		symb = lookup_global_symbol(s)
		if symb:
			symb_lookup_rv = (symb,False)
			if (v==None):
				if fr:   v = symb.value(fr)
				else:    v = symb.value()
				#if (v!=None): printf('vOK! lookup_global_symbol().value([fr])\n')
	if not b and (v!=None) and v.address:
		try: b = gdb.block_for_pc(int(v.address))
		except BaseException as whatev: None
		if b and not b.is_valid(): b=None
		if b and not symb_lookup_rv:
			symb_lookup_rv = gdb.lookup_symbol(s, block=b)
	if (v==None) and symb_lookup_rv and symb_lookup_rv[0] and symb_lookup_rv[0].is_valid():
		symb = symb_lookup_rv[0]
		try: v = symb.value()
		except BaseException as whatev: None
	if (v==None):
		v = parseAndEval(s) # Most expensive, least accurate way to find Value; last resort.
		#if (v!=None): printf('vOK! parse_and_eval(name)\n')
	return (v,symb_lookup_rv,fr,b)
