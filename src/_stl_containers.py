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
from _common import *
from _pp_base_classes import *
import _stl_iterators
import _te_args_rules


###################################################################
#### Sequence Containers ##########################################
###################################################################

class std__array (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.fixedKnownSize_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType =   v.type.template_argument(0)
		self.nElements = int(v.type.template_argument(1))
		self.p_start = v['_M_elems']
		self.nElements_allocated = self.nElements
		self.sizeof_node = self.elementType.sizeof
		self.sz_overhead = 0
		self.sz_interstitial_traversal = 0
	def populatePrintables (self):
		self.printablesPopulated=True
		baseAddress = castTo_ptrToType(self.p_start, self.elementType)
		for i in range(self.nElements):
			elementAddress = baseAddress + i
			element = elementAddress.dereference()
			self.addElem(element, int(elementAddress))
		assert(len(self.printables) == self.nElements)
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.just_raw_pointer):
			raise PPFault('Not a compatible iterator type.')
		assert (self.elementType == it.targetType.unqualified())
		start_addr = self.p_start.address
		end_addr = int(self.p_start.address) + int(self.elementType.sizeof * self.nElements)
		if int(start_addr) <= int(it.targetAddr) < int(end_addr):
			return eIteratorStanding.withinBounds_and_valid
		else:
			return eIteratorStanding.outOfBounds


# elems don't have indiv addrs, so not a Sequence; but can retrieve elems by index.
# Unlike std::bitset<M>, *does* have iterators.
class std__vector__bool (AggregatePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		AggregatePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0) # Hint: it's bool.
		self.hasConventionalElements = False
		self.start_nodeAddr        = v['_M_impl']['_M_start']['_M_p']
		self.start_intranodeOffset = v['_M_impl']['_M_start']['_M_offset']
		self.finis_nodeAddr        = v['_M_impl']['_M_finish']['_M_p']
		self.finis_intranodeOffset = v['_M_impl']['_M_finish']['_M_offset']
		self.p_eostorage           = v['_M_impl']['_M_end_of_storage']
#		printf('START{%s,%u=offs} FINIS{%s,%u=offs} EOST:%s\n',
#			   prAddr(self.start_nodeAddr), self.start_intranodeOffset,
#			   prAddr(self.finis_nodeAddr), self.finis_intranodeOffset,
#			   prAddr(self.p_eostorage))
		self.sz_interstitial_traversal=0
		self.printablesPopulated=True
		if 0x0 == int(self.p_eostorage):
			self.onesAndZeros = ''
			self.nElements = 0
			self.nElements_allocated = 0
			self.sz_overhead = v.type.sizeof
			return
		storewordType = gdb.lookup_type('unsigned long')
		nStorewords = (self.finis_nodeAddr - self.start_nodeAddr) + 1
		pWords = castTo_ptrToType(self.start_nodeAddr, storewordType)
		singleChars = ''
		for i in range(nStorewords):
			p_word = pWords + i
			word = int(p_word.dereference())
			for j in range(storewordType.sizeof * 8):
				if p_word == self.start_nodeAddr and j <  self.start_intranodeOffset:
					continue
				if p_word == self.finis_nodeAddr and j >= self.finis_intranodeOffset:
					continue
				if word & (1 << j):
					singleChars += '1'
				else:
					singleChars += '0'
		self.onesAndZeros = singleChars
		self.nElements = len(self.onesAndZeros)
		nElements_perStoreword = int(storewordType.sizeof * 8)
		self.nElements_allocated = int(((self.p_eostorage - self.start_nodeAddr) + 1)
									   * nElements_perStoreword)
		self.sz_overhead = int( v.type.sizeof +
									((self.nElements_allocated - self.nElements) /
									 storewordType.sizeof) +
									((nElements_perStoreword -
									  int(self.finis_intranodeOffset)) / 8) )
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
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__vector__bool):
			raise PPFault('Not a compatible iterator type.')
		if 0 == self.nElements_allocated:
			return eIteratorStanding.outOfBounds
		#
		if (it.target_nodeAddr        == self.start_nodeAddr    and
			it.target_intranodeOffset <  self.start_intranodeOffset):
			return eIteratorStanding.withinBounds_but_invalid
		# Important: on next code line "if" and not "elif", because
		#            start_nodeAddr could be same as finis_nodeAddr.
		if (it.target_nodeAddr        == self.finis_nodeAddr    and
			it.target_intranodeOffset >= self.finis_intranodeOffset):
			return eIteratorStanding.withinBounds_but_invalid
		#
		if self.start_nodeAddr <= it.target_nodeAddr <= self.finis_nodeAddr:
			return eIteratorStanding.withinBounds_and_valid
		else:
			return eIteratorStanding.outOfBounds


