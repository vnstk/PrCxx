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

int main ( )
{	bool dummy;
	std::array<int,0> ai_x; 					//CMD:p//	ai_x
	/*
					
	*/
	auto ai_x_it = ai_x.begin();	//CMD:q-count-elems//	ai_x
	/*
					0
	*/
	dummy=true;						//CMD:q-iter-into//		ai_x ai_x_it
	/*
					outOfBounds
	*/
	std::array<int,5> ai_y;
	auto ai_y_it = ai_y.cbegin();	//CMD:q-iter-into//		ai_y ai_y_it
	/*
					withinBounds_and_valid
	*/
	ai_y.fill(33);
	int ai_y_it_tmp = *ai_y_it;					//CMD:p//	ai_y_it_tmp
	/*
					33
	*/
	ai_y_it =std::next(ai_y_it, 5);	//CMD:q-iter-into//		ai_y ai_y_it
	/*
					outOfBounds
	*/
	std::array<int,5> ai_z{44,22,66,88,99};		//CMD:p//	ai_z
	/*
					{44,22,66,88,99}
	*/
	auto ai_z_rit = ai_z.crend();				//CMD:p//	ai_z_rit
	/*
					44
	*/
	ai_y.fill(33);								//CMD:p//	ai_z_rit
	/*
					44
	*/
	dummy=true;						//CMD:q-count-elems//	ai_z
	/*
					5
	*/
	return 0;
}
