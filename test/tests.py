#!/usr/bin/env python

import unittest
import os
from src.gftp import GoogleFTP

class TestGoogleFTP(unittest.TestCase):
    def setUp(self):
        self.api = GoogleFTP()
        self.test_file_name = "README.md"
        self.test_file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../' + self.test_file_name))

    def test_listing_files(self):
        self.assertTrue(self.api.FileList())

    def test_upload_files(self):
        self.assertTrue(self.api.FileUpload(self.test_file_path))
        self.assertTrue(self.api.FileRemove(self.test_file_name))

    def test_download_files(self):
        self.assertTrue(self.api.FileUpload(self.test_file_path))
        self.assertTrue(self.api.FileDownload(self.test_file_name, "/tmp/README.md"))
        self.assertTrue(self.api.FileRemove(self.test_file_name))

    def test_remove_files(self):
        self.assertTrue(self.api.FileUpload(self.test_file_path))
        self.assertTrue(self.api.FileRemove(self.test_file_name))

if __name__ == '__main__':
    unittest.main()
