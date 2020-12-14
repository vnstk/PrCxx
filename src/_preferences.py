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

import enum
from enum import Enum, unique
import gdb
import gdb.prompt
from _usability import *
from _formatting_aids import *


@enum.unique
class eLayout (Enum):
	full = 1  # All layout info: size + offset + alignment, + padding..
	onlySize = 2 # Only size. (But still, in offset order.)
	omit = 3  # No layout info. (But still, in offset order.)

@enum.unique
class eNestedDatamemb (Enum):
	full = 1 # Recurse, and show all intermediates.
	flatten = 2 # Recurse, but show only primitive ivars; i.e., skip all intermediate structs.
	omit = 3 # Do not recurse at all; top-level ivars will all be "opaque".

@enum.unique
class eBaseClasses (Enum):
	full = 1 # All base classes and their members, recursively.
	skipIfEmpty = 2 # Exclude bases (tags, policies, ...) w/o layout-contributing ivars.
	flatten = 3 # Only show the fundamental ivars; skip all intermediate-base structs.
	omit = 4 # No base class info at all; layout parts due to bases will be "opaque".

@enum.unique
class eTemplateArgs (Enum):
	full = 1 # All template args.
	skipIfDefault = 2 # Do not show template args unchanged from the template default.
	omit = 3 # No template arg info at all.


### Defaults ###
default__PREF_PrintWidth_MemberType = 35
default__PREF_PrintWidth_MemberName = 25
default__PREF_Debug = False
default__PREF_FullPaths = True
default__PREF_HeurAbbr = True
default__PREF_Relations = True
default__PREF_Underly = False
default__PREF_Layout = eLayout.full
default__PREF_NestedDatamemb = eNestedDatamemb.flatten
default__PREF_BaseClasses = eBaseClasses.skipIfEmpty
default__PREF_TemplateArgs = eTemplateArgs.skipIfDefault
default__PREF_PrintWidth_MemberType = 35
default__PREF_PrintWidth_MemberName = 25

PREF_PrintWidth_MemberType = default__PREF_PrintWidth_MemberType
PREF_PrintWidth_MemberName = default__PREF_PrintWidth_MemberName
PREF_Debug    = default__PREF_Debug
PREF_FullPaths= default__PREF_FullPaths
PREF_HeurAbbr = default__PREF_HeurAbbr
PREF_Relations = default__PREF_Relations
PREF_Underly  = default__PREF_Underly
PREF_Layout        = default__PREF_Layout
PREF_NestedDatamemb= default__PREF_NestedDatamemb
PREF_BaseClasses   = default__PREF_BaseClasses
PREF_TemplateArgs  = default__PREF_TemplateArgs


@accepts(enum.Enum)
@returns(bool)
def isPREF (e):
#	return isPREFin((e,))  #XXX and why not?
	klas = e.__class__
	if   klas == eLayout:       return PREF_Layout      == e
	elif klas == eNestedDatamemb:  return PREF_NestedDatamemb == e
	elif klas == eBaseClasses:  return PREF_BaseClasses == e
	elif klas == eTemplateArgs:       return PREF_TemplateArgs      == e
	else:
		raise gdb.GdbError(sprintf('Inapplicable %s', repr(e)))

@returns(bool)
def isPREFin (e_list):
	assert len(e_list)
	klas = e_list[0].__class__
	if   klas == eLayout:       return PREF_Layout      in e_list
	elif klas == eNestedDatamemb:  return PREF_NestedDatamemb in e_list
	elif klas == eBaseClasses:  return PREF_BaseClasses in e_list
	elif klas == eTemplateArgs:       return PREF_TemplateArgs      in e_list
	else:
		raise gdb.GdbError(sprintf('Inapplicable %s', repr(e_list)))


def setAllPrefs_to_defaults ( ):
	global PREF_PrintWidth_MemberType
	PREF_PrintWidth_MemberType = default__PREF_PrintWidth_MemberType
	global PREF_PrintWidth_MemberName
	PREF_PrintWidth_MemberName = default__PREF_PrintWidth_MemberName
	#
	global PREF_Debug
	PREF_Debug       = default__PREF_Debug
	global PREF_FullPaths
	PREF_FullPaths   = default__PREF_FullPaths
	global                   PREF_HeurAbbr
	PREF_HeurAbbr = default__PREF_HeurAbbr
	global PREF_Relations
	PREF_Relations   = default__PREF_Relations
	global PREF_Underly
	PREF_Underly     = default__PREF_Underly
	#
	global PREF_Layout
	PREF_Layout      = default__PREF_Layout
	global PREF_NestedDatamemb
	PREF_NestedDatamemb = default__PREF_NestedDatamemb
	global PREF_BaseClasses
	PREF_BaseClasses = default__PREF_BaseClasses
	global PREF_TemplateArgs
	PREF_TemplateArgs      = default__PREF_TemplateArgs
	#
	_reloader.reload_all_but_preferences()  #XXX Need??



