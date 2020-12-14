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
from _preferences import *
from _pp_base_classes import *
from _common import *
import _te_args_rules
import _stl_iterators


###################################################################
#### Aggregates ###################################################
###################################################################

# elems don't have indiv addrs, so not a Sequence; but can retrieve elems by index.
# NB: std::bitset<N> doesn't have iterators.
class std__bitset (AggregatePP):
	@staticmethod
	def getTeArgs_Rule ( ):
		# The actual teArg used is not N but ceil(N / sizeof(ulong));
		# N never shows up, so there's no point crafting a te args rule for it.
		return None
	"""
	onesAndZeros : string
	"""
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		AggregatePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.hasConventionalElements = False
		self.elementType = gdb.lookup_type('bool') # Fake it.
		self.sz_interstitial_traversal = 0
		self.sz_overhead = 0
		self.printablesPopulated = True
		nRepresentedBits = int(v.type.template_argument(0))
		if 0 == nRepresentedBits:
			self.onesAndZeros = ''
			self.nElements = 0
			self.nElements_allocated = 0
			return
		baseTypes = getTypesOfBaseClasses(v.type)
		assert (1 == len(baseTypes))
		baseType = baseTypes[0]
		baseObj = castTo_ptrToType(v.address, baseType).dereference()
		overallStoreType = baseObj['_M_w'].type.strip_typedefs()
		if overallStoreType.code == TYPE_CODE_ARRAY:
			storewordType = overallStoreType.target().strip_typedefs()
			pWords = castTo_ptrToType(v['_M_w'], storewordType)
		else:
			storewordType = overallStoreType
			pWords = castTo_ptrToType(v['_M_w'].address, storewordType)
		nStorewords = int(overallStoreType.sizeof / storewordType.sizeof)
		singleChars = ''
		for i in range(nStorewords):
			word = int((pWords + i).dereference())
			for j in range(storewordType.sizeof * 8):
				if word & (1 << j):
					singleChars += '1'
				else:
					singleChars += '0'
		self.nElements_allocated = nStorewords * storewordType.sizeof * 8
		a = singleChars[0:nRepresentedBits] # Trim unused bits in highest word, if any.
		self.onesAndZeros = str(a[::-1]) # The Python incantation to reverse a string.
		self.nElements = len(self.onesAndZeros)
	@returns(bool)
	def getElement (self, lookupBy):
		index = int(lookupBy)
		assert_uint(index)
		if index >= self.nElements:
			die('Out-of-bounds: =[=%u=]= >= =[=%u=]= = size.'%(index, self.nElements))
		bit = self.onesAndZeros[index]
		return bit == '1'
	def hasElement (self, lookupBy):
		index = int(lookupBy)
		assert_uint(index)
		return index < self.nElements
	@returns(str)
	def display_hint (self):
		return 'string'
	@returns(str)
	def to_string (self):
		# GDB will "compress" resultant string, unless you issue "set print repeats 0".
		return self.onesAndZeros
	def populatePrintables (self):
		pass
#	@returns(int)
#	def getElementAddress (self, lookupBy):
#		lookupBy = None # You want an int? We'll return you an int!!
#		return -1


class std__initializer_list (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.fixedSize_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)
		self.p_array = v['_M_array']
		self.nElements = int(v['_M_len'])
		self.nElements_allocated = self.nElements # Fixed at compile-time!
		self.sz_overhead = v['_M_len'].type.sizeof
		self.sz_interstitial_traversal = 0
	def populatePrintables (self):
		baseAddress = castTo_ptrToType(self.p_array, self.elementType)
		for i in range(self.nElements):
			elementAddress = baseAddress + i
			element = elementAddress.dereference()
			self.addElem(element, int(elementAddress))
		assert(len(self.printables) == self.nElements)
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.just_raw_pointer):
			raise PPFault('Not a compatible iterator type.')
		assert (self.elementType == it.targetType.unqualified())
		if (self.p_array) <= it.targetAddr < (self.p_array + self.nElements):
			return eIteratorStanding.withinBounds_and_valid
		else:
			return eIteratorStanding.outOfBounds


