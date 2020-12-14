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
#include <deque>
#include <forward_list>
#include <list>
#include <map>
#include <set>
#include <string>
#include <tuple>
#include <unordered_set>
#include <vector>


struct AaXX {        /*Illegal combinations are "//!"-commented out below. */
	//////// Elab.
	float                  _anC;          // T (non-const)
	float         const    _aCo{ 3.14F }; // const_T
	//
	float       *          _b0{ & _anC }; // ptr to T
	float       * const    _b1{ & _anC }; // const_ptr to T
//! float       *          _b2{ & _aCo }; // ptr to const_T
//!	float       * const    _b3{ & _aCo }; // const_ptr to const_T
	//
	float const *          _c0{ & _anC }; // ptr to const_T
	float const * const    _c1{ & _aCo }; // const_ptr to const_T
	//
	float               &  _d0{ _anC }; // ref to T
	float         const &  _d1{ _anC }; // ref-to-const to T
//!	float               &  _d2{ _aCo }; // ref to const_T
	float         const &  _d3{ _aCo }; // ref-to-const to const_T
	//
	float       *       &  _e0{ _b0 }; // ref to ptr to T
//!	float       *       &  _e1{ _b1 }; // ref to const_ptr to T
	float       * const &  _e2{ _b0 }; // ref-to-const to ptr to T
	float       * const &  _e3{ _b1 }; // ref-to-const to const_ptr to T
	//
	float const *       &  _f0{ _c0 }; // ref to ptr to const_T
//!	float const *       &  _f1{ _c1 }; // ref to const_ptr to const_T
	float const * const &  _f2{ _c0 }; // ref-to-const to ptr to const_T
	float const * const &  _f3{ _c1 }; // ref-to-const to const_ptr to const_T
};

struct BbXX {
	long     _b0;
};
	//////// pointers to parent type
struct DdXX : BbXX {
	BbXX       * _d0;
	const BbXX * _d1[22];
};

struct QqXX {
	//////// pointers+lvalue references to toplev type
	      QqXX *         _z0;
	const QqXX *         _z1;
	      QqXX * const   _z2{nullptr};
	const QqXX * const   _z3{nullptr};
	      QqXX *         _z4[17];
	const QqXX *         _z5[19];
	const QqXX * &       _z6{_z5[18]};
	const QqXX * const & _z7{_z6};
	      QqXX * &       _z8{_z0};
	      QqXX * const & _z9{_z8};
	//
	//////// pointers to unrelated struct type
	      BbXX *         _y0;
	const BbXX *         _y1;
	      BbXX * const   _y2{nullptr};
	const BbXX * const   _y3{nullptr};
	      BbXX *         _y4[25];
	const BbXX *         _y5[27];
	//
	//////// composition, unrelated struct type
	static const BbXX         _c4;
	       const BbXX         _c5{};
	             BbXX         _c6;
	             BbXX &       _c7{_c6};
	       const BbXX &       _c8{_c7};
	static       BbXX         _c9[0];
};

struct PpXX {
	//////// pointers to primitive
	static           float *        _f0;
	           const float *        _f1;
	static constexpr float * const  _f2{nullptr};
	           const float * const  _f3{nullptr};
	                 float *        _f4[35];
	           const float *        _f5[37];
	//
	//////// arrays of primitive
	static constexpr short       _s0 = 42;
	static           short       _s1[0];
	                 short       _s2[3] = {49,51,53,};
	                 short    *  _s4[][41];
};

struct VvXX {
	//////// volatile
       static       int         volatile  _v0;
                    int         volatile  _v1[15];
    const           int *       volatile  _v2;
    const           int *       volatile  _v3[13];
    const           int * const volatile  _v4{nullptr};
          volatile  int *                 _v5;
          volatile  int *       volatile  _v6;
    const volatile  int *                 _v7;
    const volatile  int *       volatile  _v8;
    const volatile  int * const volatile  _v9{nullptr};
	volatile int i = 42;
	      volatile  int * const           _vA{& i};
    const volatile  int * const           _vB{& i};
};

