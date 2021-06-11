import json


class JsonLoader:

    def __init__(self, filename):
        self.filename = filename
        self.lines = 0

    def read_json(self, filename=None):
        """Generator for JSON lines file

        Parameters
        ----------
        filename : str
            path to the file
        """
        if filename is not None:
            self.filename = filename
        # based on https://stackoverflow.com/a/6886417
        try:
            self.lines = 0
            if self.filename is None:
                raise ValueError('Please specify a file!')
            with open(self.filename, 'r', encoding='utf8') as f:
                for line in f:
                    # catch blank or ill formatted lines and skip them
                    try:
                        self.lines += 1
                        yield json.loads(line)
                    except json.decoder.JSONDecodeError:
                        continue
        except FileNotFoundError:
            raise FileNotFoundError("No file %s exists!" % str(self.filename))
