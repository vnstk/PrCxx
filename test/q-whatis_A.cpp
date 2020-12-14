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
#include <list>
#include <map>
#include <set>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

int main ( )
{	bool dummy;
	std::wstring           xa;
	std::string            xb[5];
	std::string           *xc;
	std::string           *xd[7];

	std::tuple<float,std::wstring,double*>   xe;
	std::tuple<float,std::string,double*>    xf[5];
	std::tuple<float,std::string,double*>   *xg;
	std::tuple<float,std::string,double*>   *xh[7];

	std::set<float>             xi;
	std::unordered_set<float>   xj;
	std::set<std::wstring>             xk;
	std::unordered_set<std::wstring>   xl;

	std::vector<double>         xm;
	std::vector<double>         xn[5];
	std::vector<double>        *xo;
	std::vector<double>        *xp[7];

	std::list<std::wstring>         xs;
	std::list<std::string>          xt[5];
	std::list<std::string>         *xu;
	std::list<std::string>         *xv[7];

	double   ya[5][7];
	double   yb[5][7][9];
	double  *yc[5][7];
	double  *yd[5][7][9];

	char         zza[] = "Bunnies";
	float        zzb[] = { 1.11, 2.22, 3.33, -42.0, 99.00017 };
	short        zzc[][3] = { {44,55,66} , {77,88,99} , {11,22,33} , {-1,-5,-9} };
	short        zzd[0];
	std::wstring zze[0];
	std::string  zzf[] = { "Klotho" , "Lachesis" , "Atropos" };

	std::vector<std::list<float>>      ye;
	std::vector<std::list<float>>      yf[5];
	std::vector<std::list<float>>     *yg;
	std::vector<std::list<float>>     *yh[7];

	std::list<std::vector<std::wstring>>     ym;
	std::list<std::vector<std::string>>      yn[5];
	std::list<std::vector<std::string>>     *yo;
	std::list<std::vector<std::string>>     *yp[7];

	std::map<float,double>                                              mp;
	std::map<float,std::string>                                         mq;
	std::map<std::wstring,float>                                        mr;
	std::map<std::string,std::string>                                   mr_a;
	std::map<std::wstring,std::string>                                  mr_b;
	std::map<std::string,std::wstring>                                  mr_c;
	std::map<float,std::vector<double>>                                 ms;
	std::map<std::string,std::vector<double>>                           mt;
	std::map<std::wstring,std::vector<std::string>>                     mu;

	std::unordered_map<float,double>                                    hp;
	std::unordered_map<float,std::string>                               hq;
	std::unordered_map<std::wstring,float>                              hr;
	std::unordered_map<std::string,std::string>                                   hr_a;
	std::unordered_map<std::wstring,std::string>                                  hr_b;
	std::unordered_map<std::string,std::wstring>                                  hr_c;
	std::unordered_map<float,std::vector<double>>                       hs;
	std::unordered_map<std::string,std::vector<double>>                 ht;
	std::unordered_map<std::wstring,std::vector<std::string>>           hu;

	std::list<std::map<double,std::vector<std::wstring>>>                xw;
//	std::map<std::string,std::unordered_map<std::string,std::string>>    xx[5];//TODO: come back && make work !!
	std::map<std::map<std::string,std::wstring>,std::list<std::string>>  xy[5][7];
	std::unordered_map<std::wstring,std::unordered_set<std::string>>     xz;


//=============================================================================================
//#############################################################################################
	dummy=true;						//CMD:set//			x-template-args full
	/*
	*/
//#############################################################################################
//=============================================================================================

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xa
	/*
				type = std::basic_string<wchar_t, #TRAITS# , #ALLO# >
	*/
	dummy=true;						//CMD:q-whatis//		xb
	/*
				type = std::basic_string<char, #TRAITS# , #ALLO# > [5]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xe
	/*
				type = std::tuple<float, std::basic_string<wchar_t, #'TRAITS# , #'ALLO# >, double*>
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xm
	/*
				type = std::vector<double, #ALLO# >
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xs
	/*
				type = std::list<std::basic_string<wchar_t, #'TRAITS# , #'ALLO#>, #ALLO# >
	*/
	dummy=true;						//CMD:q-whatis//		xt
	/*
				type = std::list<std::basic_string<char, #'TRAITS# , #'ALLO#>, #ALLO# > [5]
	*/
	dummy=true;						//CMD:q-whatis//		xu
	/*
				type = std::list<std::basic_string<char, #'TRAITS# , #'ALLO#>, #ALLO# > *
	*/
	dummy=true;						//CMD:q-whatis//		xv
	/*
				type = std::list<std::basic_string<char, #'TRAITS# , #'ALLO#>, #ALLO# > * [7]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		ya
	/*
				type = double [5] [7]
	*/
	dummy=true;						//CMD:q-whatis//		yb
	/*
				type = double [5] [7] [9]
	*/
	dummy=true;						//CMD:q-whatis//		yc
	/*
				type = double * [5] [7]
	*/
	dummy=true;						//CMD:q-whatis//		yd
	/*
				type = double * [5] [7] [9]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		ye
	/*
				type = std::vector<std::list<float, #'ALLO# >, #ALLO# >
	*/
	dummy=true;						//CMD:q-whatis//		yf
	/*
				type = std::vector<std::list<float, #'ALLO# >, #ALLO# > [5]
	*/
	dummy=true;						//CMD:q-whatis//		yg
	/*
				type = std::vector<std::list<float, #'ALLO# >, #ALLO# > *
	*/
	dummy=true;						//CMD:q-whatis//		yh
	/*
				type = std::vector<std::list<float, #'ALLO# >, #ALLO# > * [7]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		ym
	/*
				type = std::list<std::vector<std::basic_string<wchar_t, #''TRAITS# , #''ALLO#>, #'ALLO# >, #ALLO# >
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xi
	/*
				type = std::set<float, #CMP#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		xj
	/*
				type = std::unordered_set<float, #HASH#, #EQ#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		xk
	/*
				type = std::set<std::basic_string<wchar_t, #'TRAITS# , #'ALLO#>, #CMP#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		xl
	/*
				type = std::unordered_set<std::basic_string<wchar_t, #'TRAITS# , #'ALLO#>, #HASH#, #EQ#, #ALLO#>
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		mp
	/*
				type = std::map<float,double, #CMP#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		mq
	/*
				type = std::map<float, std::basic_string<char, #'TRAITS# , #'ALLO#>, #CMP#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		mr
	/*
				type = std::map<std::basic_string<wchar_t, #'TRAITS# , #'ALLO#>, float, #CMP#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		ms
	/*
				type = std::map<float,std::vector<double, #'ALLO#>, #CMP#, #ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		mt
	/*
				type = std::map<std::basic_string<char,#'TRAITS#,#'ALLO#>, std::vector<double,#'ALLO#>, #CMP#,#ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		mu
	/*
				type = std::map< std::basic_string<wchar_t,#'TRAITS#,#'ALLO#>, std::vector< std::basic_string<char,#''TRAITS#,#''ALLO#>, #'ALLO#>, #CMP#,#ALLO#>
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		hp
	/*
				type = std::unordered_map<float,double, #HASH#,#EQ#,#ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		hq
	/*
				type = std::unordered_map<float, std::basic_string<char, #'TRAITS# , #'ALLO#>, #HASH#,#EQ#,#ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		hr
	/*
				type = std::unordered_map<std::basic_string<wchar_t, #'TRAITS# , #'ALLO#>, float, #HASH#,#EQ#,#ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		hs
	/*
				type = std::unordered_map<float,std::vector<double, #'ALLO#>, #HASH#,#EQ#,#ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		ht
	/*
				type = std::unordered_map<std::basic_string<char,#'TRAITS#,#'ALLO#>, std::vector<double,#'ALLO#>, #HASH#,#EQ#,#ALLO#>
	*/
	dummy=true;						//CMD:q-whatis//		hu
	/*
				type = std::unordered_map< std::basic_string<wchar_t,#'TRAITS#,#'ALLO#>, std::vector< std::basic_string<char,#''TRAITS#,#''ALLO#>, #'ALLO#>, #HASH#,#EQ#,#ALLO#>
	*/


//=============================================================================================
//#############################################################################################
	dummy=true;						//CMD:set//			x-template-args skipIfDefault
	/*
	*/
//#############################################################################################
//=============================================================================================

//____________________________________________________________________________________________
	dummy=true;				//CMD:q-whatis//		zza
	/*
		type = char [8]
	*/
	dummy=true;				//CMD:q-whatis//		zzb
	/*
		type = float [5]
	*/
	dummy=true;				//CMD:q-whatis//		zzc
	/*
		type = short [4][3]
	*/
	dummy=true;				//CMD:q-whatis//		zzd
	/*
		type = short [0]
	*/
	dummy=true;				//CMD:q-whatis//		zze
	/*
		type = std::wstring [0]
	*/
	dummy=true;				//CMD:q-whatis//		zzf
	/*
		type = std::string [3]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xa
	/*
				type = std::wstring
	*/
	dummy=true;						//CMD:q-whatis//		xb
	/*
				type = std::string [5]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xm
	/*
				type = std::vector<double>
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xs
	/*
				type = std::list<std::wstring>
	*/
	dummy=true;						//CMD:q-whatis//		xt
	/*
				type = std::list<std::string> [5]
	*/
	dummy=true;						//CMD:q-whatis//		xu
	/*
				type = std::list<std::string> *
	*/
	dummy=true;						//CMD:q-whatis//		xv
	/*
				type = std::list<std::string> * [7]
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		xi
	/*
				type = std::set<float>
	*/
	dummy=true;						//CMD:q-whatis//		xj
	/*
				type = std::unordered_set<float>
	*/
	dummy=true;						//CMD:q-whatis//		xk
	/*
				type = std::set<std::wstring>
	*/
	dummy=true;						//CMD:q-whatis//		xl
	/*
				type = std::unordered_set<std::wstring>
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		mp
	/*
				type = std::map<float,double>
	*/
	dummy=true;						//CMD:q-whatis//		mq
	/*
				type = std::map<float,std::string>
	*/
	dummy=true;						//CMD:q-whatis//		mr
	/*
				type = std::map<std::wstring,float>
	*/

	dummy=true;						//CMD:q-whatis//		mr_a
	/*
				type = std::map<std::string,std::string>
	*/
	dummy=true;						//CMD:q-whatis//		mr_b
	/*
				type = std::map<std::wstring,std::string>
	*/
	dummy=true;						//CMD:q-whatis//		mr_c
	/*
				type = std::map<std::string,std::wstring>
	*/

	dummy=true;						//CMD:q-whatis//		ms
	/*
				type = std::map<float,std::vector<double>>
	*/
	dummy=true;						//CMD:q-whatis//		mt
	/*
				type = std::map<std::string,std::vector<double>>
	*/
	dummy=true;						//CMD:q-whatis//		mu
	/*
				type = std::map<std::wstring,std::vector<std::string>>
	*/

//____________________________________________________________________________________________
	dummy=true;						//CMD:q-whatis//		hp
	/*
				type = std::unordered_map<float,double>
	*/
	dummy=true;						//CMD:q-whatis//		hq
	/*
				type = std::unordered_map<float,std::string>
	*/
	dummy=true;						//CMD:q-whatis//		hr
	/*
				type = std::unordered_map<std::wstring,float>
	*/

	dummy=true;						//CMD:q-whatis//		hr_a
	/*
				type = std::unordered_map<std::string,std::string>
	*/
	dummy=true;						//CMD:q-whatis//		hr_b
	/*
				type = std::unordered_map<std::wstring,std::string>
	*/
	dummy=true;						//CMD:q-whatis//		hr_c
	/*
				type = std::unordered_map<std::string,std::wstring>
	*/

	dummy=true;						//CMD:q-whatis//		hs
	/*
				type = std::unordered_map<float,std::vector<double>>
	*/
	dummy=true;						//CMD:q-whatis//		ht
	/*
				type = std::unordered_map<std::string,std::vector<double>>
	*/
	dummy=true;						//CMD:q-whatis//		hu
	/*
				type = std::unordered_map<std::wstring,std::vector<std::string>>
	*/

//____________________________________________________________________________________________
	dummy=true;							//CMD:q-whatis//	xw
	/*
				type = std::list<std::map<double,std::vector<std::wstring>>>
	*/
	dummy=true;							//CMD:q-whatis//	xy
	/*
				type = std::map<std::map<std::string,std::wstring>,std::list<std::string>> [5][7]
	*/
	dummy=true;							//CMD:q-whatis//	xz
	/*
				type = std::unordered_map<std::wstring,std::unordered_set<std::string>>
	*/

	return 0;
}
