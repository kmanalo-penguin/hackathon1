import unittest
from .scoring import calculate_score, has_scoring_dice, get_valid_scoring_dice

class TestScoring(unittest.TestCase):
    def test_singles(self):
        self.assertEqual(calculate_score([1])[0], 100)
        self.assertEqual(calculate_score([5])[0], 50)
        self.assertEqual(calculate_score([1, 5])[0], 150)
        
    def test_three_of_a_kind(self):
        self.assertEqual(calculate_score([1, 1, 1])[0], 1000)
        self.assertEqual(calculate_score([2, 2, 2])[0], 200)
        self.assertEqual(calculate_score([3, 3, 3])[0], 300)
        self.assertEqual(calculate_score([4, 4, 4])[0], 400)
        self.assertEqual(calculate_score([5, 5, 5])[0], 500)
        self.assertEqual(calculate_score([6, 6, 6])[0], 600)
        
    def test_four_of_a_kind(self):
        self.assertEqual(calculate_score([2, 2, 2, 2])[0], 1000)
        self.assertEqual(calculate_score([1, 1, 1, 1])[0], 1000)
        
    def test_five_of_a_kind(self):
        self.assertEqual(calculate_score([3, 3, 3, 3, 3])[0], 2000)
        
    def test_six_of_a_kind(self):
        self.assertEqual(calculate_score([4, 4, 4, 4, 4, 4])[0], 3000)
        
    def test_three_pair(self):
        self.assertEqual(calculate_score([2, 2, 4, 4, 6, 6])[0], 1500)
        self.assertEqual(calculate_score([3, 3, 5, 5, 1, 1])[0], 1500)
        
    def test_run(self):
        self.assertEqual(calculate_score([1, 2, 3, 4, 5, 6])[0], 2500)
        
    def test_mixed(self):
        self.assertEqual(calculate_score([1, 1, 1, 5, 3, 4]), (1050, 4))
        
    def test_bust(self):
        self.assertFalse(has_scoring_dice([2, 3, 4, 6, 6, 2]))
        self.assertTrue(has_scoring_dice([1, 2, 3, 4, 5, 6]))
        self.assertTrue(has_scoring_dice([2, 2, 2, 3, 4, 6]))
        
    def test_valid_selection(self):
        self.assertTrue(get_valid_scoring_dice([1, 1, 1, 5]))
        self.assertFalse(get_valid_scoring_dice([1, 1, 1, 5, 3]))

if __name__ == '__main__':
    unittest.main()
