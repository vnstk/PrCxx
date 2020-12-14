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

ELAB_Debug=False#True
FIELD_Debug=False
LOOKUPppCLASS_Debug=False
SUBST_Debug=False
noopSUBST_Debug=False #Trace even when subst !happened?
UNRAVEL_Debug=False
TYPEnameCHOICE_Debug=False

BOTHERwithCOMPONENTS=False # Helped with understanding STL types *themselves*.


from _usability import *
from _preferences import *
from _formatting_aids import *
from _codes_stringified import *

from gdb import *
from gdb.printing import *
from gdb.types import *

import platform
class WORD_WIDTH (enum.IntEnum):
	const = int(platform.architecture()[0][:2]) / 8


def die (fmtSpec, *varargs):
	if PREF_Debug:
		dumpCallstack(omitInnermost=True)
	fmtSpec = fmtSpec.replace('=[=', resetFONT + FONTyellowBackgd)
	fmtSpec = fmtSpec.replace('=]=', resetFONT + FONTred)
	s = sprintf(FONTred + fmtSpec + resetFONT, *varargs)
	raise gdb.GdbError(s)


seq__callFrameId=0 # Reloading _common.py resets this to 0.
#
# To help match up trace messages from funcs, esp. recursive
#
def next_callFrameId ( ):
	global seq__callFrameId
	seq__callFrameId += 1
	n = seq__callFrameId
	# Leading "z", to cut false positives when searching
	return sprintf('%sz%02X%s', FONTwhiteRUDE,n % 256,resetFONT)


def mkBoldStripe (c):
	return sprintf('%s%s%s',
				   boldFONT, ''.rjust(consoleWidth(),c) ,resetFONT)

def mkRudeStripe_red (c='*'):
	return sprintf('%s%s%s',
				   FONTredRUDE, ''.rjust(80,'*'), resetFONT)


def sAbbr (maxlen, s):
	if len(s) <= maxlen:
		return s
	return s[:maxlen] + '...'


def prAddr (addr):
	return sprintf('0x%0*x', int(WORD_WIDTH.const * 2), int(addr))


def prettyPath (s):
	import os.path
	return ternary(PREF_FullPaths, s, os.path.basename(s))


def string_to_groupOfSubstrings (s, maxSubstringLen, sep=' '):
	assert_uint(maxSubstringLen)
	assert maxSubstringLen > 0
	result = ''
	totn = len(s)
	i = int(0)
	while i < totn:
		sub = (s[i:])[:maxSubstringLen]
		subn = len(sub)
		if i > 0:
			result += sep
		result += sub
		i += subn
	return result


def sprintfBrightDelimitedTag (s, delimChar):
	return sprintf('%s%c%s%s%s%s%s%c%s',
				   FONTgreen,delimChar,resetFONT,
				   boldFONT,s,resetFONT,
				   FONTgreen,delimChar,resetFONT)


# For when mutation is predicated on successful search-and-replace.
#
def traceSubst (stepTag,   sWas, replacedWhat,replacedWith ,sNow,
				traceSuccess, traceFailureToo=noopSUBST_Debug):
	if not traceSuccess: return
	dumpMax=400
	if sNow != sWas:
		printf('\n  %s%s%s\n\t+Now+  %s%s%s%s\n' +
			   '\t-Was-  %s%s%s%s\n\t  Op   s/%s%s%s/%s%s%s/g\n',
			   FONTgreenBackgd,stepTag,resetFONT,
			   boldFONT,FONTred,    sNow[:dumpMax],resetFONT,
			   boldFONT,FONTmagenta,sWas[:dumpMax],resetFONT,
			   FONTmagenta,replacedWhat,resetFONT,
			   FONTred,    replacedWith,resetFONT)
	elif traceFailureToo:
		printf('\n  %s%s%s\n\t=Same= %s%s%s%s\n\t  Op   s/%s%s%s/%s%s%s/g\n',
			   FONTgreenBackgd,stepTag,resetFONT,
			   boldFONT,FONTblue,sWas[:dumpMax],resetFONT,
			   FONTmagenta,replacedWhat,resetFONT,
			   FONTred,    replacedWith,resetFONT)

