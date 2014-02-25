from collections import namedtuple
import unittest
from .. import sigfig

TestNum = namedtuple('TestNum', 'value, sf_range')

class TestString(unittest.TestCase):

	def _test(self, test_num):
		for n, expected in test_num.sf_range.items():
			self.assertEqual(sigfig.string(test_num.value, n), expected)

	def test_invalid_n(self):
		x = 128371.131
		self.assertRaises(ValueError, sigfig.string, x, 0)
		self.assertRaises(ValueError, sigfig.string, x, -1)

	def test_zero_exponent(self):
		g = TestNum(9.80665, {
					8 : '9.8066500',
					6 : '9.80665',
					5 : '9.8066', 	# Rounding down built in behaviour
					4 : '9.807',
					3 : '9.81',
					2 : '9.8',
					1 : '10'})
		self._test(g)
	
	def test_positive_exponent(self):
		P = TestNum(101325, {
					8 : '101325.00',
					7 : '101325.0',
					6 : '101325',
					5 : '101320',	# Rounding down built in behaviour
					3 : '101000',
					2 : '100000',
					1 : '100000'}) 
		self._test(P)

	def test_positive_exponent_with_mantissa(self):
		R = TestNum(8314.4621, {
					10 : '8314.462100',
					8 : '8314.4621',
					6 : '8314.46',
					5 : '8314.5',
					4 : '8314',
					2 : '8300',
					1 : '8000'})
		self._test(R)

	def test_small_negative_exponent(self):
		P = TestNum(0.101325, {
					8 : '0.10132500',
					6 : '0.101325',
					4 : '0.1013',
					1 : '0.1'})
		self._test(P)
		
	def test_medium_negative_exponent(self):
		R = TestNum(0.0083144621, {
					10 : '0.008314462100',
					8 : '0.0083144621',
					6 : '0.00831446',
					5 : '0.0083145',
					4 : '0.008314',
					2 : '0.0083',
					1 : '0.008'})
		self._test(R)
	
	def test_large_negative_exponent(self):
		G = TestNum(6.67384e-11, {
					7 : '0.00000000006673840',
					6 : '0.0000000000667384',
					3 : '0.0000000000667'})
	
	# -----------------------------------------------------------------
	# SPECIAL CASES
	# -----------------------------------------------------------------
	def test_rounding_internal_zero_up(self):
		g = 9.80665
		self.assertEqual(sigfig.string(g, 3), '9.81')

	def test_rounding_internal_zero_down(self):
		x = 0.0021008
		self.assertEqual(sigfig.string(x, 3), '0.00210')

	def test_negative_with_mantissa(self):
		x = -1.010101
		self.assertEqual(sigfig.string(x, 3), '-1.01')
		self.assertEqual(sigfig.string(x, 1), '-1')

	def test_negative(self):
		x = -209837
		self.assertEqual(sigfig.string(x, 7), '-209837.0')
		self.assertEqual(sigfig.string(x, 3), '-210000')

class TestRound_(unittest.TestCase):

	def test_zero_exponent(self):
		x = 9.80665
		self.assertAlmostEqual(sigfig.round_(x, 5), 9.8066)
		self.assertAlmostEqual(sigfig.round_(x, 4), 9.807)
		self.assertAlmostEqual(sigfig.round_(x, 3), 9.81)
		self.assertAlmostEqual(sigfig.round_(x, 2), 9.8)
		self.assertEqual(sigfig.round_(x, 1), 10)
	
	def test_negative(self):
		x = -9.80665
		self.assertAlmostEqual(sigfig.round_(x, 5), -9.8066)
		self.assertAlmostEqual(sigfig.round_(x, 4), -9.807)
		self.assertAlmostEqual(sigfig.round_(x, 3), -9.81)
		self.assertAlmostEqual(sigfig.round_(x, 2), -9.8)
		self.assertEqual(sigfig.round_(x, 1), -10)
	
	def test_positive_exponent(self):
		x = 101325 
		self.assertEqual(sigfig.round_(x, 7), 101325)
		self.assertEqual(sigfig.round_(x, 6), 101325)
		self.assertEqual(sigfig.round_(x, 5), 101320)
		self.assertEqual(sigfig.round_(x, 3), 101000)
		self.assertEqual(sigfig.round_(x, 2), 100000)
		self.assertEqual(sigfig.round_(x, 1), 100000) 

	def test_positive_exponent_with_mantissa(self):
		x = 8314.4621 
		self.assertAlmostEqual(sigfig.round_(x, 10), 8314.4621)
		self.assertAlmostEqual(sigfig.round_(x, 8), 8314.4621)
		self.assertAlmostEqual(sigfig.round_(x, 6), 8314.46)
		self.assertAlmostEqual(sigfig.round_(x, 5), 8314.5)
		self.assertEqual(sigfig.round_(x, 4), 8314)
		self.assertEqual(sigfig.round_(x, 2), 8300)
		self.assertEqual(sigfig.round_(x, 1), 8000)
		
	def test_medium_negative_exponent(self):
		x = 0.0083144621
		self.assertAlmostEqual(sigfig.round_(x, 10), 0.008314462100)
		self.assertAlmostEqual(sigfig.round_(x,	8), 0.0083144621)
		self.assertAlmostEqual(sigfig.round_(x,	6), 0.00831446)
		self.assertAlmostEqual(sigfig.round_(x,	5), 0.0083145)
		self.assertAlmostEqual(sigfig.round_(x,	4), 0.008314)
		self.assertAlmostEqual(sigfig.round_(x,	2), 0.0083)
		self.assertAlmostEqual(sigfig.round_(x,	1), 0.008)
	
if __name__ == '__main__':
	unittest.main()
