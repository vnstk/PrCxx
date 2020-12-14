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
#include <string>

int main ( )
{	bool dummy;
	std::vector<int> vi;			//CMD:p//	vi
	/*
				
	*/
	dummy=true;			//CMD:q-count-elems//	vi
	/*
				0
	*/
	vi.push_back(11);				//CMD:p//	vi
	/*
				{11}
	*/
	vi.push_back(13);				//CMD:p//	vi
	/*
				{11,13}
	*/
	auto vi_it = vi.begin();		//CMD:p//	vi_it
	/*
				11
	*/
	vi.push_back(15);				//CMD:p//	vi
	/*
				{11,13,15}
	*/	
	vi_it = vi.begin();				//CMD:p//	vi_it
	/*
				11
	*/
	vi.insert(vi_it, 17);	//CMD:q-has-elem//	vi 3
	/*
				true
	*/
	auto vi_jt = std::next(vi.cbegin(), 4);
	dummy=true;			//CMD:q-iter-into//		vi vi_jt
	/*
				outOfBounds
	*/
	--vi_jt;			//CMD:q-iter-into//		vi vi_jt
	/*
				withinBounds_and_valid
	*/
	vi_it = vi.begin();				//CMD:p//	vi_it
	/*
				17
	*/
	++vi_it;						//CMD:p//	vi_it
	/*
				11
	*/
	*vi_it += 5000;					//CMD:p//	vi_it
	/*
				5011
	*/

//	p itC @@@ q-target-addr itC @@@ p $$1 == 17 && 17 == * $$0    /*CMDSEQ, doesn't work, sadly*/
	auto itA = vi.cbegin();	
	auto itB = std::prev(vi.cend());
	auto itC = std::make_move_iterator(itA);		//CMD:p//	itC
	/*
				17
	*/
	auto itD = std::make_reverse_iterator(itB);		//CMD:p//	itD
	/*
				15
	*/
	auto itE = std::make_reverse_iterator(itC);		//CMD:p//	itE
	/*
				17
	*/
	auto itF = std::make_move_iterator(itD);		//CMD:p//	itF
	/*
				15
	*/
	auto itG = vi.crend();							//CMD:p//	itG
	/*
				17
	*/
	auto itH = std::make_move_iterator(itG);		//CMD:p//	itH
	/*
				17
	*/

	++vi_it;
	++vi_it;						//CMD:p//	vi_it
	/*
				15
	*/
	dummy=true;			//CMD:q-iter-into//		vi vi_it
	/*
				withinBounds_and_valid
	*/
	vi.resize(3);					//CMD:p//	vi
	/*
				{17,5011,13}
	*/	
	dummy=true;			//CMD:q-has-elem//		vi 3
	/*
				false
	*/
	dummy=true;			//CMD:q-iter-into//		vi vi_it
	/*
				withinBounds_but_invalid
	*/
	dummy=true;			//CMD:q-count-elems//	vi
	/*
				3
	*/	
	std::vector<double> vd{3.14159, -0.001};
	dummy=true;			//CMD:q-iter-into//		vd vi_it
	/*
				outOfBounds
	*/
	vi.resize(6);					//CMD:p//	vi
	/*
				{17,5011,13 ,0,0,0}
	*/	
	dummy=true;			//CMD:q-has-elem//		vi 5
	/*
				true
	*/
	vi.clear();			//CMD:q-count-elems//	vi
	/*
				0
	*/
	return 0;
}