def dumpPref_val (val_asString, eqCurrent, eqDefault):
	assert_string(val_asString)
	assert_bool(eqCurrent)
	assert_bool(eqDefault)
	s = ''
	if eqDefault:  s += boldFONT + '[' + resetFONT
	else:          s += ' '
	if eqCurrent:  s += FONTyellowBackgd
	s                += val_asString
	s                += resetFONT
	if eqDefault:  s += boldFONT + ']' + resetFONT
	else:          s += ' '
	return s

def dumpBoolPref (paramTag, valCurrent, valDefault):
	s = ''
	for val in True, False:
		if len(s):
			s += ' | '
		s += dumpPref_val(ternary(val,'on','off')
						  ,val==valCurrent ,val==valDefault)
	printf('%-13s --->  %s\n', paramTag, s)

def dumpEnumPref (paramTag, valCurrent, valDefault):
	s = ''
	for name,val in valCurrent.__class__.__members__.items():
		if len(s):
			s += ' | '
		s += dumpPref_val(name
						  ,val==valCurrent ,val==valDefault)
	printf('%-18s --->  %s\n', paramTag, s)

def dumpUintPref (paramTag, valCurrent, valDefault):
	# First, print default.
	s = dumpPref_val(str(valDefault),valDefault==valCurrent,True)
	# If curr != default, then print curr right next.
	if valCurrent != valDefault:
		s += '  '
		s += dumpPref_val(str(valCurrent),True,False)
	printf('%-26s --->  %s\n', paramTag, s)


### gdb.Parameter subclasses ###

import _reloader