class std__vector (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)
		self.p_start = v['_M_impl']['_M_start']
		self.p_finish = v['_M_impl']['_M_finish']
		self.p_eostorage = v['_M_impl']['_M_end_of_storage']
		self.nElements = int(self.p_finish - self.p_start)
		self.nElements_allocated = int(self.p_eostorage - self.p_start)
		self.sizeof_node = self.elementType.sizeof
		self.sz_overhead = WORD_WIDTH.const * int(3)
		self.sz_interstitial_traversal = 0
	def populatePrintables (self):
		self.printablesPopulated=True
		baseAddress = castTo_ptrToType(self.p_start, self.elementType)
		for i in range(self.nElements):
			elementAddress = baseAddress + i
			element = elementAddress.dereference()
			self.addElem(element, int(elementAddress))
		assert(self.nElements == len(self.printables))
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__vector):
			raise PPFault('Not a compatible iterator type.')
		if self.p_start <= it.targetAddr < self.p_finish:
			return eIteratorStanding.withinBounds_and_valid
		elif self.p_finish <= it.targetAddr < self.p_eostorage:
			return eIteratorStanding.withinBounds_but_invalid
		else:
			return eIteratorStanding.outOfBounds


class std__list (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)

		v_impl_node = v['_M_impl']['_M_node']
		if v_impl_node.type.has_key('_M_storage'): # Before 2019?
			storageArr_wrapper = v_impl_node['_M_storage']
			self.payload_offset = v.type.sizeof - storageArr_wrapper.type.sizeof
			self.sizeof_node = int(self.payload_offset + self.elementType.sizeof)
			storageArr_addr = storageArr_wrapper['_M_storage'].address
			storageArr_val_uint = getValueAtAddress(storageArr_addr, gdb.lookup_type('unsigned int'))
			self.nElements = int(storageArr_val_uint)
			self.nElements_allocated = self.nElements
			self.sz_overhead = (storageArr_wrapper.type.sizeof + self.payload_offset * (self.nElements + 1))
			self.p_head = v_impl_node.address
		else:
			self.nElements = int(v_impl_node['_M_size'])
			self.nElements_allocated = self.nElements
			self.payload_offset = 2 * WORD_WIDTH.const # To accomodate _M_prev and _M_next pointers.
			targetType = get_basic_type(self.elementType)
			nodeTypeName = sprintf('std::_List_node<%s>', str(targetType))
			nodeType = gdb.lookup_type(nodeTypeName)
			self.sizeof_node = nodeType.sizeof
			self.sz_overhead = v_impl_node.type.sizeof + (self.sizeof_node - self.elementType.sizeof) * self.nElements
			self.p_head = v_impl_node.address

	def populatePrintables (self):
		self.printablesPopulated=True
		prev_beginAddr=None
		total_entry_sizeof = int(self.payload_offset + self.elementType.sizeof)
		self.sz_interstitial_traversal = 0
		if 0 == self.nElements:
			return
		nElements_scanned = int(0)
		cur = self.p_head['_M_next']
		ir = InterstitialReckoner(total_entry_sizeof)
		while cur != self.p_head:
			elementAddress = castTo_ptrToVoid(cur) + self.payload_offset
			element = getValueAtAddress(elementAddress, self.elementType)
			self.addElem(element, int(elementAddress))
			self.sz_interstitial_traversal += ir.elemIncrem(int(cur))
			nElements_scanned += 1
			if nElements_scanned >= self.nElements:
				break
			cur = cur['_M_next']
		assert(len(self.printables) == self.nElements)
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__list):
			raise PPFault('Not a compatible iterator type.')
		cur = self.p_head['_M_next']
		while cur != self.p_head:
			if cur == it.p__List_node_base:
				return eIteratorStanding.withinBounds_and_valid
			cur = cur['_M_next']
		# std::list<T> cannot have allocated but invalid elements.
		return eIteratorStanding.outOfBounds


class std__forward_list (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_container
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)
		self.sizeof_element = self.elementType.sizeof
		impl_directBases = list_parentClasses(v['_M_impl'].type)
		assert(len(impl_directBases) >= 1)
		wantType_0 = impl_directBases[0]
		assert(wantType_0 != None)
		wantType_1 = wantType_0.template_argument(0)
		assert(wantType_1 != None)
		self.sizeof_node = wantType_1.sizeof
