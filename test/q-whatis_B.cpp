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
#include "container-types-sampler.h"



int main ( )
{	bool dummy;
	TypesSampler x;

	dummy=true;		//CMD:set//		x-template-args		skipIfDefault
	/*
	*/


	//________________________________________________________
	// "a" |||    std::initializer_list<T>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.a0
	/*
		type = std::initializer_list<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.a0_it
	/*
		type = std::initializer_list<float>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.a0_cit
	/*
		type = std::initializer_list<float>::const_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.a1
	/*
		type = std::initializer_list<std::wstring>
	*/

	dummy=true;	//CMD:q-whatis//	x.a1_it
	/*
		type = std::initializer_list<std::wstring>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.a1_cit
	/*
		type = std::initializer_list<std::wstring>::const_iterator
	*/
//---------------------------------------------------------------------


	//________________________________________________________
	// "b" |||    std::array<T,N>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.b0
	/*
		type = std::array<float, 5>
	*/

	dummy=true;	//CMD:q-whatis//	x.b0_it
	/*
		type = std::array<float, 5>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.b0_cit
	/*
		type = std::array<float, 5>::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.b0_rit
	/*
		type = std::array<float, 5>::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.b0_crit
	/*
		type = std::array<float, 5>::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.b1
	/*
		type = std::array<std::wstring, 0>
	*/

	dummy=true;	//CMD:q-whatis//	x.b1_it
	/*
		type = std::array<std::wstring, 0>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.b1_cit
	/*
		type = std::array<std::wstring, 0>::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.b1_rit
	/*
		type = std::array<std::wstring, 0>::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.b1_crit
	/*
		type = std::array<std::wstring, 0>::const_reverse_iterator
	*/
//---------------------------------------------------------------------


	//________________________________________________________
	// "c" |||    std::vector<T,ALLO>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.c0
	/*
		type = std::vector<float>
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.c1
	/*
		type = std::vector<std::string>
	*/

	dummy=true;	//CMD:q-whatis//	x.c1_it
	/*
		type = std::vector<std::string>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.c1_cit
	/*
		type = std::vector<std::string>::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.c1_rit
	/*
		type = std::vector<std::string>::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.c1_crit
	/*
		type = std::vector<std::string>::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.c2
	/*
		type = std::vector<float, Mallo<#E#> >
	*/

	dummy=true;	//CMD:q-whatis//	x.c2_crit
	/*
		type = std::vector<float, Mallo<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.c3
	/*
		type = std::vector<std::string, Mallo<#E#> >
	*/

	dummy=true;	//CMD:q-whatis//	x.c3_crit
	/*
		type = std::vector<std::string, Mallo<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------



	//________________________________________________________
	// "e" |||    std::basic_string<ChT,ChTraits,ALLO>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.e0
	/*
		type = std::wstring
	*/

	dummy=true;	//CMD:q-whatis//	x.e0_it
	/*
		type = std::wstring::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e0_cit
	/*
		type = std::wstring::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e0_rit
	/*
		type = std::wstring::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e0_crit
	/*
		type = std::wstring::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.e1
	/*
		type = std::basic_string<char, caseChTraits>
	*/

	dummy=true;	//CMD:q-whatis//	x.e1_it
	/*
		type = std::basic_string<char, caseChTraits>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e1_crit
	/*
		type = std::basic_string<char, caseChTraits>::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.e6
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >
	*/

	dummy=true;	//CMD:q-whatis//	x.e6_it
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e6_cit
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e6_rit
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.e6_crit
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------



	//________________________________________________________
	// "h" |||    std::list<T,ALLO>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.h0_it
	/*
		type = std::list<float>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h0_cit
	/*
		type = std::list<float>::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h0_rit
	/*
		type = std::list<float>::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h0_crit
	/*
		type = std::list<float>::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.h1_it
	/*
		type = std::list<std::string>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h1_cit
	/*
		type = std::list<std::string>::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h1_rit
	/*
		type = std::list<std::string>::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h1_crit
	/*
		type = std::list<std::string>::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.h2_crit
	/*
		type = std::list<float, Mallo<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.h3_it
	/*
		type = std::list<std::string, Mallo<#E#> >::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h3_cit
	/*
		type = std::list<std::string, Mallo<#E#> >::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h3_rit
	/*
		type = std::list<std::string, Mallo<#E#> >::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.h3_crit
	/*
		type = std::list<std::string, Mallo<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------



	//________________________________________________________
	// "j" |||    std::deque<T,ALLO>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.j0
	/*
		type = std::deque<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.j0_it
	/*
		type = std::deque<float>::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.j0_cit
	/*
		type = std::deque<float>::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.j0_rit
	/*
		type = std::deque<float>::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.j0_crit
	/*
		type = std::deque<float>::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.j1
	/*
		type = std::deque<std::string>
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.j2
	/*
		type = std::deque<float, Mallo<#E#> >
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.j3
	/*
		type = std::deque<std::string, Mallo<#E#> >
	*/
// And if x-template-args == full, then
//		type = std::deque<std::basic_string<char, #'TRAITS#, #'ALLO#>, Mallo<std::basic_string<char, #'TRAITS#, #'ALLO#> >>

	dummy=true;	//CMD:q-whatis//	x.j3_it
	/*
		type = std::deque<std::string, Mallo<#E#> >::iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.j3_cit
	/*
		type = std::deque<std::string, Mallo<#E#> >::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.j3_rit
	/*
		type = std::deque<std::string, Mallo<#E#> >::reverse_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.j3_crit
	/*
		type = std::deque<std::string, Mallo<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------


	//________________________________________________________
	// "k" |||    std::priority_queue<T,CONT=vector<T>,CMP>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.k0
	/*
		type = std::priority_queue<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.k1
	/*
		type = std::priority_queue<float, std::deque<#E#, std::allocator<#E#> >>
	*/

	dummy=true;	//CMD:q-whatis//	x.k2
	/*
		type = std::priority_queue<float, floatGT>
	*/

	dummy=true;	//CMD:q-whatis//	x.k3
	/*
		type = std::priority_queue<float, std::deque<#E#, std::allocator<#E#> >, floatGT>
	*/

	dummy=true;	//CMD:q-whatis//	x.k4
	/*
		type = std::priority_queue<std::string>
	*/


	//________________________________________________________
	// "m" |||    std::queue<T,CONT=deque<T>>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.m0
	/*
		type = std::queue<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.m1
	/*
		type = std::queue<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.m2
	/*
		type = std::queue<float, std::vector<#E#, std::allocator<#E#> >>
	*/

	dummy=true;	//CMD:q-whatis//	x.m3
	/*
		type = std::queue<std::wstring>
	*/

	dummy=true;	//CMD:q-whatis//	x.m4
	/*
		type = std::queue<std::wstring>
	*/

	dummy=true;	//CMD:q-whatis//	x.m5
	/*
		type = std::queue<std::wstring, std::vector<#E#, std::allocator<#E#> >>
	*/


	//________________________________________________________
	// "n" |||    std::stack<T,CONT=deque<T>>
	//========================================================
	dummy=true;	//CMD:q-whatis//	x.n0
	/*
		type = std::stack<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.n1
	/*
		type = std::stack<float>
	*/

	dummy=true;	//CMD:q-whatis//	x.n2
	/*
		type = std::stack<float, std::vector<#E#, std::allocator<#E#> >>
	*/

	dummy=true;	//CMD:q-whatis//	x.n3
	/*
		type = std::stack<std::wstring>
	*/

	dummy=true;	//CMD:q-whatis//	x.n4
	/*
		type = std::stack<std::wstring>
	*/

	dummy=true;	//CMD:q-whatis//	x.n5
	/*
		type = std::stack<std::wstring, std::vector<#E#, std::allocator<#E#> >>
	*/


	//________________________________________________________
	// "o" |||    std::set<KeyT,CMP,ALLO>
	//========================================================

	dummy=true;	//CMD:q-whatis//	x.o4_cit
	/*
		type = std::set<std::wstring>::const_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.o5_cit
	/*
		type = std::set<std::string, std::greater<#E#> >::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.o5_crit
	/*
		type = std::set<std::string, std::greater<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------
	dummy=true;	//CMD:q-whatis//	x.o6_cit
	/*
		type = std::set<std::string, std::greater<#E#>, Mallo<#E#> >::const_iterator
	*/

	dummy=true;	//CMD:q-whatis//	x.o6_crit
	/*
		type = std::set<std::string, std::greater<#E#>, Mallo<#E#> >::const_reverse_iterator
	*/
//---------------------------------------------------------------------


	return 0;
}
