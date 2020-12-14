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
#include <bitset>

int main ( )
{	bool dummy;
	std::bitset<0> bs0;							//CMD:p//	bs0
	/*
					""
	*/
	dummy=true;						//CMD:q-count-elems//	bs0
	/*
					0
	*/
	dummy=true;							//CMD:q-has-elem//	bs0 0
	/*
					false
	*/
	dummy=0;								//CMD:set//		print repeats 0
	/*
	*/
	std::bitset<17> bs17;						//CMD:p//	bs17
	/*
					"00000000000000000"
	*/
	dummy=true;						//CMD:q-count-elems//	bs17
	/*
					17
	*/
	bs17.set(13);								//CMD:p//	bs17
	/*
					"00010000000000000"
	*/
	dummy=true;						//CMD:q-count-elems//	bs17
	/*
					17
	*/
	std::bitset<63> bs63;
	bs63.set(0);
	bs63.set(15);
	bs63.set(32);
	bs63.set(49);								//CMD:p//	bs63
	/*
					"000000000000010000000000000000100000000000000001000000000000001"
	*/
	std::bitset<65> bs65;
	bs65.set(20);
	bs65.set(21);
	bs65.flip(20);
	bs65.set(64);								//CMD:p//	bs65
	/*
					"10000000000000000000000000000000000000000001000000000000000000000"
	*/
	return 0;
}
