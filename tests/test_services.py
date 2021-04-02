import unittest

from src.services import ExtractionService


class TestExtractionService(unittest.TestCase):
    def test_generate_file_names(self):
        """
        Test that the generated file names list contains
        26 items and is equal to the letters of the Latin alphabet
        """
        expected_file_names = \
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
            's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        actual_file_names = ExtractionService.generate_file_names()

        self.assertEqual(len(actual_file_names), 26)
        self.assertEqual(actual_file_names, expected_file_names)