# For when mutation is predicated not on successful search-and-replace, but
# on some other cond; and input is always replaced wholly.
#
def traceExchg (stepTag,  sWas, cond ,exchangeTo,
				traceSuccess, eqLHS=None,eqRHS=None,
				traceFailureToo=noopSUBST_Debug):
	if not traceSuccess: return
	dumpMax=400
	if eqLHS!=None and eqRHS!=None:
		eqDetail = sprintf('\t%sCparing%s  %s%s%s\n\t    %sand%s  %s%s%s\n',
						   italicFONT,resetFONT,boldFONT,eqLHS[:dumpMax],resetFONT,
						   italicFONT,resetFONT,boldFONT,eqRHS[:dumpMax],resetFONT)
	else:
		eqDetail=''
	if cond:
		printf('\n  %s%s%s\n\t+Now+  %s%s%s%s\n\t-Was-  %s%s%s%s\n%s',
			   FONTgreenBackgd,stepTag,resetFONT,
			   boldFONT,FONTred,    exchangeTo[:dumpMax],resetFONT,
			   boldFONT,FONTmagenta,sWas[:dumpMax],resetFONT, eqDetail)
	elif traceFailureToo:
		printf('\n  %s%s%s\n\t=Same= %s%s%s%s\n%s',
			   FONTgreenBackgd,stepTag,resetFONT,
			   boldFONT,FONTblue,sWas[:dumpMax],resetFONT, eqDetail)


def splitTypename_atRmostNameQualifier (s):
	iRmostDoublecolon = s.rfind('::')
	if iRmostDoublecolon >= 0:
		return (s[:iRmostDoublecolon] , s[iRmostDoublecolon:])
	else:
		return None


def strip__cxx11 (s):
	return s.replace('std::__cxx11::', 'std::')


def strip__spaces (s): # Take care lest end up with "constchar" or such!
	return s.replace(' ', '')


def cmpPrep (s):
	return s.replace(' >', '>')


def fixBroketSpacing (s):
	return s.replace('>>', '> >') # how GCC does it (required before C++11)


def replace_atTokenBoundaries (sWhat, sWith, sIn):
	import re
	sWhat__escaped = sWhat
	sWhat__escaped = sWhat__escaped.replace('*', '\*')
	sWhat__escaped = sWhat__escaped.replace('.', '\.')
	sWhat__escaped = sWhat__escaped.replace('[', '\[')
	# Need escape ']' only *inside* of a charset.
	sWhat__escaped = sWhat__escaped.replace('(', '\(')
	sWhat__escaped = sWhat__escaped.replace(')', '\)')
	if PREF_Debug and (sWhat__escaped != sWhat):
		printf('Escaped %s%s%s ==> %s%s%s\n',
			   FONTgreen, sWhat,          resetFONT,
			   FONTblue,  sWhat__escaped, resetFONT)
	split_pattern = sWhat__escaped
	if (len(sWhat__escaped) < 2) or (sWhat__escaped[0:1] != '\\'):
		split_pattern = '\\b' + split_pattern
	if (len(sWhat__escaped) < 2) or (sWhat__escaped[-2:-1] != '\\'):
		split_pattern = split_pattern + '\\b'
	# https://docs.python.org/3/library/re.html#re.split
	split_tokens = re.split(split_pattern, sIn)
	result = sWith.join(split_tokens)
	return result


def stripEnclosing_quoteMarks (s):
	if not isinstance(s, str):
		return s
	if len(s) >= 2 and '"' == s[0] and '"' == s[-1]:
		return s[1:-1]
	else:
		return s


def normalizeTypename (s):
	import re
	z = s
	#
	# Convert constants like 42U to just "42"
	pat = r'\b(\d+)u\b'
	replaceWith = r'\1'
	z = re.sub(pat, replaceWith, z)
	#
	# Convert "const Flarp *" to "Flarp const *"
	pat = r'^const ([^\*]+) \*$'
	replaceWith = r'\1 const *'
	z = re.sub(pat, replaceWith, z)
	#
	# Same, but inside parens.
	pat = r'\(const ([^\*]+) \*\)'
	replaceWith = r'(\1 const *)'
	z = re.sub(pat, replaceWith, z)
	#
	#
	# Convert "const Flarp &" to "Flarp const &"
	pat = r'^const ([^\*]+) &$'
	replaceWith = r'\1 const &'
	z = re.sub(pat, replaceWith, z)
	#
	# Same, but inside parens.
	pat = r'\(const ([^\*]+) \&\)'
	replaceWith = r'(\1 const &)'
	z = re.sub(pat, replaceWith, z)
	#
	#
	# Strip space directly preceding "*"
	z = z.replace(' *', '*')
	#
	# Strip space directly preceding "&"
	z = z.replace(' &', '&')
	#
	if PREF_Debug and z != s:
		printf('Normalized %s%s%s into %s%s%s\n',
			   FONTred,s,resetFONT,FONTred,z,resetFONT)
	return z


@enum.unique
class eIteratorStanding (Enum):
	withinBounds_and_valid = 1,
	withinBounds_but_invalid = 2,
	outOfBounds = 3


class IteratorHusk:
	def __init__ (self):
		self.any_moveWrappers = False
		self.any_reverseWrappers = False
		self.coreType = None
		self.coreValue = None
	def __str__ (self):
		s = sprintf('{{ movWr:%c revWr:%c coreType=\n\t\t',
					bool_to_char(self.any_moveWrappers),
					bool_to_char(self.any_reverseWrappers))
		if None==self.coreType:
			s += 'None'
		else:
			s += sprintf('%s  %s%s%s',
						 type_codeToStr[self.coreType.code],boldFONT,
						 str(self.coreType), resetFONT)
		s += '\n}}'
		return s


