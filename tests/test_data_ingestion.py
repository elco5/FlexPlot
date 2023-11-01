# test_data_ingestion.py
import unittest
from unittest.mock import patch
import base64
import pandas as pd
from io import StringIO
from flask import Flask
import sys
sys.path.append('../')
import app

class TestDataIngestion(unittest.TestCase):

    def setUp(self):
        self.server = Flask(__name__)
        self.app = app.app.server.test_client()
        self.server_context = app.app.server.app_context()
        self.server_context.push()

    @patch('app.upload_file')  # Replace with the actual name of your upload_file function
    def test_successful_file_upload(self, mock_upload_file):
        mock_upload_file.return_value = 'Success'
        # response = self.app.post('/upload', data={'upload-data': (StringIO('col1,col2\n1,2\n3,4'), 'test.csv')})
        response = self.app.post('/upload', data={'upload-data': ('col1,col2\n1,2\n3,4'.encode('utf-8'), 'test.csv')})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Success')

    @patch('app.upload_file')  # Replace with the actual name of your upload_file function
    def test_file_type_handling(self, mock_upload_file):
        mock_upload_file.return_value = 'Success'
        # response = self.app.post('/upload', data={'upload-data': (StringIO('col1,col2\n1,2\n3,4'), 'test.txt')})
        response = self.app.post('/upload', data={'upload-data': ('col1,col2\n1,2\n3,4'.encode('utf-8'), 'test.txt')})

        self.assertEqual(response.status_code, 400)  # Assuming you return a 400 status for bad file types

    @patch('app.pd.read_csv')  # Replace with the actual import in your app
    def test_file_content_parsing(self, mock_read_csv):
        mock_df = pd.DataFrame({'col1': [1, 3], 'col2': [2, 4]})
        mock_read_csv.return_value = mock_df
        # Simulate file upload and check that read_csv is called with the correct content
        # ...

    def test_error_handling(self): 
        pass
        # Test how your app handles various error conditions
        # ...

if __name__ == '__main__':
    unittest.main()
