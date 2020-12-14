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

from _usability import *
from _preferences import *

import _indent_spec

from _pp_base_classes import BasePP,PPFault, IndirectorPP, AggregatePP, AssociativePP

import _stl_utilities
from _stl_utilities import getPP, std__shared_ptr, std__weak_ptr

import _stl_containers
from _stl_containers import getPP, HashtabAssociativePP

import _stl_iterators
from _stl_iterators import getPP, unwrap_iteratorValue

import _common

from _formatting_aids import *
from _our_p import impl__type_nameOnly

import gdb
from gdb import execute
from gdb.types import *


##### Helpers: class fetchers ##############################

# If there is only 1 arg, there can be confusion which arg we
# are complaining about, so then needn't pass an aboutTag in.

def mk_aboutStr (aboutTag):
	if 0 == len(aboutTag):
		return ''
	else:
		return sprintf('%s(about %s)%s%s\n',
					   italicFONT,aboutTag,resetFONT,FONTred)

def mk__aggreg_ppObj (v, aboutTag=''):
	aboutStr=mk_aboutStr(aboutTag)
	ppClass = _stl_containers.getPP(v.type)
	if not ppClass:
		ppClass = _stl_utilities.getPP(v.type)
	if ppClass and not issubclass(ppClass, AggregatePP):
		tStr = impl__type_nameOnly(v.type)
		_common.die('%sType =[=%s=]= is not an aggregate.' % (aboutStr,tStr))
	if not ppClass:
		tStr = impl__type_nameOnly(v.type)
		_common.die('%sType =[=%s=]= is not an applicable type.' % (aboutStr,tStr))
	return ppClass(v)

def mk__indirector_ppObj (v, aboutTag=''):
	aboutStr=mk_aboutStr(aboutTag)
	ppClass = _stl_iterators.getPP(v.type)
	if not ppClass:
		ppClass = _stl_utilities.getPP(v.type)
	if ppClass and not issubclass(ppClass, IndirectorPP):
		tStr = impl__type_nameOnly(v.type)
		_common.die('%sType =[=%s=]= is neither iterator nor smart pointer.'
					% (aboutStr,tStr))
	if not ppClass:
		tStr = impl__type_nameOnly(v.type)
		_common.die('%sType =[=%s=]= is not an applicable type.'
					% (aboutStr,tStr))
	return ppClass(v)

def mk__anyRecognized_ppObj (v):
	import _pp_base_classes
	from _common import gdbType_to_ppClass
	# We shall unwrap the iterator (if iterator) ourselves later;
	# because we need to unwrap *value*, and gdbType_to_ppClass()
	# calls _stl_iterators.getPP() which calls unwrap_iteratorType().
	(ppClass,dummy) = _common.gdbType_to_ppClass(v.type, True)
	if not ppClass:
		tStr = impl__type_nameOnly(v.type)
		_common.die('Type =[=%s=]= is not a supported STL type.'
					% (tStr))
	if issubclass(ppClass,_pp_base_classes.IteratorPP):
		iterHusk = unwrap_iteratorValue(v)
		if iterHusk.coreType != None:
			(ppClass_other,dummy) = _stl_iterators.getPP(iterHusk.coreType,
														 False)
			ppObj = ppClass_other(iterHusk.coreValue)
			if iterHusk.any_moveWrappers:
				ppObj.noteMisc('std::move_iterator adapter wrapped.')
			if iterHusk.any_reverseWrappers:
				ppObj.noteMisc('std::reverse_iterator adapter wrapped.')
			return ppObj
	#
	ppObj = ppClass(v)
	return ppObj

def mk__iter_ppObj (v, aboutTag=''):
	aboutStr=mk_aboutStr(aboutTag)
	iterHusk = _stl_iterators.unwrap_iteratorValue(v)
	v_using = nonNull(iterHusk.coreValue, v)
	(ppClass,dummy) = _stl_iterators.getPP(v_using.type,try__unwrapType=False)
	if not ppClass:
		tStr = impl__type_nameOnly(v.type)
		_common.die('%sType =[=%s=]= is not an iterator.'
					% (aboutStr,tStr))
	return ppClass(v_using)


##### Helpers for gdb.Command subclasses  ###############################

def assertArity (argv, expected_argn):
	actual_argn = len(argv)
	if actual_argn != expected_argn:
		_common.die(sprintf('Given %u argument%s, but command expects %u.',
							actual_argn, ternary(1==actual_argn,'','s'), expected_argn))

