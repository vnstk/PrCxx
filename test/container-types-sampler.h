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
#ifndef CONTAINER_TYPES_SAMPLER__H
#define CONTAINER_TYPES_SAMPLER__H

#include "nondefault-STL-types-spec-helpers.h"


#include <array>
#include <deque>
#include <forward_list>
#include <initializer_list>
#include <list>
#include <map>
#include <set>
#include <queue> //For- std::priority_queue, std::queue
#include <stack>
#include <string>
// #include <string_view>  Not available on pre-2016 GNU stdlibc++'s.
#include <unordered_map>
#include <unordered_set>
#include <vector>


struct TypesSampler
{

	//________________________________________________________
	// "a" |||    std::initializer_list<E>
	//========================================================
	std::initializer_list<float>          a0;
		IT_it(a0); IT_cit(a0);
		//NB: type of both it and cit is just "const T*"
	std::initializer_list<std::wstring>   a1;
		IT_it(a1); IT_cit(a1);

	//________________________________________________________
	// "b" |||    std::array<E,N>
	//========================================================
	std::array<float, 5>                                 b0;
		IT_it(b0); IT_cit(b0); IT_rit(b0); IT_crit(b0);
	std::array<std::wstring, 0>                          b1;
		IT_it(b1); IT_cit(b1); IT_rit(b1); IT_crit(b1);

	//________________________________________________________
	// "c" |||    std::vector<E,ALLO>
	//========================================================
	std::vector<float>                                   c0;
		IT_it(c0); IT_cit(c0); IT_rit(c0); IT_crit(c0);
	std::vector<std::string>                             c1;
		IT_it(c1); IT_cit(c1); IT_rit(c1); IT_crit(c1);
	std::vector<float, Mallo<float>>                     c2;
		IT_it(c2); IT_cit(c2); IT_rit(c2); IT_crit(c2);
	std::vector<std::string, Mallo<std::string>>         c3;
		IT_it(c3); IT_cit(c3); IT_rit(c3); IT_crit(c3);

	//________________________________________________________
	// "d" |||    std::vector<bool,ALLO>
	//========================================================
	std::vector<bool>                                   d0;
		IT_it(d0); IT_cit(d0); IT_rit(d0); IT_crit(d0);
	std::vector<bool, Mallo<bool>>                      d1;
		IT_it(d1); IT_cit(d1); IT_rit(d1); IT_crit(d1);

	//________________________________________________________
	// "e" |||    std::basic_string<ChT,ChTraits,ALLO>
	//========================================================
	std::wstring                                        e0;
		IT_it(e0); IT_cit(e0); IT_rit(e0); IT_crit(e0);
	//
	std::basic_string<char, caseChTraits>               e1;
		IT_it(e1); IT_cit(e1); IT_rit(e1); IT_crit(e1);
	//
	std::basic_string<char, caseChTraits, Mallo<char>>  e6;
		IT_it(e6); IT_cit(e6); IT_rit(e6); IT_crit(e6);

	//________________________________________________________
	// "f" |||    std::basic_string_view<ChT,ChTraits>
	//========================================================
			// Not available on pre-2016 GNU stdlibc++'s.

	//________________________________________________________
	// "g" |||    std::forward_list<E,ALLO>
	//========================================================
	std::forward_list<float>                            g0;
		IT_it(g0); IT_cit(g0);
	std::forward_list<std::string>                      g1;
		IT_it(g1); IT_cit(g1);
	std::forward_list<float, Mallo<float>>              g2;
		IT_it(g2); IT_cit(g2);
	std::forward_list<std::string, Mallo<std::string>>  g3;
		IT_it(g3); IT_cit(g3);

	//________________________________________________________
	// "h" |||    std::list<E,ALLO>
	//========================================================
	std::list<float>                                     h0;
		IT_it(h0); IT_cit(h0); IT_rit(h0); IT_crit(h0);
	std::list<std::string>                               h1;
		IT_it(h1); IT_cit(h1); IT_rit(h1); IT_crit(h1);
	std::list<float, Mallo<float>>                       h2;
		IT_it(h2); IT_cit(h2); IT_rit(h2); IT_crit(h2);
	std::list<std::string, Mallo<std::string>>           h3;
		IT_it(h3); IT_cit(h3); IT_rit(h3); IT_crit(h3);

