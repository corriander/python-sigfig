from math import floor, log10

def round_(x, n):
	"""Round a float, x, to n significant figures.

	Caution should be applied when performing this operation.
	Significant figures are an implication of precision; arbitrarily
	truncating floats mid-calculation is probably not Good Practice in
	almost all cases.

	Rounding off a float to n s.f. results in a float. Floats are, in
	general, approximations of decimal numbers. The point here is that
	it is very possible to end up with an inexact number:

		>>> roundsf(0.0012395, 3)
		0.00124
		>>> roundsf(0.0012315, 3)
		0.0012300000000000002

	Basically, rounding in this way probably doesn't do what you want
	it to.

	"""
	n = int(n)
	x = float(x)

	if x == 0: return 0

	e = floor(log10(abs(x)) - n + 1) # exponent, 10 ** e
	shifted_dp = x / (10 ** e) # decimal place shifted n d.p.  
	return round(shifted_dp) * (10 ** e) # round and revert

def string(x, n):
	"""Convert a float, x, to a string with n significant figures.

	This function returns a decimal string representation of a float
	to a specified number of significant figures.

		>>> create_string(9.80665, 3)
		'9.81'
		>>> create_string(0.0120076, 3)
		'0.0120'
		>>> create_string(100000, 5)
		'100000'

	Note the last representation is, without context, ambiguous. This
	is a good reason to use scientific notation, but it's not always
	appropriate.

	Note
	----

	Performing this operation as a set of string operations arguably
	makes more sense than a mathematical operation conceptually. It's
	the presentation of the number that is being changed here, not the
	number itself (which is in turn only approximated by a float).

	"""
	n = int(n)
	x = float(x)

	if n < 1: raise ValueError("1+ significant digits required.")

	# retrieve the significand and exponent from the S.N. form
	s, e = ''.join(( '{:.', str(n - 1), 'e}')).format(x).split('e')
	e = int(e) # might as well coerce now

	if e == 0:
		# Significand requires no adjustment
		return s

	s = s.replace('.', '')
	if e < 0:
		# Placeholder zeros need creating 
		return ''.join(('0.', '0' * (abs(e) - 1), s))
	else:
		# Decimal place need shifting
		s += '0' * (e - n + 1) # s now has correct s.f.
		i = e + 1
		sep = ''
		if i < n: sep = '.'
		if s[0] is '-': i += 1
		return sep.join((s[:i], s[i:]))

def scientific(x, n):
	"""Represent a float in scientific notation.

	This function is merely a wrapper around the 'e' type flag in the
	formatting specification.

	"""
	n = int(n)
	x = float(x)
	
	if n < 1: raise ValueError("1+ significant digits required.")

	return ''.join(('{:.', str(n - 1), 'e}')).format(x)

def general(x, n):
	"""Represent a float in general form.

	This function is merely a wrapper around the 'g' type flag in the
	formatting specification.

	"""
	n = int(n)
	x = float(x)

	if n < 1: raise ValueError("1+ significant digits required.")

	return ''.join(('{:#.', str(n), 'g}')).format(x)
