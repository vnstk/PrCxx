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
#include <utility>

int main ( )
{	bool dummy;
	std::pair<double,const unsigned long *> px;	//CMD:q-count-elems//	px
	/*
					2
	*/
	std::pair<const char *,long> py =
		std::make_pair(nullptr, 123456789);				//CMD:p//	py
	/*
					{0x0,123456789}
	*/
	dummy=true;										//CMD:q-has-elem//	py 0
	/*
					true
	*/
	dummy=true;										//CMD:q-has-elem//	py 1
	/*
					true
	*/
	dummy=true;										//CMD:q-has-elem//	py 2
	/*
					false
	*/
	dummy=true;										//CMD:q-elem//		py 1
	/*
					123456789
	*/
	return 0;
}
