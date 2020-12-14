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
#include <tuple>

struct Flarp {
	unsigned short _us;
};

int main ( )
{	bool dummy;
	Flarp aFlarp;
	Flarp *pFlarp_arr[] = {&aFlarp,};

	std::tuple<> t0 = std::make_tuple();
	std::tuple<short int> t1 = std::make_tuple(-6420);
	std::tuple<float,Flarp*> t2 = std::make_tuple(3.14F, &aFlarp);
	std::tuple<Flarp*,float> t2_flipped(&aFlarp, 3.14F);
	std::tuple<bool,Flarp*,const char *> t3(true, nullptr, "yyyy");
	std::tuple<float,Flarp*,const char *,float> t4(3.14F, &aFlarp, "xxxx",6.28F);
	auto t1_and_3 = std::tuple_cat(t1,t3);

	dummy=true;						//CMD:set//    print address off
	/*
	*/

	dummy=true;								//CMD:q-count-elems//	t0
	/*
					0
	*/
	dummy=true;								//CMD:q-has-elem//		t0 0
	/*
					false
	*/

	dummy=true;										//CMD:p//		t1
	/*
					{ -6420 }
	*/
	dummy=true;								//CMD:q-count-elems//	t1
	/*
					1
	*/
	dummy=true;								//CMD:q-has-elem//		t1 0
	/*
					true
	*/
	dummy=true;								//CMD:q-has-elem//		t1 1
	/*
					false
	*/

	dummy=true;									//CMD:q-elem//		t3 2
	/*
					"yyyy"
	*/

	return 0;
}
