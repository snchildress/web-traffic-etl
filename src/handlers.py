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