class Debug (gdb.Parameter):
	"""If on, to injury of dysfunction
adds the insult of console spam.
                                             ((Default: off))"""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_Debug
		super(Debug,
			  self).__init__("x-debug",
							 gdb.COMMAND_MAINTENANCE, gdb.PARAM_BOOLEAN)
		self.value = PREF_Debug
	def get_set_string (self):
		global PREF_Debug
		PREF_Debug = self.value
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class FullPaths (gdb.Parameter):
	"""Chooses display of a translation unit's path: absolute path if on, relative path if off.
                                              ((Default: off))"""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_FullPaths
		super(FullPaths,
		      self).__init__("x-full-paths",
		                     gdb.COMMAND_MAINTENANCE, gdb.PARAM_BOOLEAN)
		self.value = PREF_FullPaths
	def get_set_string (self):
		global PREF_FullPaths
		PREF_FullPaths = self.value
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class HeurAbbr (gdb.Parameter):
	"""A type will always be abbreviated by textual substitution of base class and template argument types, when such an abbreviation is certainly correct; this parameter approves additional abbreviations which are highly plausible (per simple heuristic rules) but not certain.
                                              ((Default: off))"""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_HeurAbbr
		super(HeurAbbr,
		      self).__init__("x-heur-abbr",
		                     gdb.COMMAND_DATA, gdb.PARAM_BOOLEAN)
		self.value = PREF_HeurAbbr
	def get_set_string (self):
		global PREF_HeurAbbr
		PREF_HeurAbbr = self.value
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class Relations (gdb.Parameter):
	"""Toggles display of composition and inheritance relations between the data members of a type; if on, such relations are shown for each data member on a separate line directly underneath its printed declaration.
                                              ((Default: on))"""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_Relations
		super(Relations,
		      self).__init__("x-relations",
		                     gdb.COMMAND_DATA, gdb.PARAM_BOOLEAN)
		self.value = PREF_Relations
	def get_set_string (self):
		global PREF_Relations
		PREF_Relations = self.value
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class Underly (gdb.Parameter):
	"""Toggles display of additional type information, such as
\to\t underlying type, with all typedefs stripped.
\to\t type as declared in the source.
\to\t GDB's internal type code.
                                              (Default: off))"""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_Underly
		super(Underly,
			  self).__init__("x-underly",
							 gdb.COMMAND_MAINTENANCE, gdb.PARAM_BOOLEAN)
		self.value = PREF_Underly
	def get_set_string (self):
		global PREF_Underly
		PREF_Underly = self.value
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class Layout (gdb.Parameter):
	"""Controls display of layout metadata inside a type.\n
When printing a field or base class, will:\n
    *full* ==> print size and offset.     ((Default))
*onlySize* ==> print only size.
    *omit* ==> not print any layout info."""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_Layout
		super(Layout,
			  self).__init__("x-layout",
							 gdb.COMMAND_DATA, gdb.PARAM_ENUM,
							 ('full', 'onlySize', 'omit'))
		self.value = PREF_Layout.name
	def get_set_string (self):
		global PREF_Layout
		PREF_Layout = eLayout[self.value]
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class NestedDatamemb (gdb.Parameter):
	"""Controls display of ivars (instance variables), or data members.\n
When printing a class or struct or union, will:
   *full* ==> recurse, and show entire graph.
*flatten* ==> recurse, but only show fundamental "leaves".   ((Default))
   *omit* ==> not recurse, making top-level ivars opaque."""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_NestedDatamemb
		super(NestedDatamemb,
			  self).__init__("x-nested-datamemb",
							 gdb.COMMAND_DATA, gdb.PARAM_ENUM,
							 ('full', 'flatten', 'omit'))
		self.value = PREF_NestedDatamemb.name
	def get_set_string (self):
		global PREF_NestedDatamemb
		PREF_NestedDatamemb = eNestedDatamemb[self.value]
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class BaseClasses (gdb.Parameter):
	"""Controls display of detailed base class information.\n
When printing a type whose definition involves inheritance, will:\n
       *full* ==> print all base classes.
*skipIfEmpty* ==> print only ones contributing to type's ivars.   ((Default))
    *flatten* ==> print only inheritance hierarchy "leaf" nodes.
       *omit* ==> not print any base classes."""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_BaseClasses
		super(BaseClasses,
			  self).__init__("x-base-classes",
							 gdb.COMMAND_DATA, gdb.PARAM_ENUM,
							 ('full', 'skipIfEmpty', 'flatten', 'omit'))
		self.value = PREF_BaseClasses.name
	def get_set_string (self):
		global PREF_BaseClasses
		PREF_BaseClasses = eBaseClasses[self.value]
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class TemplateArgs (gdb.Parameter):
	"""Controls display of template arguments.\n
When printing a templated type, will:\n
         *full* ==> print all template args.              ((Default))
*skipIfDefault* ==> not print if template default is same.
         *omit* ==> not print any template arg information."""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_TemplateArgs #XXX need??
		super(TemplateArgs,
			  self).__init__("x-template-args",
							 gdb.COMMAND_DATA, gdb.PARAM_ENUM,
							 ('full', 'skipIfDefault', 'omit'))
		self.value = PREF_TemplateArgs.name
	def get_set_string (self):
		global PREF_TemplateArgs
		PREF_TemplateArgs = eTemplateArgs[self.value]
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class PrintWidth_MemberType (gdb.Parameter):
	"""Controls width allocated for printing member types by p-type, p-stype, p-vtype, and p-deep.\n
May not be less than 10."""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_PrintWidth_MemberType
		super(PrintWidth_MemberType,
			  self).__init__("x-print-width--member-type",
							 gdb.COMMAND_DATA, gdb.PARAM_ZINTEGER)
		self.value = PREF_PrintWidth_MemberType
	def get_set_string (self):
		from _common import die
		global PREF_PrintWidth_MemberType
		n = int(self.value)
		if n < 10:
			die('May not be less than 10.')
		PREF_PrintWidth_MemberType = n
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue


class PrintWidth_MemberName (gdb.Parameter):
	"""Controls width allocated for printing member names by p-type, p-stype, p-vtype, and p-deep.\n
May not be less than 5."""
	def __init__ (self):
		self.set_doc=''
		self.show_doc=''
		global PREF_PrintWidth_MemberName
		super(PrintWidth_MemberName,
			  self).__init__("x-print-width--member-name",
							 gdb.COMMAND_DATA, gdb.PARAM_ZINTEGER)
		self.value = PREF_PrintWidth_MemberName
	def get_set_string (self):
		from _common import die
		global PREF_PrintWidth_MemberName
		n = int(self.value)
		if n < 5:
			die('May not be less than 5.')
		PREF_PrintWidth_MemberName = n
		_reloader.reload_all_but_preferences()
		return ''
	def get_show_string (self, svalue):
		return svalue
