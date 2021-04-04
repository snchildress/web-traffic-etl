import csv
import os
import unittest
from unittest.mock import patch, call

from src.etl.exceptions import InvalidParams
from src.etl.handlers import (
    ExtractionHandler,
    TransformationHandler,
    LoadingHandler
)


class TestExtractionHandler(unittest.TestCase):
    @patch('src.etl.services.ExtractionService.generate_file_names')
    @patch('src.etl.services.ExtractionService.fetch_csv_rows')
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
        # expect a flat list of the mocked data repeated for each mocked file
        expected_csv_rows = []
        for _ in range(len(mocked_file_names)):
            expected_csv_rows += mocked_csv_rows
        expected_fetch_csv_rows_calls = [
            call(file_name) for file_name in mocked_file_names
        ]

        actual_csv_rows = ExtractionHandler.extract()

        generate_file_names_mock.assert_called_once_with()
        fetch_csv_rows_mock.assert_has_calls(expected_fetch_csv_rows_calls)
        self.assertEqual(actual_csv_rows, expected_csv_rows)


class TestTransformationHandler(unittest.TestCase):
    def test_create_row(self):
        """
        Tests that a CSV row is successfully parsed into a Row instance
        """
        expected_row = TransformationHandler.Row(
            user_id=378,
            path='/',
            length=7
        )

        actual_row = TransformationHandler.Row.create([
            '1',
            '7',
            '/',
            'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0\t',  # noqa: E501
            '378'
        ])

        self.assertEqual(actual_row.user_id, expected_row.user_id)
        self.assertEqual(actual_row.path, expected_row.path)
        self.assertEqual(actual_row.length, expected_row.length)

    def test_create_row_with_invalid_params(self):
        """
        Tests that an invalid CSV row is handled correctly during creation
        """
        for invalid_row in [['1'], 1, '', None, ['a', 'a', 'a', 'a', 'a'],
                            ['', '', '', '', ''], {'a': 'a'}]:
            with self.assertRaises(InvalidParams):
                TransformationHandler.Row.create(invalid_row)

    def test_sort_rows_by_user_id(self):
        """
        Tests that Row instances are successfully sorted by user ID
        """
        expected_sorted_rows = {
            1: {
                '/': 10,
                '/test': 5
            },
            2: {
                '/': 1
            },
            3: {
                '/help': 12
            }
        }
        expected_sorted_paths = ['/', '/help', '/test']

        test_rows = [
            TransformationHandler.Row(user_id=1, path='/', length=2),
            TransformationHandler.Row(user_id=1, path='/', length=5),
            TransformationHandler.Row(user_id=1, path='/test', length=5),
            TransformationHandler.Row(user_id=2, path='/', length=1),
            TransformationHandler.Row(user_id=3, path='/help', length=2),
            TransformationHandler.Row(user_id=3, path='/help', length=2),
            TransformationHandler.Row(user_id=3, path='/help', length=8),
            TransformationHandler.Row(user_id=1, path='/', length=3),
        ]
        actual_sorted_rows, actual_sorted_paths = \
            TransformationHandler.sort_rows_by_user_id(test_rows)

        self.assertEqual(actual_sorted_rows, expected_sorted_rows)
        self.assertEqual(actual_sorted_paths, expected_sorted_paths)

    def test_transform(self):
        """
        Tests that CSV rows are transformed into a dictionary of
        user IDs and their web traffic activity
        """
        expected_sorted_rows = {
            1: {
                '/': 10,
                '/help': 0,
                '/test': 5
            },
            2: {
                '/': 1,
                '/help': 0,
                '/test': 0
            },
            3: {
                '/': 0,
                '/help': 12,
                '/test': 0
            }
        }

        test_rows = [
            ['1', '2', '/', '', '1'],
            ['0', '5', '/', '', '1'],
            ['0', '5', '/test', '', '1'],
            ['0', '1', '/', '', '2'],
            ['0', '2', '/help', '', '3'],
            ['0', '2', '/help', '', '3'],
            ['1', '8', '/help', '', '3'],
            ['0', '3', '/', '', '1'],
        ]
        actual_sorted_rows = TransformationHandler.transform(test_rows)

        self.assertEqual(actual_sorted_rows, expected_sorted_rows)

    def test_fill_missing_paths(self):
        """
        Tests that the provided sorted rows are filled in with
        the paths that each user is missing
        """
        expected_sorted_rows = {
            1: {
                '/': 10,
                '/help': 0,
                '/test': 5
            },
            2: {
                '/': 1,
                '/help': 0,
                '/test': 0
            },
            3: {
                '/': 0,
                '/help': 12,
                '/test': 0
            }
        }

        test_rows = {
            1: {
                '/': 10,
                '/test': 5
            },
            2: {
                '/': 1
            },
            3: {
                '/help': 12
            }
        }
        test_paths = ['/', '/test', '/help']

        actual_sorted_rows = TransformationHandler.fill_missing_paths(
            test_rows,
            test_paths
        )

        self.assertEqual(actual_sorted_rows, expected_sorted_rows)


class TestLoadingHandler(unittest.TestCase):
    def test_load(self):
        """
        Tests that a CSV is successfully written
        """
        test_name = 'test'
        test_rows = [
            ['a', 'b', 'c'],
            ['1', '2', '3'],
            ['4', '5', '6']
        ]

        LoadingHandler.load(test_name, test_rows)

        file_path = f'/usr/src/app/output/{test_name}.csv'
        with open(file_path, 'r') as file:
            actual_rows = list(csv.reader(file))
            self.assertEqual(actual_rows, test_rows)
            os.remove(file_path)
