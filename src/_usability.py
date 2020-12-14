#                                          Copyright 2020 Vainstein K.
# --------------------------------------------------------------------
# This file is part of PrCxx.
# 
# PrCxx is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# PrCxx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with PrCxx.  If not, see <https://www.gnu.org/licenses/>.


# Gratefully adapted from
# http://blog.mathieu-leplatre.info/python-check-arguments-types.html
#
# Drawback: inserts itself into callstack; not efficient,
# and noise in dumped callstacks when debugging.
def accepts(*argstypes, **kwargstypes):
	def wrapper(func):
		def wrapped(*args, **kwargs):
			if len(args) > len(argstypes):
				raise TypeError("%s() takes at most %d non-keyword arguments; %d given" % (func.__name__, len(argstypes), len(args)))
			argspairs = zip(args, argstypes)
			for k,v in kwargs.items():
				if k not in kwargstypes:
					raise TypeError("Unexpected keyword argument [%s] for %s()" % (k, func.__name__))
				argspairs.append((v, kwargstypes[k]))
			for param, expected in argspairs:
				if param is not None and not isinstance(param, expected):
					raise TypeError("Parameter [%s] is not %s" % (param, expected.__name__))
			return func(*args, **kwargs)
		return wrapped
	return wrapper


# Gratefully adapted from
# http://blog.mathieu-leplatre.info/python-check-arguments-types.html
#
# Drawback: inserts itself into callstack; not efficient,
# and noise in dumped callstacks when debugging.
def returns(rtype):
	def wrapper(f):
		def wrapped(*args, **kwargs):
			result = f(*args, **kwargs)
			if not isinstance(result, rtype):
				raise TypeError("Return value [%r] is not a %s" % (result,rtype))
			return result
		return wrapped
	return wrapper


# If exceptions were a good idea, they'd've been in C.
def invoke_nothrow (func, *args, **kwargs):
	try:
		return func(*args, **kwargs)
	except BaseException as whatev:
		return None


def safe_ivar (obj, ivarName):
	if obj == None:
		return None
	return getattr(obj, ivarName, None)


def ternary (cond, x, y): # Emulate C's "cond ? x : y"
	if cond:
		return x
	else:
		return y

def nonNull (x, y): # Emulate C's "x ? x : y" (just "x ? : y" in GCCese)
	if x:
		return x
	else:
		return y

@returns(str)
def pyObjAddr (obj): # XXX how differs from id(obj) ???
	if obj == None:
		return '<NULL>'
	s = str(obj.__repr__())
	i = s.find(' at ')
	if -1 == i:
		return '<????>'
	return '<' + s[i+4:]

@returns(bool)
def xor (p, q):
	return (p or q) and (not (p and q))


def is_uint (x):
	import numbers
	assert (x != None)
	return isinstance(x, numbers.Integral) and (x >= 0)


@returns(bool)
def assert_bool (x):
	assert (x != None) and ((True == x) or (False == x))
	return x
#
@returns(bool)
def assert_bool_orNone (x):
	if x != None:
		assert             ((True == x) or (False == x))
	return x

@returns(int)
def assert_uint (x):
	import numbers
	assert (x != None) and (isinstance(x, numbers.Integral) and (x >= 0))
	return x
#
@returns(int)
def assert_uint_orNone (x):
	import numbers
	if x != None:
		assert             (isinstance(x, numbers.Integral) and (x >= 0))
	return x

@returns(str)
def assert_string (x):
	assert (x != None) and (isinstance(x, str))
	return x
#
@returns(str)
def assert_string_orNone (x):
	if x != None:
		 assert            (isinstance(x, str))
	return x


def make_pair (a, b):
	return (a,b)


def boolOrNone_to_char (x):
	if None == x:
		return '?'
	elif x:
		return 'T'
	else:
		return 'F'

def bool_to_char (x):
	if x:
		return 'T'
	else:
		return 'F'


def appendLine(path,s):
	outF = open("myOutFile.txt", "a")
	outF.write(s)
	outF.close()


def sprintf (fmtSpec, *varargs):
	if len(varargs):
		return fmtSpec % varargs
	else:
		return fmtSpec


import sys

def printf (fmtSpec, *varargs):
	print(sprintf(fmtSpec, *varargs), file=sys.stderr, end='')

def printf__toStdout (fmtSpec, *varargs):
	print(sprintf(fmtSpec, *varargs), file=sys.stdout, end='', flush=True)
