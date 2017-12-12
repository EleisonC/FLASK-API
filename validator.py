"""this file contains methods that validate a username
and password
"""
import re


def validate_name(name):
    """This method is used to validate the username
    check if its fully string or string with numbers """
    name = str(name)
    validated_letter = []
    for n, letter in enumerate(name):
        letter = str(letter)
        if re.match(r'[A-Za-z]', letter) or\
                re.match(r'[A-Za-z0-9]', letter):
            validated_letter.append(letter)
    if len(name) == len(validated_letter):
        return 'Valid Name'
    return validated_letter


def validate_password(password):
    """This method is used to validate the password
    check if its strong enough with letters and numbers """
    if len(password) >= 6:
        password = str(password)
        validated_letter = []
        for n, letter in enumerate(password):
            if re.match(r'[a-zA-Z0-9]', letter):
                validated_letter.append(letter)
        if len(password) == len(validated_letter):
            return "Valid password"
    return "not strong enough"
