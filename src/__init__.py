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

# reload() of this file should be idempotent.

from gdb import *
from gdb.printing import *
from gdb.types import *

for dirPath, _, _ in os.walk(os.getcwd()):
	if dirPath not in sys.path:
		sys.path.insert(0, dirPath)

import sys
sys.path.append('../')

import _usability
import _formatting_aids
import _preferences
import _codes_stringified # No need to reload this one.
import _indent_spec
import _common
import _te_arg_profile
import _pp_base_classes
import _te_args_rules
import _our_p
import _stl_utilities
import _stl_iterators
import _stl_containers
import _launchers

from _usability import printf, sprintf, nonNull
from _common import LOOKUPppCLASS_Debug


# If we return None from this func, we tell gdb that we don't have a PP for 'val'.
def lookupPP (val):
	t = get_basic_type(val.type)
#	if LOOKUPppCLASS_Debug: printf('Given val of type %s\n', str(t))
	if _common.isTypeNativelyPrintable(t):
		return None
	tstr = str(t)
	tOriginal = t

	iii = 0
	while True:
		if LOOKUPppCLASS_Debug:
			printf('Init lookupPP, iii=%u, tstr =\n\t%s\n', iii,tstr)

		# # # Is an STL support type?
		ppClass = _stl_utilities.getPP(t)
		if ppClass:
			return ppClass(val)

		# # # Is an STL iterator?
		iterHusk = _stl_iterators.unwrap_iteratorValue(val)
		if_iterValue = nonNull(iterHusk.coreValue, val)
		(ppClass,dummy) = _stl_iterators.getPP(if_iterValue.type,    # Already
											   try__unwrapType=False)# unwrapped.
		if ppClass:
			return ppClass(if_iterValue)

		# # # Is an STL container?
		ppClass = _stl_containers.getPP(t)
		if ppClass:
			return ppClass(val)

		# # # If this type derives from another type T2, maybe we know about T2?
		tSuper = _common.get_one_parentClass(val)
		if tSuper!=None:
			val = val.cast(tSuper)
			t = tSuper
			tstr = str(t)
			iii+=1
			if LOOKUPppCLASS_Debug: printf('Switched to direct superclass\n')
			continue
		break

	if LOOKUPppCLASS_Debug:
		printf('\n%sNo specific pretty-printer found for type= %s%s\n',
			   _formatting_aids.FONTred,str(tOriginal),_formatting_aids.resetFONT)

	return None


# gdb.pretty_printers is a list of lookup functions; we only have one such.
gdb.pretty_printers = []
gdb.pretty_printers.append(lookupPP)

# Construct global instances of gdb.Parameter subclasses
_preferences.Debug()
_preferences.FullPaths()
_preferences.HeurAbbr()
_preferences.Relations()
_preferences.Underly()
_preferences.Layout()
_preferences.BaseClasses()
_preferences.NestedDatamemb()
_preferences.TemplateArgs()
_preferences.PrintWidth_MemberType()
_preferences.PrintWidth_MemberName()

# Construct global instances of gdb.Command subclasses
_launchers.Q_IterInto()
_launchers.Q_More()
_launchers.Q_Buckets()
_launchers.Q_CountElems()
_launchers.Q_HasElem()
_launchers.Q_Elem()
_launchers.Q_ElemAddr()
_launchers.Q_ElemKeyAddr()
_launchers.Q_TargetAddr()
_launchers.Q_Whatis()
_launchers.Q_Precis()
_launchers.X_Remind()
_launchers.X_DefaultAll()
_launchers.P_Type()
_launchers.P_SType()
_launchers.P_VType()
_launchers.P_Deep()
_launchers.P_Afar()
_launchers.Z_Remind()
