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

from gdb.printing import *
from gdb import *

from _usability import *
from _codes_stringified import *
from _common import *
from _pp_base_classes import IteratorPP
import _te_args_rules


def iterTypenameSuffix (is_const, is_reverse):
	assert_bool(is_const)
	assert_bool(is_reverse)
	if not is_const and not is_reverse:
		return '::iterator'
	elif is_const and not is_reverse:
		return '::const_iterator'
	elif not is_const and is_reverse:
		return '::reverse_iterator'
	elif is_const and is_reverse:
		return '::const_reverse_iterator'


def isCanonicalIterType_givenStr (s):
	return (s.endswith('::iterator') or
			s.endswith('::const_iterator') or
			s.endswith('::reverse_iterator') or
			s.endswith('::const_reverse_iterator'))

def isCanonicalIterType (t):
	s = str(t)
	return isCanonicalIterType_givenStr(s)


def simple__typeOfContainer (tIter):
	assert tIter!=None and isinstance(tIter,gdb.Type)
	retvalIfErr = (None,False)
	if PREF_Debug:
		printf('%s___________________________________%s\n',FONTred,resetFONT)
		printf('tIter =\n\t%s%s%s\n', boldFONT,str(tIter),resetFONT)
	if not isCanonicalIterType(tIter):
		if PREF_Debug: printf('\nunusable tIter "%s"\n', str(tIter))
		return retvalIfErr
	isConstIter = False
	# Now to extract "std::list<blah>" from "std::list<blah>::iterator"
	s_tIter = str(tIter)
	if s_tIter.endswith('::iterator'):
		s_tCont = s_tIter[:-(len('::iterator'))]
	elif s_tIter.endswith('::const_iterator'):
		s_tCont = s_tIter[:-(len('::const_iterator'))]
		isConstIter=True
	elif s_tIter.endswith('::reverse_iterator'):
		s_tCont = s_tIter[:-(len('::reverse_iterator'))]
	else: # Else endswith('::const_reverse_iterator')
		s_tCont = s_tIter[:-(len('::const_reverse_iterator'))]
		isConstIter=True
	try:
		tCont = gdb.lookup_type(s_tCont)
		return (tCont,isConstIter)
	except BaseException as whatev:
		if PREF_Debug: printf('\nunusable s_tCont "%s"\n', s_tCont)
		return retvalIfErr


class std__front_insert_iterator (IteratorPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0))
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = v['container']
		self.sz_overhead = 0

class std__back_insert_iterator (IteratorPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0))
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = v['container']
		self.sz_overhead = 0


def primitive__typeOfContainer (tOrig): # To return (tCont,isConstIter,markIterReverse)
	retvalIfErr = (None,False,False)
	s_tOrig = str(tOrig)
	if not (s_tOrig.startswith('std::initializer_list<') or
			s_tOrig.startswith('std::vector<bool,') or
			s_tOrig.startswith('std::array<')):
		return retvalIfErr
	(tCont,isConstIter) = simple__typeOfContainer(tOrig)
	if tCont==None:
		return retvalIfErr
	markIterReverse = s_tOrig.endswith('reverse_iterator')
	return (tCont,isConstIter,markIterReverse)


# Iterators into std::initializer_list<T> and std::array<T,N> are just raw pointers.
# Also, iterators into std::basic_string_view<Ch,ChTRAITS>
class just_raw_pointer (IteratorPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type).target()
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = v
		self.sz_overhead = 0
		self.targetType = targetType # For _stl_utilities::std__string_view::iteratorStanding()'s benefit


class std__string (IteratorPP):
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		return simple__typeOfContainer(tIterHusk) # Yeah????
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0)).target()
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = v['_M_current']
		self.sz_overhead = 0


class std__vector__bool (IteratorPP):
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		return simple__typeOfContainer(tIterHusk) # Yeah????
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = gdb.lookup_type('bool') # Fake it.
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.sz_overhead = 0
		self.target_nodeAddr        = v['_M_p']
		self.target_intranodeOffset = v['_M_offset']
		# Need to figure targetVal, so that IndirectorPP::figureVal() won't try to.
		storewordType = gdb.lookup_type('unsigned long')
		p_word = castTo_ptrToType(self.target_nodeAddr, storewordType)
		if 0x0 == int(p_word):
			self.targetAddr = p_word # IndirectorPP::figureVal(), "<NULL indirector>"
			self.empty=True
			return
		self.empty=False
		word = int(p_word.dereference())
		if word & (1 << self.target_intranodeOffset):
			self.targetVal = gdb.Value(True)
		else:
			self.targetVal = gdb.Value(False)


