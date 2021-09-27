import requests
import unittest
import os
import shutil
import tempfile


class TestBase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def assertEqualDecode(self, output, checkStr):
        self.assertEqual(output.decode("utf-8"), checkStr)


if __name__ == "__main__":
    unittest.main()