#		printf('wantType_1 i.e. node = %s%s%s; sizeof_node = %u\n',
#			   FONTblue,str(wantType_1), resetFONT, self.sizeof_node)
		payload_offset = _stl_iterators.std__forward_list.reckon_payloadOffset(self.sizeof_node)
#		printf('payload_offset = %u\n', payload_offset)
		self.impl_head = v['_M_impl']['_M_head']
		self.nElements = int(0)
		prev_beginAddr=None
		total_entry_sizeof = int(payload_offset + self.elementType.sizeof)
		self.sz_interstitial_traversal = 0
		cur = self.impl_head['_M_next']
#		printf('total_entry_sizeof = %u; impl_head = %s , cur = %s\n',
#			   total_entry_sizeof, prAddr(self.impl_head.address), prAddr(cur))
		while cur != 0:
			elementAddress = castTo_ptrToVoid(cur) + payload_offset
			element = getValueAtAddress(elementAddress, self.elementType)
			self.addElem(element, int(elementAddress))
			self.nElements += 1
			# Reckoning of sz_interstitial_traversal -- BEGIN
			cur_beginAddr = int(elementAddress - payload_offset)
			cur_endAddr = cur_beginAddr + total_entry_sizeof
			if prev_beginAddr:
				prev_endAddr = prev_beginAddr + total_entry_sizeof
				self.sz_interstitial_traversal += max(
					(cur_beginAddr - prev_endAddr),
					(prev_beginAddr - cur_endAddr))
			prev_beginAddr = cur_beginAddr
			# Reckoning of sz_interstitial_traversal -- END
			cur = cur['_M_next']
		self.nElements_allocated = self.nElements
		if 0 == self.nElements:
			self.sz_overhead = v.type.sizeof
		else:
			self.sz_overhead = v.type.sizeof + payload_offset * (self.nElements + 1)
		self.printablesPopulated=True
	def populatePrintables (self):
		pass # For this container, we're forced to populate printables in ctor itself.
	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__forward_list):
			raise PPFault('Not a compatible iterator type.')
		cur = self.impl_head['_M_next']
		while cur != 0:
			if cur == it.p__Fwd_list_node_base:
				return eIteratorStanding.withinBounds_and_valid
			cur = cur['_M_next']
		# std::forward_list<T> cannot have allocated but invalid elements.
		return eIteratorStanding.outOfBounds


"""
  _M_map_size = 8,  // # nodes; at least 8
  _M_map = 0x6a9610, // Arry of _M_map_size node pointers; initially unused;
                     // initialized to 0xBAADF00D
      ///// A deque iterator (deque itself has 2 of these):
      //
      _Map_pointer _M_node; // Points into _M_map arry (! points directly to a node)
      _Elt_pointer _M_first; // * _M_node
      _Elt_pointer _M_last; // = _M_first + nodeSize (which is always 512)
      _Elt_pointer _M_cur; // [i.first, i.last) ; alw dereferenceable, even if iter past end.
"""
class std__deque (SequencePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__deque
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v.type.template_argument(0)
		sizeofElem = int(self.elementType.sizeof)

		if sizeofElem < 512:
			self.nElems_perNode =   int(512 / sizeofElem)
			sizeof_unused_perNode = int(512 % sizeofElem)
		else:
			self.nElems_perNode = int(1)
			sizeof_unused_perNode = int(0)

		self.nNodes = int(v['_M_impl']['_M_map_size'])
		self.pNodes =     v['_M_impl']['_M_map']
		self.startIter =  v['_M_impl']['_M_start']
		self.finisIter =  v['_M_impl']['_M_finish']

		startNode = self.startIter['_M_node']
		finisNode = self.finisIter['_M_node']
		startCur = self.startIter['_M_cur']
		finisCur = self.finisIter['_M_cur']

		if int(startNode) == int(finisNode): # Only 1 active node?
			self.nElements = (finisCur - startCur)
		else:
			self.nElements = (  self.nElems_perNode - (startCur - self.startIter['_M_first'])
							  + self.nElems_perNode * (finisNode - startNode - 1)
							  + (finisCur - self.finisIter['_M_first']))
		self.nElements = int(self.nElements)
		self.nElements_allocated = self.nElems_perNode * self.nNodes
		self.sz_overhead = (v['_M_impl'].type.sizeof +
								sizeof_unused_perNode * self.nNodes)
	def populatePrintables (self):
		self.printablesPopulated=True
		self.sz_interstitial_traversal = int(0)
		sizeofPayloadPerNode = int(self.nElems_perNode * self.elementType.sizeof)
		pNode = self.startIter['_M_node']
		ir = InterstitialReckoner(sizeofPayloadPerNode)
		while pNode <= self.finisIter['_M_node']:
			if pNode == self.startIter['_M_node'] and pNode == self.finisIter['_M_node']:
				pElem_from = self.startIter['_M_cur']
				pElem_upTo = self.finisIter['_M_cur']
			elif pNode == self.startIter['_M_node']:
				pElem_from = self.startIter['_M_cur']
				pElem_upTo = self.startIter['_M_last']
			elif pNode == self.finisIter['_M_node']:
				pElem_from = self.finisIter['_M_first']
				pElem_upTo = self.finisIter['_M_cur']
			else:
				pElem_from = pNode.dereference()
				pElem_upTo = pElem_from + self.nElems_perNode
			pElem = pElem_from
			while pElem < pElem_upTo:
				elementAddress = castTo_ptrToVoid(pElem)
				element = getValueAtAddress(elementAddress, self.elementType)
				self.addElem(element, int(elementAddress))
				pElem += 1
			if pNode != self.startIter['_M_node']:
				self.sz_interstitial_traversal += ir.elemIncrem(int(pNode))
			pNode += 1
		assert(len(self.printables) == self.nElements)

	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__deque):
			raise PPFault('Not a compatible iterator type.')
		if not((self.pNodes) <= it.p_node < (self.pNodes + self.nNodes)):
			return eIteratorStanding.outOfBounds

		startNode = self.startIter['_M_node']
		finisNode = self.finisIter['_M_node']
		startCur = self.startIter['_M_cur']
		if (((it.p_node == startNode) and (it.p_cur <  self.startIter['_M_cur'])) or
			((it.p_node == finisNode) and (it.p_cur >= self.finisIter['_M_cur']))  ):
			# Oh, for braces to delimit a then-clause!
			return eIteratorStanding.withinBounds_but_invalid

		return eIteratorStanding.withinBounds_and_valid



