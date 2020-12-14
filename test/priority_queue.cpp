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
#include <queue> // Is no <priority_queue>.
#include <vector>

int main ( )
{	bool dummy; int iv; size_t sz;

	std::priority_queue<int> unk_pqi;		//CMD:p//	unk_pqi
	/*
					
	*/
	dummy=true;					//CMD:q-count-elems//	unk_pqi
	/*
					0
	*/
{
	std::deque<int> di({11,99,33,77,99,-42});
	di.push_back(246);						//CMD:p//	di
	/*
					{11,99,33,77,99,-42,246}
	*/
	std::priority_queue<int,std::deque<int>> deq_pqi(std::less<int>(),
		di);								//CMD:p//	deq_pqi
	/*
					{246,99,33,77,99,-42,11}
	*/
	sz = deq_pqi.size(); 					//CMD:p//	sz
	/*
					7
	*/
	iv = deq_pqi.top();						//CMD:p//	iv
	/*
					246
	*/
	for (unsigned j = 0U; j < 5U; ++j) deq_pqi.push(200+(int)j);
	iv = deq_pqi.top();						//CMD:p//	iv
	/*
					246
	*/
	deq_pqi.pop();				//CMD:q-count-elems//	deq_pqi
	/*
					11
	*/
	iv = deq_pqi.top();						//CMD:p//	iv
	/*
					204
	*/
	sz = deq_pqi.size();					//CMD:p//	sz
	/*
					11
	*/
}{
	std::deque<int> di({11,99,33,77});		//CMD:p//	di
	/*
					{11,99,33,77}
	*/
	// Didn't have to specify std::less<int> te arg, because is default.
	std::priority_queue<int,std::deque<int>,std::greater<int>> deq_pqi(
		std::greater<int>(), di);			//CMD:p//	deq_pqi
	/*
					{11,77,33,99}
	*/
	iv = deq_pqi.top();						//CMD:p//	iv
	/*
					11
	*/
	deq_pqi.pop();
	iv = deq_pqi.top();						//CMD:p//	iv
	/*
					33
	*/
}

{
	std::vector<int> vi({7,77,777,7777});
	std::priority_queue<int/*,std::vector<int>*/> vec_pqi(
		std::less<int>(), vi);				//CMD:p//	vec_pqi
	/*
					{7777,77,777,7}
	*/
	iv = vec_pqi.top();						//CMD:p//	iv
	/*
					7777
	*/
}{
	std::priority_queue<int,std::vector<int>,std::greater<int>> vec_pqi(
		std::greater<int>(),
		std::vector<int>({7,77,777,7777}));	//CMD:p//	vec_pqi
	/*
					{7,77,777,7777}
	*/
	iv = vec_pqi.top();						//CMD:p//	iv
	/*
					7
	*/
}

	return 0;
}
