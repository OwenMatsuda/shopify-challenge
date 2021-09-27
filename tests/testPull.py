import os
import subprocess
import unittest
import tempfile
import shutil

from tests.testbase import TestBase


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


if __name__ == "__main__":
    unittest.main()
