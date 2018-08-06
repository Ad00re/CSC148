"""Unit test for recommender_functions.movies_to_users"""
import unittest

from recommender_functions import movies_to_users

class TestMoviesToUsers(unittest.TestCase):

    def test_movies_to_users(self):
        """
        default test case
        """
        actual = movies_to_users({1: {10: 3.0}, 2: {10: 3.5}})
        expected = {10: [1, 2]}
        self.assertEqual(actual, expected)

    def test_movies_to_users1(self):
        """
        no movie
        """
        actual = movies_to_users({1: {10: 3.0}, 2: {10: 3.5}})
        expected = {10: [1, 2]}
        self.assertEqual(actual, expected)

    def test_movies_to_users2(self):
        """
        single movie no user
        """
        actual = movies_to_users({1: {}})
        expected = {}
        self.assertEqual(actual, expected)

    def test_movies_to_users3(self):
        """
        single movie one user
        """
        actual = movies_to_users({1: {10: 3.0}})
        expected = {10: [1]}
        self.assertEqual(actual, expected)

    def test_movies_to_users4(self):
        """
        single movie with muliple user
        """
        actual = movies_to_users({1: {10: 3.0, 5: 4.0}})
        expected = {10: [1], 5: [1]}
        self.assertEqual(actual, expected)

    def test_movies_to_users5(self):
        """
        mutiple movie with no user
        """
        actual = movies_to_users({1: {}, 2: {}})
        expected = {}
        self.assertEqual(actual, expected)

    def test_movies_to_users_muti6(self):
        """
        mutiple movie and one_user
        """
        actual = movies_to_users({1: {10: 3.0}, 2: {10: 3.5}})
        expected = {10: [1, 2]}
        self.assertEqual(actual, expected)

    def test_movies_to_users_muti7(self):
        """
        mutiple movie muliple user
        """
        actual = movies_to_users({1: {10: 3.0}, 2: {9: 3.5}})
        expected = {10: [1], 9: [2]}
        self.assertEqual(actual, expected)

    # Add tests below to create a complete set of tests without redundant tests
    # Redundant tests are tests that would only catch bugs that another test
    # would also catch.

if __name__ == '__main__':

    unittest.main(exit=False)