def isVirtualBase (f):
	assert isinstance(f, gdb.Field)
	return f.is_base_class and int(f.bitpos) < 0



def isUnexpected (cxxType):
	return cxxType.code in (TYPE_CODE_FLAGS,
							TYPE_CODE_SET,
							TYPE_CODE_RANGE,
							TYPE_CODE_ERROR,
							TYPE_CODE_COMPLEX,
							TYPE_CODE_NAMESPACE,
							TYPE_CODE_DECFLOAT)
#,
#							TYPE_CODE_MODULE)

def isCallable (cxxType):
	return cxxType.code in (TYPE_CODE_FUNC, TYPE_CODE_METHOD,
							TYPE_CODE_INTERNAL_FUNCTION)

def isPointer (cxxType):
	return cxxType.code in (TYPE_CODE_METHODPTR, TYPE_CODE_MEMBERPTR, TYPE_CODE_PTR)

def performsIndirection (cxxType):
	return cxxType.code in (TYPE_CODE_METHODPTR, TYPE_CODE_MEMBERPTR, TYPE_CODE_PTR,
							TYPE_CODE_REF, TYPE_CODE_RVALUE_REF)

def isPlain (cxxType):
	return not cxxType.code in (TYPE_CODE_PTR,
								TYPE_CODE_REF,
								TYPE_CODE_RVALUE_REF,
								TYPE_CODE_ARRAY)

def isFundamental (cxxType):
	return cxxType.code in (TYPE_CODE_INT,
							TYPE_CODE_FLT, TYPE_CODE_VOID, TYPE_CODE_CHAR,
							TYPE_CODE_BOOL)

def isScalar (cxxType):
	return cxxType.code in (TYPE_CODE_PTR, TYPE_CODE_ENUM, TYPE_CODE_INT,
							TYPE_CODE_FLT, TYPE_CODE_CHAR, TYPE_CODE_BOOL,
							TYPE_CODE_METHODPTR, TYPE_CODE_MEMBERPTR,
							TYPE_CODE_PTR, TYPE_CODE_REF, TYPE_CODE_RVALUE_REF)

def isTypeNativelyPrintable (cxxType):
	return cxxType.code in (TYPE_CODE_ARRAY, TYPE_CODE_INT, TYPE_CODE_FLT,
							TYPE_CODE_BOOL,	TYPE_CODE_RANGE, TYPE_CODE_PTR,
							TYPE_CODE_VOID, TYPE_CODE_CHAR)

def couldHaveFields (cxxType):
	return cxxType.code in (TYPE_CODE_STRUCT, TYPE_CODE_UNION,
							TYPE_CODE_FUNC, TYPE_CODE_METHOD)


class InterstitialReckoner:
	"""
		total_entry_sizeof : uint
		prev_beginAddr     : uint
	"""
	def __init__ (self, total_entry_sizeof):
		assert_uint(total_entry_sizeof)
		self.total_entry_sizeof = total_entry_sizeof
		self.prev_beginAddr = None
	def elemIncrem (self, cur_beginAddr):
		assert_uint(cur_beginAddr)
		ret = 0
		cur_endAddr = cur_beginAddr + self.total_entry_sizeof
		if self.prev_beginAddr:
			prev_endAddr = self.prev_beginAddr + self.total_entry_sizeof
			ret = max( (cur_beginAddr - prev_endAddr),
					   (self.prev_beginAddr - cur_endAddr))
		self.prev_beginAddr = cur_beginAddr
		return ret


def stringify_aList (aList): # Convert list of <obj> to list of str(<obj>).
	result = []
	for x in aList:
		result.append(str(x))
	return result

def toOnelineStr_aList (aList, intraElem_fontEffect = FONTred):
	stringifElems = []
	for x in aList:
		stringifElems.append(sprintf('%s(%s%s%s%s%s)%s', boldFONT,resetFONT,
									 intraElem_fontEffect, str(x), resetFONT,
									 boldFONT,resetFONT))
	return sprintf('%s%u%s-elem:%s{%s %s %s}%s',
				   italicFONT, len(aList), resetFONT, italicFONT,resetFONT,
				   ' ~ '.join(stringifElems), italicFONT,resetFONT)

def dump_aList (aList, varNam):
	if 0 == len(aList):
		printf('Dumping empty list "%s" = %s{ }%s\n',varNam, boldFONT, resetFONT)
		return
	printf('\nDumping %u-long list "%s" = %s{%s\n',
		   len(aList), varNam, boldFONT, resetFONT)
	for x in aList:
		printf('    %s\n', str(x))
	printf('%s}%s\n', boldFONT, resetFONT)


