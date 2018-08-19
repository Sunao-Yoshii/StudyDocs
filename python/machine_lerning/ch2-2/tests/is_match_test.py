import unittest
import lernstok


class TestIsMatch(unittest.TestCase):
    def test_2_matches_1(self):
        actual = lernstok.is_match(
            [1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            '1')
        self.assertEqual(True, actual)

    def test_2_matches_0(self):
        actual = lernstok.is_match(
            [1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            '1')
        self.assertEqual(True, actual)

    def test_0_matches_0_only(self):
        actual = lernstok.is_match(
            [1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            '0')
        self.assertEqual(True, actual)

    def test_1_matches_1_only(self):
        actual = lernstok.is_match(
            [1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            '0')
        self.assertEqual(True, actual)

    def test_other_are_no_match(self):
        actual = lernstok.is_match(
            [1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            '1')
        self.assertEqual(False, actual)


if __name__ == '__main__':
    unittest.main()
