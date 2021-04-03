import csv
import string

import requests

from .exceptions import InvalidParams, InvalidFilename, BadRequest, BadResponse
from .config import WEB_TRAFFIC_DATA_ROOT_URL


class ExtractionService:
    root_url = WEB_TRAFFIC_DATA_ROOT_URL

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
            list[list[str]]: a list of CSV row lists, each list
                             containing the following headers: [
                                 'drop',
                                 'length',
                                 'path',
                                 'user_agent',
                                 'user_id'
                             ]

        """
        if not isinstance(name, str) or name == '':
            raise InvalidParams()

        try:
            url: str = f'{self.root_url}/{name}.csv'
            response: requests.Response = requests.get(url)
        except Exception:
            raise BadRequest()

        if not response.ok:
            raise InvalidFilename()

        try:
            response_content = response.iter_lines()
            if not response_content:
                raise BadResponse()
            lines: list[str] = [line.decode('utf-8')
                                for line in response_content]
            if lines[0] != 'drop,length,path,user_agent,user_id':
                raise BadResponse()
            lines = lines[1:]  # remove the expected headers row
        except (AttributeError, TypeError):
            raise BadResponse()

        return list(filter(None, csv.reader(lines)))
