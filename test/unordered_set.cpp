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
#include <unordered_set>
#include <cstring>

int main ( )
{	bool dummy;

	std::unordered_set<const char *> xs;	//CMD:p//	xs
	/*
					
	*/
	auto it = xs.cbegin();		//CMD:q-iter-into//		xs it
	/*
					outOfBounds
	*/
	dummy=true;					//CMD:q-count-elems//	xs
	/*
					0
	*/
	const bool didInsA =
	   xs.insert("cccc").second;//CMD:q-count-elems//	xs
	/*
					1
	*/
	dummy=true;							//CMD:p//		didInsA
	/*
					true
	*/
	xs.insert("qqqq");
	it = xs.cbegin();			//CMD:q-iter-into//		xs it
	/*
					withinBounds_and_valid
	*/
	xs.insert("bbbb");		//CMD:set//		print address off
	/*
	*/
	const bool didInsB =
	    xs.insert("cccc").second;		//CMD:p//		didInsB
	/*
					false
	*/
	dummy=true;					//CMD:q-count-elems//	xs
	/*
					3
	*/
	xs.insert("aaaa");			//CMD:q-has-elem//		xs aaa
	/*
					false
	*/
	dummy=true;					//CMD:q-has-elem//		xs aaaa
	/*
					true
	*/
	dummy=true;					//CMD:q-count-elems//	xs
	/*
					4
	*/
	auto jt = xs.insert("dddd").first;		//CMD:p//	jt
	/*
					"dddd"
	*/
	std::unordered_set<const char *> const& cref_xs = xs;
	auto jjt = cref_xs.find("dddd");
	(void) xs.erase(jjt);		//CMD:q-has-elem//		xs dddd
	/*
					false
	*/
	auto kt = xs.find("dddd");	//CMD:q-iter-into//		xs kt
	/*
					outOfBounds
	*/
	xs.insert({"AAAA", "ffff", "BBBB", "tttt", "ffff", "ZZZZ",
	  "BBBB", "dddd", "eeee"});	//CMD:q-has-elem//		xs dddd
	/*
					true
	*/
	kt = xs.find("dddd");	//CMD:q-iter-into//			xs kt
	/*
					withinBounds_and_valid
	*/
	dummy=true;					//CMD:q-count-elems//	xs
	/*
					11
	*/
	xs.insert({"AAAA", "ffff", "BBBB", "tttt", "ffff", "ZZZZ",
	  "BBBB", "dddd", "eeee"});	//CMD:q-count-elems//	xs
	/*
					11
	*/

	//========================================================//
	std::unordered_multiset<const char *>
	    ys;						//CMD:q-count-elems//	ys
	/*
					0
	*/
	ys.insert({"AAAA", "ffff", "BBBB", "tttt", "ffff", "ZZZZ",
	  "BBBB", "dddd", "eeee"});	//CMD:q-count-elems//	ys
	/*
					9
	*/
	ys.insert({"AAAA", "ffff", "BBBB", "tttt", "ffff", "ZZZZ",
	  "BBBB", "dddd", "eeee"});	//CMD:q-count-elems//	ys
	/*
					18
	*/
	ys.clear();					//CMD:q-count-elems//	ys
	/*
					0
	*/


	/* ========================================================
	   Make sure q-elem and q-has-elem succeed with elements
	   _not_ at head of a bucket's chained list, too.
	   ========================================================
	*/
	std::unordered_set<const char *> zs(
		{"ccc", "qqq", "bbb", "ddd", "fff", "ttt", "eee"}
	);

	dummy=true;					//CMD:q-count-elems//	zs
	/*
					7
	*/
//
	dummy=true;					//CMD:q-has-elem//		zs  "noneSuch"
	/*
					false
	*/
	dummy=true;					//CMD:q-elem//			zs  "ccc"
	/*
					"ccc"
	*/
//
	dummy=true;					//CMD:q-has-elem//		zs  "ccc"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "qqq"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "bbb"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "ddd"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "fff"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "ttt"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "eee"
	/*
					true
	*/

	zs.max_load_factor(/*# elems per bucket*/ 5.0);
	zs.rehash(/*bucket count*/ 2U);

	dummy=true;					//CMD:q-count-elems//	zs
	/*
					7
	*/
//
	dummy=true;					//CMD:q-has-elem//		zs  "noneSuch"
	/*
					false
	*/
	dummy=true;					//CMD:q-elem//			zs  "ccc"
	/*
					"ccc"
	*/
//
	dummy=true;					//CMD:q-has-elem//		zs  "ccc"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "qqq"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "bbb"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "ddd"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "fff"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "ttt"
	/*
					true
	*/
	dummy=true;					//CMD:q-has-elem//		zs  "eee"
	/*
					true
	*/


	return 0;
}
