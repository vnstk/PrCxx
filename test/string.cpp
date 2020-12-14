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

int main ( )
{	bool dummy;

	const char  nulChar_plain =  '\0';
	const wchar_t   nulChar_w = L'\0';
	const char16_t nulChar_16 = u'\0';
	const char32_t nulChar_32 = U'\0';

	static
	const char  qChar_plain =  'q';
	const wchar_t   qChar_w = L'q';
	const char16_t qChar_16 = u'q';
	const char32_t qChar_32 = U'q';

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


/**************************************************************/
/** Check printing of empties. ********************************/
/**************************************************************/

	std::string     s_plain_empty;								//CMD:p//	s_plain_empty
	/*
					""
	*/
	std::wstring        s_w_empty;								//CMD:p//	s_w_empty
	/*
					L""
	*/
	std::u16string     s_16_empty;								//CMD:p//	s_16_empty
	/*
					u""
	*/
	std::u32string     s_32_empty;								//CMD:p//	s_32_empty
	/*
					U""
	*/


/**************************************************************/
/** Check that avoid Dummheit of strlen(c_str()) to get size. */
/**************************************************************/
{
	std::string     s_plain_small{ "b\0unnies", 8U};	//CMD:q-count-elems//	s_plain_small
	/*
					8
	*/
	std::wstring        s_w_small{L"bun\0nies", 8U};	//CMD:q-count-elems//	s_w_small
	/*
					8
	*/
	std::u16string     s_16_small{u"bunn\0ies", 8U};	//CMD:q-count-elems//	s_16_small
	/*
					8
	*/
	std::u32string     s_32_small{U"bunni\0es", 8U};	//CMD:q-count-elems//	s_32_small
	/*
					8
	*/
	dummy=true;
}

	std::string     s_plain_small{ "xyz"};
	std::wstring        s_w_small{L"xyz"};
	std::u16string     s_16_small{u"xyz"};
	std::u32string     s_32_small{U"xyz"};

/**************************************************************/
/** Sanity-check iterator standing.  Could use much more testing on this. */
/**************************************************************/

/*______________________________________________________________________________________________*/
	s_plain_small.reserve(10U);		{
	auto ita_plain_small = s_plain_small.begin();	//CMD:q-iter-into//		s_plain_small ita_plain_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;							//CMD:q-iter-into//	   s_from_cs_plain_large_off3 ita_plain_small
	/*
					outOfBounds
	*/
	auto itb_plain_small = s_plain_small.end();		//CMD:q-iter-into//		s_plain_small itb_plain_small
	/*
					withinBounds_but_invalid
	*/
	--itb_plain_small;								//CMD:q-iter-into//		s_plain_small itb_plain_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;						}

/*______________________________________________________________________________________________*/
	s_w_small.reserve(10U);			{
	auto ita_w_small = s_w_small.begin();			//CMD:q-iter-into//		s_w_small ita_w_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;							//CMD:q-iter-into//		s_from_cs_w_large_off3 ita_w_small
	/*
					outOfBounds
	*/
	auto itb_w_small = s_w_small.end();				//CMD:q-iter-into//		s_w_small itb_w_small
	/*
					withinBounds_but_invalid
	*/
	--itb_w_small;									//CMD:q-iter-into//		s_w_small itb_w_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;						}

/*______________________________________________________________________________________________*/
	s_16_small.reserve(10U);		{
	auto ita_16_small = s_16_small.begin();			//CMD:q-iter-into//		s_16_small ita_16_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;							//CMD:q-iter-into//		s_from_cs_16_large_off3 ita_16_small
	/*
					outOfBounds
	*/
	auto itb_16_small = s_16_small.end();			//CMD:q-iter-into//		s_16_small itb_16_small
	/*
					withinBounds_but_invalid
	*/
	--itb_16_small;									//CMD:q-iter-into//		s_16_small itb_16_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;						}

/*______________________________________________________________________________________________*/
	s_32_small.reserve(0U);		{
	auto ita_32_small = s_32_small.begin();			//CMD:q-iter-into//		s_32_small ita_32_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;							//CMD:q-iter-into//		s_from_cs_32_large_off3 ita_32_small
	/*
					outOfBounds
	*/
	auto itb_32_small = s_32_small.end();			//CMD:q-iter-into//		s_32_small itb_32_small
	/*
					withinBounds_but_invalid
	*/
	--itb_32_small;									//CMD:q-iter-into//		s_32_small itb_32_small
	/*
					withinBounds_and_valid
	*/
	dummy=true;						}



	/* Text excerpt is from https://en.cppreference.com, copyrighted as per their FAQ. */
	std::string s_plain_large{"A pattern followed by an ellipsis, in which the name of at least one parameter pack appears at least once, is expanded into zero or more comma-separated instantiations of the pattern, where the name of the parameter pack is replaced by each of the elements from the pack, in order."
			"If the names of two parameter packs appear in the same pattern, they are expanded simultaneously, and they must have the same length:"
			"If a pack expansion is nested within another pack expansion, the parameter packs that appear inside the innermost pack expansion are expanded by it, and there must be another pack mentioned in the enclosing pack expansion, but not in the innermost one:"
};

	std::string copy_s_plain_large{s_plain_large};
	copy_s_plain_large.clear();									//CMD:p//	copy_s_plain_large
	/*
					""
	*/


/*
	std::string::iterator it_emptystr = emptystr.begin();
	std::string::iterator it_bunnystr = bunnystr.begin();
	++it_bunnystr;
	auto cit_bunnystr = bunnystr.cbegin();
	auto endit_bunnystr = bunnystr.cend();

	std::wstring widexy{wxy_c_str};
	std::wstring widepi = std::to_wstring(3.14159);
	std::u32string quadbunnies{U"bunnies"};
	std::u32string quadxy{U'x', U'y', U'\0'};
*/


	return 0;
}
