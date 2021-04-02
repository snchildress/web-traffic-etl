import string 


class ExtractionService:
    @classmethod
    def generate_file_names(self):
        """
        returns an exhaustive list of the web traffic data file names

        returns:
            [str]: the list of web traffic data file names
        """
        return list(string.ascii_lowercase)
