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
#include <stack>
#include <vector>
#include <cstddef> //For: size_t

int main ( )
{	bool dummy; int iv; size_t sz;

	std::stack<int> unk_si;				//CMD:p//	unk_si
	/*
					
	*/
	dummy=true;				//CMD:q-count-elems//	unk_si
	/*
					0
	*/
{
	std::stack<int> deq_si(
		std::deque<int>({11,55,99}));	//CMD:p//	deq_si
	/*
					{11,55,99}
	*/
	iv = deq_si.top();					//CMD:p//	iv
	/*
					99
	*/
}{
	std::deque<int> di({11,55,99});
	std::stack<int> deq_si(di); 		//CMD:p//	deq_si
	/*
					{11,55,99}
	*/
	iv = deq_si.top();					//CMD:p//	iv
	/*
					99
	*/
	dummy=true;				//CMD:q-count-elems//	deq_si
	/*
					3
	*/
	for (unsigned j = 0U; j < 5U; ++j) deq_si.push(200+(int)j);
	deq_si.push(1111);					//CMD:p//	deq_si
	/*
					{11,55,99 ,200,201,202,203,204 ,1111}
	*/
	sz = deq_si.size();					//CMD:p//	sz
	/*
					9
	*/
}

{
	std::list<int> li({22,66,88});
	std::stack<int,std::list<int>> lis_si(
		li);							//CMD:p//	lis_si
	/*
					{22,66,88}
	*/
	iv = lis_si.top();					//CMD:p//	iv
	/*
					88
	*/
}{
	std::stack<int,std::list<int>> lis_si(
		std::list<int>({22,66,88}));	//CMD:p//	lis_si
	/*
					{22,66,88}
	*/
	iv = lis_si.top();					//CMD:p//	iv
	/*
					88
	*/
}

{
	std::vector<int> vi({7,77,777});
	std::stack<int,std::vector<int>> vec_si(
		vi);							//CMD:p//	vec_si
	/*
					{7,77,777}
	*/
	iv = vec_si.top();					//CMD:p//	iv
	/*
					777
	*/
}{
	std::stack<int,std::vector<int>> vec_si(
		std::vector<int>({7,77,777}));	//CMD:p//	vec_si
	/*
					{7,77,777}
	*/
	iv = vec_si.top();					//CMD:p//	iv
	/*
					777
	*/
}

	return 0;
}
