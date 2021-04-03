import os
import csv
import string

import requests


class ExtractionService:
    WEB_TRAFFIC_DATA_ROOT_URL = os.environ['WEB_TRAFFIC_DATA_ROOT_URL']

    @classmethod
    def generate_file_names(self) -> list[str]:
        """
        returns an exhaustive list of the web traffic data file names

        returns:
            list[str]: the list of web traffic data file names
        """
        return list(string.ascii_lowercase)

    @classmethod
    def fetch_csv_rows(self, name: str) -> list[list[str]]:
        """
        returns the contents of a given CSV file name

        name  str: the name of the CSV file to fetch
                   without the file extension

        returns:
            list[list[str]]: a list of CSV row lists, starting
                             with a list of column headers
        """
        url = f'{self.WEB_TRAFFIC_DATA_ROOT_URL}/{name}.csv'
        response = requests.get(url)
        lines = [line.decode('utf-8') for line in response.iter_lines()]
        return list(csv.reader(lines))
