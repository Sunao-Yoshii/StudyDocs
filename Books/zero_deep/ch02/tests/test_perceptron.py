# !/bin/python
from unittest import TestCase
import perceptrons as ps


class test_perceptron(TestCase):
    def test_and_1(self):
        self.assertEqual(ps.AND(1, 1), 1)
    
    def test_and_0(self):
        self.assertEqual(ps.AND(1, 0), 0)
        self.assertEqual(ps.AND(0, 1), 0)
        self.assertEqual(ps.AND(0, 0), 0)
    
    def test_nand_0(self):
        self.assertEqual(ps.NAND(1, 1), 0)

    def test_nand_1(self):
        self.assertEqual(ps.NAND(1, 0), 1)
        self.assertEqual(ps.NAND(0, 1), 1)
        self.assertEqual(ps.NAND(0, 0), 1)

    def test_or_0(self):
        self.assertEqual(ps.OR(0, 0), 0)
        
    def test_or_1(self):
        self.assertEqual(ps.OR(1, 0), 1)
        self.assertEqual(ps.OR(1, 1), 1)
        self.assertEqual(ps.OR(0, 1), 1)

    def test_xor_0(self):
        self.assertEqual(ps.XOR(1, 0), 1)
        self.assertEqual(ps.XOR(0, 1), 1)

    def test_xor_1(self):
        self.assertEqual(ps.XOR(0, 0), 0)
        self.assertEqual(ps.XOR(1, 1), 0)


