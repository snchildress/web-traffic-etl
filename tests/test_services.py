import csv
import os
from typing import Union
import unittest
from unittest.mock import patch

from src.etl.exceptions import (
    InvalidParams,
    InvalidFilename,
    BadRequest,
    BadResponse
)
from src.etl.services import ExtractionService, LoadingService


class TestExtractionService(unittest.TestCase):
    test_request_url: str = \
        'https://public.wiwdata.com/engineering-challenge/data/{name}.csv'

    def test_generate_file_names(self):
        """
        Tests that the generated file names list is
        a list of the letters of the Latin alphabet
        """
        expected_file_names: list[str] = \
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
             'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
             's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        actual_file_names: list[str] = ExtractionService.generate_file_names()

        self.assertEqual(actual_file_names, expected_file_names)

    class MockResponse:
        def __init__(self, ok: bool = True, condition: str = 'success'):
            self.ok: bool = ok
            self.condition: str = condition
            self.response_content: list[bytes] = [
                    b'drop,length,path,user_agent,user_id',
                    b'1,7,/,Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0\t,378',  # noqa: E501
                    b'0,11,/,"Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1",220',  # noqa: E501
                    b''
                ]

        def iter_lines(self) -> Union[list[bytes], str]:
            if self.ok and self.condition == 'success':
                return self.response_content
            elif self.condition == 'missing_headers':
                return self.response_content[1:]
            return self.condition

    @patch('requests.get')
    def test_fetch_csv_rows(self, requests_get_mock):
        """
        Tests that the given CSV file returns successfully
        """
        test_file_name: str = 'a'
        expected_request_url: str = self.test_request_url.format(
            name=test_file_name
        )
        expected_csv_rows: list[list[str]] = [
            ['1', '7', '/', 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0\t', '378'],  # noqa: E501
            ['0', '11', '/', 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', '220']  # noqa: E501
        ]
        requests_get_mock.return_value = self.MockResponse()

        actual_csv_rows: list[list[str]] = ExtractionService.fetch_csv_rows(
            test_file_name
        )

        requests_get_mock.assert_called_once_with(expected_request_url)
        self.assertEqual(actual_csv_rows, expected_csv_rows)

    @patch('requests.get')
    def test_fetch_csv_rows_invalid_name(self, requests_get_mock):
        """
        Tests that the given CSV file name is invalid
        """
        test_file_name: str = 'invalid'
        expected_request_url: str = self.test_request_url.format(
            name=test_file_name
        )
        requests_get_mock.return_value = self.MockResponse(ok=False)

        with self.assertRaises(InvalidFilename):
            ExtractionService.fetch_csv_rows(test_file_name)

        requests_get_mock.assert_called_once_with(expected_request_url)

    @patch('requests.get')
    def test_fetch_csv_rows_invalid_param(self, requests_get_mock):
        """
        Tests that CSV rows cannot be fetched using invalid
        inputs for filename
        """
        for test_file_name in ['', None, 1, True, [''], {'': ''}]:
            with self.assertRaises(InvalidParams):
                ExtractionService.fetch_csv_rows(test_file_name)

            requests_get_mock.assert_not_called()

    @patch('requests.get')
    def test_fetch_csv_rows_with_bad_request(self, requests_get_mock):
        """
        Tests that a generic error while fetching the CSV file
        is handled
        """
        test_file_name: str = 'a'
        expected_request_url: str = self.test_request_url.format(
            name=test_file_name
        )
        requests_get_mock.side_effect = Exception()

        with self.assertRaises(BadRequest):
            ExtractionService.fetch_csv_rows(test_file_name)

        requests_get_mock.assert_called_once_with(expected_request_url)

    @patch('requests.get')
    def test_fetch_csv_rows_with_bad_response_content(self, requests_get_mock):
        """
        Tests that an unexpected HTTP response body is handled
        """
        test_file_name: str = 'a'
        expected_request_url: str = self.test_request_url.format(
            name=test_file_name
        )
        for condition in ['missing_headers', [], None, 'test', ['test'], 1]:
            requests_get_mock.return_value = self.MockResponse(
                condition=condition
            )

            with self.assertRaises(BadResponse):
                ExtractionService.fetch_csv_rows(test_file_name)

            requests_get_mock.assert_called_with(expected_request_url)


class TestLoadingService(unittest.TestCase):
    def test_load(self):
        """
        Tests that a CSV is successfully written
        """
        test_name: str = 'test'
        test_rows: list[list[str]] = [
            ['a', 'b', 'c'],
            ['1', '2', '3'],
            ['4', '5', '6']
        ]

        LoadingService.load(test_name, test_rows)

        file_path = f'/usr/src/app/output/{test_name}.csv'
        with open(file_path, 'r') as file:
            actual_rows: list[list[str]] = list(csv.reader(file))
            self.assertEqual(actual_rows, test_rows)
            os.remove(file_path)
