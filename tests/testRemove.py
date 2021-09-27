import os
import subprocess
import unittest

from tests.testbase import TestBase


class TestRemove(TestBase):
    def test_remove_success(self):
        filename = "bowser.jpeg"
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, "w") as f:
            f.write("mario")
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], capture_output=True
        )
        self.assertEqualDecode(result.stdout, "file 0 successfully deleted\n")
        self.assertFalse(os.path.exists(f"./images/{filename}"))

    def test_remove_bad_index(self):
        result = subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], capture_output=True
        )
        self.assertEqualDecode(
            result.stderr, 'Error 404. "This image id does not exist"\n\n'
        )

    def test_remove_confirmation(self):
        filename = "bowser.jpeg"
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, "w") as f:
            f.write("mario")
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(
            ["./Shopository", "remove", "0"], input=b"n", capture_output=True
        )
        self.assertEqualDecode(result.stderr, "Aborted!\n")
        result = subprocess.run(
            ["./Shopository", "remove", "0"], input=b"y", capture_output=True
        )
        self.assertEqualDecode(
            result.stdout,
            "This will permanently delete this image. Are you sure you want to continue? [y/N]: file 0 successfully deleted\n",
        )


if __name__ == "__main__":
    unittest.main()
