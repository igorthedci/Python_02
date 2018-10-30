import unittest
from HtmlTestRunner import HTMLTestRunner

s = """
aaaaaaa
bbbbbbb
cccccc
dddddd
"""

s2 = """
aaaaaaa
bbbbbbb
ccccccc
dddddd
"""
import sys

class OurClassTest(unittest.TestCase):
    @unittest.expectedFailure
    def test_method(self):
        self.assertEqual(s, s2)

    # @unittest.skipIf(sys.platform.startswith("win"), "не для Windows")
    def test_method_2(self):
        num = [12, 17, 0, 10]
        for n in num:
            with self.subTest(number=n):
                self.assertEqual(n % 2, 0)


# unittest.main(verbosity=3)
# test1 = OurClass("some_method")
# test2 = OurClass("some_method_2")
#
# suite = unittest.TestSuite([test1, test2])
#
# result = unittest.TestResult()
# suite.run(result)
#
# suite2 = unittest.TestLoader().loadTestsFromTestCase(OurClass)
# suite2.run(result)
# print(result)
# print(test2.run())

