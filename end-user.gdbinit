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

set python print-stack message



define z-frames
	py _launchers.dump_all_frames()
end

# Could also guard against empty strings, for slightly more robust args validation.
# Here's a clever way to do that: stringify, then ask for the 0th char:
#
#		"$arg0"[0]
#
define z-iterdump-block-of-frame-N
	py _launchers.iterdump_Block_ofFrame_N($arg0)
end

define z-iterdump-block-curr
	py _launchers.iterdump_Block_curr()
end

define z-iterdump-block-global
	py _launchers.iterdump_Block_global_ofFrame_curr()
end

define z-iterdump-block-static
	py _launchers.iterdump_Block_static_ofFrame_curr()
end

define z-blocks
	py _launchers.dump_blocks_from_deepest_out()
end
