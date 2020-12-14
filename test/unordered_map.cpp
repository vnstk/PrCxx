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
#include <unordered_map>
#include <cstring>

int main ( )
{	bool dummy;

	std::unordered_map<const char *,int>
	    xm;									//CMD:p//	xm
	/*
					
	*/
	auto it = xm.cbegin();		//CMD:q-iter-into//		xm it
	/*
					outOfBounds
	*/
	dummy=true;					//CMD:q-count-elems//	xm
	/*
					0
	*/
	dummy=true;					//CMD:q-has-elem//		xm cccc
	/*
					false
	*/
	const bool didInsA = xm.insert({"cccc",-42}
	    ).second;				//CMD:q-count-elems//	xm
	/*
					1
	*/
	dummy=true;							//CMD:p//		didInsA
	/*
					true
	*/
	xm.insert({"qqqq",3337});
	it = xm.cbegin();			//CMD:q-iter-into//		xm it
	/*
					withinBounds_and_valid
	*/
	xm.insert({"bbbb",91});		//CMD:set//		print address off
	/*
	*/
	const bool didInsB =
	    xm.insert({"cccc",-43}).second;		//CMD:p//	didInsB
	/*
					false
	*/
	dummy=true;						//CMD:q-elem//		xm cccc
	/*
					-42
	*/
	//NB: does **not** update!
	dummy=true;					//CMD:q-count-elems//	xm
	/*
					3
	*/
	xm.insert({"aaaa",538});	//CMD:q-has-elem//		xm aaa
	/*
					false
	*/
	dummy=true;					//CMD:q-has-elem//		xm aaaa
	/*
					true
	*/
	dummy=true;					//CMD:q-count-elems//	xm
	/*
					4
	*/
	auto jt = xm.insert({"dddd",9331
	    }).first;							//CMD:p//	jt
	/*
					{"dddd",9331}
	*/
	std::unordered_map<const char *,int> const& cref_xm = xm;
	auto jjt = cref_xm.find("dddd");
	(void) xm.erase(jjt);		//CMD:q-has-elem//		xm dddd
	/*
					false
	*/
	auto kt = xm.find("dddd");	//CMD:q-iter-into//		xm kt
	/*
					outOfBounds
	*/
	xm.insert({{"AAAA",8011} , {"ffff",8022} , {"BBBB",8033} ,
	  {"tttt",8044} , {"ffff",8055} , {"ZZZZ",8066} ,
	  {"BBBB",8077} , {"dddd",8088} , {"eeee",8099}
	  });							//CMD:q-has-elem//	xm dddd
	/*
					true
	*/
	kt = xm.find("dddd");	//CMD:q-iter-into//			xm kt
	/*
					withinBounds_and_valid
	*/
	dummy=true;					//CMD:q-count-elems//	xm
	/*
					11
	*/
	xm.insert({{"AAAA",8011} , {"ffff",8022} , {"BBBB",8033} ,
	  {"tttt",8044} , {"ffff",8055} , {"ZZZZ",8066} ,
	  {"BBBB",8077} , {"dddd",8088} , {"eeee",8099}
	  });						//CMD:q-count-elems//	xm
	/*
					11
	*/

	//========================================================//
	std::unordered_multimap<const char *,int>
	    ym;						//CMD:q-count-elems//	ym
	/*
					0
	*/
	ym.insert({{"AAAA",8011} , {"ffff",8022} , {"BBBB",8033} ,
	  {"tttt",8044} , {"ffff",8055} , {"ZZZZ",8066} ,
	  {"BBBB",8077} , {"dddd",8088} , {"eeee",8099}
	  });						//CMD:q-count-elems//	ym
	/*
					9
	*/
	ym.insert({{"AAAA",8011} , {"ffff",8022} , {"BBBB",8033} ,
	  {"tttt",8044} , {"ffff",8055} , {"ZZZZ",8066} ,
	  {"BBBB",8077} , {"dddd",8088} , {"eeee",8099}
	  });						//CMD:q-count-elems//	ym
	/*
					18
	*/
	ym.clear();					//CMD:q-count-elems//	ym
	/*
					0
	*/

	return 0;
}
