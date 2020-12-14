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

import gdb
from gdb import *


addr_classToStr = {}
addr_classToStr[gdb.SYMBOL_LOC_UNDEF] = '??bad symbol table??'
addr_classToStr[gdb.SYMBOL_LOC_CONST] = 'scalar (single-word) constant'
addr_classToStr[gdb.SYMBOL_LOC_STATIC] = 'static'
addr_classToStr[gdb.SYMBOL_LOC_REGISTER] = 'value itself, in a register'
addr_classToStr[gdb.SYMBOL_LOC_ARG] = 'value itself, passed as arg'
addr_classToStr[gdb.SYMBOL_LOC_REF_ARG] = 'address, passed as arg'
addr_classToStr[gdb.SYMBOL_LOC_LOCAL] = 'local variable' # A.k.a. on-stack
addr_classToStr[gdb.SYMBOL_LOC_TYPEDEF] = 'a type, not a value!'
addr_classToStr[gdb.SYMBOL_LOC_LABEL] = 'label'
addr_classToStr[gdb.SYMBOL_LOC_BLOCK] = 'a scope block, not a value!'
addr_classToStr[gdb.SYMBOL_LOC_CONST_BYTES] = 'byte-sequence constant'
addr_classToStr[gdb.SYMBOL_LOC_UNRESOLVED] = 'fixed addr + offset decided runtime'
#                                             Instance of a runtime-polymorphic type.
addr_classToStr[gdb.SYMBOL_LOC_OPTIMIZED_OUT] = 'optimized out'
addr_classToStr[gdb.SYMBOL_LOC_COMPUTED] = 'addr decided runtime'
addr_classToStr[gdb.SYMBOL_LOC_REGPARM_ADDR] = 'address, in a register'
#
addr_classToStr[gdb.SYMBOL_UNDEF_DOMAIN] = 'undef domain'
addr_classToStr[gdb.SYMBOL_VAR_DOMAIN] = 'var domain'
addr_classToStr[gdb.SYMBOL_STRUCT_DOMAIN] = 'struct domain'
addr_classToStr[gdb.SYMBOL_LABEL_DOMAIN] = 'label domain'
addr_classToStr[gdb.SYMBOL_VARIABLES_DOMAIN] = 'variables domain'
addr_classToStr[gdb.SYMBOL_FUNCTIONS_DOMAIN] = 'functions domain'
addr_classToStr[gdb.SYMBOL_TYPES_DOMAIN] = 'types domain'



frame_typeToStr = {}
frame_typeToStr[gdb.NORMAL_FRAME] = 'normal'
frame_typeToStr[gdb.DUMMY_FRAME] = 'dummy'
frame_typeToStr[gdb.INLINE_FRAME] = 'inlined'
frame_typeToStr[gdb.TAILCALL_FRAME] = 'tail-call'
frame_typeToStr[gdb.SIGTRAMP_FRAME] = 'signal handler'
frame_typeToStr[gdb.ARCH_FRAME] = 'cross-arch'
frame_typeToStr[gdb.SENTINEL_FRAME] = 'newest normal'



type_codeToStr = {}
"""
gdbBanner=gdb.execute('show version', True)
gdbVer_complete=gdbBanner.splitlines()[0]
gdbVer_major=int(gdbVer_major.split('.')[0])
if gdbVer_major < 8:
		type_codeToStr[ 1] = 'PTR'
		type_codeToStr[ 2] = 'ARRAY'
		type_codeToStr[ 3] = 'STRUCT'
		type_codeToStr[ 4] = 'UNION'
		type_codeToStr[ 5] = 'ENUM'
		type_codeToStr[ 6] = 'FLAGS'
		type_codeToStr[ 7] = 'FUNC'
		type_codeToStr[ 8] = 'INT'
		type_codeToStr[ 9] = 'FLT'
		type_codeToStr[10] = 'VOID'
		type_codeToStr[11] = 'SET'
		type_codeToStr[12] = 'RANGE'
		type_codeToStr[13] = 'STRING'
		type_codeToStr[14] = 'ERROR'
		type_codeToStr[15] = 'METHOD'
		type_codeToStr[16] = 'METHODPTR'
		type_codeToStr[17] = 'MEMBERPTR'
		type_codeToStr[18] = 'REF'
		type_codeToStr[19] = 'CHAR'
		type_codeToStr[20] = 'BOOL'
		type_codeToStr[21] = 'COMPLEX'
		type_codeToStr[22] = 'TYPEDEF'
		type_codeToStr[23] = 'NAMESPACE'
		type_codeToStr[24] = 'DECFLOAT'
		type_codeToStr[25] = 'MODULE'
else:
"""
type_codeToStr[ 1] = 'PTR'
type_codeToStr[ 2] = 'ARRAY'
type_codeToStr[ 3] = 'STRUCT'
type_codeToStr[ 4] = 'UNION'
type_codeToStr[ 5] = 'ENUM'
type_codeToStr[ 6] = 'FLAGS'
type_codeToStr[ 7] = 'FUNC'
type_codeToStr[ 8] = 'INT'
type_codeToStr[ 9] = 'FLT'
type_codeToStr[10] = 'VOID'
type_codeToStr[11] = 'SET'
type_codeToStr[12] = 'RANGE'
type_codeToStr[13] = 'STRING'
type_codeToStr[14] = 'ERROR'
type_codeToStr[15] = 'METHOD'
type_codeToStr[16] = 'METHODPTR'
type_codeToStr[17] = 'MEMBERPTR'
type_codeToStr[18] = 'REF'
type_codeToStr[19] = 'RVALUE_REF'
type_codeToStr[20] = 'CHAR'
type_codeToStr[21] = 'BOOL'
type_codeToStr[22] = 'COMPLEX'
type_codeToStr[23] = 'TYPEDEF'
type_codeToStr[24] = 'NAMESPACE'
type_codeToStr[25] = 'DECFLOAT'
type_codeToStr[26] = 'MODULE'
type_codeToStr[27] = 'INTERNAL_FUNCTION'

# The above assignments to populate this dict were generated by parsing
# whereYouUncompressedTheGdbTarball/gdb/gdbtypes.h, via the following shell one-liner:
#
#    $ sed -n '/^enum type_code/,/};/ { /^    TYPE_CODE_[A-Z0-9_]*\>,/ s/,.*$//p }' gdb/gdbtypes.h | awk '{sub("TYPE_CODE_", ""); printf("type_codeToStr[%2d] = \047%s\047\n", NR, $1)}'
#