def dump_templateArgs (actual_teArgs):
	printf('\nDumping %u-long actual_teArgs = %s{%s\n',
		   len(actual_teArgs), boldFONT, resetFONT)
	for x in actual_teArgs:
		printf('    %6s === %s\n', x.__class__.__name__, str(x))
	printf('%s}%s\n', boldFONT, resetFONT)

def list_templateArgs (cxxType):
	result = []
	i = int(0)
	while True:
		try:
			result.append(cxxType.template_argument(i))
			i += int(1)
		except BaseException as e:
#			se = str(e)
#			if se != sprintf('No argument %d in template.',i):
#				if PREF_Debug: printf('%sUnusual exception%s "%s" when i=%d t="%s"\n',
#									  FONTredRUDE,resetFONT, se, i, str(cxxType))
			break
	return result


#def castTo_ptrToVoid (ptr):
#	printf('Using *first* one\n')
#	assert isinstance(ptr, gdb.Value)
#	assert ptr.type.strip_typedefs().code == TYPE_CODE_PTR
#	ptrToVoid_type = gdb.lookup_type('void*')
#	cast_ptr = ptr.reinterpret_cast(ptrToVoid_type)
#	return cast_ptr

@returns(gdb.Value)
def castTo_ptrToType (val, valueType_new):
	assert isinstance(val, gdb.Value)
	assert isinstance(valueType_new, gdb.Type)
	ptrType = valueType_new.pointer()
	return val.cast(ptrType)


@returns(gdb.Value)
def castTo_ptrToVoid (val):
#	printf('Using *second* one\n')
	assert isinstance(val, gdb.Value)
	void_type = gdb.lookup_type('void')
	return castTo_ptrToType(val, void_type)


def getValueAtAddress (address, valueType): # Rets a gdb.Value, or None.
	assert isinstance(valueType, gdb.Type)
	ptrType = valueType.pointer()
	#
	assert address != None
	if isinstance(address, gdb.Value):
		assert performsIndirection(address.type.strip_typedefs())
		try:
			ptr = castTo_ptrToType(address, valueType)
		except BaseException as whatev:
			printf('Cannot static_cast %s%s%s addr %s, to %s%s%s\n',
			   FONTred, str(arg__address.type), resetFONT,
			   prAddr(address), FONTmagenta, str(ptrType), resetFONT)
			raise
	else:
		assert_uint(address)
		try:
			ptr = gdb.Value(address).reinterpret_cast(ptrType)
		except BaseException as whatev:
			printf('Cannot reinterpret_cast given-as-int addr %s, to %s%s%s\n',
				   prAddr(address), FONTmagenta, str(ptrType), resetFONT)
			raise
	#
	try:
		return ptr.dereference()
	except BaseException as whatev:
		printf('Cannot deref bad address %s%s%s\n',
			   FONTred, prAddr(address), resetFONT)
		return None


def getTypesOfBaseClasses (cxxType):
	assert (isinstance(cxxType, gdb.Type))
	result = []
	for f in get_basic_type(cxxType).fields():
		if f.is_base_class:
			result.append(get_basic_type(f.type))
	return result

def list_parentClasses (cxxType): # I.e. only *direct* base classes.
	assert isinstance(cxxType, gdb.Type)
	assert TYPE_CODE_STRUCT == cxxType.strip_typedefs().code
	result = []
	for f in cxxType.fields():
		if f.is_base_class:
			result.append(f.type)
	return result

def get_one_parentClass (val): # I.e. only *direct* base class.
	cxxType = get_basic_type(val.type)
	if isTypeNativelyPrintable(cxxType):
		return None
	if not couldHaveFields(cxxType):
		return None
	all_parentClasses = list_parentClasses(cxxType)
	if 1 == len(all_parentClasses):
		return all_parentClasses[0]
	return None


def list_sourceDirectories ( ):
	import os.path
	asOneStr = gdb.parameter('directories')
	# Are these Windows paths? Look for evidence of substrings like
	#   [a] C:/msys32/home/bjarne/myProj
	#   [b] ....;$cdir;......
	#   [c] ....;$cwd;......
	if (':/' in asOneStr) or (';$c' in asOneStr):
		asList = asOneStr.split(';')
	else:
		asList = asOneStr.split(':')
	result = []
	for s in asList:
		if s != '$cdir' and s != '$cwd' and os.path.isabs(s):
			result.append(os.path.normpath(s))
	return result

sourceDirectories = list_sourceDirectories()
#
def isUnder_sourceDirectories (xitem):
	import os.path
	s = xitem.symtab.fullname()
	for sD in sourceDirectories:
		prefix = os.path.commonprefix([sD,s])
		#printf('commonprefix( %s , %s ) ==> %s\n', s, sD, prefix)
		if prefix == sD:
			return True
	#printf('Skipping [%s]\n', s)
	return False

