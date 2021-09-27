import requests
import unittest
import os
import sys
import shutil
import subprocess
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


class TestPull(TestBase):
    def test_pull_success(self):
        filename = "skatroopa.png"
        if os.path.exists(f"./{filename}"):
            os.remove(f"./{filename}")
        # Push file to test pull
        filepath = os.path.join(self.test_dir, filename)
        f = open(filepath, "x")
        f.close()
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(["./Shopository", "pull", "0"], capture_output=True)
        # Asserts proper output and file existence
        self.assertEqualDecode(
            result.stdout, f"{filename} was successfully pulled to ./{filename}\n"
        )
        self.assertTrue(os.path.exists(f"./{filename}"))
        # Serve cleanup
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )
        # File cleanup
        os.remove(f"./{filename}")

    def test_pull_success_custom_out(self):
        filename = "skatroopa.png"
        test_dir_2 = tempfile.mkdtemp()
        # Push file to test pull
        file_push_path = os.path.join(self.test_dir, filename)
        f = open(file_push_path, "x")
        f.close()
        subprocess.run(
            ["./Shopository", "push", file_push_path], stdout=subprocess.DEVNULL
        )
        file_pull_path = os.path.join(test_dir_2, filename)
        result = subprocess.run(
            ["./Shopository", "pull", "0", "-o", file_pull_path], capture_output=True
        )
        # Asserts proper output and file existence
        self.assertEqualDecode(
            result.stdout, f"{filename} was successfully pulled to {file_pull_path}\n"
        )
        self.assertTrue(os.path.exists(file_pull_path))
        # Server cleanup
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )
        # File cleanup
        os.remove(file_pull_path)
        shutil.rmtree(test_dir_2)

    def test_pull_bad_id(self):
        # Test some bad pulls
        result = subprocess.run(["./Shopository", "pull", "1"], capture_output=True)
        self.assertEqualDecode(result.stderr, 'Error 400. "Invalid image id"\n\n')
        result = subprocess.run(["./Shopository", "pull", "100"], capture_output=True)
        self.assertEqualDecode(result.stderr, 'Error 400. "Invalid image id"\n\n')
        # Push files to test other bad pulls
        filename = "skatroopa.png"
        filepath = os.path.join(self.test_dir, filename)
        f = open(filepath, "x")
        f.close()
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        subprocess.run(
            ["./Shopository", "remove", "2", "--yes"], stdout=subprocess.DEVNULL
        )
        result = subprocess.run(["./Shopository", "pull", "2"], capture_output=True)
        self.assertEqualDecode(result.stderr, 'Error 400. "Invalid image id"\n\n')
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "1", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "3", "--yes"], stdout=subprocess.DEVNULL
        )

    def test_pull_correct_file(self):
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
        pulled_file1 = os.path.join(self.test_dir, "taast1")
        pulled_file2 = os.path.join(self.test_dir, "taast2")
        pulled_file3 = os.path.join(self.test_dir, "taast3")
        result = subprocess.run(
            ["./Shopository", "pull", "2", "-o", pulled_file3],
            stdout=subprocess.DEVNULL,
        )
        result = subprocess.run(
            ["./Shopository", "pull", "0", "-o", pulled_file1],
            stdout=subprocess.DEVNULL,
        )
        result = subprocess.run(
            ["./Shopository", "pull", "1", "-o", pulled_file2],
            stdout=subprocess.DEVNULL,
        )
        with open(pulled_file1) as f:
            self.assertEqual(f.read(), "kirby")
        with open(pulled_file2) as f:
            self.assertEqual(f.read(), "wario")
        with open(pulled_file3) as f:
            self.assertEqual(f.read(), "princess peach")
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "1", "--yes"], stdout=subprocess.DEVNULL
        )
        subprocess.run(
            ["./Shopository", "remove", "2", "--yes"], stdout=subprocess.DEVNULL
        )

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
        result = subprocess.run(["./Shopository", "rename", "0", new_name], capture_output=True)
        self.assertEqualDecode(result.stdout, f"file 0 successfully renamed to {new_name}\n")
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

    def test_bad_index(self):
        filepath = os.path.join(self.test_dir, "bowser.jpeg")
        with open(filepath, "w") as f:
            f.write("mario")
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(["./Shopository", "rename", "1", "wario.jpeg"], capture_output=True)
        self.assertEqualDecode(result.stderr, f"Error 404. \"This image id does not exist\"\n\n")
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )

    def test_bad_new_name(self):
        filepath = os.path.join(self.test_dir, "bowser.jpeg")
        with open(filepath, "w") as f:
            f.write("mario")
        subprocess.run(["./Shopository", "push", filepath], stdout=subprocess.DEVNULL)
        result = subprocess.run(["./Shopository", "rename", "0", "wario.banana"], capture_output=True)
        self.assertEqualDecode(result.stderr, f"Error 400. \"Bad file extension. Filetypes png, jpg, jpeg, gif, pdf are supported\"\n\n")
        subprocess.run(
            ["./Shopository", "remove", "0", "--yes"], stdout=subprocess.DEVNULL
        )


if __name__ == "__main__":
    unittest.main()
