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
from _codes_stringified import *
from _common import *
from _preferences import *
import _te_args_rules


@enum.unique
class eActualTeArgKind (Enum):
	noDefaultKnown = 1          # Our term for these shall be, "elemental".
	sameAs_knownDefault = 2
	not_sameAs_knownDefault = 3 # I.e., custom.


class TeArg_Profile:
	"""
All we know about a single te arg (an item in te arg list), as
we go through process of simplifying a C++ type's designation.
________
		i_teArg            : uint
		actual_teArg       : uint (wrapped in gdb.Value) or else gdb.Type
		tar                : TeArgs_Rule
		strOriginal        : string
		strBest            : string // Best-at-time pre-subst
		strFinal           : string // post-subst
		want_derElementals  : bool
		derElementals       : string // *output* of an elemental composition.
		kind               : eActualTeArgKind
		printThis_teArg    : bool
	"""
	def __init__ (self, tar, i_teArg, actual_teArg):
		assert (None==tar) or isinstance(tar,_te_args_rules.TeArgs_Rule)
		self.i_teArg = assert_uint(i_teArg)
		assert actual_teArg !=None
		self.actual_teArg = actual_teArg
		self.strOriginal = str(self.actual_teArg)
		self.strBest = normalizeTypename(self.strOriginal)
		if tar:
			presav = self.strBest
			#
			indices = list(range(len(tar.elementalCompositions)))
			indices.reverse() # On assumption that te args start with the simpler types.
			for k in indices:
				eC = tar.elementalCompositions[k]
				if None==eC[1]: continue
				sav = self.strBest
				self.strBest = self.strBest.replace(eC[0], eC[1])
				traceSubst('suP-bst TAPctor',
						   sav,   eC[0],eC[1]   ,self.strBest,  SUBST_Debug)
			#
			if self.strBest != presav and PREF_Debug:
				printf('%sstrBest change-CTOR%s[%d],\n\t"%s"\nto\n\t"%s"\n',
					   FONTredRUDE,resetFONT,self.i_teArg,presav,self.strBest)
			#
			self.want_derElementals = (isinstance(self.actual_teArg,gdb.Type)  and
									  ('<' in self.strOriginal)               and
									  (self.i_teArg < tar.n_elementalTeParams()))
		else:
			self.want_derElementals =False
		self.derElementals =None
		self.strFinal =None
		self.kind =None
		self.printThis_teArg =True
		self.tar =tar

	def __str__ (self):
		s = sprintf('\ti=%s%s%d%s\n', boldFONT,FONTmagenta,self.i_teArg,resetFONT)
		if self.kind!=None:
			s += sprintf('\t%s%s%s', underscFONT,self.kind.name,resetFONT)
		else:
			s += sprintf('\t%s?kind?%s', underscFONT,resetFONT)
		tarStr='None'
		if self.tar!=None:
			if 0 == self.i_teArg:
				tarStr = self.tar.__class__.__name__
			else:
				tarStr = 'Same'
		s += sprintf(' printThis_teArg:%s%c%s tar/%s/ want_derElementals=%c\n',
					 boldFONT,bool_to_char(self.printThis_teArg),resetFONT,
					 tarStr, bool_to_char(self.want_derElementals))
		s += sprintf('\t\t  strOriginal[%s%s%s]\n',
					 FONTred,    self.strOriginal, resetFONT)
		s += sprintf('\t\t      strBest[%s%s%s]\n',
					 FONTmagenta,self.strBest,     resetFONT)
		s += sprintf('\t\t     strFinal[%s%s%s]\n',
					 FONTblue,   self.strFinal,    resetFONT)
		s += sprintf('\t\tderElementals[%s%s%s]\n',
					 FONTblue,   self.derElementals,resetFONT)
		return s

	def set__strBest (self, x):
		assert_string(x)
		self.strBest = x

	def set__strFinal (self, x):
		assert_string(x)
		self.strFinal = x

	def set__derElementals (self, x):
		cfid = next_callFrameId()
		assert_string(x)
		x = normalizeTypename(x)
		if SUBST_Debug:
			printf('%s%s%s\n%s i_teArg=%u tar/%s/ Passed "%s%s%s"\n',
				   FONTblue,listCallers(stairwise=True),resetFONT, cfid,
				   self.i_teArg, self.tar.__class__.__name__,
				   FONTred,x,resetFONT)
		if self.strBest == x:
			if SUBST_Debug:
				printf('%s No-op, because == strBest already had.\n',cfid)
		else:
			self.derElementals = x

	def decide_kind (self):
		cfid = next_callFrameId()
		assert(self.tar!=None)
		if self.i_teArg >= len(self.tar.defaultStrings):
			self.kind = eActualTeArgKind.noDefaultKnown
		elif None == self.tar.defaultStrings[self.i_teArg]:
			self.kind = eActualTeArgKind.noDefaultKnown
		else:
			comparandA = cmpPrep(strip__cxx11(self.strBest))
			comparandB = cmpPrep(strip__cxx11(self.tar.defaultStrings[self.i_teArg]))
			if PREF_Debug:
				printf('%s %s____________%s\n',boldFONT,resetFONT,cfid)
				printf('%sCmp%s  strBest "%s%s%s"\n  to default "%s%s%s"    (%s i=%u)\n',
					   boldFONT,resetFONT, FONTred,comparandA,resetFONT,
					   FONTblue,comparandB,resetFONT,
					   self.tar.__class__.__name__,self.i_teArg)
			if comparandA == comparandB:
				if isPREF(eTemplateArgs.skipIfDefault):
					self.printThis_teArg =False
				self.kind = eActualTeArgKind.sameAs_knownDefault
			else:                 # not sameAs knownDefault ==> Custom.
				if PREF_Debug:
					sOut = sprintf('%s /%s/ Reckon %d=i_teArg %s%s!= known default%s:',
								   cfid, self.tar.__class__.__name__, self.i_teArg,
								   boldFONT,FONTred,resetFONT)
					sOut += sprintf('\n\tstrBest =\n\t\t%s\ndiffers from\n\t', comparandA)
					sOut += sprintf('tar.defaultStrings[i_teArg] =\n\t\t%s\n.', comparandB)
					printf('%s\n', sOut)
				self.kind = eActualTeArgKind.not_sameAs_knownDefault

	def generateDebugLabel (self):
		if isinstance(self.actual_teArg, gdb.Type):
			code = self.actual_teArg.code # yestype?
		else:
			code = self.actual_teArg.type.code # nontype?
		return sprintf('%-10s %2d=i ', type_codeToStr[code], self.i_teArg)


