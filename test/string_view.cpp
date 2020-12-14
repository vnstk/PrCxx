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
#include <string>
#include <string_view>


int main ( )
{	bool dummy;

	const char *const  cs_plain_empty =  "";
	static
	const wchar_t *const   cs_w_empty = L"";
	const char16_t *const cs_16_empty = u"";
	const char32_t *const cs_32_empty = U"";

	const char *const  cs_plain_small =  "xyz";
	const wchar_t *const   cs_w_small = L"xyz";
	static
	const char16_t *const cs_16_small = u"xyz";
	const char32_t *const cs_32_small = U"xyz";


	/* Text excerpt is from https://en.cppreference.com, copyrighted as per their FAQ. */
	const char *const cs_plain_large = "If the input has been parsed into preprocessing tokens up to a given character, the next preprocessing token is generally taken to be the longest sequence of characters that could constitute a preprocessing token, even if that would cause subsequent analysis to fail. This is commonly known as maximal munch.";
	const wchar_t *const cs_w_large = L"If the input has been parsed into preprocessing tokens up to a given character, the next preprocessing token is generally taken to be the longest sequence of characters that could constitute a preprocessing token, even if that would cause subsequent analysis to fail. This is commonly known as maximal munch.";
	const char16_t *const cs_16_large = u"If the input has been parsed into preprocessing tokens up to a given character, the next preprocessing token is generally taken to be the longest sequence of characters that could constitute a preprocessing token, even if that would cause subsequent analysis to fail. This is commonly known as maximal munch.";
	static
	const char32_t *const cs_32_large = U"If the input has been parsed into preprocessing tokens up to a given character, the next preprocessing token is generally taken to be the longest sequence of characters that could constitute a preprocessing token, even if that would cause subsequent analysis to fail. This is commonly known as maximal munch.";

	std::string  s_from_cs_plain_large_off3(cs_plain_large + 3U);
	std::wstring     s_from_cs_w_large_off3(    cs_w_large + 3U);
	std::u16string  s_from_cs_16_large_off3(   cs_16_large + 3U);
	std::u32string  s_from_cs_32_large_off3(   cs_32_large + 3U);

	std::string                   s_plain_empty;
	std::wstring                      s_w_empty;
	std::u16string                   s_16_empty;
	std::u32string                   s_32_empty;


/**************************************************************/
/** Try string_view objs constructed from string objs *********/
/**************************************************************/
	std::string_view    sv_plain_large(s_from_cs_plain_large_off3);

/*    deref of itA will be the char at offset 3, namely the first character of "the input..."
 *    */
	std::string_view::const_iterator itA = sv_plain_large.cbegin();		//CMD:p//	*itA
	/*
					116 't'
	*/

	std::wstring_view       sv_w_large(    s_from_cs_w_large_off3);
	std::u16string_view    sv_16_large(   s_from_cs_16_large_off3);
	std::u32string_view    sv_32_large(   s_from_cs_32_large_off3);



/**************************************************************/
/** Check printing of empties. ********************************/
/**************************************************************/
{
	std::string_view sv_plain_empty(s_plain_empty);				//CMD:p//	sv_plain_empty
	/*
					""
	*/
	std::string_view sv_plain_nada;								//CMD:p//	sv_plain_nada
	/*
					
	*/

	std::wstring_view  sv_w_empty(s_w_empty);					//CMD:p//	sv_w_empty
	/*
					L""
	*/
	std::wstring_view             sv_w_nada;					//CMD:p//	sv_w_nada
	/*
					
	*/

	std::u16string_view  sv_16_empty(s_16_empty);				//CMD:p//	sv_16_empty
	/*
					u""
	*/
	std::u16string_view  sv_16_nada;							//CMD:p//	sv_16_nada
	/*
					
	*/

	std::u32string_view  sv_32_empty(s_32_empty);				//CMD:p//	sv_32_empty
	/*
					U""
	*/
	std::u32string_view  sv_32_nada;							//CMD:p//	sv_32_nada
	/*
					
	*/
	dummy=true;
}

/**************************************************************/
/** Check that avoid Dummheit of strlen(c_str()) to get size. */
/** Also check for robustness after remove_suffix(), remove_prefix(),
    edge case where NUL is first elem, edge case where NUL is last. */
/** Also see what happens when **arg** to copy ctor is later modified. */
/**************************************************************/
{
	std::string_view  sv_plain_small{ "b\0unnies", 8U};  	//CMD:q-count-elems//	sv_plain_small
	/*
					8
	*/
	std::string_view  sv_plain_copy{sv_plain_small};
	sv_plain_small.remove_prefix(1U);						//CMD:q-count-elems//	sv_plain_small
	/*
					7
	*/
	dummy=true;												//CMD:q-count-elems//	sv_plain_copy
	/*
					8
	*/

	std::wstring_view   sv_w_small{L"bunn\0ies", 8U};		//CMD:q-count-elems//	sv_w_small
	/*
					8
	*/
	sv_w_small.remove_suffix(3U);							//CMD:q-count-elems//	sv_w_small
	/*
					5
	*/

	std::u16string_view  sv_16_small{u"bunn\0ies", 8U};		//CMD:q-count-elems//	sv_16_small
	/*
					8
	*/
	sv_16_small.remove_suffix(3);
	sv_16_small.remove_prefix(4);							//CMD:q-count-elems//	sv_16_small
	/*
					1
	*/

	std::u32string_view     sv_32_nada;
	std::u32string_view     sv_32_small{U"bunni\0es", 8U};	//CMD:q-count-elems//	sv_32_small
	/*
					8
	*/
	sv_32_nada.swap(sv_32_small);							//CMD:q-count-elems//	sv_32_small
	/*
					0
	*/
	dummy=true;
}


/**************************************************************/
/** Printing of string_view objs constructed from literals.  **/
/**************************************************************/
{
	std::string_view     sv_plain_small{ "xyz"};	//CMD:p//		sv_plain_small
	/*
					"xyz"
	*/
	std::wstring_view        sv_w_small{L"xyz"};	//CMD:p//		sv_w_small
	/*
					L"xyz"
	*/
	std::u16string_view     sv_16_small{u"xyz"};	//CMD:p//		sv_16_small
	/*
					u"xyz"
	*/
	std::u32string_view     sv_32_small{U"xyz"};	//CMD:p//		sv_32_small
	/*
					U"xyz"
	*/
	dummy=true;
}


/**************************************************************/
/** Sanity-check iterator standing.  Could use much more testing on this. */
/**************************************************************/
	std::string       s_plain_small__alt;
	s_plain_small__alt.append("x");
	s_plain_small__alt.append("y");
	s_plain_small__alt.append("z");
	// Roundabout assignment, to ensure compiler doesn't take shortcuts on our behalf here.

/*______________________________________________________________________________________________*/
	{
	std::string_view  sv_plain_small{ "bunnies" };

	auto ita = sv_plain_small.begin();		//CMD:q-iter-into//		sv_plain_small     ita
	/*
					withinBounds_and_valid
	*/
	std::string_view       sv_plain_smallAlt{s_plain_small__alt};
	auto itc = sv_plain_smallAlt.begin();	//CMD:q-iter-into//		sv_plain_smallAlt  ita
	/*
					outOfBounds
	*/
//Even though underly string is same!

	dummy=true;							//CMD:q-iter-into//	   	sv_plain_large     ita
	/*
					outOfBounds
	*/
	auto itb = sv_plain_small.end();	//CMD:q-iter-into//		sv_plain_small 		itb
	/*
					outOfBounds
	*/
	--itb;								//CMD:q-iter-into//		sv_plain_small 		itb
	/*
					withinBounds_and_valid
	*/
	dummy=true;						}


//Much addit'l testing would be much welcome, natch.  TODO, a marginal modicum at least, eh??


	return 0;
}