class std__vector (IteratorPP):
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		if tIterCore==None:
			tIter = tIterHusk
		else:
			tIterHusk_teArgs = list_templateArgs(tIterHusk)
			if len(tIterHusk_teArgs) == 1:
				tIter = tIterCore
			else:
				tIter = tIterHusk
		retvalIfErr = (None,False)
		tIterUsing = tIter
		if isCanonicalIterType(tIter):
			tIterUsing = tIter.strip_typedefs()
		teArgs = list_templateArgs(tIterUsing)
		if len(teArgs) != 2:
			if PREF_Debug: printf('len(teArgs)=%u != 2\n',len(teArgs))
			return retvalIfErr
		tElemPtr = teArgs[0].strip_typedefs()
		if tElemPtr.code != TYPE_CODE_PTR:
			if PREF_Debug: printf('tElemPtr.code=%s != PTR\n', type_codeToStr[tElemPtr.code])
			return retvalIfErr
		tElem = tElemPtr.target()
		isConstIter = tElem == tElem.const()
		return (teArgs[1] , isConstIter)
	#
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0)).target()
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = v['_M_current']
		self.sz_overhead = 0


class std__list (IteratorPP):
	#
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		if tIterCore==None:
			return simple__typeOfContainer(tIterHusk)
		tIterHusk_teArgs = list_templateArgs(tIterHusk)
		tIterCore_teArgs = list_templateArgs(tIterCore)
		if len(tIterCore_teArgs) > len(tIterHusk_teArgs):
			return simple__typeOfContainer(tIterCore)
		else:
			return simple__typeOfContainer(tIterHusk)
	#
	@staticmethod
	def appx_typenameOfContainer (tIter):
		retvalIfErr = (None,False)
		tIter_teArgs = list_templateArgs(tIter)
		if len(tIter_teArgs) != 1:
			printf('\nunusable tIter "%s"\n', str(tIter))
			return retvalIfErr
		tElem = tIter_teArgs[0]
		s_tCont = sprintf('std::list<%s%s??%s>', str(tElem), FONTredBackgd,resetFONT)
		isConstIter = str(tIter).startswith('std::_List_const_iterator<')
		return (s_tCont,isConstIter)
	#
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0))
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.p__List_node_base = v['_M_node']
		type__List_node_base = self.p__List_node_base.type.target()
		payload_offset = type__List_node_base.sizeof
		self.targetAddr = (castTo_ptrToVoid(self.p__List_node_base) + payload_offset)
		self.sz_overhead = max(0,v.type.sizeof - targetType.sizeof - WORD_WIDTH.const)


class std__forward_list (IteratorPP):
	#
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		if tIterCore==None:
			return simple__typeOfContainer(tIterHusk)
		assert(False) #XXX What, *can* we get a non-NULL tIterCore here???
		tIterHusk_teArgs = list_templateArgs(tIterHusk)
		tIterCore_teArgs = list_templateArgs(tIterCore)
		if len(tIterCore_teArgs) > len(tIterHusk_teArgs):
			return simple__typeOfContainer(tIterCore)
		else:
			return simple__typeOfContainer(tIterHusk)
	#
	@staticmethod
	def appx_typenameOfContainer (tIter):
		retvalIfErr = (None,False)
		tIter_teArgs = list_templateArgs(tIter)
		if len(tIter_teArgs) != 1:
			printf('\nunusable tIter "%s"\n', str(tIter))
			return retvalIfErr
		tElem = tIter_teArgs[0]
		s_tCont = sprintf('std::forward_list<%s%s??%s>',
						  str(tElem), FONTredBackgd,resetFONT)
		isConstIter = str(tIter).startswith('std::_Fwd_list_const_iterator<')
		return (s_tCont,isConstIter)
	#
	@staticmethod
	def reckon_payloadOffset (sizeof_node):
		if sizeof_node < WORD_WIDTH.const * 4:
			return WORD_WIDTH.const
		else:
			return min(8, WORD_WIDTH.const * 2)
	#
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0))
		nodeTypeName = sprintf('std::_Fwd_list_node<%s>', str(targetType))
		nodeType = gdb.lookup_type(nodeTypeName)
		payload_offset = std__forward_list.reckon_payloadOffset(nodeType.sizeof)
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.p__Fwd_list_node_base = v['_M_node']
		self.targetAddr = castTo_ptrToVoid(self.p__Fwd_list_node_base) + payload_offset
		self.sz_overhead = max(0,v.type.sizeof - payload_offset - WORD_WIDTH.const)