	//________________________________________________________
	// "j" |||    std::deque<E,ALLO>
	//========================================================
	std::deque<float>                                    j0;
		IT_it(j0); IT_cit(j0); IT_rit(j0); IT_crit(j0);
	std::deque<std::string>                              j1;
		IT_it(j1); IT_cit(j1); IT_rit(j1); IT_crit(j1);
	std::deque<float, Mallo<float>>                      j2;
		IT_it(j2); IT_cit(j2); IT_rit(j2); IT_crit(j2);
	std::deque<std::string, Mallo<std::string>>          j3;
		IT_it(j3); IT_cit(j3); IT_rit(j3); IT_crit(j3);

	//________________________________________________________
	// "k" |||    std::priority_queue<E,CONT=vector<E>,CMP>
	//========================================================
	std::priority_queue<float>                                  k0;
	std::priority_queue<float, std::deque<float>>               k1;
	std::priority_queue<float, std::vector<float>, floatGT>     k2;
	std::priority_queue<float, std::deque<float>, floatGT>      k3;
	std::priority_queue<std::string, std::vector<std::string>>  k4;

	//________________________________________________________
	// "m" |||    std::queue<E,CONT=deque<E>>
	//========================================================
	std::queue<float>                                     m0;
	std::queue<float, std::deque<float>>                  m1;
	std::queue<float, std::vector<float>>                 m2;
	std::queue<std::wstring>                              m3;
	std::queue<std::wstring, std::deque<std::wstring>>    m4;
	std::queue<std::wstring, std::vector<std::wstring>>   m5;

	//________________________________________________________
	// "n" |||    std::stack<E,CONT=deque<E>>
	//========================================================
	std::stack<float>                                     n0;
	std::stack<float, std::deque<float>>                  n1;
	std::stack<float, std::vector<float>>                 n2;
	std::stack<std::wstring>                              n3;
	std::stack<std::wstring, std::deque<std::wstring>>    n4;
	std::stack<std::wstring, std::vector<std::wstring>>   n5;

	//________________________________________________________
	// "o" |||    std::set<E,CMP,ALLO>
	//========================================================
	std::set<float>                                     o0;
		IT_it(o0); IT_cit(o0); IT_rit(o0); IT_crit(o0);
	std::set<float, std::greater<float>>                o1;
		IT_it(o1); IT_cit(o1); IT_rit(o1); IT_crit(o1);
	std::set<float, floatGT>                            o2;
		IT_it(o2); IT_cit(o2); IT_rit(o2); IT_crit(o2);
	//
	std::set<float, floatGT, Mallo<float>>              o3;
		IT_it(o3); IT_cit(o3); IT_rit(o3); IT_crit(o3);
	//
	std::set<std::wstring>                              o4;
		IT_it(o4); IT_cit(o4); IT_rit(o4); IT_crit(o4);
	//
	std::set<std::string, std::greater<std::string>>    o5;
		IT_it(o5); IT_cit(o5); IT_rit(o5); IT_crit(o5);
	//
	std::set<std::string, std::greater<std::string>,
	                             Mallo<std::string>>    o6;
		IT_it(o6); IT_cit(o6); IT_rit(o6); IT_crit(o6);

