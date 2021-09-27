import os
import subprocess
import unittest

from tests.testbase import TestBase


class TestPush(TestBase):
    def push_success(self, filename):
        filepath = os.path.join(self.test_dir, filename)
        f = open(filepath, "x")
        f.close()
        # Check that image was successfully added
        result = subprocess.run(
            ["./Shopository", "push", filepath], capture_output=True
        )
        self.assertEqualDecode(
            result.stdout, f"{filename} was successfully added with id 0\n"
        )
        # Check that image was added to directory
        self.assertTrue(os.path.exists(f"./images/00{filename}"))
        result = subprocess.run(["./Shopository", "ls"], capture_output=True)
        self.assertEqualDecode(result.stdout, f"Index: 0, Image Name: {filename}\n")
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )

    def test_push_success_one(self):
        self.push_success("koopa.jpg")

    def test_push_success_correct_file_type(self):
        # Allowed extensions are png, jpg, jpeg, gif, pdf
        for extension in ["png", "jpg", "jpeg", "gif", "pdf"]:
            self.push_success(f"koopa.{extension}")

    def test_push_fail_missing_file(self):
        result = subprocess.run(["./Shopository", "push"], capture_output=True)
        checkStr = """Usage: Shopository push [OPTIONS] IMAGE_FILE
Try 'Shopository push --help' for help.

Error: Missing argument 'IMAGE_FILE'.
"""
        self.assertEqualDecode(result.stderr, checkStr)

    def test_push_fail_file_doesnt_exist(self):
        filepath = os.path.join(self.test_dir, "doesnt_exist")
        result = subprocess.run(
            ["./Shopository", "push", filepath], capture_output=True
        )
        self.assertEqualDecode(
            result.stderr,
            "This file doesn't exist. Check to make sure your path is correct\n",
        )

    def test_push_fail_bad_file_ext(self):
        for bad_ext in ["troopa", "mario", "luigi"]:
            filepath = os.path.join(self.test_dir, f"koops{bad_ext}")
            f = open(filepath, "x")
            f.close()
            result = subprocess.run(
                ["./Shopository", "push", filepath], capture_output=True
            )
            self.assertEqualDecode(
                result.stderr,
                'Error 400. "Bad file extension. Filetypes png, jpg, jpeg, gif, pdf are supported"\n\n',
            )


if __name__ == "__main__":
    unittest.main()
