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
#ifndef nonSTL_TEMPLATED_TYPES_SAMPLER__H
#define nonSTL_TEMPLATED_TYPES_SAMPLER__H

#include "nondefault-STL-types-spec-helpers.h"


template<typename TTT, size_t NNN>
struct Ta {
	TTT                  * _a1;
	TTT                  * _a2[NNN];
	double                 _a3[NNN];
	std::list<TTT>             _a4;
	std::list<TTT,Mallo<TTT>>  _a5;
	std::array<float,NNN>  _a6;
	std::array<TTT,NNN>    _a7;
	std::array<TTT,7>      _a8;
	Ta<TTT,NNN>          * _next;
};

template<typename ELEM,
		 typename CONT = std::vector<ELEM>>
struct Tb {
	ELEM                           * _b1[0];
	typename CONT::value_type      * _b2[0];
	typename CONT::reverse_iterator  _b3;
	Ta<ELEM,11>                    * _b4;
	std::map<ELEM,CONT>              _b5;
	std::set<ELEM>                                   _b6;
	std::set<ELEM, std::greater<ELEM>>               _b7;
#if wantGDBconfused
	std::set<ELEM,                     Mallo<ELEM>>  _b8;
#endif
	std::set<ELEM, std::less<ELEM>,    Mallo<ELEM>>  _b8;
	std::set<ELEM, std::greater<ELEM>, Mallo<ELEM>>  _b9;
};


template<typename TONL>
struct Tc {
	static std::set<TONL, Mallo<TONL>>   c1;
	       std::set<TONL, Mallo<TONL>>  _c2;	
};


template<typename TFIR, typename TSEC, size_t NU>
struct Td {
	static std::map<TSEC ,
					TFIR ,
					Mallo<std::pair<const TFIR&,TSEC>>>  d1;
};

template<typename TFIR, typename TSEC, size_t NU>
struct Te {
	static Tc<TFIR>  e1;
	static Tc<TSEC>  e2;
	double          _e3[NU];
};



#endif //nonSTL_TEMPLATED_TYPES_SAMPLER__H
