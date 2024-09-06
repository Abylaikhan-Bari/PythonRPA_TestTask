import unittest
import tempfile
import os
from datetime import datetime, timedelta
from main import categorize_files_by_type

class TestFileCategorization(unittest.TestCase):

    def setUp(self):

        #Set up a temporary directory and create test files.

        self.test_dir = tempfile.TemporaryDirectory()
        self._create_test_files()

    def tearDown(self):

        #Remove the temporary directory and its contents.

        self.test_dir.cleanup()

    def _create_test_files(self):

        #Create test files with different sizes and modification times.

        now = datetime.now()
        old_time = now - timedelta(days=10)

        # Create files with different sizes
        with open(os.path.join(self.test_dir.name, 'file1.txt'), 'w') as f:
            f.write('A' * 500)
        with open(os.path.join(self.test_dir.name, 'file2.txt'), 'w') as f:
            f.write('B' * 1500)
        with open(os.path.join(self.test_dir.name, 'file3.txt'), 'w') as f:
            f.write('C' * 2500)

        # Set modification times
        os.utime(os.path.join(self.test_dir.name, 'file1.txt'), (old_time.timestamp(), old_time.timestamp()))
        os.utime(os.path.join(self.test_dir.name, 'file2.txt'), (now.timestamp(), now.timestamp()))
        os.utime(os.path.join(self.test_dir.name, 'file3.txt'), (now.timestamp(), now.timestamp()))

    def test_categorize_files_by_type_filter_extension(self):

        #Test categorization with a filter for '.txt' files.

        global FILTER_EXTENSION
        FILTER_EXTENSION = '.txt'
        result = categorize_files_by_type(self.test_dir.name)
        self.assertIn('.txt', result)
        self.assertEqual(len(result['.txt']), 3)

    def test_categorize_files_by_type_invalid_directory(self):

        #Test categorization with an invalid directory path.

        with self.assertRaises(FileNotFoundError):
            categorize_files_by_type('invalid_path')

    def test_categorize_files_by_type_not_a_directory(self):

        #Test categorization with a file path instead of a directory.

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            with self.assertRaises(NotADirectoryError):
                categorize_files_by_type(temp_file.name)
        finally:
            temp_file.close()
            os.remove(temp_file.name)

    def test_categorize_files_by_type_valid(self):

        #Test categorization with no filters.

        global MIN_SIZE, MODIFIED_AFTER, FILTER_EXTENSION
        MIN_SIZE = None
        MODIFIED_AFTER = None
        FILTER_EXTENSION = None
        result = categorize_files_by_type(self.test_dir.name)
        self.assertIn('.txt', result)
        self.assertEqual(len(result['.txt']), 3)

if __name__ == '__main__':
    unittest.main()