###################################################################
#### Sequence Container Adaptors ##################################
###################################################################

class SeqContainerAdaptor (SequencePP):
	def __init__ (self, v, canAdapt_deque, canAdapt_list, canAdapt_vector):
		assert (isinstance(v, gdb.Value))
		assert (isinstance(canAdapt_deque, bool))
		assert (isinstance(canAdapt_list, bool))
		assert (isinstance(canAdapt_vector, bool))
		SequencePP.__init__(self)
		self.sz_used__objProper = v.type.sizeof
		self.adapteeType = v.type.template_argument(1)
		adapteeType_asStr = str(self.adapteeType).replace('std::__cxx11::', 'std::')
		if adapteeType_asStr.startswith('std::deque<') and canAdapt_deque:
			self.adaptee = std__deque(v['c'])
		elif adapteeType_asStr.startswith('std::list<') and canAdapt_list:
			self.adaptee = std__list(v['c'])
		elif adapteeType_asStr.startswith('std::vector<') and canAdapt_vector:
			self.adaptee = std__vector(v['c'])
		else:
			raise PPFault('Unexpected adapteeType_asStr[%s]' % adapteeType_asStr)
		#
		self.printables = self.adaptee.printables # Shallow copy, will be fine.

	def populatePrintables (self): self.adaptee.populatePrintables()
	def countElements (self): return self.adaptee.countElements()
	def hasElement (self, lookupBy):
		return self.adaptee.hasElement(lookupBy)
	def getElement (self, lookupBy):
		return self.adaptee.getElement(lookupBy)
	def getElementAddress (self, lookupBy):
		return self.adaptee.getElementAddress(lookupBy)
	def moreInfo (self): self.adaptee.moreInfo()
	def iterStanding (self, it): self.adaptee.iterStanding(it)


class std__priority_queue (SeqContainerAdaptor):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__priority_queue
	def __init__ (self, v):
		SeqContainerAdaptor.__init__(self, v, True, False, True)
		self.elementType = v.type.template_argument(0)

class std__queue (SeqContainerAdaptor):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_sequence_adapter
	def __init__ (self, v):
		SeqContainerAdaptor.__init__(self, v, True, True, False)
		self.elementType = v.type.template_argument(0)

class std__stack (SeqContainerAdaptor):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.simple_sequence_adapter
	def __init__ (self, v):
		SeqContainerAdaptor.__init__(self, v, True, True, True)
		self.elementType = v.type.template_argument(0)



###################################################################
#### Tree-based Associative Containers ############################
###################################################################

