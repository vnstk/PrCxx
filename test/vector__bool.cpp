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
#include <vector>

int main ( )
{	bool dummy;
	std::vector<bool> vb_a;				//CMD:p//		vb_a
	/*
					""
	*/
	dummy=true;					//CMD:q-count-elems//	vb_a
	/*
					0
	*/
	auto it_x = vb_a.begin();	//CMD:q-iter-into//		vb_a it_x
	/*
					outOfBounds
	*/
	vb_a.reserve(10U);			//CMD:q-has-elem//		vb_a 0
	/*
					false
	*/
	it_x = vb_a.begin();		//CMD:q-iter-into//		vb_a it_x
	/*
					withinBounds_but_invalid
	*/
	vb_a.push_back(true);
	it_x = vb_a.begin();		//CMD:q-iter-into//		vb_a it_x
	/*
					withinBounds_and_valid
	*/
	vb_a.push_back(true);				//CMD:p//		vb_a
	/*
					"11"
	*/
	auto it_y = vb_a.cend();	//CMD:q-iter-into//		vb_a it_y
	/*
					withinBounds_but_invalid
	*/
	vb_a.push_back(true);		//CMD:q-has-elem//		vb_a 0
	/*
					true
	*/
	dummy=true; 				//CMD:q-iter-into//		vb_a it_y
	/*
					withinBounds_and_valid
	*/
	dummy=true; 				//CMD:q-has-elem//		vb_a 3
	/*
					false
	*/
	std::vector<bool> vb_b{false,true,false,true, false,false,true,true,
	    false,false,false,true, false};	//CMD:p//		vb_b
	/*
					"0101001100010"
	*/
	dummy=true; 				//CMD:q-count-elems//	vb_b
	/*
					13
	*/
	auto it_z = vb_b.crend();			//CMD:p//		it_z
	/*
					false
	*/
	vb_b.flip();						//CMD:p//		it_z
	/*
					true
	*/
	dummy=true; 				//CMD:q-count-elems//	vb_b
	/*
					13
	*/
	dummy=true;					//CMD:q-iter-into//		vb_b it_z
	/*
					withinBounds_and_valid
	*/
	dummy=true;					//CMD:q-iter-into//		vb_a it_z
	/*
					outOfBounds
	*/
	dummy=true;					//CMD:q-iter-into//		vb_b it_y
	/*
					outOfBounds
	*/
	vb_b.clear();						//CMD:p//		vb_b
	/*
					""
	*/
	auto it_q = vb_b.cbegin();	//CMD:q-iter-into//		vb_b it_q
	/*
					withinBounds_but_invalid
	*/
	vb_b.shrink_to_fit();		//CMD:q-iter-into//		vb_b it_q
	/*
					outOfBounds
	*/
	dummy=true;							//CMD:p//		vb_b
	/*
					""
	*/
	vb_b.resize(9U);					//CMD:p//		vb_b
	/*
					"000000000"
	*/
	vb_b.flip();						//CMD:p//		vb_b
	/*
					"111111111"
	*/
	return 0;
}