class std__deque (IteratorPP):
	#
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		return simple__typeOfContainer(tIterHusk)
	#

	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0))
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.p_node = v['_M_node'] # Here, "node" is a 512B chunk, storing 1+ elems.
		self.p_cur = v['_M_cur']
		self.targetAddr = self.p_cur
		self.sz_overhead = max(0,v.type.sizeof - targetType.sizeof - WORD_WIDTH.const)


class std__Node (IteratorPP):
	#
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		if tIterCore==None:
			return simple__typeOfContainer(tIterHusk)
		tIterHusk_teArgs = list_templateArgs(tIterHusk)
		tIterCore_teArgs = list_templateArgs(tIterCore)
		if len(tIterCore_teArgs) > len(tIterHusk_teArgs):
			return simple__typeOfContainer(tIterCore)
		else:
			return simple__typeOfContainer(tIterHusk)
	#
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		kvType = v.type.template_argument(0)
		IteratorPP.__init__(self, kvType)
		self.sz_used__objProper = v.type.sizeof
		self.nodeAddr = v['_M_cur']
		p_node = v['_M_cur']
		if int(p_node):
			x_addr = castTo_ptrToVoid(p_node) + int(WORD_WIDTH.const)
			uintType = gdb.lookup_type('unsigned int')
			while True:
				x_addr_as_uintPtr = castTo_ptrToType(x_addr, uintType)
				x_val = int(x_addr_as_uintPtr.dereference())
				if x_val != 0xBAADF00D:
					break
				x_addr += int(WORD_WIDTH.const)
			self.targetAddr = int(x_addr)
		else:
			self.targetAddr = int(p_node)
		self.sz_overhead = max(0,v.type.sizeof - kvType.sizeof - WORD_WIDTH.const)


class std__Rb_tree (IteratorPP):
	#
	@staticmethod
	def typeOfContainer (tIterHusk, tIterCore):
		if tIterCore==None:
			return simple__typeOfContainer(tIterHusk)
		tIterHusk_teArgs = list_templateArgs(tIterHusk)
		tIterCore_teArgs = list_templateArgs(tIterCore)
		if len(tIterCore_teArgs) > len(tIterHusk_teArgs):
			return simple__typeOfContainer(tIterCore)
		else:
			return simple__typeOfContainer(tIterHusk)
	#
	@staticmethod
	def appx_typenameOfContainer (tIter):
		retvalIfErr = (None,False)
		tIter_teArgs = list_templateArgs(tIter)
		if len(tIter_teArgs) == 1: #set?
			tElem = tIter_teArgs[0]
			s_tCont = sprintf('std::set<%s%s??%s>', str(tElem), FONTredBackgd,resetFONT)
			isConstIter = str(tIter).startswith('std::_Rb_tree_const_iterator<')
			return (s_tCont,isConstIter)
		elif len(tIter_teArgs) == 2: # map?
			printf('Not yet implemented!  Passed "%s"\n', str(tIter))
			return retvalIfErr
#	return (s_tCont,isConstIter)
		else:
			printf('\nunusable tIter "%s"\n', str(tIter))
			return retvalIfErr
	#
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = get_basic_type(v.type.template_argument(0))
		IteratorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.nodeAddr = v['_M_node']
		self.targetAddr = int(castTo_ptrToVoid(self.nodeAddr) + int(4) * WORD_WIDTH.const)
		self.sz_overhead = max(0,v.type.sizeof - targetType.sizeof - WORD_WIDTH.const)