# Not for pretty-printing; just for better p-deep/p-vtype output.
class std__Rb_tree (BasePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__Rb_tree
	def __init__ (self, v):
		BasePP.__init__(self)


class TreeAssociativePP (AssociativePP):
	def __init__ (self, v, keysOnly, elementType__i__tree_teArgs):
		assert_bool(keysOnly)
		assert_uint(elementType__i__tree_teArgs)
		AssociativePP.__init__(self, keysOnly)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v['_M_t'].type.template_argument(elementType__i__tree_teArgs)
		self.sizeof_node = int(4) * WORD_WIDTH.const + int(self.elementType.sizeof)
		self.amMulti = str(v.type).startswith('std::multi')
		treeImpl = v['_M_t']['_M_impl']
		self.header = treeImpl['_M_header']
		self.nElements = int(treeImpl['_M_node_count'])
		self.nElements_allocated = self.nElements
		self.sz_overhead = (treeImpl.type.sizeof +
								int(self.header.type.sizeof) * self.nElements)

	def addElem_given_payloadAddr (self, payloadAddr, nodeAddr): pass # Subclasses must oride.

	def populatePrintables (self):
		self.printablesPopulated=True
		self.sz_interstitial_traversal = 0
		if 0 == self.nElements:
			self.rbTree_height = 0
			return
		root = self.header['_M_parent']
		# It's a binary search tree (BST), so inorder traversal visits in sorted order.
		# We'll use a list for a stack: "a.insert(0,X)" to push; "a.pop(0)" to pop.
		pstack = [root]
		h = int(1)
		p_prev = self.header.address # Neither 0, nor the address of any node.
		ir = InterstitialReckoner(self.sizeof_node)
		while len(pstack):
			h = max(h, len(pstack))
			p_curr = pstack[0]
			from_Lchild = p_prev == p_curr['_M_left']
			from_Rchild = p_prev == p_curr['_M_right']
			p_prev = p_curr
			if PREF_Debug:
				printf('%s%s%s  [%s< %s >%s]  prev=%s\n', FONTred,prAddr(p_curr),resetFONT,
					   prAddr(p_curr['_M_left']), prAddr(p_curr['_M_parent']),
					   prAddr(p_curr['_M_right']), prAddr(p_prev))
			if (not from_Lchild) and (not from_Rchild) and p_curr['_M_left']:
				pstack.insert(0, p_curr['_M_left'])  ## goto L subtree
				continue
			if ((not p_curr['_M_left']) or from_Lchild) and (not from_Rchild):
				payloadAddr = castTo_ptrToVoid(p_curr) + int(4) * WORD_WIDTH.const
				self.addElem_given_payloadAddr(payloadAddr, p_curr)
				self.sz_interstitial_traversal += ir.elemIncrem(int(p_curr))
			if not from_Rchild and p_curr['_M_right']:
				pstack.insert(0, p_curr['_M_right']) ## goto R subtree
				continue
			pstack.pop(0)                            ## goto parent
		assert(len(self.printables) == int(ternary(self.keysOnly,1,2) * self.nElements))
		self.rbTree_height = int(h - 1)

	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__Rb_tree):
			raise PPFault('Not a compatible iterator type.')
		for na in self.nodeAddrs:
			if na == it.nodeAddr: return eIteratorStanding.withinBounds_and_valid
		return eIteratorStanding.outOfBounds


