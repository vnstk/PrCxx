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


FONTred     = '\033[31m'
FONTgreen   = '\033[32m'
FONTblue    = '\033[34m'
FONTmagenta = '\033[35m'

FONTredBackgd    = '\033[41m'
FONTgreenBackgd  = '\033[42m'
FONTyellowBackgd = '\033[43m'
FONTcyanBackgd   = '\033[46m' # "cyan" == light blue.

boldFONT    = '\033[1m'
italicFONT  = '\033[3m' # Avoid this + bold, for lowercase.
underscFONT = '\033[4m'
reverseFONT = '\033[7m'

# The "...RUDE" aliases combine bold + background + inverse
# video; thus, cyanRUDE = thick cyan letters against black
# background.  ("RUDE" is short for "OBTRUDE".)
FONTwhiteRUDE   = '\033[37;40;1m'
FONTredRUDE     = '\033[31;40;1m'
FONTgreenRUDE   = '\033[32;40;1m'
FONTyellowRUDE  = '\033[33;40;1m'
FONTmagentaRUDE = '\033[35;40;1m'
FONTcyanRUDE    = '\033[36;40;1m'

resetFONT = '\033[0m'


@returns(int)
def consoleWidth ( ):
	return 80
# Approach A:
#	import os
#	import gdb
#	(nCols,nRows) = os.get_terminal_size(gdb.STDOUT)
#	return int(nCols)
#
# Approach B:
	#
	#	rows, columns = os.popen('stty size', 'r').read().split()
