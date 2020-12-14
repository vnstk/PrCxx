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
#include <deque>
#include <list>
#include <queue>

int main ( )
{	bool dummy; int iv; size_t sz;

	std::queue<int> unk_qi;				//CMD:p//	unk_qi
	/*
					
	*/
	dummy=true;				//CMD:q-count-elems//	unk_qi
	/*
					0
	*/
{
	std::queue<int> deq_qi(
		std::deque<int>({11,55,99}));	//CMD:p//	deq_qi
	/*
					{11,55,99}
	*/
	deq_qi.push(37);
	iv = deq_qi.back();					//CMD:p//	iv
	/*
					37
	*/
	iv = deq_qi.front();				//CMD:p//	iv
	/*
					11
	*/
	deq_qi.pop();
	iv = deq_qi.front();				//CMD:p//	iv
	/*
					55
	*/
	deq_qi.push(73);		//CMD:q-count-elems//	deq_qi
	/*
					4
	*/
}{
	std::deque<int> di({11,55,99});
	std::queue<int> deq_qi(di); 		//CMD:p//	deq_qi
	/*
					{11,55,99}
	*/
	iv = deq_qi.front();				//CMD:p//	iv
	/*
					11
	*/
	dummy=true;				//CMD:q-count-elems//	deq_qi
	/*
					3
	*/
	for (unsigned j = 0U; j < 5U; ++j) deq_qi.push(200+(int)j);
	deq_qi.push(1111);					//CMD:p//	deq_qi
	/*
					{11,55,99 ,200,201,202,203,204 ,1111}
	*/
	sz = deq_qi.size();					//CMD:p//	sz
	/*
					9
	*/
}

{
	std::list<int> li({22,66,88});
	std::queue<int,std::list<int>> lis_qi(
		li);							//CMD:p//	lis_qi
	/*
					{22,66,88}
	*/
	iv = lis_qi.front();				//CMD:p//	iv
	/*
					22
	*/
	iv = lis_qi.back();					//CMD:p//	iv
	/*
					88
	*/
}{
	std::queue<int,std::list<int>> lis_qi(
		std::list<int>({22,66,88}));	//CMD:p//	lis_qi
	/*
					{22,66,88}
	*/
	iv = lis_qi.front();				//CMD:p//	iv
	/*
					22
	*/
	iv = lis_qi.back();					//CMD:p//	iv
	/*
					88
	*/
}

	return 0;
}
