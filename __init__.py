"""this file contains methods that validate a username
and password
"""
import re


def validate_name(name):
    """This method is used to validate the username
    check if its fully string or string with numbers """
    validated_letter = []
    for letter in enumerate(name):
        if re.match(r'[A-Za-z]', letter) or re.match(r'[A-Za-z0-9]', letter):
            validated_letter.append(letter)
    if len(name) == len(validated_letter):
        return 'Valid Name'
    return 'Invalid Name'


def validate_password(password):
    """This method is used to validate the password
    check if its strong enough with letters and numbers """
    if len(password) >= 6:
        validated_letter = []
        for letter in enumerate(password):
            if re.match(r'[a-zA-Z0-9]', letter):
                validated_letter.append(letter)
        if len(password) == len(validated_letter):
            return "Valid password"
    return "not strong enough"
