# -*- coding: utf-8 -*-

from .context import lib

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(lib.hmm())


if __name__ == '__main__':
    unittest.main()
