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


class IndentSpec:
	def __init__ (self, nestLev):
		assert_uint(nestLev)
		self.nestLev = nestLev
		
	def incrIndent (self, nestLevIncr=1):
		self.nestLev = self.nestLev + nestLevIncr
	
	def decrIndent (self, nestLevDecr=1):
		assert (self.nestLev > 0)
		self.nestLev = self.nestLev - nestLevDecr

	def newLine_beginList (self, listOpeningChar):
		printf(''.join(['\n',
						''.ljust(4 * self.nestLev),
						listOpeningChar,
						''.ljust(3)]))

	def sameLine_beginList (self, listOpeningChar):
		printf(''.join([listOpeningChar,
						''.ljust(3)]))

	def newLine_nextItem (self, itemSeparatorChar):
		printf(''.join(['\n',
						''.ljust(4 * self.nestLev),
						''.ljust(2),
						itemSeparatorChar,
						''.ljust(1)]))

	def sameLine_nextItem (self, itemSeparatorChar):
		printf(''.join([itemSeparatorChar,
						''.ljust(1)]))

	def newLine_endList (self, listClosingChar):
		printf(''.join(['\n',
						''.ljust(4 * self.nestLev),
						listClosingChar]))

	def sameLine_endList (self, listClosingChar):
		printf(''.join([''.ljust(3),
						  listClosingChar]))

	def newLine_misc (self, nestLevIncr=0):
		printf(''.join(['\n',
						''.ljust(4 * (self.nestLev + nestLevIncr))]))
