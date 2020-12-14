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

#include "nonSTL-templated-types-sampler.h"

	//TODO:
		// More "explicitly default" examples.
		// With *addit* ways to declare a nondefault hasher: as obj, as functor, ...
		// Similarly, addit ways to decl nondefault comparator: floatGT, ...
		// Iterators, with IT_it IT_cit IT_rit IT_crit macreaux.
		// std::unique_ptr<Flarp,FlarpDeleter> and std::weak_ptr<Flarp,FlarpDeleter>

int main ( )
{	bool dummy;

	Ta<std::wstring, 5>                    aq;
	Ta<long, 9>                            ax;
	Ta<std::vector<long>, 9>               ay;
	Ta<std::vector<long,Mallo<long>>, 9>   az;

	Tb<std::wstring>                         bq;
	Tb<long>                                 bx;
	Tb<long, std::vector<long>>              by;
	Tb<long, std::vector<long,Mallo<long>>>  bz;

	Tc<float>    cx;

	Td<float,double,5>  dx;

	Te<double,long,11>  ex;


	dummy=true;		//CMDSEQ//	set x-heur-abbr on @@@ set x-layout omit @@@ set x-nested-datamemb full @@@ set x-template-args full @@@ set x-relations off
	/*
	*/


//____________________________________________________________________________________________
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a1
	/*
					#0#			*				_a1 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a2
	/*
					#0#			*				_a2 [9] ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a3
	/*
					double					_a3 [9] ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a4
	/*
		std::list<#0#, #ALLO#>				_a4 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a5
	/*
		std::list<#0#, Mallo<#E#> >			_a5 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a6
	/*
				std::array<float, 9>		_a6 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a7
	/*
				std::array<#0#, 9>			_a7 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a8
	/*
				std::array<#0#, 7>			_a8 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_next
	/*
					@TOPLEV@	*			_next ;
	*/

//____________________________________________________________________________________________
	dummy=true;	//GREP1:p-vtype//	bx	,,,	_b1
	/*
					#0#			*			_b1 [0] ;
	*/
	///TODO/// _b3
	dummy=true;	//GREP1:p-vtype//	bx	,,,	_b4
	/*
				Ta<#0#, 11>		*			_b4 ;
	*/
	///TODO/// _b5
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b6
	/*
		std::set<#0#, #CMP#, #ALLO#>					_b6 ;
	*/
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b7
	/*
         std::set<#0#, std::greater<#E#>, #ALLO#>		_b7 ;
	*/
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b8
	/*
		std::set<#0#, #CMP#, Mallo<#E#>>				_b8 ;
	*/
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b9
	/*
		std::set<#0#, std::greater<#E#>, Mallo<#E#> >	_b9 ;
	*/



//=============================================================================================
//#############################################################################################
	dummy=true;						//CMD:set//			x-template-args skipIfDefault
	/*
	*/
//#############################################################################################

//____________________________________________________________________________________________
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a4
	/*
		std::list<#0#>						_a4 ;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_a5
	/*
		std::list<#0#, Mallo<#E#> >			_a5 ;
	*/

//____________________________________________________________________________________________
	///TODO/// _b3
	dummy=true;	//GREP1:p-vtype//	bx	,,,	_b4
	/*
				Ta<#0#, 11>		*			_b4 ;
	*/
	///TODO/// _b5
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b6
	/*
		std::set<#0#>									_b6 ;
	*/
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b7
	/*
         std::set<#0#, std::greater<#E#>>				_b7 ;
	*/
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b8
	/*
		std::set<#0#, Mallo<#E#>>						_b8 ;
	*/
	dummy=true;	//GREP1:p-vtype//				bx	,,,	_b9
	/*
		std::set<#0#, std::greater<#E#>, Mallo<#E#> >	_b9 ;
	*/


//=============================================================================================
	return 0;
}
