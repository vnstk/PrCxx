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

from imp import reload

import _usability
import _formatting_aids
import _indent_spec
import _common
import _te_arg_profile
import _pp_base_classes
import _te_args_rules
import _stl_utilities
import _stl_iterators
import _stl_containers
import _our_p
import _launchers

# Reloading _preferences resets prefs to their defaults, that's why not.
def reload_all_but_preferences ():
	# In reverse order of dependency; if A depends on B, must reload B before A.
	reload(_usability)
	reload(_formatting_aids)
	reload(_indent_spec)
	reload(_common)
	reload(_te_arg_profile)
	reload(_pp_base_classes)
	reload(_te_args_rules)
	reload(_stl_utilities)
	reload(_stl_iterators)
	reload(_stl_containers)
	reload(_our_p)
	reload(_launchers)
