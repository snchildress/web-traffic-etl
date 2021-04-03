import unittest
from unittest.mock import patch, call

from src.handlers import ExtractionHandler


class TestExtractionHandler(unittest.TestCase):
    @patch('src.services.ExtractionService.generate_file_names')
    @patch('src.services.ExtractionService.fetch_csv_rows')
    def test_extract(self, fetch_csv_rows_mock, generate_file_names_mock):
        """
        Tests that the extraction handler is successful
        """
        mocked_file_names = ['a', 'b', 'c']
        mocked_csv_rows = [
            ['1', '7', '/', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0\t', '378'],  # noqa: E501
            ['0', '11', '/', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', '220']  # noqa: E501
        ]
        generate_file_names_mock.return_value = mocked_file_names
        fetch_csv_rows_mock.return_value = mocked_csv_rows
        expected_csv_rows = [
            mocked_csv_rows for _ in range(len(mocked_file_names))
        ]  # expect a concatenated list of the same mocked rows for each file
        expected_fetch_csv_rows_calls = [
            call(file_name) for file_name in mocked_file_names
        ]

        actual_csv_rows = ExtractionHandler.extract()

        generate_file_names_mock.assert_called_once_with()
        fetch_csv_rows_mock.assert_has_calls(expected_fetch_csv_rows_calls)
        self.assertEqual(actual_csv_rows, expected_csv_rows)
