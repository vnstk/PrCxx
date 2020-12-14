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
#include <set>
#include <cstring>

struct cstr_less { bool operator() (const char *const& a,
	const char *const & b) const { return strcmp(a,b) < 0; } };
struct cstr_greater { bool operator() (const char *const& a,
	const char *const & b) const { return strcmp(a,b) > 0; } };

int main ( )
{	bool dummy;

	std::set<const char *, cstr_less> xs;	//CMD:p//	xs
	/*
					
	*/
	auto ita = xs.cbegin();		//CMD:q-iter-into//		xs ita
	/*
					outOfBounds
	*/
	dummy=true;				//CMD:q-count-elems//		xs
	/*
					0
	*/
	xs.insert("cccc");		//CMD:q-count-elems//		xs
	/*
					1
	*/
	xs.insert("qqqq");
	xs.insert("bbbb");		//CMD:set//		print address off
	/*
	*/
	auto itb = xs.begin();				//CMD:p//		xs
	/*
					{"bbbb" , "cccc" , "qqqq"}
	*/
	xs.insert("aaaa");			//CMD:q-has-elem//		xs "aaa"
	/*
					false
	*/
	xs.insert("aaaa");			//CMD:q-count-elems//	xs
	/*
					4
	*/
	xs.insert("yyyy"); 			//CMD:q-has-elem//		xs bbbb
	/*
					true
	*/
	auto itc = xs.cend();		//CMD:q-iter-into//		xs itb
	/*
					withinBounds_and_valid
	*/
	itb = xs.begin();
	xs.erase(itb);				//CMD:q-iter-into//		xs itc
	/*
					outOfBounds
	*/
	xs.erase("bbbb");					//CMD:p//		xs
	/*
					{"cccc" , "qqqq" , "yyyy"}
	*/
	auto itd = xs.find("bbbb");	//CMD:q-iter-into//		xs itd
	/*
					outOfBounds
	*/
	auto ite = xs.find("qqqq");	//CMD:q-iter-into//		xs ite
	/*
					withinBounds_and_valid
	*/
	dummy=true;							//CMD:p//		ite
	/*
					"qqqq"
	*/
	++ite;								//CMD:p//		ite
	/*
					"yyyy"
	*/
	ite = xs.find("qqqq");
	--ite;								//CMD:p//		ite
	/*
					"cccc"
	*/

	std::set<const char *, cstr_greater> ys{"ggg","zzz",
	    "aaa","ggg","eee","eee"};		//CMD:p//		ys
	/*
					{"zzz" , "ggg" , "eee" , "aaa"}
	*/

	//========================================================//
	std::multiset<const char *, cstr_greater> zs{"ggg","zzz",
	    "aaa","ggg","eee","eee"};		//CMD:p//		zs
	/*
					{"zzz" , "ggg","ggg" , "eee","eee" , "aaa"}
	*/


	return 0;
}