class TeArg_Profile__Deck:
	"""
What we know about the entire te arg list ("deck"), as we
go through process of simplifying a C++ type's designation.
________
		tapDeck            : TeArg_Profile[]
		max_tap_card       : uint // Expected eventual |tapDeck|
	"""
	def __init__ (self, n):
		self.tapDeck = []
		self.max_tap_card = assert_uint(n)

	def __str__ (self):
		s = sprintf('maxn%u', self.max_tap_card)
		if 0 == len(self.tapDeck):
			s += '{<empty>}'
			return s
		s += '{\n'
		for tap in self.tapDeck:
			s += str(tap)
		s += '}'
		return s

	def add__TeArg_Profile (self, tar, actual_teArg):
		i_teArg = len(self.tapDeck)
		tap = TeArg_Profile(tar, i_teArg, actual_teArg)
		self.tapDeck.append(tap)
		return tap

	def composeElementals_maybe (self, i_teArg):
		cfid = next_callFrameId()
		tar = self.tapDeck[i_teArg].tar
		if (i_teArg + 1) != tar.n_elementalTeParams():
			return
		all__actual_teArg = self.mk_listOf__actual_teArg()
		all__derElementals = self.mk_listOf__derElementals()
		all__strBest      = self.mk_listOf__strBest()
		if PREF_Debug:
			_te_args_rules.TeArgs_Rule.dump(tar, all__actual_teArg, 'XFbef')
		tar.composeElementals(all__strBest, all__derElementals)
		if SUBST_Debug:
			printf('Compos done, elementalCompositions= %s\n',
				   tar.str_elementalCompositions())
		if PREF_Debug:
			_te_args_rules.TeArgs_Rule.dump(tar, all__actual_teArg, 'XFaft')
		if not len(tar.elementalCompositions):
			if PREF_Debug:
				printf('%s Non-0 elemental te params, but 0 elementals; weird?\n', cfid)
			return
		for i in range(min(len(tar.elementalCompositions), len(self.tapDeck))):
			replaceWhat = tar.elementalCompositions[i][0]
			replaceWith = tar.elementalCompositions[i][1]
			if None==replaceWith: continue
			sav = self.tapDeck[i].strBest
			if sav == replaceWhat:
				self.tapDeck[i].set__strBest(replaceWith)
				self.tapDeck[i].set__strFinal(replaceWith) #dog buried here eh?
			#WTF????
			traceSubst(sprintf('suQ-bst i=%u',i),
					   sav,  replaceWhat,replaceWith  ,self.tapDeck[i].strBest ,
					   SUBST_Debug)

	def mk_listOf__actual_teArg (self):
		result = []
		for tap in self.tapDeck:
			result.append(tap.actual_teArg)
		return result
	def mk_listOf__strOriginal (self):
		result = []
		for tap in self.tapDeck:
			result.append(tap.strOriginal)
		return result
	def mk_listOf__strBest (self):
		result = []
		for tap in self.tapDeck:
			result.append(tap.strBest)
		return result
	def mk_listOf__strFinal (self):
		result = []
		for tap in self.tapDeck:
			if tap.strFinal==None: continue
			result.append(tap.strFinal)
		return result
	def mk_listOf__strFinal_evenIfNone (self):
		result = []
		for tap in self.tapDeck:
			result.append(tap.strFinal)
		return result
	def mk_listOf__strBest__concise (self):
		result = []
		if not isPREF(eTemplateArgs.omit):
			for tap in self.tapDeck:
				if tap.printThis_teArg:
					result.append(tap.strFinal)
		return result
	def mk_listOf__derElementals (self):
		result = []
		for tap in self.tapDeck:
			result.append(tap.derElementals)
		return result