struct EeXX {
	//////// a few elementary STL types, just as sanity check
	static std::string                 _e0;
	std::string                        _e1{"bunnies"};
	std::vector<std::wstring>          _e2;
	std::tuple<float,bool,DdXX*>       _e3[11];
	std::list<long>                 *  _e4;
};

struct MmXX {
	std::list<EeXX *>::const_iterator  _m1;
	std::list<MmXX *>::const_iterator  _m2;
	//////// nested types
	struct FfXX {        // nested, plain
		uint8_t     _ff;
		FfXX     *  _pnext;
	};
	FfXX                               _m4;
	static FfXX                     *  _m5;
	std::list<FfXX>                    _m6;
	struct GgXX : FfXX { // nested, inherit from nested
		uint16_t    _gg;
	};
	GgXX                               _m7;
	struct HhXX : BbXX { // nested, inherit from elsewhere
		uint32_t    _hh;
	};
	HhXX                               _m8;
};

template<typename TtXX, size_t TtNN>
struct JjXX {
	//////// pointers to a template parameter type
	const TtXX             * _j0;
	      TtXX             * _j1;
	      TtXX             * _j2[TtNN];
	    double               _j3[TtNN];
	//////// instantiate a-mere-typedef STL types with te params
	std::array<double,TtNN>  _j4;
	std::array<TtXX,TtNN>    _j5;
	std::array<JjXX*,TtNN>   _j6;
};

template<typename ELEM, typename CONT = std::vector<ELEM>>
struct ZzXX {
	//////// a few rudimentary uses of CONT's member types.
	typename CONT::iterator                _z0;
	typename CONT::const_iterator          _z1;
	typename CONT::reverse_iterator        _z2;
	typename CONT::const_reverse_iterator  _z3;
	typename CONT::value_type              _z4; // i.e. ELEM
	//
	//////// instantiate full-on-datastruct STL types with te params
	std::set<typename CONT::iterator>         _z5;
	std::list<typename CONT::const_iterator>  _z6;
	ZzXX<ELEM,CONT>                      *    _z7[1];
	std::set<ELEM>                            _z8;
	std::map<ELEM,CONT>                       _z9;
};

template<typename ELEM, typename CONT = std::vector<ELEM>>
struct NoRevZzXX {
	//////// iterator member types of containers without reverse iterators.
	typename CONT::iterator                _nrz0;
	typename CONT::const_iterator          _nrz1;
};