	//________________________________________________________
	// "p" |||    std::multiset<E,CMP,ALLO>
	//========================================================
	std::multiset<float>                                   p0;
		IT_it(p0); IT_cit(p0); IT_rit(p0); IT_crit(p0);
	std::multiset<float, std::greater<float>>              p1;
		IT_it(p1); IT_cit(p1); IT_rit(p1); IT_crit(p1);
	std::multiset<float, floatGT>                          p2;
		IT_it(p2); IT_cit(p2); IT_rit(p2); IT_crit(p2);
	//
	std::multiset<float, floatGT, Mallo<float>>            p3;
		IT_it(p3); IT_cit(p3); IT_rit(p3); IT_crit(p3);
	//
	std::multiset<std::wstring>                            p4;
		IT_it(p4); IT_cit(p4); IT_rit(p4); IT_crit(p4);
	//
	std::multiset<std::string, std::greater<std::string>>  p5;
		IT_it(p5); IT_cit(p5); IT_rit(p5); IT_crit(p5);
	//
	std::multiset<std::string, std::greater<std::string>,
	                             Mallo<std::string>>       p6;
		IT_it(p6); IT_cit(p6); IT_rit(p6); IT_crit(p6);

	//________________________________________________________
	// "q" |||    std::map<K,V,CMP,ALLO>
	//========================================================
	std::map<float, double>                                q0;
		IT_it(q0); IT_cit(q0); IT_rit(q0); IT_crit(q0);
	std::map<float, double, std::greater<float>>           q1;
		IT_it(q1); IT_cit(q1); IT_rit(q1); IT_crit(q1);
	std::map<float, double, floatGT>                       q2;
		IT_it(q2); IT_cit(q2); IT_rit(q2); IT_crit(q2);
	std::map<float, std::string>                           q3;
		IT_it(q3); IT_cit(q3); IT_rit(q3); IT_crit(q3);
	std::map<float, std::string, floatGT>                  q4;
		IT_it(q4); IT_cit(q4); IT_rit(q4); IT_crit(q4);
	//
	std::map<std::wstring, double,
	          std::greater<std::wstring>>                  q5;
		IT_it(q5); IT_cit(q5); IT_rit(q5); IT_crit(q5);
	//
	std::map<float, double, floatGT,
	      Mallo<std::pair<const float&,double>>>           q6;
		IT_it(q6); IT_cit(q6); IT_rit(q6); IT_crit(q6);
	//
	std::map<float, std::string, floatGT,
	      Mallo<std::pair<const float&,std::string>>>      q7;
		IT_it(q7); IT_cit(q7); IT_rit(q7); IT_crit(q7);

	//________________________________________________________
	// "r" |||    std::multimap<K,V,CMP,ALLO>
	//========================================================
	std::multimap<float, double>                           r0;
		IT_it(r0); IT_cit(r0); IT_rit(r0); IT_crit(r0);
	std::multimap<float, double, std::greater<float>>      r1;
		IT_it(r1); IT_cit(r1); IT_rit(r1); IT_crit(r1);
	std::multimap<float, double, floatGT>                  r2;
		IT_it(r2); IT_cit(r2); IT_rit(r2); IT_crit(r2);
	std::multimap<float, std::string>                      r3;
		IT_it(r3); IT_cit(r3); IT_rit(r3); IT_crit(r3);
	std::multimap<float, std::string, floatGT>             r4;
		IT_it(r4); IT_cit(r4); IT_rit(r4); IT_crit(r4);
	//
	std::multimap<std::wstring, double,
	          std::greater<std::wstring>>                  r5;
		IT_it(r5); IT_cit(r5); IT_rit(r5); IT_crit(r5);
	//
	std::multimap<float, double, floatGT,
	      Mallo<std::pair<const float&,double>>>           r6;
		IT_it(r6); IT_cit(r6); IT_rit(r6); IT_crit(r6);
	//
	std::multimap<float, std::string, floatGT,
	      Mallo<std::pair<const float&,std::string>>>      r7;
		IT_it(r7); IT_cit(r7); IT_rit(r7); IT_crit(r7);

	//________________________________________________________
	// "s" |||    std::unordered_set<E,HASH,EQ,ALLO>
	//========================================================
	std::unordered_set<float>                                   s0;
		IT_it(s0); IT_cit(s0);
	std::unordered_set<float, floatHasher>                    s2;
		IT_it(s2); IT_cit(s2);
	std::unordered_set<float, floatHasher, Mallo<float>>      s3;
		IT_it(s3); IT_cit(s3);
	//
	std::unordered_set<float, std::hash<float>,
	                      std::equal_to<float>, Mallo<float>>   s4;
		IT_it(s4); IT_cit(s4);
	//
	std::unordered_set<std::wstring>                            s5;
		IT_it(s5); IT_cit(s5);
	//
	std::unordered_set<std::string, std::hash<std::string>,
	          std::equal_to<std::string>, Mallo<std::string>>   s6;
		IT_it(s6); IT_cit(s6);

