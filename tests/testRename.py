import os
import subprocess
import unittest

from tests.testbase import TestBase


class TestRename(TestBase):
    def test_rename_success(self):
        filepath = os.path.join(self.test_dir, "bowser.jpeg")
        new_name = "wario.jpeg"
        pulled_file = f"./{new_name}"
        with open(filepath, "w") as f:
            f.write("mario")
        if os.path.exists(pulled_file):
            os.remove(pulled_file)
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(
            ["./Shopository", "rename", "0", new_name], capture_output=True
        )
        self.assertEqualDecode(
            result.stdout, f"file 0 successfully renamed to {new_name}\n"
        )
        subprocess.run(
            ["./Shopository", "pull", "0"],
            stdout=subprocess.DEVNULL,
        )
        self.assertTrue(os.path.exists(pulled_file))
        with open(pulled_file) as f:
            self.assertEqual(f.read(), "mario")
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )

    def test_rename_bad_index(self):
        filepath = os.path.join(self.test_dir, "bowser.jpeg")
        with open(filepath, "w") as f:
            f.write("mario")
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(
            ["./Shopository", "rename", "1", "wario.jpeg"], capture_output=True
        )
        self.assertEqualDecode(
            result.stderr, f'Error 404. "This image id does not exist"\n\n'
        )
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )

    def test_rename_bad_new_name(self):
        filepath = os.path.join(self.test_dir, "bowser.jpeg")
        with open(filepath, "w") as f:
            f.write("mario")
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(
            ["./Shopository", "rename", "0", "wario.banana"], capture_output=True
        )
        self.assertEqualDecode(
            result.stderr,
            f'Error 400. "Bad file extension. Filetypes png, jpg, jpeg, gif, pdf are supported"\n\n',
        )
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )


if __name__ == "__main__":
    unittest.main()