def cmp_gdbSymbols (x, y):
	if x.symtab.filename == y.symtab.filename:
		return ternary(x.line < y.line, -1, 1)
	return ternary(x.symtab.filename < y.symtab.filename, -1, 1)


def zdecode (x):
	unparsedPortion = x[0]
	if None==unparsedPortion:
		printf('Fully parsed.\n')
	else:
		printf('Parsed up until /// %s ///\n', unparsedPortion)
	stalList = x[1]
	if None==stalList:
		printf('No matching locations.\n')
	else:
		for i in range(len(stalList)):
			stal = stalList[i]
			printf('\t[i=%u] valid=%c pc=%s line=%u\n',
				   i, bool_to_char(stal.is_valid()), prAddr(stal.pc), stal.line)
			stab = stal.symtab



def dump_Block (x, stal=None):
	import os.path
	manyUnderscores = ''.ljust(80,'_')
	printf('%s\n\tBlock[%s,%s] valid:%c static:%c global:%c\n', manyUnderscores,
		   prAddr(x.start), prAddr(x.end), bool_to_char(x.is_valid()),
		   bool_to_char(x.is_static), bool_to_char(x.is_global))
	if stal !=None and stal.symtab !=None:
		stab = stal.symtab
		locTag = 'srcLocation='
		if PREF_FullPaths and (stab.fullname() !=None):
			locTag += sprintf('%s%s%s', FONTblue,stab.fullname(),resetFONT)
		else:
			locTag += sprintf('%s%s%s', FONTblue,stab.filename,resetFONT)
		ltab = stab.linetable()
		if ltab !=None:
			startLineno=-1
			endLineno=-1
			startLine_pcGap=999999999999
			endLine_pcGap=999999999999
			for xitem in ltab:
				gap=abs(xitem.pc - x.start)
				if gap < startLine_pcGap:
					startLine_pcGap = gap
					startLineno = xitem.line
				gap=abs(xitem.pc - x.end)
				if gap < endLine_pcGap:
					endLine_pcGap = gap
					endLineno = xitem.line
			if endLineno < startLineno: # Happens sometimes; why??
				tmpLineno = startLineno
				startLineno = endLineno
				endLineno = tmpLineno
			if startLineno != -1:
				locTag += sprintf(':%s%d%s,%s%d%s',
								  boldFONT,startLineno,resetFONT,
								  boldFONT,endLineno,resetFONT)
		printf('\t\t%s\n', locTag)
		#
#		objf = stab.objfile
#		if objf !=None and objf.filename !=None:
#			if PREF_FullPaths:
#				printf('\t\tobjFile=%s\n', objf.filename)
#			else:
#				printf('\t\tobjFile=%s\n', os.path.basename(objf.filename))
	if x.function !=None and hasattr(x.function,'name'):
		printf('\t\tfunc="%s%s%s"\n', FONTmagenta,x.function.name,resetFONT)


class PrBlockElem:
	def __init__ (self):
		self.objfTag = None
		self.locTag = ''
		self.smallTags = ''
		self.typeCateg = ''
		self.addrCateg = ''
		self.astr = ''
		self.printName = ''
		self.vstr = ''

