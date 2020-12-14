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
#include <map>
#include <cstring>

struct cstr_less { bool operator() (const char *const& a,
	const char *const & b) const { return strcmp(a,b) < 0; } };
struct cstr_greater { bool operator() (const char *const& a,
	const char *const & b) const { return strcmp(a,b) > 0; } };

int main ( )
{	bool dummy;

	std::map<const char*, int, cstr_less> xm;	//CMD:p//	xm
	/*
					
	*/
	auto it = xm.cbegin();			//CMD:q-iter-into//		xm it
	/*
					outOfBounds
	*/
	xm["qqq"] = -789;			//CMD:set//		print address off
	/*
	*/
	xm["jjj"] = -234;							//CMD:p//	xm
	/*
					{	["jjj"] = -234 , ["qqq"] = -789 }
	*/
	xm["qqq"] = -6583;				//CMD:q-count-elems//	xm
	/*
					2
	*/
	dummy=true;									//CMD:p//	xm
	/*
					{	["jjj"] = -234 , ["qqq"] = -6583 }
	*/
	it = xm.cbegin();							//CMD:p//	it
	/*
					{"jjj",-234}
	*/
	auto jt = xm.find("aaa");		//CMD:q-iter-into//		xm jt
	/*
					outOfBounds
	*/
	xm["aaa"] = 1001;				//CMD:q-has-elem//		xm "bbb"
	/*
					false
	*/
	jt = xm.find("aaa");			//CMD:q-iter-into//		xm jt
	/*
					withinBounds_and_valid
	*/
	dummy=true;									//CMD:p//	jt
	/*
					{"aaa",1001}
	*/
	xm.insert(std::make_pair("ccc", 917));
	it = xm.cbegin();							//CMD:p//	it
	/*
					{"aaa",1001}
	*/
	auto kt = xm.erase(it);						//CMD:p//	kt
	/*
					{"ccc",917}
	*/

	std::map<const char*, int, cstr_greater> ym( { {"rr",34} ,
	    {"ee",5} , {"hh",42} , {"ff",29} , {"ee",-5} } );
	auto iit = ym.begin();			//CMD:q-count-elems//	ym
	/*
					4
	*/
	auto jjt = ym.insert(ym.cend(),
	                     {"ccc",917});			//CMD:p//	jjt
	/*
					{"ccc",917}
	*/
	dummy=true;						//CMD:q-iter-into//		ym jjt
	/*
					withinBounds_and_valid
	*/
	dummy=true;						//CMD:q-iter-into//		xm jjt
	/*
					outOfBounds
	*/
	dummy=true;						//CMD:q-iter-into//		ym kt
	/*
					outOfBounds
	*/
	dummy=true;						//CMD:q-iter-into//		xm kt
	/*
					withinBounds_and_valid
	*/

	//========================================================//
	std::multimap<const char*, int, cstr_greater> zm( { {"rr",34} ,
	    {"ee",5} , {"hh",42} , {"ff",29} , {"ee",-5} } );
	auto kkt = zm.crend();			//CMD:q-count-elems//	zm
	/*
					5
	*/
	dummy=true;									//CMD:p//	kkt
	/*
					{"rr",34}
	*/

	return 0;
}
