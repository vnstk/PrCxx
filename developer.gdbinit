# vim: syntax=gdb

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


set auto-load python-scripts on

# Settings we want, even if what we want is the GDB default.
set demangle-style gnu
#set disable-randomization on #Li only
set opaque-type-resolution on
set overload-resolution on

set print address on
set print asm-demangle on
set print demangle on
set print elements 0
                 # 0 ==> unlimited.
set print object on
set print pretty on
set print static-members on
set print symbol-filename on
set print union on
set print vtbl on
#	set trace-commands on


# This command will get you back to plain gdb data formatting; source this very
# .gdbinit file again, to regain pretty-printing.

define deactive--all--pretty-printers
	py gdb.pretty_printers=[]
end

define reload
		# In reverse order of dependency; if A depends on B, must reload B before A.
	py reload(_usability)
	py reload(_formatting_aids)
#	py reload(_preferences)    Reloading _preferences resets prefs to their defaults.
	py reload(_indent_spec)
	py reload(_common)
	py reload(_te_arg_profile)
	py reload(_pp_base_classes)	
	py reload(_te_args_rules)
	py reload(_stl_utilities)
	py reload(_stl_iterators)
	py reload(_stl_containers)
	py reload(_our_p)
	py reload(_launchers)
end


# Find pretty-printer for given C++ obj, and dump info about that pretty-printer.
define z-dump-pprinter-innards
	py _launchers.dump_ppObj_innards(gdb.parse_and_eval('$arg0'))
end

define z-iterdump-type
	py _launchers.wrap__iterdump_Type('$arg0')
end

define z-iterdump-type--with-anon-fields
	py _launchers.wrap__iterdump_Type_withAnonFields('$arg0')
end

define z-iterdump-objfile
	py _launchers.iterdump_Objfile('$arg0')
end

define z-iterdump-symtab-linetab-curr
	py _launchers.wrap__iterdump_SymtabLinetab()
end

define z-decode-1
	py _launchers.decode_1arg('$arg0')
end

define z-decode-0
	py _launchers.decode_0args()
end

define z-terminal-characteristics
	py _launchers.terminal_characteristics()
end


# In end-user.gdbinit, we set this to "message".
set python print-stack full

