from .exceptions import InvalidParams
from .services import ExtractionService


class ExtractionHandler:
    @classmethod
    def extract(cls) -> list[list[str]]:
        """
        returns all CSV file rows across all CSV files

        returns:
            list[list[[str]]: a list of CSV row lists, each list
                              containing the following headers: [
                                 'drop',
                                 'length',
                                 'path',
                                 'user_agent',
                                 'user_id'
                             ]
        """
        file_names = ExtractionService.generate_file_names()
        flattened_rows = []
        for file_name in file_names:
            flattened_rows += ExtractionService.fetch_csv_rows(file_name)
        return flattened_rows


class TransformationHandler:
    @classmethod
    def transform(cls, rows: list[list[str]]) \
            -> dict[int, dict[str, int]]:
        """
        placeholder
        """
        parsed_rows = [cls.Row.create(row) for row in rows]
        return cls.sort_rows_by_user_id(parsed_rows)

    class Row:
        user_id: int
        path: str
        length: int

        def __init__(self, user_id, path, length):
            self.user_id = user_id
            self.path = path
            self.length = length

        @ classmethod
        def create(cls, row: list[str]):
            """
            returns an instance of the Row class
            for a given CSV row

            row  list[str]: a CSV row, where user ID and
                            length can be parsed as integers

            returns:
                Row: the provided CSV row as a Row instance
            """
            try:
                user_id = int(row[4])
                path = row[2]
                length = int(row[1])
            except (TypeError, ValueError, IndexError, KeyError):
                raise InvalidParams()
            return cls(user_id=user_id, path=path, length=length)

    @ classmethod
    def sort_rows_by_user_id(cls, rows: list[Row]) -> \
            dict[int, dict[str, int]]:
        """
        sorts the given list of Row instances into a dict
        of user IDs to a dict of the pages and cumulative
        length of time spent (in seconds) per page

        rows  list[Row]: the list of rows to be sorted

        returns:
            {int: {str: int}} a of user IDs to paths/durations
        """
        sorted_rows = {}

        for row in rows:
            user_id = row.user_id
            path = row.path
            length = row.length

            if user_id not in sorted_rows:
                sorted_rows[user_id] = {
                    path: length
                }
            else:
                user = sorted_rows[user_id]
                if path in user:
                    user[path] += length
                else:
                    user[path] = length

        return sorted_rows
