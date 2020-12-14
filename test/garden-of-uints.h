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
#ifndef GARDEN_OF_UINTs__H
#define GARDEN_OF_UINTs__H
#include <stdint.h>
/* For testing with elements of these sizes:
    //................    8b
    //................   16b
    //................   32b
    //................   40b
    //................   64b
    //................   72b
    //................   96b
    //................  136b
*/

// Here, want easy-to-recognize values to which can add a tiny addend (such
// that sum doesn't overflow) and get something with Lmost bit definitely set.
//
// Except for uint8_t, where we want value to be within ASCII isgraph()able
// set, so that tests easier to write; GDB prints will print a uint8_t's char
// value beside the numeric value, and helps if said char value easy to predict.
// 100='d' 103='g' 106='j' 109='m' 112='p' 115='s' 118='v' 121='y'
static const  uint8_t  U8FROM =  (uint8_t)100U;//0xF0;
static const uint16_t U16FROM = (uint16_t)60000U;//0xA5F0;
static const uint32_t U32FROM = (uint32_t)4000000000U;//0xA5FFA500;
static const uint64_t U64FROM = (uint64_t)10000000000000000000ULL;//0xDEADBEEFA5FFA500;

struct S24 {
	uint16_t  _e;
	uint8_t   _b;
	S24 (uint8_t b) : _b(U8FROM + b) ,
		_e(U16FROM + ((uint16_t)b << (uint16_t)1)) { }
};
//
bool operator< (const S24& x, const S24& y) {
	return (x._e < y._e)
	       ||
	       ((x._e == y._e) && (x._b < y._b));
}

struct S40 {
	uint32_t  _a;
	uint8_t   _b;
	S40 (uint8_t b) : _b(U8FROM + b) ,
		_a(U32FROM + ((uint32_t)b << (uint32_t)1)) { }
};
//
bool operator< (const S40& x, const S40& y) {
	return (x._a < y._a)
	       ||
	       ((x._a == y._a) && (x._b < y._b));
}

struct S56 {
	uint32_t  _a;
	uint16_t  _e;
	uint8_t   _b;
	S56 (uint8_t b) : _b(U8FROM + b) ,
		_a(U32FROM + ((uint32_t)b << (uint32_t)1) + 1U) ,
		_e(U16FROM + ((uint16_t)b << (uint16_t)1)) { }
};
//
bool operator< (const S56& x, const S56& y) {
	return (x._a < y._a)
	       ||
	       ((x._a == y._a) && (x._e < y._e))
	       ||
	       ((x._a == y._a) && (x._e == y._e) && (x._b < y._b));
}

struct S72 {
	uint64_t  _c;
	uint8_t   _b;
	S72 (uint8_t b) : _b(U8FROM + b) ,
		_c(U64FROM + ((uint64_t)b << (uint64_t)1)) { }
};
//
bool operator< (const S72& x, const S72& y) {
	return (x._c < y._c)
	       ||
	       ((x._c == y._c) && (x._b < y._b));
}

struct S96 {
	uint64_t  _c;
	uint32_t  _a;
	S96 (uint32_t a) : _a((uint32_t)U32FROM + a) ,
		_c(U64FROM + ((uint64_t)a << (uint64_t)1)) { }
};
//
bool operator< (const S96& x, const S96& y) {
	return (x._c < y._c)
	       ||
	       ((x._c == y._c) && (x._a < y._a));
}

struct S136 {
	uint64_t  _d;
	uint64_t  _c;
	uint8_t   _b;
	S136 (uint8_t b) : _b(U8FROM + b) ,
		_c((uint64_t)U32FROM + ((uint64_t)b << (uint64_t)1) + 1U) ,
		_d(U64FROM + ((uint64_t)b << (uint64_t)1)) { }
};
//
bool operator< (const S136& x, const S136& y) {
	return (x._d < y._d)
	       ||
	       ((x._d == y._d) && (x._c < y._c))
	       ||
	       ((x._d == y._d) && (x._c == y._c) && (x._b < y._b));
}

#endif

#if 0
struct S40 {
	uint32_t  _a;
	uint8_t   _b;
	S40 (uint8_t b) :     _b((uint8_t)U8FROM + b) ,
		_a((uint32_t)0xA5FFA500 & (uint32_t)b) { }
};

struct S72 {
	uint64_t  _c;
	uint8_t   _b;
	S72 (uint8_t b) :             _b((uint8_t)U8FROM + b) ,
		_c((uint64_t)0xA5A5A5A500FF5A00 & (uint64_t)b) { }
};

struct S96 {
	uint64_t  _c;
	uint32_t  _a;
	S96 (uint32_t a) :    _a((uint32_t)4000000000 + a) ,
		_c((uint64_t)0xA5A5A5A500FF5A00 & (uint64_t)a) { }
};

struct S136 {
	uint64_t  _d;
	uint64_t  _c;
	uint8_t   _b;
	S136 (uint8_t b) :            _b((uint8_t)U8FROM + b) ,
		_c((uint64_t)0xA5A5A5A500FF5A00 & (uint64_t)b) ,
		_d((uint64_t)0xFFA2A3A4A5A6A7FF ^ (uint64_t)b) { }
};

#endif