# Will return 3-ple   (S,moveWrapper,reverseWrapper)   , where S is
# expected name of wrapper ivar if t is a wrapper type, else None.
def is_iteratorType_wrapperType (t, wrapDepth):
	assert isinstance(t, gdb.Type)
	tstr = str(t)
	dTag = sprintf('[%s%sd=%u%s %s]', FONTmagenta,boldFONT,wrapDepth,resetFONT,
				   immedCaller())
	tTag = sprintf('t=%s%s((%s  %s  %s%s))%s', boldFONT,italicFONT,resetFONT,
				   tstr, boldFONT,italicFONT,resetFONT)
	if tstr.startswith('std::move_iterator<'):
		if UNRAVEL_Debug:
			printf('%s Peeling move_iterator from %s\n', dTag, tTag)
		return ('_M_current',True,False)
	elif (tstr.startswith('std::reverse_iterator<') or
	      tstr.startswith('std::const_reverse_iterator<') or
	      tstr.endswith('>::reverse_iterator') or
		  tstr.endswith('>::const_reverse_iterator')):
		if UNRAVEL_Debug:
			printf('%s Peeling reverse_iterator from %s\n', dTag, tTag)
		return ('current',False,True)
	else:
		if UNRAVEL_Debug:
			printf('%s Nothing to peel from %s\n', dTag, tTag)
		return (None,False,False)


def unwrap_iteratorType (tOriginal): #To return an IteratorHusk.
	assert isinstance(tOriginal, gdb.Type)
	t = tOriginal
#	printf('\nCallers  %s\nShall try peel tOriginal =\n\t%s\n', listCallers(6),str(t))
	theType_whichWraps_t = None
	wrapDepth = int(0)
	husk = IteratorHusk()
	while True:
		didUnwrap=False
		(wrapperIvarName,movWr,revWr) = is_iteratorType_wrapperType(t, wrapDepth)
		if wrapperIvarName != None:
			if movWr: husk.any_moveWrappers=True
			if revWr: husk.any_reverseWrappers=True
			teArgs = list_templateArgs(t)
			if len(teArgs) == 1:
				te0 = teArgs[0]
				if isinstance(te0, gdb.Type):
					theType_whichWraps_t = t
					t = te0
					wrapDepth += int(1)
#					printf('d=%u Type-peel succ, now t=\n\t%s\n', wrapDepth, str(t))
					didUnwrap=True
				else:
					printf('d=%u %sWeird!%s Sole teArg of t[%s] is not a gdb.Type\n',
						   wrapDepth, FONTred, resetFONT, str(t))
			else:
				printf('d=%u  %sWeird!%s t[%s] has %u teArgs and not a sole teArg\n',
					   wrapDepth, FONTred, resetFONT, str(t), len(teArgs))
		if not didUnwrap: # No more layers left to unwrap?
			break
	if None == theType_whichWraps_t: # Hadn't been even one layer to unwrap?
		assert not husk.any_moveWrappers and not husk.any_reverseWrappers #Sanity
		return husk#None
	husk.coreType=t
	return husk#t


def unwrap_iteratorValue (vOriginal): #To return an IteratorHusk.
	assert isinstance(vOriginal, gdb.Value)
	v = vOriginal
#	printf('\n\%s\nShall try peel vOrig, type =\n\t%s\n',listCallers(6),str(v.type))
	theValue_whichWraps_v = None
	wrapDepth = int(0)
	husk = IteratorHusk()
	while True:
		didUnwrap=False
		t = v.type
		(wrapperIvarName,movWr,revWr) = is_iteratorType_wrapperType(t, wrapDepth)
		if wrapperIvarName != None:
			if movWr: husk.any_moveWrappers=True
			if revWr: husk.any_reverseWrappers=True
			if gdb.types.has_field(t, wrapperIvarName):
				theValue_whichWraps_v = v
				v = v[wrapperIvarName]
				wrapDepth += int(1)
#				printf('d=%u Value-peel succ, now v t=\n\t%s\n', wrapDepth, str(v.type))
				didUnwrap=True
			else:
				printf('d=%u %sWeird!%s The t[%s] lacks expected ivar "%s"\n',
					   wrapDepth, FONTred, resetFONT, str(t), wrapperIvarName)
		if not didUnwrap: # No more layers left to unwrap?
			break
	if None == theValue_whichWraps_v: # Hadn't been even one layer to unwrap?
		assert not husk.any_moveWrappers and not husk.any_reverseWrappers #Sanity
		return husk#None
	husk.coreType=v.type
	husk.coreValue=v
	return husk#v


typeName_to_iteratorPP = {}
# Pls keep sorted by alpha.
#		typeName_to_iteratorPP[ 'OrderedMap' ] = OrderedMap


