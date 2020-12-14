/*                                         Copyright 2020 Vainstein K.
* --------------------------------------------------------------------
* This file is part of PrCxx.
* 
* PrCxx is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* any later version.
* 
* PrCxx is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with PrCxx.  If not, see <https://www.gnu.org/licenses/>.
*/
#include <deque>
#include "garden-of-uints.h"

int main ( )
{
	std::deque<int> di(3U, 55);		//CMD:p//		di
	/*
					{55,55,55}
	*/
	di.push_back(11);
	auto di_it = di.begin();		//CMD:p//		di_it
	/*
					55
	*/
	di_it = di.insert(di_it,77);	//CMD:p//		di_it
	/*
					77
	*/
	di_it = di.insert(di_it,4U,99);	//CMD:p//		di
	/*
					{99,99,99,99,77,55,55,55,11}
	*/
	int di_back;
	di.back() += 80;
	di_back = di.back();			//CMD:p//		di_back
	/*
					91
	*/
	di.push_front(66);	//CMD:q-count-elems//		di
	/*
					10
	*/
	di.resize(20U);		//CMD:q-count-elems//		di
	/*
					20
	*/
	di.back() += 80;
	di_back = di.back();			//CMD:p//		di_back
	/*
					80
	*/
	di.resize(0U);		//CMD:q-count-elems//		di
	/*
					0
	*/
	di.resize(0U);					//CMD:p//		di
	/*
					
	*/
	di.clear();						//CMD:p//		di
	/*
					
	*/


	bool dummy;

	//==================  8b  =======================================
	//
	std::deque<uint8_t> cont8({200, 122, 165, 83, 159});
	decltype(cont8)::iterator it8 = cont8.begin();		//CMD:p/u//	it8
	/*
					200
	*/
	auto jt8 = std::next(it8, 3);						//CMD:p/u//	jt8
	/*
					83
	*/
	dummy=true;									//CMD:q-elem//	cont8 1
	/*
					122 'z'
	*/

	//==================  16b  ======================================
	//
	std::deque<uint16_t> cont16({200,128,165,83,159});
	decltype(cont16)::iterator it16 = cont16.begin();	//CMD:p//	it16
	/*
					200
	*/
	auto jt16 = std::next(it16, 3);						//CMD:p//	jt16
	/*
					83
	*/
	dummy=true;									//CMD:q-elem//	cont16 2
	/*
					165
	*/

	//==================  24b  ======================================
	//
	std::deque<S24> cont24{ S24(7) , S24(5) , S24(9) , S24(3) };
	decltype(cont24)::iterator it24 = cont24.begin();	//CMD:p//	it24
	/*
					{_e = 60014 ,_b = 107 'k' }
	*/
	auto jt24 = std::next(it24, 3);						//CMD:p//	jt24
	/*
					{_e = 60006 ,_b = 103 'g' }
	*/
	dummy=true;									//CMD:q-elem//	cont24 1
	/*
					{_e = 60010 ,_b = 105 'i' }
	*/

	//==================  32b  ======================================
	//
	std::deque<uint32_t> cont32({200,128,165,83,159});
	decltype(cont32)::iterator it32 = cont32.begin();	//CMD:p//	it32
	/*
					200
	*/
	auto jt32 = std::next(it32, 3);						//CMD:p//	jt32
	/*
					83
	*/
	dummy=true;									//CMD:q-elem//	cont32 2
	/*
					165
	*/

	//==================  40b  ======================================
	//
	std::deque<S40> cont40{ S40(3) , S40(5) , S40(9) , S40(7) };
	decltype(cont40)::iterator it40 = cont40.begin();	//CMD:p//	it40
	/*
					{_a = 4000000006 ,_b = 103 'g' }
	*/
	auto jt40 = std::next(it40, 3);						//CMD:p//	jt40
	/*
					{_a = 4000000014 ,_b = 107 'k' }
	*/
	dummy=true;									//CMD:q-elem//	cont40 1
	/*
					{_a = 4000000010 ,_b = 105 'i' }
	*/

	//==================  56b  ======================================
	//
	std::deque<S56> cont56{ S56(7) , S56(11) , S56(3) , S56(9) , S56(31) };
	decltype(cont56)::iterator it56 = cont56.begin();	//CMD:p/u//	it56
	/*
					{_a = 4000000015, _e = 60014, _b = 107 }
	*/
	auto jt56 = std::next(it56, 3);						//CMD:p/u//	jt56
	/*
					{_a = 4000000019 ,_e = 60018, _b = 109 }
	*/
	dummy=true;									//CMD:q-elem//	cont56 1
	/*
					{_a = 4000000023 ,_e = 60022, _b = 111 'o' }
	*/

	//==================  64b  ======================================
	//
	std::deque<uint64_t> cont64({1111,5,99,133,22,129});
	decltype(cont64)::iterator it64 = cont64.begin();	//CMD:p//	it64
	/*
					1111
	*/
	auto jt64 = std::next(it64, 3);						//CMD:p//	jt64
	/*
					133
	*/
	dummy=true;									//CMD:q-elem//	cont64 2
	/*
					99
	*/

	//==================  72b  ======================================
	//
	std::deque<S72> cont72{ S72(3) , S72(5) , S72(9) , S72(7) };
	decltype(cont72)::iterator it72 = cont72.begin();	//CMD:p//	it72
	/*
					{_c = 10000000000000000006 ,_b = 103 'g' }
	*/
	auto jt72 = std::next(it72, 3);						//CMD:p//	jt72
	/*
					{_c = 10000000000000000014 ,_b = 107 'k' }
	*/
	dummy=true;									//CMD:q-elem//	cont72 1
	/*
					{_c = 10000000000000000010 ,_b = 105 'i' }
	*/

	//==================  96b  ======================================
	//
	std::deque<S96> cont96{ S96(3) , S96(5) , S96(9) , S96(7) };
	decltype(cont96)::iterator it96 = cont96.begin();	//CMD:p//	it96
	/*
					{_c = 10000000000000000006 ,_a = 4000000003 }
	*/
	auto jt96 = std::next(it96, 3);						//CMD:p//	jt96
	/*
					{_c = 10000000000000000014 ,_a = 4000000007 }
	*/
	dummy=true;									//CMD:q-elem//	cont96 1
	/*
					{_c = 10000000000000000010 ,_a = 4000000005 }
	*/

	//==================  136b  ======================================
	//
	std::deque<S136> cont136{ S136(3) , S136(5) , S136(9) , S136(7) };
	decltype(cont136)::iterator it136 = cont136.begin();	//CMD:p//	it136
	/*
		{_d = 10000000000000000006 ,_c = 4000000007 ,_b = 103 'g' }
	*/
	auto jt136 = std::next(it136, 3);						//CMD:p//	jt136
	/*
		{_d = 10000000000000000014 ,_c = 4000000015 ,_b = 107 'k' }
	*/
	dummy=true;										//CMD:q-elem//	cont136 1
	/*
		{_d = 10000000000000000010 ,_c = 4000000011 ,_b = 105 'i' }
	*/


	return 0;
}
