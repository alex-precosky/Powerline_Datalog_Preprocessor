from pyPowerLine import DataLogLoader


class DataLogFileLoader(DataLogLoader.DataLogLoader):
    def __init__(self, filename):
        DataLogLoader.DataLogLoader.__init__(self)

        self.in_file = open(filename, 'r')

    def get(self):
        line = self.in_file.readline()
        if line != "":
            return line.strip()
        else:
            return None

    def close(self):
        self.in_file.close()