	//________________________________________________________
	// "t" |||    std::unordered_multiset<E,HASH,EQ,ALLO>
	//========================================================
	std::unordered_multiset<float>                                t0;
		IT_it(t0); IT_cit(t0);
	std::unordered_multiset<float, floatHasher>                 t2;
		IT_it(t2); IT_cit(t2);
	std::unordered_multiset<float, floatHasher, Mallo<float>>   t3;
		IT_it(t3); IT_cit(t3);
	//
	std::unordered_multiset<float, std::hash<float>,
	                      std::equal_to<float>, Mallo<float>>     t4;
		IT_it(t4); IT_cit(t4);
	//
	std::unordered_multiset<std::wstring>                         t5;
		IT_it(t5); IT_cit(t5);
	//
	std::unordered_multiset<std::string, std::hash<std::string>,
	          std::equal_to<std::string>, Mallo<std::string>>     t6;
		IT_it(t6); IT_cit(t6);

	//________________________________________________________
	// "u" |||    std::unordered_map<K,V,HASH,EQ,ALLO>
	//========================================================
	std::unordered_map<float, double>                          u0;
		IT_it(u0); IT_cit(u0);
	std::unordered_map<float, double, floatHasher>           u2;
		IT_it(u2); IT_cit(u2);
	//
	std::unordered_map<float, double, std::hash<float>,
	                              std::equal_to<float>>        u3;
		IT_it(u3); IT_cit(u3);
	//
	std::unordered_map<float, double, std::hash<float>,
	                              std::equal_to<float>,
	             Mallo<std::pair<const float&,double>>>        u4;
		IT_it(u4); IT_cit(u4);
	//
	std::unordered_map<float, std::string>                     u5;
		IT_it(u5); IT_cit(u5);
	//
	std::unordered_map<float, std::string, std::hash<float>,
	                                   std::equal_to<float>,
	             Mallo<std::pair<const float&,std::string>>>   u6;
		IT_it(u6); IT_cit(u6);
	//
	std::unordered_map<std::wstring, double>                   u7;
		IT_it(u7); IT_cit(u7);
	//
	std::unordered_map<std::wstring, double,
	                              anyHasher<std::wstring>>   u8;
		IT_it(u8); IT_cit(u8);

	//________________________________________________________
	// "v" |||    std::unordered_multimap<K,V,HASH,EQ,ALLO>
	//========================================================
	std::unordered_multimap<float, double>                        v0;
		IT_it(v0); IT_cit(v0);
	std::unordered_multimap<float, double, floatHasher>         v2;
		IT_it(v2); IT_cit(v2);
	//
	std::unordered_multimap<float, double, std::hash<float>,
	                              std::equal_to<float>>           v3;
		IT_it(v3); IT_cit(v3);
	//
	std::unordered_multimap<float, double, std::hash<float>,
	                              std::equal_to<float>,
	             Mallo<std::pair<const float&,double>>>           v4;
		IT_it(v4); IT_cit(v4);
	//
	std::unordered_multimap<float, std::string>                   v5;
		IT_it(v5); IT_cit(v5);
	//
	std::unordered_multimap<float, std::string, std::hash<float>,
	                                   std::equal_to<float>,
	             Mallo<std::pair<const float&,std::string>>>      v6;
		IT_it(v6); IT_cit(v6);
	//
	std::unordered_multimap<std::wstring, double>                 v7;
		IT_it(v7); IT_cit(v7);
	//
	std::unordered_multimap<std::wstring, double,
	                              anyHasher<std::wstring>>      v8;
		IT_it(v8); IT_cit(v8);

};


#endif // CONTAINER_TYPES_SAMPLER__H