def overtlyIgnoreArgs (argsAsOneString):
	if len(argsAsOneString):
		printf('%sIgnoring arguments (command expects none).%s\n', FONTred,resetFONT)

def prep__single_gdbValue (argsAsOneString):
	argv = gdb.string_to_argv(argsAsOneString)
	assertArity(argv, 1)
	return gdb.parse_and_eval(argv[-1])

def prep__single_nonValue_string (argsAsOneString):
	from _common import stripEnclosing_quoteMarks
	argv = gdb.string_to_argv(argsAsOneString)
	assertArity(argv, 1)
	return stripEnclosing_quoteMarks(argv[-1])

def prep__aggregObj_and_lookupBy (argsAsOneString, lookupBy_key_only=False):
	from _common import stripEnclosing_quoteMarks
	argv = gdb.string_to_argv(argsAsOneString)
	assertArity(argv, 2)
	lookupBy = stripEnclosing_quoteMarks(argv[-1])
	aggreg_v = gdb.parse_and_eval(argv[-2])
	aggreg_ppObj = mk__aggreg_ppObj(aggreg_v, 'first arg')
	if lookupBy_key_only and not isinstance(aggreg_ppObj, AssociativePP):
		_common.die('%sType =[=%s=]= does not support key lookup.'
					 % (mk_aboutStr('first arg'), impl__type_nameOnly(aggreg_v.type)))
	return (aggreg_ppObj,lookupBy)

def complete__aggregObj_and_lookupBy (argsAsOneString):
	argv = gdb.string_to_argv(argsAsOneString)
	if 0 == len(argv):   return gdb.COMPLETE_SYMBOL
	elif 1 == len(argv): return gdb.COMPLETE_EXPRESSION
	else:                return None


##### Launcher logic proper: q-* commands  ##############################

