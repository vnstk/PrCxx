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
#include <array>
#include <deque>
#include <list>
#include <map>
#include <set>
#include <queue> //For- std::priority_queue, std::queue
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "nondefault-STL-types-spec-helpers.h"

	//TODO:
		// More "explicitly default" examples.
		// With *addit* ways to declare a nondefault hasher: as obj, as functor, ...
		// Similarly, addit ways to decl nondefault comparator: floatGT, ...
		// Iterators, with IT_it IT_cit IT_rit IT_crit macreaux.
		// std::unique_ptr<Flarp,FlarpDeleter> and std::weak_ptr<Flarp,FlarpDeleter>

int main ( )
{	bool dummy;

	//_____________________________________________________________________________//
	//_____________________________________________________________________________//
	std::vector<float>                          vec_f__deAllo;
	std::vector<float, std::allocator<float>>   vec_f__deAllo_expli;
	std::vector<float, Mallo<float>>            vec_f__cuAllo;
	std::vector<std::wstring, Mallo<std::wstring>>   vec_ws__cuAllo;

	//_____________________________________________________________________________//
	std::string                                         str__deTrai__deAllo;
	std::basic_string<char, caseChTraits>               str__cuTrai__deAllo;
	std::basic_string<char, caseChTraits, Mallo<char>>  str__cuTrai__cuAllo;
#if wantCOMPILEerror
	std::basic_string<char, Mallo<char>>                str__deTrai__cuAllo;
#endif
	std::basic_string<char, std::char_traits<char>,
	                                      Mallo<char>>  str__deTrai_expli__cuAllo;

	//_____________________________________________________________________________//
	std::queue<float>                                    que__deCont__deAllo;
	std::queue<float, std::deque<float>>                 que__deCont_expli__deAllo;
	std::queue<float, std::deque<float, Mallo<float>>>   que__deCont__cuAllo;
	std::queue<float, std::vector<float>>                que__cuCont;
	std::queue<float, std::vector<float, Mallo<float>>>  que__cuCont__cuAllo;

	//_____________________________________________________________________________//
	std::set<float>                                     set__deCmp__deAllo;
	std::set<float, std::greater<float>>                set__cuCmp__deAllo;
	std::set<float, std::greater<float>, Mallo<float>>  set__cuCmp__cuAllo;
	std::set<float, std::less<float>, Mallo<float>>     set__deCmp_expli__cuAllo;
#if wantGDBconfused
	std::set<float, Mallo<float>>                       set__deCmp__cuAllo;
#endif

	std::set< std::basic_string<char,caseChTraits,Mallo<char>>
	         , std::greater<std::basic_string<char,caseChTraits>> >   a_problem_set;

	//_____________________________________________________________________________//
	std::map<float, double>                          map_f_d__deCmp__deAllo;
	std::map<float, double, std::less<float>>        map_f_d__deCmp_expli__deAllo;
	std::map<float, double, std::greater<float>>     map_f_d__cuCmp__deAllo;
	//
#if wantGDBconfused
	std::map<float, double,
	         Mallo<std::pair<const float&,double>>>  map_f_d__deCmp__cuAllo;
#endif
	//
	std::map<float, double, std::less<float>,
             Mallo<std::pair<const float&,double>>>  map_f_d__deCmp_expli__cuAllo;
	//
	std::map<float, double, std::greater<float>,
             Mallo<std::pair<const float&,double>>>  map_f_d__cuCmp__cuAllo;

	std::map<float, std::wstring>   map_f_ws__deCmp__deAllo;//TODO:as with map_f_d__...

	std::map<std::wstring, float>   map_ws_f__deCmp__deAllo;//TODO:also add variants, incl. say
	std::map<std::wstring, float, std::greater<std::wstring>>   map_ws_f__cuCmp__deAllo; //this?

	//_____________________________________________________________________________//
	std::unordered_set<float>                             uset__deHash__deEq__deAllo;
	std::unordered_set<float, floatHasher>                uset__cuHash__deEq__deAllo;
#if wantCOMPILEerror
	std::unordered_set<float, floatAppxEQ>                uset__deHash__cuEq__deAllo;
#endif
	std::unordered_set<float, std::hash<float>, floatAppxEQ>   uset__deHash_expli__cuEq__deAllo;
	std::unordered_set<float, floatHasher, floatAppxEQ>        uset__cuHash__cuEq__deAllo;
#if wantGDBconfused
	std::unordered_set<float, std::hash<float>, Mallo<float>>  uset__deHash_expli__deEq__cuAllo;
	std::unordered_set<float, floatHasher, Mallo<float>>       uset__cuHash__deEq__cuAllo;
#endif
	//
	std::unordered_set<float, std::hash<float>,
	                   floatAppxEQ, Mallo<float>>              uset__deHash_expli__cuEq__cuAllo;
	//
	std::unordered_set<float, floatHasher, floatAppxEQ,
                       Mallo<float>>                           uset__cuHash__cuEq__cuAllo;

	//_____________________________________________________________________________//
	std::unordered_map<float, double, floatHasher, floatAppxEQ>   umap_f_d__cuHash__cuEq__deAllo;

	std::unordered_map<float, std::wstring, floatHasher, floatAppxEQ>   umap_f_ws__cuHash__cuEq__deAllo;

	std::unordered_map<std::wstring, float, std::hash<std::wstring>>    umap_ws_f__deHash_expli__deEq__deAllo;

	std::unordered_map<std::wstring, float,
	    std::hash<std::wstring>, std::equal_to<std::wstring>,
	    Mallo<std::pair<const std::wstring&,float>>>            umumap_ws_f__deHash_expli__deEq_expli__cuAllo;

	//_____________________________________________________________________________//
	std::unordered_multimap<float, double,
	    floatHasher, floatAppxEQ>                umumap__cuHash__cuEq__deAllo;
	//
#if wantGDBconfused
	std::unordered_multimap<float, double,
	    std::hash<float>,
	    Mallo<std::pair<const float&,double>>>   umumap__deHash_expli__deEq__cuAllo;
#endif
	//
	std::unordered_multimap<float, double,
	    std::hash<float>, std::equal_to<float>,
	    Mallo<std::pair<const float&,double>>>   umumap__deHash_expli__deEq_expli__cuAllo;



//=============================================================================================
//#############################################################################################
//#############################################################################################
	dummy=true;						//CMD:set//			x-template-args full
	/*
	*/
//#############################################################################################

	dummy=true;		//CMD:q-whatis//		vec_f__deAllo
	/*
		type = std::vector<float, #ALLO#>
	*/

	dummy=true;		//CMD:q-whatis//		vec_f__deAllo_expli
	/*
		type = std::vector<float, #ALLO#>                 
	*/

	dummy=true;		//CMD:q-whatis//		vec_f__cuAllo
	/*
		type = std::vector<float, Mallo<#E#> >                       
	*/

	dummy=true;		//CMD:q-whatis//		vec_ws__cuAllo
	/*
		type = std::vector<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, Mallo<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#> >>                      
	*/

	dummy=true;		//CMD:q-whatis//		str__deTrai__deAllo
	/*
		type = std::basic_string<char, #TRAITS#, #ALLO#>                 
	*/

	dummy=true;		//CMD:q-whatis//		str__cuTrai__deAllo
	/*
		type = std::basic_string<char, caseChTraits, #ALLO#>                 
	*/

	dummy=true;		//CMD:q-whatis//		str__cuTrai__cuAllo
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >                 
	*/

	dummy=true;		//CMD:q-whatis//		str__deTrai_expli__cuAllo
	/*
		type = std::basic_string<char, #TRAITS#, Mallo<#CH#> >           
	*/

	dummy=true;		//CMD:q-whatis//		que__deCont__deAllo
	/*
		type = std::queue<float, #CONT#>                 
	*/

	dummy=true;		//CMD:q-whatis//		que__deCont_expli__deAllo
	/*
		type = std::queue<float, #CONT#>           
	*/

	dummy=true;		//CMD:q-whatis//		que__deCont__cuAllo
	/*
		type = std::queue<float, std::deque<#E#, Mallo<#E#> >>                 
	*/

	dummy=true;		//CMD:q-whatis//		que__cuCont
	/*
		type = std::queue<float, std::vector<#E#, std::allocator<#E#> >>                         
	*/

	dummy=true;		//CMD:q-whatis//		que__cuCont__cuAllo
	/*
		type = std::queue<float, std::vector<#E#, Mallo<#E#> >>                 
	*/

	dummy=true;		//CMD:q-whatis//		set__deCmp__deAllo
	/*
		type = std::set<float, #CMP#, #ALLO#>                  
	*/

	dummy=true;		//CMD:q-whatis//		set__cuCmp__deAllo
	/*
		type = std::set<float, std::greater<#E#>, #ALLO#>                  
	*/

	dummy=true;		//CMD:q-whatis//		set__cuCmp__cuAllo
	/*
		type = std::set<float, std::greater<#E#>, Mallo<#E#> >                  
	*/

	dummy=true;		//CMD:q-whatis//		set__deCmp_expli__cuAllo
	/*
		type = std::set<float, #CMP#, Mallo<#E#> >            
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__deCmp__deAllo
	/*
		type = std::map<float, double, #CMP#, #ALLO#>              
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__deCmp_expli__deAllo
	/*
		type = std::map<float, double, #CMP#, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__cuCmp__deAllo
	/*
		type = std::map<float, double, std::greater<#K#>, #ALLO#>              
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__deCmp_expli__cuAllo
	/*
		type = std::map<float, double, #CMP#, Mallo<std::pair<#K# const&, #V#> >>           
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__cuCmp__cuAllo
	/*
		type = std::map<float, double, std::greater<#K#>, Mallo<std::pair<#K# const&, #V#> >>              
	*/

	dummy=true;		//CMD:q-whatis//		map_f_ws__deCmp__deAllo
	/*
		type = std::map<float, std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, #CMP#, #ALLO#>             
	*/

	dummy=true;		//CMD:q-whatis//		map_ws_f__deCmp__deAllo
	/*
		type = std::map<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, float, #CMP#, #ALLO#>             
	*/

	dummy=true;		//CMD:q-whatis//		map_ws_f__cuCmp__deAllo
	/*
		type = std::map<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, float, std::greater<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#> >, #ALLO#>             
	*/

	dummy=true;		//CMD:q-whatis//		uset__deHash__deEq__deAllo
	/*
		type = std::unordered_set<float, #HASH#, #EQ#, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__cuHash__deEq__deAllo
	/*
		type = std::unordered_set<float, floatHasher, #EQ#, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__deHash_expli__cuEq__deAllo
	/*
		type = std::unordered_set<float, #HASH#, floatAppxEQ, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__cuHash__cuEq__deAllo
	/*
		type = std::unordered_set<float, floatHasher, floatAppxEQ, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__deHash_expli__cuEq__cuAllo
	/*
		type = std::unordered_set<float, #HASH#, floatAppxEQ, Mallo<#E#> >           
	*/

	dummy=true;		//CMD:q-whatis//		uset__cuHash__cuEq__cuAllo
	/*
		type = std::unordered_set<float, floatHasher, floatAppxEQ, Mallo<#E#> >           
	*/

	dummy=true;		//CMD:q-whatis//		umap_f_d__cuHash__cuEq__deAllo
	/*
		type = std::unordered_map<float, double, floatHasher, floatAppxEQ, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		umap_f_ws__cuHash__cuEq__deAllo
	/*
		type = std::unordered_map<float, std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, floatHasher, floatAppxEQ, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		umap_ws_f__deHash_expli__deEq__deAllo
	/*
		type = std::unordered_map<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, float, #HASH#, #EQ#, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		umumap_ws_f__deHash_expli__deEq_expli__cuAllo
	/*
		type = std::unordered_map<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#>, float, #HASH#, #EQ#, Mallo<std::pair<std::basic_string<wchar_t, #'TRAITS#, #'ALLO#> const&, #V#> >>           
	*/

	dummy=true;		//CMD:q-whatis//		umumap__cuHash__cuEq__deAllo
	/*
		type = std::unordered_multimap<float, double, floatHasher, floatAppxEQ, #ALLO#>           
	*/

	dummy=true;		//CMD:q-whatis//		umumap__deHash_expli__deEq_expli__cuAllo
	/*
		type = std::unordered_multimap<float, double, #HASH#, #EQ#, Mallo<std::pair<#K# const&, #V#> >>           
	*/




//=============================================================================================
//#############################################################################################
//#############################################################################################
	dummy=true;						//CMD:set//			x-template-args skipIfDefault
	/*
	*/
//#############################################################################################



	dummy=true;		//CMD:q-whatis//		vec_f__deAllo
	/*
		type = std::vector<float>                       
	*/

	dummy=true;		//CMD:q-whatis//		vec_f__deAllo_expli
	/*
		type = std::vector<float>                 
	*/

	dummy=true;		//CMD:q-whatis//		vec_f__cuAllo
	/*
		type = std::vector<float, Mallo<#E#> >                       
	*/

	dummy=true;		//CMD:q-whatis//		vec_ws__cuAllo
	/*
		type = std::vector<std::wstring, Mallo<#E#> >                      
	*/

	dummy=true;		//CMD:q-whatis//		str__deTrai__deAllo
	/*
		type = std::string
	*/

	dummy=true;		//CMD:q-whatis//		str__cuTrai__deAllo
	/*
		type = std::basic_string<char, caseChTraits>                 
	*/

	dummy=true;		//CMD:q-whatis//		str__cuTrai__cuAllo
	/*
		type = std::basic_string<char, caseChTraits, Mallo<#CH#> >                 
	*/

	dummy=true;		//CMD:q-whatis//		str__deTrai_expli__cuAllo
	/*
		type = std::basic_string<char, Mallo<#CH#> >           
	*/

	dummy=true;		//CMD:q-whatis//		que__deCont__deAllo
	/*
		type = std::queue<float>                 
	*/

	dummy=true;		//CMD:q-whatis//		que__deCont_expli__deAllo
	/*
		type = std::queue<float>           
	*/

	dummy=true;		//CMD:q-whatis//		que__deCont__cuAllo
	/*
		type = std::queue<float, std::deque<#E#, Mallo<#E#> >>                 
	*/

	dummy=true;		//CMD:q-whatis//		que__cuCont
	/*
		type = std::queue<float, std::vector<#E#, std::allocator<#E#> >>                         
	*/

	dummy=true;		//CMD:q-whatis//		que__cuCont__cuAllo
	/*
		type = std::queue<float, std::vector<#E#, Mallo<#E#> >>                 
	*/

	dummy=true;		//CMD:q-whatis//		set__deCmp__deAllo
	/*
		type = std::set<float>                  
	*/

	dummy=true;		//CMD:q-whatis//		set__cuCmp__deAllo
	/*
		type = std::set<float, std::greater<#E#> >                  
	*/

	dummy=true;		//CMD:q-whatis//		set__cuCmp__cuAllo
	/*
		type = std::set<float, std::greater<#E#>, Mallo<#E#> >                  
	*/

	dummy=true;		//CMD:q-whatis//		set__deCmp_expli__cuAllo
	/*
		type = std::set<float, Mallo<#E#> >            
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__deCmp__deAllo
	/*
		type = std::map<float, double>              
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__deCmp_expli__deAllo
	/*
		type = std::map<float, double>           
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__cuCmp__deAllo
	/*
		type = std::map<float, double, std::greater<#K#> >              
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__deCmp_expli__cuAllo
	/*
		type = std::map<float, double, Mallo<std::pair<#K# const&, #V#> >>           
	*/

	dummy=true;		//CMD:q-whatis//		map_f_d__cuCmp__cuAllo
	/*
		type = std::map<float, double, std::greater<#K#>, Mallo<std::pair<#K# const&, #V#> >>              
	*/

	dummy=true;		//CMD:q-whatis//		map_f_ws__deCmp__deAllo
	/*
		type = std::map<float, std::wstring>             
	*/

	dummy=true;		//CMD:q-whatis//		map_ws_f__deCmp__deAllo
	/*
		type = std::map<std::wstring, float>             
	*/

	dummy=true;		//CMD:q-whatis//		map_ws_f__cuCmp__deAllo
	/*
		type = std::map<std::wstring, float, std::greater<#K#> >             
	*/

	dummy=true;		//CMD:q-whatis//		uset__deHash__deEq__deAllo
	/*
		type = std::unordered_set<float>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__cuHash__deEq__deAllo
	/*
		type = std::unordered_set<float, floatHasher>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__deHash_expli__cuEq__deAllo
	/*
		type = std::unordered_set<float, floatAppxEQ>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__cuHash__cuEq__deAllo
	/*
		type = std::unordered_set<float, floatHasher, floatAppxEQ>           
	*/

	dummy=true;		//CMD:q-whatis//		uset__deHash_expli__cuEq__cuAllo
	/*
		type = std::unordered_set<float, floatAppxEQ, Mallo<#E#> >           
	*/

	dummy=true;		//CMD:q-whatis//		uset__cuHash__cuEq__cuAllo
	/*
		type = std::unordered_set<float, floatHasher, floatAppxEQ, Mallo<#E#> >           
	*/

	dummy=true;		//CMD:q-whatis//		umap_f_d__cuHash__cuEq__deAllo
	/*
		type = std::unordered_map<float, double, floatHasher, floatAppxEQ>           
	*/

	dummy=true;		//CMD:q-whatis//		umap_f_ws__cuHash__cuEq__deAllo
	/*
		type = std::unordered_map<float, std::wstring, floatHasher, floatAppxEQ>           
	*/

	dummy=true;		//CMD:q-whatis//		umap_ws_f__deHash_expli__deEq__deAllo
	/*
		type = std::unordered_map<std::wstring, float>           
	*/

	dummy=true;		//CMD:q-whatis//		umumap_ws_f__deHash_expli__deEq_expli__cuAllo
	/*
		type = std::unordered_map<std::wstring, float, Mallo<std::pair<#K# const&, #V#> >>           
	*/

	dummy=true;		//CMD:q-whatis//		umumap__cuHash__cuEq__deAllo
	/*
		type = std::unordered_multimap<float, double, floatHasher, floatAppxEQ>           
	*/

	dummy=true;		//CMD:q-whatis//		umumap__deHash_expli__deEq_expli__cuAllo
	/*
		type = std::unordered_multimap<float, double, Mallo<std::pair<#K# const&, #V#> >>           
	*/




//=============================================================================================
//____________________________________________________________________________________________
	return 0;
}