def iterdump_Block (x):
	import functools
	import os.path
	from _our_p import addrcStorageCategory
	assert(isinstance(x, gdb.Block))
	fr = gdb.selected_frame()
	#
	ltab = None
	stal = fr.find_sal()
	if stal and stal.is_valid():
		stab = stal.symtab
		if stab and stab.is_valid():
			ltab = stab.linetable()
			if ltab and not ltab.is_valid():
				ltab = None # Clear it, if it is useless.
			else:
				#printf('Have ltab.\n')
				pass
	#
	printf('Block[%s,%s] static:%c global:%c\n',
		   prAddr(x.start), prAddr(x.end), bool_to_char(x.is_static), bool_to_char(x.is_global))
	if x.function !=None and hasattr(x.function,'name'):
		printf('\t\tfunc="%s%s%s"\n', FONTmagenta,x.function.name,resetFONT)
	#
	# Phase-0: filter out unwanted gdb.Symbol objects, and sort the wanted ones.
	sortedSymbols = sorted(filter(isUnder_sourceDirectories,x)
						   , key=functools.cmp_to_key(cmp_gdbSymbols))
	#
	# Phase-1: generate array of PrBlockElem.
	prArr = []
	for xitem in sortedSymbols:
		prElem = PrBlockElem()
		#
		objf = xitem.symtab.objfile
		if objf:
			prElem.objfTag = sprintf('%s%s%s%s', FONTblue,boldFONT,
										objf.filename,resetFONT)
			if objf.build_id != None:
				prElem.objfTag += sprintf('  build_id=%s', objf.build_id)
		#
		baseName = os.path.basename(xitem.symtab.filename)
		fullPath = xitem.symtab.fullname()
		prElem.locTag = sprintf('%s:%u',
								ternary(PREF_FullPaths,fullPath,baseName) ,xitem.line)
		#
		if xitem.is_argument: prElem.smallTags += '|arg'
		if xitem.is_variable: prElem.smallTags += '|var'
		if xitem.is_constant: prElem.smallTags += '|const'
		if xitem.is_function: prElem.smallTags += '|func'
		#
		if gdb.SYMBOL_LOC_BLOCK == xitem.addr_class:
			prElem.addrCateg += 'Scope block'
		elif gdb.SYMBOL_LOC_TYPEDEF == xitem.addr_class:
			prElem.addrCateg += 'A type.'
		else:
			prElem.addrCateg += addrcStorageCategory(xitem.addr_class).capitalize()
		#
		prElem.printName = xitem.print_name
		#
		v=None
		if gdb.SYMBOL_LOC_TYPEDEF == xitem.addr_class:
			pass
		elif gdb.SYMBOL_LOC_BLOCK == xitem.addr_class:
			if ltab !=None:
				for yitem in ltab:
					if yitem.line == xitem.line:
						prElem.astr = prAddr(yitem.pc) # OK to trust this???
						break
		else:
			try:
				v = xitem.value(fr)
			except BaseException as whatev: None
			if None==v:
				prElem.vstr = '?None?'
			else:
				tUnderly = v.type.strip_typedefs()
				prElem.typeCateg = type_codeToStr[tUnderly.code]
				if isPointer(tUnderly):
					if not int(v):
						prElem.vstr='nullptr'
					else:
						prElem.vstr = prAddr(v)
				elif isTypeNativelyPrintable(tUnderly):
					prElem.vstr=str(v)
				else:
					prElem.vstr = '----' # Not natively printable.
		prElem.vstr = prElem.vstr.replace('\n',' ')
		#
		if v!=None and v.address!=None:
			prElem.astr = prAddr(v.address)
		#
		prArr.append(prElem)
	#
	# Phase-2: figure column widths for print formatting.
	maxlen_locTag=0
	maxlen_smallTags=0
	maxlen_typeCateg=0
	maxlen_addrCateg=0
	maxlen_astr=0
	maxlen_printName=0
	for prElem in prArr:
		maxlen_locTag = max(maxlen_locTag, len(prElem.locTag))
		maxlen_smallTags = max(maxlen_smallTags, len(prElem.smallTags))
		maxlen_typeCateg = max(maxlen_typeCateg, len(prElem.typeCateg))
		maxlen_addrCateg = max(maxlen_addrCateg, len(prElem.addrCateg))
		maxlen_astr = max(maxlen_astr, len(prElem.astr))
		maxlen_printName = max(maxlen_printName, len(prElem.printName))
	#
	if PREF_Debug:
		printf('maxlen_locTag=%u maxlen_smallTags=%u maxlen_addrCateg=%u\n',
			   maxlen_locTag,maxlen_smallTags,maxlen_addrCateg)
		printf('maxlen_astr=%u maxlen_printName=%u\n',
			   maxlen_astr, maxlen_printName)
	# Phase-3: print each PrBlockElem, finally.
	prev_objfTag=None
	for prElem in prArr:
		if prElem.objfTag and ((not prev_objfTag) or (prElem.objfTag != prev_objfTag)):
			printf('\n%s\n', prElem.objfTag)
			prev_objfTag = prElem.objfTag
		printf('%-*s  %s%s%-*s%s  %*s  %s%s%*s%s  %s%*s%s  %s%s%s%s  %s\n',
			   maxlen_locTag,    prElem.locTag,
			   FONTmagenta,italicFONT,  maxlen_smallTags, prElem.smallTags,  resetFONT,
			   maxlen_typeCateg, prElem.typeCateg,
			   FONTblue,italicFONT,  maxlen_addrCateg, prElem.addrCateg,  resetFONT,
			   FONTblue, maxlen_astr,      prElem.astr, resetFONT,
			   boldFONT,FONTred,prElem.printName,resetFONT,
			   prElem.vstr)


def list_all_Frame ( ):
	result = []
	fr = gdb.newest_frame()
	while fr !=None:
		result.append(fr)
		fr = fr.older()
	return result