int main ( )
{	bool dummy;

	dummy=true;		//CMDSEQ//	set x-base-classes skipIfEmpty @@@ set x-heur-abbr on @@@ set x-layout omit @@@ set x-nested-datamemb omit @@@ set x-template-args skipIfDefault @@@ set x-relations off
	/*
	*/


/*                     For ref, here's how GDB-native "ptype" renders AaXX:
    float _anC;
    const float _aCo;
    float *_b0;
    float * const _b1;
    const float *_c0;
    const float * const _c1;
    float &_d0;
    const float &_d1;
    const float &_d3;
    float *&_e0;
    float * const&_e2;
    float * const&_e3;
    const float *&_f0;
    const float * const&_f2;
    const float * const&_f3;
*/

/*______________________________________________________________
####################  AaXX #####################################
*/
	AaXX ax;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_anC
	/*
					float					_anC;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_aCo
	/*
					float			C		_aCo;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_b0
	/*
					float		*			_b0;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_b1
	/*
					float		*	C		_b1;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_c0
	/*
					float	C 	*			_c0;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_c1
	/*
					float	C 	*	C		_c1;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_d0
	/*
					float	 			&	_d0;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_d1
	/*
					float	 		C	&	_d1;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_d3
	/*
					float	 		C	&	_d3;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_e0
	/*
					float	 	*		&	_e0;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_e2
	/*
					float	 	*	C	&	_e2;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_e3
	/*
					float	 	*	C	&	_e3;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_f0
	/*
					float	 C	*		&	_f0;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_f2
	/*
					float	 C	*	C	&	_f2;
	*/
	dummy=true;	//GREP1:p-vtype//	ax	,,,	_f3
	/*
					float	 C	*	C	&	_f3;
	*/


/*______________________________________________________________
####################  BbXX and DdXX  ###########################
*/
	BbXX bx;
	DdXX dx;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	bx	,,,	_b0
	/*
				long						_b0;
	*/
	dummy=true;	//GREP1:p-vtype//	dx	,,,	_d0
	/*
				@0@				*			_d0;
	*/
	dummy=true;	//GREP1:p-vtype//	dx	,,,	_d1
	/*
				@0@			C	*			_d1	[22];
	*/


/*______________________________________________________________
####################  QqXX  ####################################
*/
	QqXX qx;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_z1
	/*
				@TOPLEV@	C	*			_z1;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_z2
	/*
				@TOPLEV@		*	C		_z2;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_z3
	/*
				@TOPLEV@	C	*	C		_z3;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_z5
	/*
				@TOPLEV@	C	*			_z5[19];
	*/

/********* XXX fix !!!!! XXX */
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_z6
	/*
				@TOPLEV@	C	*		&	_z6;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_z8
	/*
				@TOPLEV@		*		&	_z8;
	*/

	dummy=true;	//GREP1:p-vtype//	qx	,,,	_y0
	/*
				BbXX			* 			_y0;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_y1
	/*
				BbXX		C	* 			_y1;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_y2
	/*
				BbXX			* 	C		_y2;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_y3
	/*
				BbXX		C	* 	C		_y3;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_y4
	/*
				BbXX			* 			_y4[25];
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_y5
	/*
				BbXX		C	* 			_y5[27];
	*/

	dummy=true;	//GREP1:p-vtype//	qx	,,,	_c4
	/*
		|S		BbXX			 	C		_c4;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_c5
	/*
				BbXX			 	C		_c5;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_c6
	/*
				BbXX			 			_c6;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_c7
	/*
				BbXX			 &			_c7;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_c8
	/*
				BbXX		C	 &			_c8;
	*/
	dummy=true;	//GREP1:p-vtype//	qx	,,,	_c9
	/*
		|S		BbXX						_c9[0];
	*/


/*______________________________________________________________
####################  PpXX  ####################################
*/
	PpXX px;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	px	,,,	_f0
	/*
		|S		float			*			_f0;
	*/
	//NB: pointer-to-constexpr is not a pointer-to-const!
	dummy=true;	//GREP1:p-vtype//	px	,,,	_f2
	/*
		|S		float			*	C		_f2;
	*/
	//NB: ahh, but a constexpr ivar *is* const.
	dummy=true;	//GREP1:p-vtype//	px	,,,	_s0
	/*
		|S		short				C		_s0;
	*/
	dummy=true;	//GREP1:p-vtype//	px	,,,	_s1
	/*
		|S		short						_s1[0];
	*/
	dummy=true;	//GREP1:p-vtype//	px	,,,	_s2
	/*
				short						_s2[3];
	*/


/*______________________________________________________________
####################  VvXX  ####################################
*/
	VvXX vx;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v0
	/*
		|S		int					 V		_v0;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v1
	/*
				int					 V		_v1[15];
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v2
	/*
				int			C	*	 V		_v2;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v3
	/*
				int			C	*	 V		_v3[13];
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v4
	/*
				int			C 	*	CV		_v4;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v5
	/*
				int			 V	*			_v5;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v6
	/*
				int			 V	*	 V		_v6;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v7
	/*
				int			CV	*			_v7;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v8
	/*
				int			CV	*	 V		_v8;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_v9
	/*
				int			CV	*	CV		_v9;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_vA
	/*
				int			 V	*	C		_vA;
	*/
	dummy=true;	//GREP1:p-vtype//	vx	,,,	_vB
	/*
				int			CV	*	C		_vB;
	*/


/*______________________________________________________________
####################  EeXX  ####################################
*/
	EeXX ex;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	ex	,,,	_e0
	/*
		|S		std::string					_e0;
	*/
	dummy=true;	//GREP1:p-vtype//	ex	,,,	_e1
	/*
				std::string					_e1;
	*/
	dummy=true;	//GREP1:p-vtype//	ex	,,,	_e2
	/*
		std::vector<std::wstring>			_e2;
	*/
	dummy=true;	//GREP1:p-vtype//	ex	,,,	_e3
	/*
		std::tuple<float,bool,DdXX*>		_e3[11];
	*/
	dummy=true;	//GREP1:p-vtype//	ex	,,,	_e4
	/*
		std::list<long>			*			_e4;
	*/


/*______________________________________________________________
####################  MmXX  ####################################
*/
	MmXX mx;

	// Since here we're focusing on nexted classes:
	dummy=true;		//CMD:set//		x-nested-datamemb full
	/*
	*/

/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	mx		,,,	_m1
	/*
	std::list<EeXX *>::const_iterator			_m1;
	*/

	dummy=true;	//GREP1:p-vtype//	mx		,,,	_m2
	/*
	std::list<MmXX *>::const_iterator 			_m2;
	*/
//

	dummy=true;	//GREP1:p-vtype//	mx		,,,	_m4
	/*
				@TOPLEV@::FfXX 					_m4;
	*/

//
//======> "@TOPLEV" refers to MmXX when we "p-vtype mx",
//======>     but to MmXX::FfXX when we "p-vtype" mx._m4 !
//
	dummy=true;	//GREP1:p-vtype//	mx._m4	,,,	_pnext
	/*
				@TOPLEV@ 		*				_pnext;
	*/

	dummy=true;	//GREP1:p-vtype//	mx		,,,	_m6
	/*
				std::list<MmXX::FfXX>			_m6;
	*/

	dummy=true;		//CMD:set//		x-nested-datamemb omit
	/*
	*/


/*______________________________________________________________
####################  JjXX<TtXX,TtNN>  #########################
*/
	JjXX<float,7>                    jax;
	JjXX<double,0>                   jbx;
	JjXX<float *,7>                  jcx;
	JjXX<const float *,7>            jdx;
	JjXX<std::string,7>              jex;
	JjXX<std::list<std::wstring>,0>  jfx;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	jax		,,,	_j0
	/*
				#0#				C	*			_j0;
	*/
	dummy=true;	//GREP1:p-vtype//	jax		,,,	_j1
	/*
				#0#					*			_j1;
	*/

	dummy=true;	//GREP1:p-vtype//	jax		,,,	_j3
	/*
				double							_j3[7];
	*/
//======> We could "_j3[#1#]" here but don't --- not
//======>     with "x-heur-abbr on".

	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j0
	/*
				#0#				C	*			_j0;
	*/

	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j3
	/*
				#0#   							_j3[0];
	*/

//======> That was jbx._j3 with "x-heur-abbr on" ...

	dummy=true;		//CMD:set//		x-heur-abbr off
	/*
	*/

//======> But now see jbx._j3 with "x-heur-abbr off" !

	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j3
	/*
				double							_j3[0];
	*/

//======> Sadly note, jbx._j2 affected by "x-heur-abbr off" too:
//======>    an unintended casualty.
	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j2
	/*
				double				*			_j2[0];
	*/
//======> ...And back to your regularly scheduled x-heur-abbr.
	dummy=true;		//CMD:set//		x-heur-abbr on
	/*
	*/

	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j2
	/*
				#0#					*			_j2[0];
	*/

//======> Underscoring that type of jbx is "JjXX<double,0>"

	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j5
	/*
	std::array<#0#,0>							_j5;
	*/
//======> Be kinda cool to "std::array<@TOPLEV@>"
//======>     here, but case too rare to bother with.

	dummy=true;	//GREP1:p-vtype//	jbx		,,,	_j6
	/*
	std::array<JjXX<double,0>,0>				_j6;
	*/

//======> The types we print for _j0 and _j1 of jcx and
//======>    jdx should be same as for _j0 and _j1 of jax.
	dummy=true;	//GREP1:p-vtype//	jcx		,,,	_j0
	/*
				#0#				C	*			_j0;
	*/
	dummy=true;	//GREP1:p-vtype//	jcx		,,,	_j1
	/*
				#0#					*			_j1;
	*/
	dummy=true;	//GREP1:p-vtype//	jdx		,,,	_j0
	/*
				#0#				C	*			_j0;
	*/
	dummy=true;	//GREP1:p-vtype//	jdx		,,,	_j1
	/*
				#0#					*			_j1;
	*/

	dummy=true;	//GREP1:p-vtype//	jex		,,,		_j5
	/*
	std::array<#0#,7>								_j5;
	*/
///TODO///		dummy=true;	//GREP1:p-vtype//	jex		,,,		_j6
///TODO///		/*
///TODO///		std::array<JjXX<std::string,7>,7>				_j6;
///TODO///		*/

	dummy=true;	//GREP1:p-vtype//	jfx		,,,		_j5
	/*
	std::array<#0#,0>								_j5;
	*/
///TODO///		dummy=true;	//GREP1:p-vtype//	jfx		,,,		_j6
///TODO///		/*
///TODO///		std::array<JjXX<std::list<std::wstring>,0>,0>	_j6;
///TODO///		*/


/*______________________________________________________________
####################  ZzXX<ELEM,CONT>  #########################
*/
	ZzXX<float>                                zax;
	ZzXX<float,std::vector<float>>             zbx;
	ZzXX<float,std::list<float>>               zcx;
	ZzXX<double,std::list<double>>             zdx;
	ZzXX<std::wstring>                         zex;
	ZzXX<std::string, std::list<std::string>>  zfx;
	//
	ZzXX<float,std::deque<float>>              zhx;
	ZzXX<float,std::array<float,11>>           zix;
/*____________________________________________________________*/

//======> For all instances of all ZzXX instantiations, as
//======>     type of _z4 we ought print "#0#".
//
	dummy=true;	//GREP1:p-vtype//	zax		,,,		_z4
	/*
					#0#								_z4;
	*/
	dummy=true;	//GREP1:p-vtype//	zbx		,,,		_z4
	/*
					#0#								_z4;
	*/
	dummy=true;	//GREP1:p-vtype//	zcx		,,,		_z4
	/*
					#0#								_z4;
	*/
	dummy=true;	//GREP1:p-vtype//	zdx		,,,		_z4
	/*
					#0#								_z4;
	*/
	dummy=true;	//GREP1:p-vtype//	zex		,,,		_z4
	/*
					#0#								_z4;
	*/
	dummy=true;	//GREP1:p-vtype//	zfx		,,,		_z4
	/*
					#0#								_z4;
	*/

//======> For all instances of all ZzXX instantiations, as
//======>     type of _z7 we ought print "@TOPLEV@ * [1]".
//
	dummy=true;	//GREP1:p-vtype//	zax		,,,		_z7
	/*
					@TOPLEV@		*				_z7[1];
	*/
	dummy=true;	//GREP1:p-vtype//	zbx		,,,		_z7
	/*
					@TOPLEV@		*				_z7[1];
	*/
	dummy=true;	//GREP1:p-vtype//	zcx		,,,		_z7
	/*
					@TOPLEV@		*				_z7[1];
	*/
	dummy=true;	//GREP1:p-vtype//	zdx		,,,		_z7
	/*
					@TOPLEV@		*				_z7[1];
	*/
	dummy=true;	//GREP1:p-vtype//	zex		,,,		_z7
	/*
					@TOPLEV@		*				_z7[1];
	*/
	dummy=true;	//GREP1:p-vtype//	zfx		,,,		_z7
	/*
					@TOPLEV@		*				_z7[1];
	*/

//======> Be neat if "std::set<#1::iterator>" for _z5, and
//======>    "std::list<#1::const_iterator>" for _z6; oh sure.
//
///TODO///		dummy=true;	//GREP1:p-vtype//	zax		,,,		_z5
///TODO///		/*
///TODO///		std::set<std::vector<float>::iterator>			_z5;
///TODO///		*/
///TODO///		dummy=true;	//GREP1:p-vtype//	zax		,,,		_z6
///TODO///		/*
///TODO///		std::list<std::vector<float>::const_iterator>	_z6;
///TODO///		*/
//
///TODO///		dummy=true;	//GREP1:p-vtype//	zbx		,,,		_z5
///TODO///		/*
///TODO///		std::set<std::vector<float>::iterator>			_z5;
///TODO///		*/
///TODO///		dummy=true;	//GREP1:p-vtype//	zbx		,,,		_z6
///TODO///		/*
///TODO///		std::list<std::vector<float>::const_iterator>	_z6;
///TODO///		*/
//
///TODO///		dummy=true;	//GREP1:p-vtype//	zcx		,,,		_z5
///TODO///		/*
///TODO///		std::set<std::list<float>::iterator>			_z5;
///TODO///		*/
///TODO///		dummy=true;	//GREP1:p-vtype//	zcx		,,,		_z6
///TODO///		/*
///TODO///		std::list<std::list<float>::const_iterator>		_z6;
///TODO///		*/

	dummy=true;	//GREP1:p-vtype//	zex		,,,			_z8
	/*
	std::set<#0#>										_z8;
	*/
///TODO///			dummy=true;	//GREP1:p-vtype//	zex		,,,			_z9
///TODO///			/*
///TODO///			std::map<#0#, #1#>									_z9;
///TODO///			*/
///TODO///		
///TODO///			dummy=true;	//GREP1:p-vtype//	zfx		,,,			_z9
///TODO///			/*
///TODO///			std::map<#0#, #1#>									_z9;
///TODO///			*/

//======> For all instances of all ZzXX instantiations, as
//======>     type of _z0 we ought print "#1#::iterator" ...in my dreams!?!?
//
	dummy=true;	//GREP1:p-vtype//	zax		,,,		_z0
	/*
		std::vector<float>::iterator				_z0;
	*/
	dummy=true;	//GREP1:p-vtype//	zbx		,,,		_z0
	/*
		std::vector<float>::iterator				_z0;
	*/
	dummy=true;	//GREP1:p-vtype//	zcx		,,,		_z0
	/*
		std::list<float>::iterator					_z0;
	*/
	dummy=true;	//GREP1:p-vtype//	zhx		,,,		_z0
	/*
		std::deque<float>::iterator					_z0;
	*/
	dummy=true;	//GREP1:p-vtype//	zix		,,,		_z0
	/*
		std::array<float,11>::iterator				_z0;
	*/
//
	dummy=true;	//GREP1:p-vtype//	zax		,,,		_z1
	/*
		std::vector<float>::const_iterator			_z1;
	*/
	dummy=true;	//GREP1:p-vtype//	zbx		,,,		_z1
	/*
		std::vector<float>::const_iterator			_z1;
	*/
	dummy=true;	//GREP1:p-vtype//	zcx		,,,		_z1
	/*
		std::list<float>::const_iterator			_z1;
	*/
	dummy=true;	//GREP1:p-vtype//	zhx		,,,		_z1
	/*
		std::deque<float>::const_iterator			_z1;
	*/
	dummy=true;	//GREP1:p-vtype//	zix		,,,		_z1
	/*
		std::array<float,11>::const_iterator		_z1;
	*/
//
//TODO: Tests for _z[01] of z[ef]x and _z[23] of z[abcdefhi]x,
//TODO      once *above* works!


/*______________________________________________________________
####################  NoRevZzXX<ELEM,CONT>  ####################
*/
	NoRevZzXX<float,std::set<float>>           zjx;
	NoRevZzXX<float,std::unordered_set<float>> zkx;
	NoRevZzXX<float,std::forward_list<float>>  zlx;
/*____________________________________________________________*/
	dummy=true;	//GREP1:p-vtype//	zjx		,,,		_nrz0
	/*
		std::set<float>::iterator					_nrz0;
	*/
	dummy=true;	//GREP1:p-vtype//	zkx		,,,		_nrz0
	/*
		std::unordered_set<float>::iterator			_nrz0;
	*/
	dummy=true;	//GREP1:p-vtype//	zlx		,,,		_nrz0
	/*
		std::forward_list<float>::iterator			_nrz0;
	*/
//
	dummy=true;	//GREP1:p-vtype//	zjx		,,,		_nrz1
	/*
		std::set<float>::const_iterator				_nrz1;
	*/
	dummy=true;	//GREP1:p-vtype//	zkx		,,,		_nrz1
	/*
		std::unordered_set<float>::const_iterator	_nrz1;
	*/
	dummy=true;	//GREP1:p-vtype//	zlx		,,,		_nrz1
	/*
		std::forward_list<float>::const_iterator	_nrz1;
	*/


	return 0;
}
