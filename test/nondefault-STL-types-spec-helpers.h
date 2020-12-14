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
#ifndef NONDEFAULT_STL_TYPES_SPEC_HELPERS__H
#define NONDEFAULT_STL_TYPES_SPEC_HELPERS__H

#include <cctype> //For- std::tolower()
#include <cmath> //For- std::fabs()
#include <cstdint> //For- uint32_t, size_t
#include <cstdlib> //For- std::malloc()
#include <functional> //For- struct hash
#include <new> //For- std::bad_alloc


union BitwiseConverter__float_X_uint32 {
	float     _f;
	uint32_t  _u;
};


/*
**_________________________________________________________________
**  custom allocators
**#################################################################
*/

// Adapted from https://en.cppreference.com/w/cpp/named_req/Allocator
template <class T>
struct Mallo {
	typedef T value_type;
	Mallo() = default;
	template <class U> constexpr Mallo (const Mallo<U>&) noexcept {}
	[[nodiscard]] T* allocate (const std::size_t n) {
		if(n > std::size_t(-1) / sizeof(T)) throw std::bad_alloc();
		if(auto p = static_cast<T*>(std::malloc(n*sizeof(T)))) return p;
		throw std::bad_alloc();
	}
	void deallocate (T* p, const std::size_t) noexcept { std::free(p); }
};
template <class T, class U>
bool operator==(const Mallo<T>&, const Mallo<U>&) { return true; }
template <class T, class U>
bool operator!=(const Mallo<T>&, const Mallo<U>&) { return false; }


/*
**_________________________________________________________________
**  custom comparators
**#################################################################
*/

struct floatGT {
	bool operator() (const float& a, const float& b) const {
		BitwiseConverter__float_X_uint32 xa; xa._f = a;
		BitwiseConverter__float_X_uint32 xb; xb._f = b;
		return (~ xa._u) > (~ xb._u); 
	}
};

template<typename T> //A stunningly dumb idea, because not idempotent!
struct anyLT {
	bool operator() (const T& a, const T& b) const {
		return (uintptr_t)(T const*)(a) < (uintptr_t)(T const*)(b);
	}
};

struct floatAppxEQ {
	bool operator() (const float& a, const float& b) const {
		return fabs(a - b) < 0.000001F;
	}
};


/*
**_________________________________________________________________
**  custom hashers
**#################################################################
*/

struct floatHasher {
    std::size_t operator() (float const& f) const noexcept {
		BitwiseConverter__float_X_uint32 x; x._f = f;
		return (size_t) x._u;
	}
};

template<typename T>
struct anyHasher {
    std::size_t operator() (T const& t) const noexcept {
		return (size_t)(uintptr_t)(T const*)(t);
	}
};


/*
**_________________________________________________________________
**  custom char traits
**#################################################################
*/

//Adapted from https://en.cppreference.com/w/cpp/string/char_traits
struct caseChTraits : public std::char_traits<char> {
	static char smash (char c) {
		return std::tolower((unsigned char) c);
	}
	static bool eq (char c1, char c2) {
		return smash(c1) == smash(c2);
	}
	static bool lt (char c1, char c2) {
		return smash(c1) <  smash(c2);
	}
	static int compare(const char* s1, const char* s2, std::size_t n) {
		while ( n-- != 0 ) {
			if ( smash(*s1) < smash(*s2) ) return -1;
			if ( smash(*s1) > smash(*s2) ) return 1;
			++s1; ++s2;    }
		return 0;
	}
	static const char* find(const char* s, std::size_t n, char a) {
		const char c = smash(a);
		while ( n-- != 0 ) {
			if (smash(*s) == c) return s;
			++s;           }
		return nullptr;
	}
};



// "IT_cit(bunnies)" defines "bunnies_cit", etc.
#define IT_it(nam)   decltype(nam)::iterator nam ## _it
#define IT_cit(nam)  decltype(nam)::const_iterator nam ## _cit
#define IT_rit(nam)  decltype(nam)::reverse_iterator nam ## _rit
#define IT_crit(nam) decltype(nam)::const_reverse_iterator nam ## _crit


#endif // NONDEFAULT_STL_TYPES_SPEC_HELPERS__H
