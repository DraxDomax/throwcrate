import tempfile
import time
import unittest
from multiprocessing import Process
from os import makedirs
from os.path import join, isdir
from uuid import uuid4

from client import client as client_main
from server import server as server_main


class SocketTestCase(unittest.TestCase):
    client_temp_dir = tempfile.TemporaryDirectory()
    server_temp_dir = tempfile.TemporaryDirectory()

    @classmethod
    def setUpClass(cls) -> None:
        cls.client_process = Process(target=client_main, args=(cls.client_temp_dir.name,))
        cls.server_process = Process(target=server_main, args=(cls.server_temp_dir.name,))

        cls.server_process.start()
        cls.client_process.start()

    def setUp(self) -> None:
        # Recreate temp dirs for next test (Ignores if already exists)
        makedirs(self.client_temp_dir.name, exist_ok=True)
        makedirs(self.server_temp_dir.name, exist_ok=True)

    def tearDown(self) -> None:
        # Clear temp dirs
        self.client_temp_dir.cleanup()
        self.server_temp_dir.cleanup()

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "client_process"):
            cls.client_process.terminate()

        if hasattr(cls, "server_process"):
            cls.server_process.terminate()

    def test_file_transfer(self):
        """
        This test will verify if a file created on client is created on server with the same contents
        """
        # Prepare test contents for file
        source_contents = str(uuid4())

        # Generate a unique name for test file
        test_file = str(uuid4())

        # Write these contents to the test file
        with open(join(self.client_temp_dir.name, test_file), 'w') as source_file:
            source_file.write(source_contents)

        # Wait for the programs to work
        time.sleep(5)

        # Read from the destination, with the saved file name earlier
        with open(join(self.server_temp_dir.name, test_file)) as destination_file:
            destination_contents = destination_file.read()

        # Verify contents match
        self.assertEqual(source_contents, destination_contents,
                         msg="Source file and destination file does not have identical contents")

    def test_file_structure(self):
        """
        This test will verify if server is able to create matching directory structure from client's watched dir
        """

        # When you are changing this make sure you dont add a "/" prefix,
        # abc/pqr/rst is right, /abc/pqr/rst is wrong as / represents root.
        dirs = ["Primary/A/A/test", "Primary/A/B/test", "Secondary/A/C", "Secondary/A/D"]

        # Create directories
        for d in dirs:
            makedirs(join(self.client_temp_dir.name, d), exist_ok=True)

        # Wait for programs to work
        time.sleep(5)

        # Check if directory structures were created onto the server machine
        assert all(isdir(join(self.server_temp_dir.name, d)) for d in dirs), "Structure does not match"


if __name__ == '__main__':
    unittest.main()
