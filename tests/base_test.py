import os
import unittest

TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')


class BaseTest(unittest.TestCase):
    ...