class Q_IterInto (gdb.Command):
	"""q-iter-into   <aggregate_obj>   <iterator_obj>\n
Reports whether iterator_obj is valid with respect to aggregate_obj.
Prints one of: withinBounds_and_valid, withinBounds_but_invalid, outOfBounds."""
	def __init__ (self):
		super(Q_IterInto,self).__init__("q-iter-into", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		argv = gdb.string_to_argv(argsAsOneString)
		if len(argv) < 2: return gdb.COMPLETE_SYMBOL
		else:             return None
	def invoke (self, argsAsOneString, isFromTTY):
		argv = gdb.string_to_argv(argsAsOneString)
		assertArity(argv, 2)
		#
		aggreg_v = gdb.parse_and_eval(argv[-2])
		aggreg_ppObj = mk__aggreg_ppObj(aggreg_v, 'first arg')
		#
		iter_v = gdb.parse_and_eval(argv[-1])
		iter_ppObj = mk__iter_ppObj(iter_v, 'second arg')
		#
		aggreg_ppObj.relateIter(iter_ppObj)


class Q_More (gdb.Command):
	"""q-more  <any_supported_STL_obj>\n
Prints information about given object, more than what simple GDB commands can."""
	def __init__ (self):
		super(Q_More, self).__init__("q-more", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		some_v = prep__single_gdbValue(argsAsOneString)
		some_ppObj = mk__anyRecognized_ppObj(some_v)
		some_ppObj.moreInfo()


class Q_Buckets (gdb.Command):
	"""q-buckets  <std::unordered_.... aggregate_obj>\n
Prints elements' keys grouped by bucket; shows every key's hashcode."""
	def __init__ (self):
		super(Q_Buckets, self).__init__("q-buckets", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		aggreg_v = prep__single_gdbValue(argsAsOneString)
		aggreg_ppObj = mk__aggreg_ppObj(aggreg_v)
		if isinstance(aggreg_ppObj, HashtabAssociativePP):
			aggreg_ppObj.printBucketwise()
		else:
			_common.die('Neither std::unordered_map nor std::unordered_set; inapplicable.')


class Q_CountElems (gdb.Command):
	"""q-count-elems  <aggregate_obj>\n
Returns count of valid elements in the aggregate_obj container."""
	def __init__ (self):
		super(Q_CountElems, self).__init__("q-count-elems", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL #If all args desired are objects, why not.
	def invoke (self, argsAsOneString, isFromTTY):
		aggreg_v = prep__single_gdbValue(argsAsOneString)
		aggreg_ppObj = mk__aggreg_ppObj(aggreg_v)
		gdb.execute(sprintf('p/u %u', aggreg_ppObj.countElements()))


class Q_HasElem (gdb.Command):
	"""q-has-elem  <aggregate_obj>  <lookup_idx|lookup_key>\n
Looks up element in the aggregate_obj container, and returns whether found such an element (i.e. true or false).\n
Expects a uint lookup_idx for sequence-type containers, else a string lookup_key."""
	def __init__ (self):
		super(Q_HasElem, self).__init__("q-has-elem", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return complete__aggregObj_and_lookupBy(argsAsOneString)
	def invoke (self, argsAsOneString, isFromTTY):
		(aggreg_ppObj,lookupBy) = prep__aggregObj_and_lookupBy(argsAsOneString)
		aggreg_ppObj.ensure_printablesPopulated()
		if aggreg_ppObj.hasElement(lookupBy): gdb.execute('p true')
		else:                                 gdb.execute('p false')


class Q_Elem (gdb.Command):
	"""q-elem  <aggregate_obj>  <lookup_idx|lookup_key>\n
Looks up element in the aggregate_obj container, and pretty-prints such an element if found.\n
Expects a uint lookup_idx for sequence-type containers, else a string lookup_key."""
	def __init__ (self):
		super(Q_Elem, self).__init__("q-elem", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return complete__aggregObj_and_lookupBy(argsAsOneString)
	def invoke (self, argsAsOneString, isFromTTY):
		import numbers
		(aggreg_ppObj,lookupBy) = prep__aggregObj_and_lookupBy(argsAsOneString)
		aggreg_ppObj.ensure_printablesPopulated()
		v = aggreg_ppObj.getElement(lookupBy)[1]
		if   isinstance(v, numbers.Integral):  gdb.execute(sprintf('p/d %d', int(v)))
		elif isinstance(v, numbers.Real):      gdb.execute(sprintf('p/f %f', float(v)))
		elif isinstance(v, str):               gdb.execute(sprintf('p/s %s', v))
		elif not isinstance(v, gdb.Value):     gdb.execute(sprintf('p %s', str(v)))
		else:
			t = v.type
			if _common.isStringform(t):
				s = _common.extractString_from_gdbValue(v)
				gdb.execute(sprintf('p/s "%s"', s))
			elif t and v.address:
				gdb.execute(sprintf('p *(%s *)0x%x', str(t), v.address))
			elif _common.isPointer(t):         gdb.execute(sprintf('p/a %u', int(v)))
			elif t.code == gdb.TYPE_CODE_INT:  gdb.execute(sprintf('p/d %d', int(v)))
			elif t.code == gdb.TYPE_CODE_FLT:  gdb.execute(sprintf('p/f %f', float(v)))
			else:                              gdb.execute(sprintf('p %s', str(v)))


class Q_ElemAddr (gdb.Command):
	"""q-elem-addr  <aggregate_obj>  <lookup_idx|lookup_key>\n
Looks up element in the aggregate_obj container, and returns address of such an element if found.  If container stores key-value pairs, returns address of the *value*.\n
Expects a uint lookup_idx for sequence-type containers, else a string lookup_key."""
	def __init__ (self):
		super(Q_ElemAddr, self).__init__("q-elem-addr", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return complete__aggregObj_and_lookupBy(argsAsOneString)
	def invoke (self, argsAsOneString, isFromTTY):
		(aggreg_ppObj,lookupBy) = prep__aggregObj_and_lookupBy(argsAsOneString)
		aggreg_ppObj.ensure_printablesPopulated()
		gdb.execute(sprintf('p/a %u', aggreg_ppObj.getElementAddress(lookupBy)))


class Q_ElemKeyAddr (gdb.Command):
	"""q-elem-key-addr  <aggregate_obj>  <lookup_key>\n
Looks up element in the aggregate_obj container, and returns address of its key if found.\n
Expects a string lookup_key."""
	def __init__ (self):
		super(Q_ElemKeyAddr, self).__init__("q-elem-key-addr", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return complete__aggregObj_and_lookupBy(argsAsOneString)
	def invoke (self, argsAsOneString, isFromTTY):
		(aggreg_ppObj,lookupBy) = prep__aggregObj_and_lookupBy(argsAsOneString,
															   lookupBy_key_only=True)
		aggreg_ppObj.ensure_printablesPopulated()
		gdb.execute(sprintf('p/a %u', aggreg_ppObj.getElementKeyAddress(lookupBy)))


class Q_TargetAddr (gdb.Command):
	"""q-target-addr  <indirector_obj>\n
Returns address of whatever the given indirector points to or wraps."""
	def __init__ (self):
		super(Q_TargetAddr, self).__init__("q-target-addr", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		indirector_v = prep__single_gdbValue(argsAsOneString)
		indirector_ppObj = mk__indirector_ppObj(indirector_v)
		gdb.execute(sprintf('p (%s *) 0x%x',
							str(indirector_ppObj.targetType),
							indirector_ppObj.getTargetAddress()))


# Subset of p-over's functionality: only prints simplified type name.
class Q_Whatis (gdb.Command):
	"""q-whatis  <someObj>\n
Prints type of given obj, concisely."""
	def __init__ (self):
		super(Q_Whatis, self).__init__("q-whatis", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		someObj_v = prep__single_gdbValue(argsAsOneString)
		tNamePrecis = impl__type_nameOnly(someObj_v.type)
		printf__toStdout('type = %s\n', tNamePrecis) # Just like GDB's own "whatis".


class Q_Precis (gdb.Command):
	"""q-precis  <fully_expanded_typeName>\n
Prints a corresponding abbreviated type name, if GDB recognizes the type."""
	def __init__ (self):
		super(Q_Precis, self).__init__("q-precis", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return None
	def invoke (self, argsAsOneString, isFromTTY):
		s = prep__single_nonValue_string(argsAsOneString)
		try:
			t = gdb.lookup_type(s)
			tNamePrecis = impl__type_nameOnly(t)
			printf__toStdout('%s\n', tNamePrecis)
		except BaseException as e:
			_common.die('Cannot discern a type from input.')



##### Launcher logic proper: x-* commands  ##############################

from _preferences import *

class X_Remind (gdb.Command):
	"""x-remind\n
Shows at once all of V2_GDB_Pretty_Cxx's custom GDB parameters.\nFor each, lists the possible values; of those,
\to\t the *default* value is shown bracketed
\to\t the *current* value is shown with yellow background"""
	def __init__ (self):
		super(X_Remind, self).__init__("x-remind", gdb.COMMAND_STATUS)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_NONE
	def invoke (self, argsAsOneString, isFromTTY):
		# Remind how to interpret x-remind's output.
		printf('%s %s%sLEGEND:%s    %s[%sdefaults to%s]%s   %sis currently%s\n',
			   ''.ljust(42), italicFONT,FONTyellowRUDE,resetFONT,
			   boldFONT,resetFONT, boldFONT,resetFONT,
			   FONTyellowBackgd,resetFONT)
		overtlyIgnoreArgs(argsAsOneString)
#		dumpBoolPref('x-debug',     PREF_Debug,    default__PREF_Debug)
		dumpBoolPref('x-full-paths',PREF_FullPaths,default__PREF_FullPaths)
		dumpBoolPref('x-heur-abbr', PREF_HeurAbbr, default__PREF_HeurAbbr)
		dumpBoolPref('x-relations', PREF_Relations,  default__PREF_Relations)
		dumpBoolPref('x-underly',   PREF_Underly,  default__PREF_Underly)
		printf('\n')
		dumpEnumPref('x-base-classes', PREF_BaseClasses, default__PREF_BaseClasses)
		dumpEnumPref('x-layout',       PREF_Layout,      default__PREF_Layout)
		dumpEnumPref('x-nested-datamemb',
					 PREF_NestedDatamemb, default__PREF_NestedDatamemb)
		dumpEnumPref('x-template-args',
					 PREF_TemplateArgs,   default__PREF_TemplateArgs)
		printf('\n')
		dumpUintPref('x-print-width--member-type',
					 PREF_PrintWidth_MemberType, default__PREF_PrintWidth_MemberType)
		dumpUintPref('x-print-width--member-name',
					 PREF_PrintWidth_MemberName, default__PREF_PrintWidth_MemberName)
		printf('\n')


class X_DefaultAll (gdb.Command):
	"""x-default-all\n
Resets all V2_GDB_Pretty_Cxx's custom GDB parameters to respective defaults."""
	def __init__ (self):
		super(X_DefaultAll, self).__init__("x-default-all", gdb.COMMAND_STATUS)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_NONE
	def invoke (self, argsAsOneString, isFromTTY):
		overtlyIgnoreArgs(argsAsOneString)
		setAllPrefs_to_defaults()


##### Launcher logic proper: p-* commands  ##############################

from _our_p import parseAndEval, find_ValueSymbolFrameBlock, impl__type
from gdb import lookup_type

class P_Type (gdb.Command):
	"""p-type  <type> | <obj>\n
Prints template arguments, base classes, and (the types of) data members of given type; or if given an object, of that object's type."""
	def __init__ (self):
		super(P_Type, self).__init__("p-type", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		s = prep__single_nonValue_string(argsAsOneString)
		haveType = False
		mustBeValue = False
		for c in s:
			if not (c.isidentifier() or (c == ':')):
				mustBeValue = True
				break
		if not mustBeValue:
			try:
				t = gdb.lookup_type(s)
				haveType = True
			except BaseException as whatev:
				mustBeValue = True
		if not haveType or mustBeValue:
			v = parseAndEval(s)
			if (v==None):
				_common.die('Cannot discern a type from input.')
			t = v.type
		impl__type(t)

class P_SType (gdb.Command):
	"""p-stype  <type>\n
Prints template arguments, base classes, and (the types of) data members of given type."""
	def __init__ (self):
		super(P_SType, self).__init__("p-stype", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return None
	def invoke (self, argsAsOneString, isFromTTY):
		s = prep__single_nonValue_string(argsAsOneString)
		t = None
		try:
			t = gdb.lookup_type(s)
		except BaseException as whatev:
			_common.die('Cannot discern a type from input.')
		impl__type(t)

class P_VType (gdb.Command):
	"""p-vtype  <obj>\n
Prints template arguments, base classes, and (the types of) data members of the object's type."""
	def __init__ (self):
		super(P_VType, self).__init__("p-vtype", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		v = prep__single_gdbValue(argsAsOneString)
		impl__type(v.type)


class P_Deep (gdb.Command):
	"""p-deep  <obj>\n
Prints template arguments, base classes, and (the types of) data members of the object's type; also prints data members' values where possible."""
	def __init__ (self):
		super(P_Deep, self).__init__("p-deep", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		s = prep__single_nonValue_string(argsAsOneString)
		find_rv = find_ValueSymbolFrameBlock(s)
		v              = find_rv[0]
		symb_lookup_rv = find_rv[1]
		b              = find_rv[3]
		if (None==v):
			_common.die('Unusable input.')
		impl__type(v.type, v)

class P_Afar (gdb.Command):
	"""p-afar  <obj>\n
Prints a few items of summary information about the given object."""
	def __init__ (self):
		super(P_Afar, self).__init__("p-afar", gdb.COMMAND_DATA)
	def complete (self, argsAsOneString, lastArg):
		return gdb.COMPLETE_SYMBOL
	def invoke (self, argsAsOneString, isFromTTY):
		from _our_p import impl__afar, wrap__valueProper
		s = prep__single_nonValue_string(argsAsOneString)
		find_rv = find_ValueSymbolFrameBlock(s)
		v              = find_rv[0]
		symb_lookup_rv = find_rv[1]
		fr             = find_rv[2]
		b              = find_rv[3]
		if (v!=None) or symb_lookup_rv or b: # Just fr, on its own, is not worthwile.
			impl__afar(v, symb_lookup_rv, fr, b)
		else:
			_common.die('Unusable input.')
		if (v!=None):
			indents = _indent_spec.IndentSpec(2)
			indents.newLine_misc()
			wrap__valueProper(v, indents)
			printf('\n')
		else: # **Can** control reach here?
			_common.die('Cannot find symbol.')


################### Eh??? #######
from _codes_stringified import *
from _pp_base_classes import dump_ppObj_pythonClassDerivation
from _pp_base_classes import dump_ppObj_internalLookups

# This is closest I've figured how to get, in Python, to the idea of a readonly var.
class MAX_NEST_DUMP_DEPTH (enum.IntEnum):
	const = int(100)


def dump_ppObj_innards (v):
	some_ppObj = mk__anyRecognized_ppObj(v)
	dump_ppObj_pythonClassDerivation(some_ppObj)
	printf('\n')
	dump_ppObj_internalLookups(some_ppObj)
	printf('\n')


def decode_1arg (s):
	from _common import zdecode
	x = gdb.decode_line(s)
	zdecode(x)

def decode_0args ():
	from _common import zdecode
	x = gdb.decode_line()
	zdecode(x)


def wrap__iterdump_Type (s):
	from _common import iterdump_Type, stripEnclosing_quoteMarks
	s = stripEnclosing_quoteMarks(s)
	try:
		t = gdb.lookup_type(s)
		iterdump_Type(t, t.items())
	except BaseException as e:
		_common.die('No such type?')

def wrap__iterdump_Type_withAnonFields (s):
	from _common import iterdump_Type, stripEnclosing_quoteMarks
	s = stripEnclosing_quoteMarks(s)
	try:
		t = gdb.lookup_type(s)
		iterdump_Type(t, deep_items(t))
	except BaseException as e:
		_common.die('No such type?')


def dump_blocks_from_deepest_out ( ):
	fr = gdb.selected_frame()
	if not fr: _common.die('No frame selected.')
	from _common import dump_Block
	b = fr.block()
	stal = fr.find_sal() # Surely correct for the *first* Block.
	i_block = 0
	while b !=None:
		if i_block > 0 and not b.is_static and not b.is_global:
			stalOther = gdb.find_pc_line(b.start)
			if stalOther !=None:
				stal = stalOther
		dump_Block(b, stal)
		b = b.superblock
		if i_block >= MAX_NEST_DUMP_DEPTH.const: _common.die('Halt, max dump depth.')
		i_block += 1

def dump_all_frames ( ):
	from _common import list_all_Frame, dump_Frame
	aF = list_all_Frame()
	for i_fr in range(len(aF)):
		dump_Frame(i_fr,aF[i_fr])
		if i_fr >= MAX_NEST_DUMP_DEPTH.const: _common.die('Halt, max dump depth.')

def iterdump_Block_ofFrame_N (j_fr):
	if not is_uint(j_fr):
		_common.die('Argument is not a valid frame #.')
	from _common import list_all_Frame, iterdump_Block
	aF = list_all_Frame()
	for i_fr in range(len(aF)):
		if i_fr != j_fr:
			continue
		fr = aF[i_fr]
		b = fr.block()
		iterdump_Block(b)
		return
	_common.die('No frame with so high a number; check "backtrace past-main" and "backtrace past-entry" parameters?')

def iterdump_Block_curr ( ):
	from _common import iterdump_Block
	fr = gdb.selected_frame()
	if not fr: _common.die('No frame selected.')
	b = fr.block()
	iterdump_Block(b)

def iterdump_Block_global_ofFrame_curr ( ):
	from _common import iterdump_Block
	fr = gdb.selected_frame()
	if not fr: _common.die('No frame selected.')
	b = fr.block().global_block
	if not b: _common.die('No global block.')
	iterdump_Block(b)

def iterdump_Block_static_ofFrame_curr ( ):
	from _common import iterdump_Block
	fr = gdb.selected_frame()
	if not fr: _common.die('No frame selected.')
	b = fr.block().static_block
	if not b: _common.die('No static block.')
	iterdump_Block(b)


def iterdump_Objfile (objfileName):
	x = None
	try:
		x = gdb.lookup_objfile(objfileName)
	except ValueError as err:
		pass
	if not x:
		_common.die('None such.')
	printf('Objfile {\n')
	for k,v in x.__dict__:
		printf('\t%s --> %s\n', str(k), str(v))
	printf('}\n')
	y = x.progspace
	if not y:
		_common.die('No progspace associated.')
	printf('\nProgspace {\n')
	for k,v in y.__dict__:
		printf('\t%s --> %s\n', str(k), str(v))
	printf('}\n')


def wrap__iterdump_SymtabLinetab_curr ( ):
	from _common import prAddr, iterdump_LineTable
	fr = gdb.selected_frame()
	printf('Frame name="%s" pc=%s type=%s\n',
		   fr.name(), prAddr(fr.pc()), frame_typeToStr[fr.type()])
	stal = fr.find_sal()
	if not stal or not stal.is_valid():
		_common.die('Bad stal')
	printf('Symtab_and_line line=%d pc=%s last=%s\n',
		   stal.line, prAddr(stal.pc), prAddr(stal.last))
	stab = stal.symtab
	if not stab or not stab.is_valid():
		_common.die('Bad stab')
	printf('Symtab filename="%s" fullname="%s"\n',
		   stab.filename, stab.fullname())
	objf = stab.objfile
	if objf:
		printf('Objfile filename="%s"\n', objf.filename)
	ltab = stab.linetable()
	if not ltab or not ltab.is_valid():
		_common.die('Bad ltab')
	b = fr.block()
	iterdump_LineTable(ltab, b.start, b.end)#stal.pc, stal.last)