class std__pair (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__pair
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.hasConventionalElements=False # Heterogeneous!
		self.addElem(v['first'], int(v['first'].address))
		self.addElem(v['second'], int(v['second'].address))
		self.nElements = 2 # (Surprised?)
		self.nElements_allocated = self.nElements
		self.sz_overhead = 0
		self.sz_interstitial_traversal = 0
	def populatePrintables (self): pass # Done in ctor.
	@returns(int)
	def indexAlternatively (self, lookupBy):
		assert_string(lookupBy)
		if lookupBy == 'first':
			return 0
		if lookupBy == 'second':
			return 1
		raise PPFault('Found no element keyed by =[=%s=]=' % (lookupBy))



class std__tuple (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.heterogenous_container
	"""
		elemTypes : gdb.Type[]
	"""
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.hasConventionalElements=False # Heterogeneous!
		self.nElements = 0
		self.nElements_allocated = self.nElements
		self.sz_overhead = 0
		self.sz_interstitial_traversal = 0 # N/A, really.
		self.elemTypes = []
		objAddr = v.address
		baseTypes = getTypesOfBaseClasses(v.type)
		if 0 == len(baseTypes):
			return
		next_mostDerived_baseType = baseTypes[0]
		i = int(0)
		while next_mostDerived_baseType:
			"""
		        Say next_mostDerived_baseType is std::_Tuple_impl<42,Something_t>.  It
		        will have **one** base class named std::_Head_base<42,Something_t,bool>
		        , which we shall use to get at the offset=42 element.  And, if 42 is
		        not the last offset, there will also be **another** base class named
		        std::_Tuple_impl<43,SomethingElse_t> ,which we shall use to loop again.
			"""
			baseTypes = getTypesOfBaseClasses(next_mostDerived_baseType)
			assert (1 <= len(baseTypes) <= 2)
			elemFetchType = None
			typeOne = baseTypes[0]
			typeOne_i = int(typeOne.template_argument(0))
			if 2 == len(baseTypes):
				typeTwo = baseTypes[1]
				typeTwo_i = int(typeTwo.template_argument(0))
				if typeTwo_i == i:
					(elemFetchType,next_mostDerived_baseType) = (typeTwo,typeOne)
				else:
					(elemFetchType,next_mostDerived_baseType) = (typeOne,typeTwo)
			else:
				(elemFetchType,next_mostDerived_baseType) = (typeOne,None)
			# Having sorted which type does what, we proceed to fetch the i'th elem.
			elemWrapAddr = castTo_ptrToType(objAddr, elemFetchType)
			elemWrap = elemWrapAddr.dereference()
			elemAddr = elemWrap['_M_head_impl'].address
			elemType = elemFetchType.template_argument(1)
			elemVal = castTo_ptrToType(elemAddr, elemType).dereference()
			self.addElem(elemVal, int(elemAddr))
			self.elemTypes.append(elemType)
			# Prepare for next loop iter.
			i += 1
		self.nElements = i
		self.nElements_allocated = self.nElements

	def populatePrintables (self): pass # Done in ctor.

	def getElementType (self, index):
		assert_unsigned(index)
		if index >= self.nElements:
			die('Out-of-bounds: =[=%u=]= >= =[=%u=]= = size.'%(index, self.nElements))
		return self.elemTypes[index]



#class std__valarray (SequencePP):
#		# ??



###################################################################
#### Smart Pointers, "Modern C++" Ref Wrappers ####################
###################################################################

class std__any (IndirectorPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		mgr = v['_M_manager']
		if not int(mgr):
			IndirectorPP.__init__(self, v.type) # So, type will be just "std::any"
			self.sz_used__objProper = v.type.sizeof
			self.empty=True
			return
		target = gdb.execute('p/a %u' % (castTo_ptrToVoid(mgr)), to_string=True)
		"""
        Sample value of 'target', with internal storage and currType of "unsigned int":
________
$94 = 0x4126cc <std::any::_Manager_internal<unsigned int>::_S_manage(std::any::_Op, std::any const*, std::any::_Arg*)>
		"""
		iZ = target.rfind('>::_S_manage')
		iX = target[:iZ].find('std::any::_Manager_') + len('std::any::_Manager_')
		internalStorage = target[iX:].startswith('internal')
		externalStorage = target[iX:].startswith('external')
		assert xor(internalStorage, externalStorage)
		iY = iX + len('internal<')
		targetType_asString = target[iY:iZ]
		indirectionLevels = int(0)
		while targetType_asString.endswith('*'):
			indirectionLevels = indirectionLevels + int(1)
			targetType_asString = targetType_asString[:-1]
		targetType_asString = normalizeTypename(targetType_asString)
		targetType = gdb.lookup_type(targetType_asString)
		for i in range(indirectionLevels):
			targetType = targetType.pointer()
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		if internalStorage:
			targetAddr_untyped = v['_M_storage']['_M_buffer']['__data']
			self.targetaddr = castTo_ptrToType(targetAddr_untyped, targetType)
		else:
			targetAddr_untyped = v['_M_storage']['_M_ptr']
			self.targetAddr = castTo_ptrToType(targetAddr_untyped, targetType)
		self.sz_overhead = 4 # Hard to say.
		self.empty=False


class std__optional (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return None
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = v.type.template_argument(0)
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.sz_overhead = v.type.sizeof - self.targetType.sizeof
		self.empty = not bool(v['_M_payload']['_M_engaged'])
		if self.empty:
			return
		targetAddr_untyped = v['_M_payload']['_M_payload'].address
		self.targetAddr = int(castTo_ptrToType(targetAddr_untyped, targetType))


class std__variant (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return None
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		# If invalid, _M_index is set to -1 i.e. all 1-bits.
		invalid=True
		iTarget_addr = castTo_ptrToVoid(v['_M_index'].address)
		uchar_type = gdb.lookup_type('unsigned char')
		for j in range(v['_M_index'].type.sizeof):
			uchar_addr_untyped = iTarget_addr + j
			uchar_addr_typed = castTo_ptrToType(uchar_addr_untyped, uchar_type)
			if 0xFF != int(uchar_addr_typed.dereference()):
				invalid=False
				break
		if invalid:
			IndirectorPP.__init__(self, v.type.template_argument(0))
			self.sz_used__objProper = v.type.sizeof
			self.empty = True
			return
		iTarget = int(v['_M_index'])
		targetWrapper = v['_M_u']
		for i in range(iTarget):
			targetWrapper = targetWrapper['_M_rest']
		targetObj = targetWrapper['_M_first']
		targetType = targetObj.type.template_argument(0)
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		targetAddr_untyped = targetObj['_M_storage'].address
		self.targetAddr = castTo_ptrToType(targetAddr_untyped, targetType)
		self.sz_overhead = 0
		# Now let's try to find some traits.
		directBases = list_parentClasses(v.type)
		#
		for db in directBases:
			if '_Enable_copy_move' in db.name:
				ecm_teArgs = list_templateArgs(db)
				if len(ecm_teArgs) >= 4:
					self.noteTrait('Enable_copy_move','Enable copy ctor',ecm_teArgs[0])
					self.noteTrait('Enable_copy_move','Enable copy assign',ecm_teArgs[1])
					self.noteTrait('Enable_copy_move','Enable move ctor',ecm_teArgs[2])
					self.noteTrait('Enable_copy_move','Enable move assign',ecm_teArgs[3])
					#
			elif '_Enable_default_constructor' in db.name:
				edc_teArgs = list_templateArgs(db)
				if len(edc_teArgs) >= 1:
					self.noteTrait('Enable_default constructor','Enable',edc_teArgs[0])



class std__reference_wrapper (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_pointer_wrapper
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetAddr = v['_M_data'] # A reference is ultimately a pointer.
		targetType = targetAddr.type.target()
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = targetAddr
		self.sz_overhead = 0


class std__unique_ptr (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__unique_ptr
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = v.type.template_argument(0)
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.targetAddr = v['_M_t']['_M_t']['_M_head_impl']
		self.sz_overhead = max(0,v.type.sizeof - self.targetAddr.type.sizeof -
							   WORD_WIDTH.const)


class smart_ptr_withOwnerhip (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_pointer_wrapper
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = v.type.template_argument(0)
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		targetAndPolicyAddr = v['_M_ptr']
		self.targetAddr = castTo_ptrToType(targetAndPolicyAddr, targetType)
		self.sz_overhead = max(0, v.type.sizeof - self.targetAddr.type.sizeof)
		#
		p_ownerBlock = v['_M_refcount']['_M_pi']
		if not int(p_ownerBlock):
			self.ownerInfo.append('Owns nothing.')
		else:
			ownerBlock = p_ownerBlock.dereference()
			self.ownerInfo.append(sprintf('use_count = %u', ownerBlock['_M_use_count']))
			self.ownerInfo.append(sprintf('weak_count = %u', ownerBlock['_M_weak_count']))
			dynTyp = ownerBlock.dynamic_type
			if dynTyp:
				p_ownerBlock_dynTyp = castTo_ptrToType(p_ownerBlock, dynTyp)
				ownerBlock_dynTyp = p_ownerBlock_dynTyp.dereference()
				if has_field(dynTyp,'_M_impl'):
					owneePtr = ownerBlock_dynTyp['_M_impl']['_M_ptr']
				else:
					owneePtr = ownerBlock_dynTyp['_M_ptr']
				self.ownerInfo.append(sprintf('Ownee ptr = %s', prAddr(owneePtr)))

class std__shared_ptr (smart_ptr_withOwnerhip):
	def __init__ (self, v):
		smart_ptr_withOwnerhip.__init__(self, v)

class std__weak_ptr (smart_ptr_withOwnerhip):
	def __init__ (self, v):
		smart_ptr_withOwnerhip.__init__(self, v)



###################################################################
#### std::chrono Types ############################################
###################################################################

#	class std__chrono__duration (ScalarPP):
#	class std__chrono__time_point (ScalarPP):


###################################################################
#### std::string, std::string_view Types ##########################
###################################################################

class std__string_view (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__basic_string_view
	def __init__ (self, v):
		assert isinstance(v, gdb.Value)
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)
		szElem = int(self.elementType.sizeof)
		self.payloadAddr = v['_M_str']
		self.nElements = int(v['_M_len']) # How many chars, not how many bytes!
		self.nElements_allocated = 0 # These chars aren't *ours*; we don't manage them.
		self.sz_interstitial_traversal = 0
		self.sizeof_node = szElem
		self.printablesPopulated=True
	def populatePrintables (self):
		pass
	def to_string (self):
		return gdb.Value(self.payloadAddr)
	def display_hint (self):
		return 'string' # (Surprised?)
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.just_raw_pointer):
			raise PPFault('Altogether unexpected iterator type.')
		# A string_view<Ch> iterator is just a Ch pointer.
		contPtrType = get_basic_type(self.elementType).pointer()
		#printf('contPtrType =  %s\n', str(contPtrType))
		iterPtrType = get_basic_type(it.targetType).pointer()
		#printf('iterPtrType =  %s\n', str(iterPtrType))
		if iterPtrType != contPtrType:
			raise PPFault('Not a compatible iterator type.')
#		if 0 == self.nElements:
#			return eIteratorStanding.outOfBounds
		if it.targetAddr < self.payloadAddr:
			return eIteratorStanding.outOfBounds
		validEndExcl = int(self.payloadAddr) + int(self.elementType.sizeof) * self.nElements
		if it.targetAddr >= validEndExcl:
			return eIteratorStanding.outOfBounds
		return eIteratorStanding.withinBounds_and_valid


class std__string (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__basic_string
	def __init__ (self, v):
		assert isinstance(v, gdb.Value)
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)
		szElem = int(self.elementType.sizeof)
		self.nElements = int(v['_M_string_length']) # How many chars, not how many bytes!
		self.payloadAddr = v['_M_dataplus']['_M_p']
		self.localBufAddr = v['_M_local_buf'].address
		self.objEndAddrExcl = int(v.address) + int(v.type.sizeof)
		self.smallObjectOptimization = int(self.payloadAddr) == int(self.localBufAddr)
		if self.smallObjectOptimization: ## ## Small Obj Opti?
			self.nElements_allocated = int((v.type.sizeof - WORD_WIDTH.const * 2) / szElem)
			# One word for the "_M_p" pointer, one word for "_M_string_length".
			self.sz_overhead = int(v.type.sizeof) - szElem * self.nElements
		else:                            ## ## regular arrangement?
			self.nElements_allocated = int(v['_M_allocated_capacity']) # Also how many *chars*.
			self.sz_overhead = (int(v.type.sizeof - WORD_WIDTH.const) + szElem *
								(self.nElements_allocated - self.nElements))
		if PREF_Debug:
			printf('szElem=%u nElements=%d nElements_allocated=%d smObjOpti:%s\n', szElem,
				   self.nElements, self.nElements_allocated, str(self.smallObjectOptimization))
		self.sz_interstitial_traversal = 0
		self.sizeof_node = szElem
		self.printablesPopulated=True
	def populatePrintables (self):
		pass
	def to_string (self):
		return gdb.Value(self.payloadAddr)
	def display_hint (self):
		return 'string' # (Surprised?)
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__string):
			raise PPFault('Not a compatible iterator type.')
		if PREF_Debug:
			printf('it.targetAddr:%s | payloadAddr:%s localBufAddr:%s\n',
				   prAddr(it.targetAddr), prAddr(self.payloadAddr), prAddr(self.localBufAddr))
		szElem = int(self.elementType.sizeof)
		if self.smallObjectOptimization:
			validBeginIncl = int(self.localBufAddr)
			validEndExcl = int(self.localBufAddr) + szElem * self.nElements
			allocEndExcl = self.objEndAddrExcl
		else:
			validBeginIncl = int(self.payloadAddr)
			validEndExcl = int(self.payloadAddr) + szElem * self.nElements
			allocEndExcl = int(self.payloadAddr) + szElem * self.nElements_allocated
		if PREF_Debug:
			printf('validBeginIncl:%s validEndExcl:%s allocEndExcl:%s\n',
				   prAddr(validBeginIncl), prAddr(validEndExcl), prAddr(allocEndExcl))
		if validBeginIncl <= int(it.targetAddr) < validEndExcl:
#			storage_offset__inElements = (int(it.targetAddr) - validBeginIncl)/szElem
			return eIteratorStanding.withinBounds_and_valid
		elif validEndExcl <= int(it.targetAddr) < allocEndExcl:
#			storage_offset__inElements = (int(it.targetAddr) - validBeginIncl)/szElem
			return eIteratorStanding.withinBounds_but_invalid
		else:
			return eIteratorStanding.outOfBounds



###################################################################
#### std::regex Types #############################################
###################################################################

#XXX https://en.cppreference.com/w/cpp/header/regex   Go see


#class std__regex (BasePP):
#	def __init__ (self, v):
#		BasePP.__init__(self)
#
#
#class std__match (BasePP):




###################################################################
#### Miscellaneous ################################################
###################################################################

class std__exception (ScalarPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		ScalarPP.__init__(self, str(get_basic_type(v.type)))
		self.sz_used__objProper = v.type.sizeof

class std__ratio (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__ratio
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = gdb.lookup_type('int')
		self.addElem(v.type.template_argument(0))
		self.addElem(v.type.template_argument(1))
		self.nElements = 2
		self.nElements_allocated = self.nElements
		self.sz_overhead = 0
		self.sz_interstitial_traversal = 0
	def display_hint (self):
		return 'string'
	def to_string (self):
		return ('%s / %s' % (self.getElement('numer'), self.getElement('denom')))
	def populatePrintables (self): pass # Done in ctor.
	@returns(int)
	def indexAlternatively (self, lookupBy):
		assert_string(lookupBy)
		s = lookupBy.lower()
		if s == 'numer' or s == 'num':
			return 0
		if s == 'denom' or s == 'den':
			return 1
		raise PPFault('Found no element keyed by =[=%s=]=' % (lookupBy))


class std__function (IndirectorPP):
	@staticmethod
	def getTeArgs_Rule ( ): return None #_te_args_rules. ?????
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		targetType = v.type.template_argument(0)
		IndirectorPP.__init__(self, targetType)
		self.sz_used__objProper = v.type.sizeof
		self.empty = int(v['_M_manager']) == 0x0
		self.targetAddr = v['_M_manager']
		self.sz_overhead = int(v.type.sizeof) - WORD_WIDTH.const


###################################################################
#### std::atomic Types ############################################
###################################################################

class std__atomic_integralType_wrapper (ScalarHolderPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		if has_field(v.type, '_M_i'):
			ScalarHolderPP.__init__(self, v['_M_i'])
		else:
			ScalarHolderPP.__init__(self, v['_M_base']['_M_i'])
		self.sz_used__objProper = v.type.sizeof
		self.sizeof_total = v.type.sizeof

class std__atomic_flag (ScalarHolderPP):
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		ScalarHolderPP.__init__(self, v['_M_i'])
		self.sz_used__objProper = v.type.sizeof
		self.sizeof_total = v.type.sizeof


###################################################################
#### **Really** Miscellaneous #####################################
###################################################################

class std__integer_sequence (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.fixedSize_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		ty = (v.type)
		teArgs = list_templateArgs(ty)
		assert(len(teArgs) >= 1)
		self.elementType = teArgs[0]
		# For an unknown reason, _common.list_templateArg() doesn't work here, as
		# far as grabbing the actual integer sequence goes.  So we fake it.   :-(
		self.nElements = 0
		tyStr = str(v.type)
		integersStr = None
		for i in range(len(tyStr)):
			if tyStr[i].isnumeric():
				integersStr = tyStr[i:-1]
				integersList = integersStr.split(', ')
				self.nElements = len(integersList)
				for x in integersList:
					self.addElem(x)
				break
		assert(len(self.printables) == self.nElements)
		self.printablesPopulated=True
		self.nElements_allocated = 0 # No associated storage: is only a template.
		self.sizeof_node = 0
		self.sz_overhead = 0
		self.sz_interstitial_traversal = 0
	def populatePrintables (self): pass


# traits? (pointer_traits?)  policies?

# non-default base classes?


def getPP (valType):
	assert isinstance(valType, gdb.Type)
	t = str(valType)
	if LOOKUPppCLASS_Debug:
		printf('\n%s_________________________________________________________________%s\n'\
			   '%s%s_stl_util%s%s%s((%s  %s  %s%s))%s\n\t%s\n', FONTgreenBackgd,resetFONT,
			   boldFONT,FONTgreenBackgd,resetFONT,boldFONT,italicFONT,resetFONT,
			   t, boldFONT,italicFONT,resetFONT,listCallers(11))

	if t.startswith('std::any'):
		return std__any
	if t.startswith('std::atomic<'):
		return std__atomic_integralType_wrapper
	if t.startswith('std::atomic_flag'):
		return std__atomic_flag
	if (is_typeName__std_string_view(t)):
		return std__string_view
	if (is_typeName__std_string(t)):
		return std__string
	if t.startswith('std::bitset<'):
		return std__bitset
	if t.startswith('std::function<'):
		return std__function
	if t.startswith('std::initializer_list<'):
		return std__initializer_list
	if t.startswith('std::integer_sequence<'):
		return std__integer_sequence
	if t.startswith('std::optional'):
		return std__optional
	if t.startswith('std::pair<'):
		return std__pair
	if t.startswith('std::ratio<'):
		return std__ratio
	if t.startswith('std::reference_wrapper<'):
		return std__reference_wrapper
	if t.startswith('std::shared_ptr<'):
		return std__shared_ptr
	if t.startswith('std::tuple<'):
		return std__tuple
	if t.startswith('std::unique_ptr<'):
		return std__unique_ptr
	if t.startswith('std::variant'):
		return std__variant
	if t.startswith('std::weak_ptr<'):
		return std__weak_ptr


#	if PREF_Debug: printf('T="%s" is not a known STL utility type.\n', t)
	return None