#To return pair<IteratorPP,IteratorHusk> if try__unwrapType, else pair<IteratorPP,None>.
def getPP (t, try__unwrapType):
	assert_bool(try__unwrapType)
	assert isinstance(t, gdb.Type)
	tstr = str(t)
	if LOOKUPppCLASS_Debug:
		printf('%s_________________________________________________________________%s\n'\
			   '%s%s_stl_iter%s%s%s((%s  %s  %s%s))%s%s%s%s\n\t%s\n',
			   FONTgreenBackgd,resetFONT,
			   boldFONT,FONTgreenBackgd,resetFONT,boldFONT,italicFONT,resetFONT,
			   tstr, boldFONT,italicFONT,resetFONT,
			   FONTgreen,type_codeToStr[t.code],resetFONT,  listCallers(2))

	if try__unwrapType:
		iterHusk = unwrap_iteratorType(t)
		if iterHusk.coreType !=None:
			t = iterHusk.coreType
			tstr = str(t)
#		else:
#			printf('No core to de-husk; tstr perforce stays "%s"\n',tstr)
	else:
		iterHusk = None

	teArgs = list_templateArgs(t) # Rets list of gdb.Type (and/or gdb.Value)
#	dump_aList(teArgs, 'tIter teArgs')

	if False and PREF_Debug:
		dump_templateArgs(teArgs)
		parClasses = list_parentClasses(t)
		dump_aList(parClasses, 'parClasses')

	if (len(teArgs) == 0): # Iterators are all templated types, except iterators into...
		if t.code == TYPE_CODE_PTR:
			return (just_raw_pointer,iterHusk)  # ...std::array<T,N> or std::initializer_list<T>
		if tstr in ('std::_Bit_iterator', 'std::_Bit_const_iterator'):
			return (std__vector__bool,iterHusk) # ...std::vector<bool>
		if LOOKUPppCLASS_Debug: printf('iter::getPP retNone ((A))\n')
		return (None,iterHusk)

	first__template_paramList__startsAt = tstr.find('<')
	if not isCanonicalIterType_givenStr(tstr) and (first__template_paramList__startsAt > 1):
		before__template_paramList = tstr[:first__template_paramList__startsAt]
		first__scope_op__startsAt = before__template_paramList.find('::')
		if first__scope_op__startsAt < 0:
			tstrFocus = before__template_paramList
		else:
			tstrFocus = before__template_paramList[(first__scope_op__startsAt + 2):]
		if 'iterator' not in tstrFocus:
			if LOOKUPppCLASS_Debug: printf('iter::getPP retNone ((B))\n')
			return (None,iterHusk)

	te0 = str(teArgs[0])
	te1 = None
	if len(teArgs) >= 2:
		te1 = str(teArgs[1])

	if (len(teArgs) == 2) and ('char' in te0) and is_typeName__std_string(te1):
		return (std__string,iterHusk)

	if ((len(teArgs) >= 2)) and te1.startswith('std::vector<'):
		return (std__vector,iterHusk)

	if tstr.startswith('std::_List_') or (isCanonicalIterType_givenStr(tstr) and
										  strip__cxx11(tstr).startswith('std::list<')):
		return (std__list,iterHusk)

	if tstr.startswith('std::_Fwd_list_') or (isCanonicalIterType_givenStr(tstr) and
											  tstr.startswith('std::forward_list<')):
		return (std__forward_list,iterHusk)

	if tstr.startswith('std::_Deque_') or (isCanonicalIterType_givenStr(tstr) and
										   tstr.startswith('std::deque<')):
		return (std__deque,iterHusk)

	if tstr.startswith('std::__detail::_Node_') or (isCanonicalIterType_givenStr(tstr) and
													(tstr.startswith('std::unordered_set<') or
													 tstr.startswith('std::unordered_multiset<') or
													 tstr.startswith('std::unordered_map<') or
													 tstr.startswith('std::unordered_multimap<'))):
		return (std__Node,iterHusk)    # unordered associative (hashtable)

	if tstr.startswith('std::_Rb_tree_') or (isCanonicalIterType_givenStr(tstr) and
											 (tstr.startswith('std::set<') or
											  tstr.startswith('std::multiset<') or
											  tstr.startswith('std::map<') or
											  tstr.startswith('std::multimap<'))):
		return (std__Rb_tree,iterHusk) # ordered associative

	# Insert iterators point to *an entire container*, not to an element therein.
	if tstr.startswith('std::front_insert_iterator'):
		return (std__front_insert_iterator,iterHusk)
	if tstr.startswith('std::back_insert_iterator'):
		return (std__back_insert_iterator,iterHusk)

	if LOOKUPppCLASS_Debug: printf('iter::getPP retNone ((C))\n')
	return (None,iterHusk)
