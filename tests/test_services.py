import unittest
from unittest.mock import patch

from src.exceptions import InvalidParams, InvalidFilename
from src.services import ExtractionService


class TestExtractionService(unittest.TestCase):
    test_request_url = 'https://public.wiwdata.com/engineering-challenge/data/{name}.csv'  # noqa: E501

    def test_generate_file_names(self):
        """
        Tests that the generated file names list contains
        26 items and is equal to the letters of the Latin alphabet
        """
        expected_file_names = \
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
             'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        actual_file_names = ExtractionService.generate_file_names()

        self.assertEqual(len(actual_file_names), 26)
        self.assertEqual(actual_file_names, expected_file_names)

    class MockResponse:
        def __init__(self, ok=True):
            self.ok = ok

        def iter_lines(self):
            if self.ok:
                return [
                    b'drop,length,path,user_agent,user_id',
                    b'1,7,/,Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0\t,378',  # noqa: E501
                    b'0,11,/,"Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1",220'  # noqa: E501
                ]

    @patch('requests.get')
    def test_fetch_csv_rows(self, mock_get):
        """
        Tests that the given CSV file returns successfully
        """
        test_file_name = 'a'
        expected_request_url = self.test_request_url.format(
            name=test_file_name
        )
        expected_csv_rows = [
            ['drop', 'length', 'path', 'user_agent', 'user_id'],
            ['1', '7', '/', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0\t', '378'],  # noqa: E501
            ['0', '11', '/', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', '220']  # noqa: E501
        ]
        mock_get.return_value = self.MockResponse()

        actual_rows = ExtractionService.fetch_csv_rows(test_file_name)

        mock_get.assert_called_once_with(expected_request_url)
        self.assertEqual(len(actual_rows), 3)
        self.assertEqual(actual_rows, expected_csv_rows)

    @patch('requests.get')
    def test_fetch_csv_rows_invalid_name(self, mock_get):
        """
        Tests that the given CSV file name is invalid
        """
        test_file_name = 'invalid'
        expected_request_url = self.test_request_url.format(
            name=test_file_name
        )
        mock_get.return_value = self.MockResponse(ok=False)

        with self.assertRaises(InvalidFilename):
            ExtractionService.fetch_csv_rows(test_file_name)

        mock_get.assert_called_once_with(expected_request_url)

    @patch('requests.get')
    def test_fetch_csv_rows_invalid_param(self, mock_get):
        """
        Tests that CSV rows cannot be fetched using invalid
        inputs for filename
        """
        for test_file_name in ['', None, 1, True, [''], {'': ''}]:
            with self.assertRaises(InvalidParams):
                ExtractionService.fetch_csv_rows(test_file_name)