def dump_Frame (i_fr, fr):
	manyUnderscores = ''.ljust(80,'_')
	isCurrTag = 'Selected'
	#####
	s = sprintf('#%s%-4u%s', FONTred,i_fr,resetFONT)
	#
	if fr == gdb.selected_frame():
		s += sprintf('%s%s%s%s', italicFONT,FONTcyanBackgd,isCurrTag,resetFONT)
	else:
		s += ''.ljust(len(isCurrTag))
	#
	s += sprintf(' valid:%c', bool_to_char(fr.is_valid()))
	#
	s += sprintf(' %skind%s=%s%s%s',
				italicFONT,resetFONT, boldFONT,frame_typeToStr[fr.type()],resetFONT)
	#
	s += sprintf(' resumePC=%s', prAddr(fr.pc()))
	#
	b = fr.block()
	if b !=None:
		s += sprintf(' Block[%s,%s]', prAddr(b.start), prAddr(b.end))
	#
	fu = fr.function()
	if fu != None and hasattr(fu,'name'):
		s += sprintf('\n\t\tfunc="%s%s%s"', FONTmagenta,fu.name,resetFONT)
	#
	printf('%s\n%s\n', manyUnderscores, s)

def dump_all_frames ( ):
	fr = gdb.newest_frame()
	manyUnderscores = ''.ljust(80,'_')
	isCurrTag = 'Selected'
	i_fr=0
	while fr !=None:
		s = sprintf('#%s%-4u%s', FONTred,i_fr,resetFONT)
		#
		if fr == gdb.selected_frame():
			s += sprintf('%s%s%s%s', italicFONT,FONTcyanBackgd,isCurrTag,resetFONT)
		else:
			s += ''.ljust(len(isCurrTag))
		#
		s += sprintf(' valid:%c', bool_to_char(fr.is_valid()))
		#
		s += sprintf(' %skind%s=%s%s%s',
					italicFONT,resetFONT, boldFONT,frame_typeToStr[fr.type()],resetFONT)
		#
		s += sprintf(' resumePC=%s', prAddr(fr.pc()))
		#
		b = fr.block()
		if b !=None:
			s += sprintf(' Block[%s,%s]', prAddr(b.start), prAddr(b.end))
		#
		fu = fr.function()
		if fu != None and hasattr(fu,'name'):
			s += sprintf('\n\t\tfunc="%s%s%s"', FONTmagenta,fu.name,resetFONT)
		#
		printf('%s\n%s\n', manyUnderscores, s)
		#
		fr = fr.older()
		i_fr += 1


def iterdump_LineTable_curr (x, pcMin, pcMax):
	assert(isinstance(x, gdb.LineTable))
	printf('\nLineTable 0x%08X {\n', id(x))
	for xitem in x:
		if xitem.pc < pcMin: continue
		if xitem.pc > pcMax: continue
		printf('\t%4u=line %08X=pc\n', xitem.line, xitem.pc)
	printf('}\n')


def iterdump_Type (x, iterableItems):
	assert(isinstance(x, gdb.Type))
	printf('Type sizeof=%u %s {\n', x.sizeof, x.name)
	for xname,xf in iterableItems:
		xtcod='????'
		if xf.type and xf.type.code:
			xtcod=type_codeToStr[xf.type.code]
		misc = '['
		if hasattr(xf, 'bitpos'):
			misc += sprintf('%6d=bitpos', xf.bitpos)
		else:
			misc += ''.ljust(6 + len('bitpos='))
		if hasattr(xf, 'bitsize'):
			misc += sprintf('%5d=bitsize', int(xf.bitsize))
		else:
			misc += ''.ljust(5 + len('bitsize='))
		if xf.parent_type and xf.parent_type != x:
			misc += sprintf(' parentType="%s"', str(xf.parent_type))
		misc += ']'
		printf('%30s --> %10s %s\n', xname, xtcod, misc)
	printf('}\n')


def is_typeName__std_string_view (tStr): # Be sure to call this before is_typeName__std_string()
	s = strip__cxx11(tStr)
	return (s.startswith('std::basic_string_view') or
			s.startswith('std::string_view') or
			s.startswith('std::wstring_view') or
			s.startswith('std::u8string_view') or
			s.startswith('std::u16string_view') or
			s.startswith('std::u32string_view'))

def is_typeName__std_string (tStr):
	s = strip__cxx11(tStr)
	return (s.startswith('std::basic_string') or
			s.startswith('std::string') or
			s.startswith('std::wstring') or
			s.startswith('std::u8string') or
			s.startswith('std::u16string') or
			s.startswith('std::u32string'))

def isStringform (t):
	assert isinstance(t, gdb.Type)
	if performsIndirection(t):
		target_t = get_basic_type(t.target())
		if target_t == gdb.lookup_type('char'):
			return True
	elif TYPE_CODE_STRUCT == t.code:
		if is_typeName__std_string(str(t)):
			return True
	return False


def extractString_from_gdbValue (v):
	assert isinstance(v, gdb.Value)
	t = get_basic_type(v.type)
	if performsIndirection(t):
		target_t = get_basic_type(t.target())
		if target_t == gdb.lookup_type('char'):
			return v.string()
	elif is_typeName__std_string(str(t)):
		v2 = gdb.Value(v['_M_dataplus']['_M_p'])
		s3 = v2.string()
		return s3
	printf('Do not know how to extract from [%s]\n', str(v))
	assert 0


