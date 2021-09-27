import os
import subprocess
import unittest

from tests.testbase import TestBase


class TestLS(TestBase):
    def test_ls(self):
        filepath1 = os.path.join(self.test_dir, "toost1.gif")
        filepath2 = os.path.join(self.test_dir, "toost2.gif")
        filepath3 = os.path.join(self.test_dir, "toost3.gif")
        with open(filepath1, "w") as f:
            f.write("kirby")
        with open(filepath2, "w") as f:
            f.write("wario")
        with open(filepath3, "w") as f:
            f.write("princess peach")
        subprocess.run(["./Shopository", "push", filepath1], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath2], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath3], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath3], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath3], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath3], stdout=subprocess.DEVNULL)
        result = subprocess.run(["./Shopository", "ls"], capture_output=True)
        checkStr = """Index: 0, Image Name: toost1.gif
Index: 1, Image Name: toost2.gif
Index: 2, Image Name: toost3.gif
Index: 3, Image Name: toost3.gif
Index: 4, Image Name: toost3.gif
Index: 5, Image Name: toost3.gif
"""
        self.assertEqualDecode(result.stdout, checkStr)
        subprocess.run(
            ["./Shopository", "remove", "2", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "3", "--yes"], stdout=subprocess.DEVNULL
        )
        result = subprocess.run(["./Shopository", "ls"], capture_output=True)
        checkStr = """Index: 0, Image Name: toost1.gif
Index: 1, Image Name: toost2.gif
Index: 4, Image Name: toost3.gif
Index: 5, Image Name: toost3.gif
"""
        self.assertEqualDecode(result.stdout, checkStr)
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "1", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "4", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "5", "--yes"], stdout=subprocess.DEVNULL
        )
        result = subprocess.run(["./Shopository", "ls"], capture_output=True)
        self.assertEqualDecode(result.stdout, "\n")


if __name__ == "__main__":
    unittest.main()
