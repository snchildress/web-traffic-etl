from .exceptions import InvalidParams
from .services import ExtractionService


class ExtractionHandler:
    @classmethod
    def extract(self) -> list[list[str]]:
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
        return [ExtractionService.fetch_csv_rows(file_name) for file_name
                in file_names]


class TransformationHandler:
    @classmethod
    def transform(self, rows: list[list[str]]) \
            -> dict[int, dict[str, list[int]]]:
        """
        placeholder
        """
        parsed_rows = [self.parse_row(row) for row in rows]
        return self.sort_rows_by_user_id(parsed_rows)

    class Row:
        user_id: int
        path: str
        length: int

        def __init__(self, user_id, path, length):
            self.user_id = user_id
            self.path = path
            self.length = length

    @ classmethod
    def parse_row(self, row: list[str]) -> Row:
        """
        returns an instance of the Row class
        for a given CSV row

        row  list[str]: a CSV row, where user ID and
                        length can be parsed as integers

        returns:
            Row()
        """
        try:
            user_id = int(row[4])
            path = row[2]
            length = int(row[1])
        except (TypeError, ValueError, IndexError, KeyError):
            raise InvalidParams()
        return self.Row(user_id=user_id, path=path, length=length)

    @ classmethod
    def sort_rows_by_user_id(self, rows: Row) -> \
            dict[int, dict[str, list[int]]]:
        """
        placholder
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
