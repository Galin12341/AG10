"""
Utility functions with code quality and security issues
"""

import hashlib
import random


def weak_password_hash(password):
    """Security Issue: Using MD5 for password hashing"""
    return hashlib.md5(password.encode()).hexdigest()


def generate_token():
    """Security Issue: Weak random number generation"""
    return random.randint(1000, 9999)


def validate_input(user_input):
    """Code quality issue: No actual validation"""
    pass


# Code quality issue: Unused imports and variables
import sys
import json
import time

unused_var = "This is never used"
ANOTHER_UNUSED = 42


# Code quality issue: Too complex function
def complex_function(a, b, c, d, e):
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    if e > 0:
                        return a + b + c + d + e
                    else:
                        return a + b + c + d
                else:
                    return a + b + c
            else:
                return a + b
        else:
            return a
    else:
        return 0


# Code quality issue: Poor naming
def f(x,y):
    return x+y


# Security issue: Using assert for validation
def check_admin(user):
    assert user.is_admin, "User must be admin"
    return True
