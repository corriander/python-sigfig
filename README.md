Significant Figures in Python
=============================

This repository contains a couple of functions of dubious merit
related to significant figures.

  - `sigfig.string()` returns a (decimal) string representation of a
    float with *n* significant figures. 
  - `sigfig.round_()` rounds floats (sort of) to *n* significant
    figures.
  - `sigfig.scientific()` is a wrapper for scientific notation.
  - `sigfig.general()` is a wrapper for general form without zero
    truncation.

Further Details
---------------

Floating point numbers can be represented in terms of significant
figures in both the old and new string formatting syntaxes.
Significant digits are explicit in scientific notation, so if we have
`n` significant figures, we can specify a precision `p` in the
scientific notation where `p = n - 1`.

	>>> x = 0.0120076

The significant figures of `x` are 0.0[120076], so `x` expressed to
3 significant figures *should be* 0.0120. This can be expressed
correctly in scientific notation: 

	>>> '%.2e' % x	# general form: '%.pe' where p = n - 1
	'1.20e-02'
	>>> '{:.2e}'.format(x)
	'1.20e-02'

When scientific notation is not desirable, Python also provides a
"general form" syntax where `p` is the *number of significant
figures*:

	>>> '%.3g' % x
	'0.012'
    >>> '{:.3g}'.format(x)                                             
    '0.012'

Neither of these are correct. The reason can be seen in [the
docs][formatspec] describing the general form behaviour:

> The precise rules are as follows: suppose that the result formatted
> with presentation type `'e'` and precision `p-1` would have exponent
> `exp`. Then if `-4 <= exp < p`, the number is formatted with
> presentation type `'f'` and precision `p-1-exp`. Otherwise, the
> number is formatted with presentation type `'e'` and precision
> `p-1`. **In both cases insignificant trailing zeros are removed from
> the significand**, and the decimal point is also removed if there are
> no remaining digits following it.

I emphasised the important bit. The general form treats trailing zeros
in the mantissa as insignificant. This is not terribly unreasonable
but it is misleading. Consider:

	>>> '%.16f' % 2.007
	'2.0070000000000001'

Here, any zero at or after the 5th digit (i.e. 2.007[0...]) is
technically "insignificant" in the context of the floating point
representation of the decimal. However, this has the unfortunate side
effect of treating all trailing zeros after truncation as
insignificant:

	>>> '%.2g' % 2.007
	'2'

This is simply incorrect. *Fortunately*, an "alternate form" of the
general form is provided:

	>>> '%#.2g' % 2.007
	'2.0'

However, the format equivalent of this does not exist in `2.7.x`
according to the documentation (and tested on `2.7.3`). The alternate
form flag `#` is only applicable to integers. It *does* exist in the
format specification in `3.2.3` (and although this is preferred, the
old style string formatting is still present). The alternate form is
correct (although it will allow for "insignificant" figures in floats
to find their way into the representation; cake, can't have and eat). 

So why these functions?

  - I'd already written this before digging deep enough to find the
    alternate form is present across Python releases. Sigh.
  - There are some edge cases when it's desirable to force the
    representation in decimal, rather than scientific
	notation/standard form.
  - There is some potential for porting this to other languages
    which aren't quite so full featured (Scilab, I'm looking at you).

Finally, these come with tests but performance has not been looked at.
It may, for example, be more efficient to perform the dodgy maths than
use the string formatting as a jumping-off point.

Also, I'd like to give some
[credit](https://github.com/randlet/to-precision) here as this was the
best attempt at resolving this I encountered on my digging and it
helped confirm the funky behaviour of `'g'` in the format spec.

[formatspec]: http://docs.python.org/2/library/string.html#format-specification-mini-language
