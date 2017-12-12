"""
This file contains testcases for the validator functions
"""

import unittest
from validator import validate_name, validate_password


class ValidatorTestCase(unittest.TestCase):
    """ this clas contains test for validations"""

    def test_valid_username(self):
        """ this testcase is for a username with uppercase and
            lowercase letters"""
        result = validate_name("Chris")
        # assertion to check for the result output
        self.assertEqual(result, "Valid Name")

    def test_valid_username_withnumbers(self):
        """this testcase is used for username with both lowercase
            text and numbers"""
        result = validate_name("chris21")
        # assertion of the output value
        self.assertEqual(result, "Valid Name")
    
    def test_valid_username_lowercase(self):
        """ this testcase is for lowercase."""
        result = validate_name("chris")
        self.assertEqual(result, "Valid Name")

    def test_valid_username_uppercase(self):
        """ this testcase id for upppercase"""
        result = validate_name("CHRIS")
        self.assertEqual(result, "Valid Name")

    def test_valid_password(self):
        """ this testcase if for password"""
        result = validate_password("qwert12")
        self.assertEqual(result, "Valid password")

    def test_invalid_password(self):
        """ this test is for an invalid password"""
        result = validate_password("qwert")
        self.assertEqual(result, "not strong enough")