class std__map (TreeAssociativePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__map
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		TreeAssociativePP.__init__(self, v, keysOnly=False, elementType__i__tree_teArgs=1)
		self.kvType = self.elementType
		self.kType = get_basic_type(self.kvType.template_argument(0))
		self.vType = get_basic_type(self.kvType.template_argument(1))
		self.decide_whether_stringformKeys(self.kType)
	def addElem_given_payloadAddr (self, payloadAddr, nodeAddr):
		kv_addr = payloadAddr
		kv = getValueAtAddress(kv_addr, self.kvType)
		k_addr = kv_addr
		k_value = kv['first']
		v_value = kv['second']
		v_addr = v_value.address
		self.addElem_KeyVal(k_value, v_value, int(k_addr), int(v_addr), int(nodeAddr))

class std__set (TreeAssociativePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__set
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		TreeAssociativePP.__init__(self, v, keysOnly=True, elementType__i__tree_teArgs=0)
		self.kType = self.elementType
		self.decide_whether_stringformKeys(self.kType)
	def addElem_given_payloadAddr (self, payloadAddr, nodeAddr):
		k_addr = payloadAddr
		k_value = getValueAtAddress(k_addr, self.kType)
		self.addElem_Key(k_value, int(k_addr), int(nodeAddr))



###################################################################
#### Hashtab-based Associative Containers #########################
###################################################################

# Not for pretty-printing; just for better p-deep/p-vtype output.
class std__Hashtable (BasePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__Hashtable
	def __init__ (self, v):
		BasePP.__init__(self)



class HashtabAssociativePP (AssociativePP):
	def __init__ (self, v, keysOnly, elementType__i__hashtab_teArgs):
		assert_bool(keysOnly)
		assert_uint(elementType__i__hashtab_teArgs)
		AssociativePP.__init__(self, keysOnly)
		self.sz_used__objProper = v.type.sizeof
		self.elementType = v['_M_h'].type.template_argument(elementType__i__hashtab_teArgs)
		wantType_0=None
		directBases = list_parentClasses(v['_M_h'].type)
		for db in directBases:
			if '_Hashtable_alloc' in db.name:
				wantType_0 = db
				break
		assert(wantType_0 != None)
		# Example of wantType_0,
		#
		# std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<
		#                std::pair<char const* const, float>, false> > >
		#
		wantType_1 = wantType_0.template_argument(0)
		# Example of wantType_1,
		#
		# std::allocator<std::__detail::_Hash_node<std::pair<char const* const, float>, false> >
		#
		wantType_2 = wantType_1.template_argument(0)
		# Example of wantType_2,
		#
		#                std::__detail::_Hash_node<std::pair<char const* const, float>, false>
		#
		# *This*, finally, will crack opaqueness of "std::__detail::_Hash_node_base *" for us!
		# Just cast to this special type, then "->_M_storage._M_storage.__data" and done.
		#
		self.nodeDelveType = wantType_2
		self.sizeof_node = int(self.nodeDelveType.sizeof)
		self.hashCodesCached = bool(wantType_2.template_argument(1))
		self.nBuckets = int(v['_M_h']['_M_bucket_count'])
		if PREF_Debug:
			printf('nBuckets=%u hashCodesCached=%c; the %u=sz nodeDelveType is\n\t%s\n',
				   self.nBuckets, bool_to_char(self.hashCodesCached),
				   self.sizeof_node, str(self.nodeDelveType))
		self.nElements = int(v['_M_h']['_M_element_count'])
		self.nElements_allocated = self.nElements
		self.ht = v['_M_h']
		if int(self.ht['_M_single_bucket']): singleBucketPointers=1
		else:                                singleBucketPointers=0
		self.sz_overhead = (self.ht.type.sizeof +
							WORD_WIDTH.const * singleBucketPointers +
							WORD_WIDTH.const * self.nBuckets + # the _M_buckets array
							(self.sizeof_node - int(self.elementType.sizeof)) * self.nElements)

		ht_teArgs = list_templateArgs(self.ht.type)
		if len(ht_teArgs) >= 10:
			ht_traits = list_templateArgs(ht_teArgs[9])
			if len(ht_traits) == 3:
				self.noteTrait('hashtable_traits', 'cache_hash_code',    ht_traits[0])
				self.noteTrait('hashtable_traits', 'constant_iterators', ht_traits[1])
				self.noteTrait('hashtable_traits', 'unique_keys',        ht_traits[2])

	def pbucket_to_pnode (self, pbucket):
		if not int(pbucket):
			return pbucket
		pnode = pbucket.dereference() # A bucket, itself, is a pointer to a node.
		if not int(pnode):
			return pnode
		nodeOpaque = pnode.dereference()
		return nodeOpaque['_M_nxt']

	def kStr_from_payload (self, payload): pass # Subclasses must oride.

	def print_oneNode (self, pnode): # Returns ptr to next node in the singly-linked list.
		pnodeReal = castTo_ptrToType(pnode, self.nodeDelveType)
		nodeReal = pnodeReal.dereference()
		payload_addr = nodeReal['_M_storage']['_M_storage']['__data'].address
		if PREF_Debug:
			printf('node_addr=%s payload_addr=%s\n', prAddr(pnodeReal), prAddr(payload_addr))
		payload = getValueAtAddress(payload_addr, self.elementType)
		kStr = self.kStr_from_payload(payload).replace('\t', ' ').replace('\n', '')
		hashcodeStr = ''
		if self.hashCodesCached:
			hashcodeStr = sprintf('hashcode %s%10u%s, ',
								  FONTblue, int(nodeReal['_M_hash_code']), resetFONT)
		printf('%s%s  Node, %skey= %s\n', ''.ljust(26), prAddr(pnode), hashcodeStr, kStr)
		return nodeReal['_M_nxt']

	def print_oneBucket (self, i, pbucket_pnode):
		printf('Bucket index %s%4d%s, &node= %s\n',
			   FONTmagenta,i,resetFONT, prAddr(pbucket_pnode))

	def printBucketwise (self):
		if self.ht['_M_single_bucket']: # In this case, is only 1 bucket.
			pbucket_pnode = self.pbucket_to_pnode(self.ht['_M_single_bucket'])
			self.print_oneBucket(0, pbucket_to_pnode)
			pnode = self.ht['_M_before_begin']['_M_nxt']
			while pnode:
				pnode = self.print_oneNode(pnode)
		else:
			for i in range(0, self.nBuckets):
				i_pbucket_pnode = self.pbucket_to_pnode(self.ht['_M_buckets'] + int(i))
				self.print_oneBucket(i, i_pbucket_pnode)
				if i_pbucket_pnode:
					reachedNodesOfAnotherBucket=False
					pnode = i_pbucket_pnode
					while pnode and not reachedNodesOfAnotherBucket:
						pnode = self.print_oneNode(pnode)
						for j in range(0, self.nBuckets):
							if j == i: continue # Not strictly necessary
							j_pbucket_pnode = self.pbucket_to_pnode(self.ht['_M_buckets'] + int(j))
							if j_pbucket_pnode == pnode:
								reachedNodesOfAnotherBucket=True
								break

	def next_pnode (self, pnode):
		pnodeReal = castTo_ptrToType(pnode, self.nodeDelveType)
		nodeReal = pnodeReal.dereference()
		return nodeReal['_M_nxt']

	def reckon_bucketLoadStats (self):
		if 0 == self.nBuckets:
			return
		bucketLoads = []
		# Populate the bucketLoads vector.
		if self.ht['_M_single_bucket']:
			thisBucketLoad = int(self.nElements)
			bucketLoads.append(thisBucketLoad)
		else:
			for i in range(0, self.nBuckets):
				thisBucketLoad = int(0)
				i_pbucket_pnode = self.pbucket_to_pnode(self.ht['_M_buckets'] + int(i))
				if i_pbucket_pnode:
					reachedNodesOfAnotherBucket=False
					pnode = i_pbucket_pnode
					while pnode and not reachedNodesOfAnotherBucket:
						thisBucketLoad += int(1)
						pnode = self.next_pnode(pnode)
						for j in range(0, self.nBuckets):
							if j == i: continue # Not strictly necessary
							j_pbucket_pnode = self.pbucket_to_pnode(self.ht['_M_buckets'] + int(j))
							if j_pbucket_pnode == pnode:
								reachedNodesOfAnotherBucket=True
								break
				bucketLoads.append(thisBucketLoad)
		# Now that we have bucketLoads, crunch them to get stats.
		assert len(bucketLoads)
		seq = sorted(bucketLoads)
		n = len(seq)
		popn = self.nElements
		xsum = int(0)
		xprod = int(1)
		for x in seq:
			xsum += x
			if x != 0:
				xprod *= x
		stats = [] #Alias, purely for brevity.
		import statistics
		if popn:
			stats.append( ("geometric mean", sprintf("%.3f", pow(xprod,-popn))) )
			stats.append( ("arithmetic mean", sprintf("%.3f",    xsum / popn)) )
			stats.append( ("population standard deviation", sprintf("%.3f",statistics.pstdev(seq))) )
			stats.append( ("  0th percentile (minimum)", sprintf("%u", seq[0])) )
			stats.append( (" 25th percentile", statistics.median(seq[:(n//2)])) ) #Close enough.
			stats.append( (" 50th percentile (median)", statistics.median(seq)) )
			stats.append( (" 75th percentile", statistics.median(seq[(n//2):])) ) #Close enough.
			stats.append( ("100th percentile (maximum)", sprintf("%u", seq[n-1])) )
		self.bucketLoadStats = stats

	def addElem_given_payloadAddr (self, payloadAddr, nodeAddr): pass # Subclasses must oride.

	def populatePrintables (self):
		self.printablesPopulated=True
		self.sz_interstitial_traversal = 0
		pnode = self.ht['_M_before_begin']['_M_nxt']
		total_entry_sizeof = self.sizeof_node
		ir = InterstitialReckoner(total_entry_sizeof)
		while pnode:
			pnodeReal = castTo_ptrToType(pnode, self.nodeDelveType)
			nodeReal = pnodeReal.dereference()
			payloadAddr = nodeReal['_M_storage']['_M_storage']['__data'].address
			self.addElem_given_payloadAddr(payloadAddr, pnode)
			self.sz_interstitial_traversal += ir.elemIncrem(int(pnode))
			pnode = nodeReal['_M_nxt']
		assert(len(self.printables) == int(ternary(self.keysOnly,1,2) * self.nElements))

	def iterStanding (self, it):
		if not isinstance(it, _stl_iterators.std__Node):
			raise PPFault('Not a compatible iterator type.')
		for na in self.nodeAddrs:
			if na == it.nodeAddr: return eIteratorStanding.withinBounds_and_valid
		return eIteratorStanding.outOfBounds


class std__unordered_map (HashtabAssociativePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__unordered_map
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		HashtabAssociativePP.__init__(self, v, keysOnly=False,
									  elementType__i__hashtab_teArgs=1)
		self.kvType = self.elementType
		kType = v.type.template_argument(0)
		self.decide_whether_stringformKeys(kType)
	def kStr_from_payload (self, payload):
		return str(payload['first'])
	def addElem_given_payloadAddr (self, payloadAddr, nodeAddr):
		kv_addr = payloadAddr
		kv = getValueAtAddress(kv_addr, self.kvType)
		k_addr = kv_addr
		k_value = kv['first']
		v_value = kv['second']
		v_addr = v_value.address
		self.addElem_KeyVal(k_value, v_value, int(k_addr), int(v_addr), int(nodeAddr))


class std__unordered_set (HashtabAssociativePP):
	@staticmethod
	def getTeArgs_Rule ( ): return _te_args_rules.std__unordered_set
	def __init__ (self, v):
		assert (isinstance(v, gdb.Value))
		HashtabAssociativePP.__init__(self, v, keysOnly=True,
									  elementType__i__hashtab_teArgs=0)
		self.kType = self.elementType
		self.decide_whether_stringformKeys(self.kType)
	def kStr_from_payload (self, payload):
		return str(payload)
	def addElem_given_payloadAddr (self, payloadAddr, nodeAddr):
		k_addr = payloadAddr
		k_value = getValueAtAddress(k_addr, self.kType)
		self.addElem_Key(k_value, int(k_addr), int(nodeAddr))



def getPP (valType, includeComponents=False):
	assert isinstance(valType, gdb.Type)
	t = str(valType)
	if LOOKUPppCLASS_Debug:
		printf('\n%s_________________________________________________________________%s\n'\
			   '%s%s_stl_cont%s%s%s((%s  %s  %s%s))%s\n\t%s\n', FONTgreenBackgd,resetFONT,
			   boldFONT,FONTgreenBackgd,resetFONT,boldFONT,italicFONT,resetFONT,
			   t, boldFONT,italicFONT,resetFONT,listCallers(11))

	t = strip__cxx11(t)

	# # # Full-fledged containers.
	if t.startswith('std::array<'):
		return std__array

	if t.startswith('std::vector<') or t.startswith('std::_Vector_base<'):
		if t.startswith('std::vector<bool,') or t.startswith('std::_Vector_base<bool,'):
			return std__vector__bool
		return std__vector

	if t.startswith('std::list<') or t.startswith('std::_List_base<'):
		return std__list

	if t.startswith('std::forward_list<'):
		return std__forward_list

	if t.startswith('std::deque<') or t.startswith('std::_Deque_base<'):
		return std__deque

	if t.startswith('std::map<') or t.startswith('std::_Map_base<') \
	                             or t.startswith('std::multimap<'):
		return std__map

	if t.startswith('std::set<') or t.startswith('std::_Set_base<') \
	                             or t.startswith('std::multiset<'):
		return std__set

	if t.startswith('std::unordered_map<') or t.startswith('std::unordered_multimap<'):
		return std__unordered_map

	if t.startswith('std::unordered_set<') or t.startswith('std::unordered_multiset<'):
		return std__unordered_set

	# # # Mere adapters.
	if t.startswith('std::priority_queue<'):
		return std__priority_queue

	if t.startswith('std::queue<'):
		return std__queue

	if t.startswith('std::stack<'):
		return std__stack

	# # # Significant top-level **components** of full-fledged containers.
	if includeComponents and t.startswith('std::_Hashtable<'):
		return std__Hashtable

#	if includeComponents and t.startswith('std::_Rb_tree<'):
#		return std__Rb_tree

#	if PREF_Debug: printf('T="%s" is not a known STL container type.\n', t)
	return None