def debug_stringify_gdbValue (v):
	if None==v:
		return '<None>'
	if not isinstance(v, gdb.Value):
		return sprintf('/%s/ %s', str(type(v)), str(v))
	t = get_basic_type(v.type)
	tStr = str(t)
	codeStr = type_codeToStr[t.code]
	prefixStr = ''
	if PREF_Debug:
		prefixStr = sprintf('%s | %s | ', codeStr, tStr)
	if performsIndirection(t): # isPointer(t):
		target_tStr = str(get_basic_type(t.target()))
		if target_tStr == 'char':
			return sprintf('%s%s', prefixStr, str(v))
		else:
			return sprintf('%s%s /%s/ %s', prefixStr, target_tStr, codeStr, prAddr(v))
	if isFundamental(t) or t.code in (TYPE_CODE_ENUM, TYPE_CODE_STRING):
		return sprintf('%s/%s/ %s', prefixStr, codeStr, str(v))
	# If here, v is func or struct or array, which would cause gdb to invoke
	# prettyprinter or in any case to print some large ungainly mess.  Avoid!
	if isStringform(t):
		return sprintf('"%s"', extractString_from_gdbValue(v))
	a = v.address
	if a:
		return sprintf('%s/%s/ at %s', prefixStr, codeStr, prAddr(a))
	else:
		return sprintf('/%s/ of %s', codeStr, tStr)


def dumpCallstack (omitInnermost=False):
	import traceback
	printf('\n')
	stackFrames = reversed(traceback.extract_stack())
	i=-1
	for sf in stackFrames:
		i+=1
		if omitInnermost and 1 == i: # Innermost frame?
			continue
		if sf.name.startswith('dumpCallstack'):
			continue
		printf('%s:%s%u%s,%s',
			   sf.filename.replace('..\\',''),
			   FONTmagenta,sf.lineno,resetFONT,
			   sf.name)
		if sf.line != None and not ('dumpCallstack' in sf.line):
			printf('\n\t%s%s%s', FONTgreen,sf.line,resetFONT)
		printf('\n')
	printf('\n')


def listCallers (max_nCallers=99, omitInnermost=True, stairwise=False):
	import traceback
	listResult = []
	stackFrames = reversed(traceback.extract_stack())
	for sf in stackFrames:
		sFile = sf.filename.replace('..\\','').replace('.py','').split('/')[-1]
		sFunc = sf.name
		if sFunc.startswith('listCallers'):
			continue
		listResult.append(sprintf('%s:%u,%s',
								  sFile, sf.lineno, sFunc))
		if len(listResult) >= (max_nCallers + ternary(omitInnermost,1,0)):
			break
	if omitInnermost:
		listResult = listResult[1:]
	if stairwise:
		strResult = ''
		for i in range(len(listResult)):
			strResult += sprintf('\n%s%s', ''.ljust(i*3), listResult[i])
	else:
		strResult = ' '.join(listResult)
	return strResult

def immedCaller ( ):
	return listCallers(1)

def innermCallee ( ): # Retval is what "__FILE__:__LINE__,__func__" would've been.
	return listCallers(1, omitInnermost=False)


import _stl_containers
import _stl_iterators
import _stl_utilities
#
# Beware of the following pitfall:
#   0.  given a gdb.Value
#   1.  extract its gdb.Type
#   2.  unwrap that gdb.Type's *underlying* gdb.Type
#   3.  try to use this underlying gdb.Type with original gdb.Value
#   4.  original gdb.Value lacks fields expected by this gdb.Type ==> bug!
#
# Returns pair<ppClass,x> where x is an IteratorHusk if ppClass is an IteratorPP
# *and* caller had asked us to try__unwrap_iteratorType; otherwise, x is None.

def gdbType_to_ppClass (t, try__unwrap_iteratorType=True):
	ppClass=None
	iterHusk=None
	tryItersFirst = 'iterator' in str(t)
	# Checking to see whether maybe iterator: not to optimize performance,
	# but merely for less clutter when debugging.
	if tryItersFirst:
		(ppClass,iterHusk) = _stl_iterators.getPP(t,try__unwrap_iteratorType)
	if not ppClass:
		ppClass = _stl_utilities.getPP(t)
		if not ppClass:
			ppClass = _stl_containers.getPP(t)
			if not ppClass and not tryItersFirst:
				(ppClass,iterHusk) = _stl_iterators.getPP(t,try__unwrap_iteratorType)
	assert None==iterHusk or isinstance(iterHusk,IteratorHusk)
	if LOOKUPppCLASS_Debug:
		if not ppClass: printf('For this gdbType, ppClass None!\n')
		else:           printf('For this gdbType, ppClass "%s".\n', ppClass.__name__)
	return (ppClass,iterHusk)
