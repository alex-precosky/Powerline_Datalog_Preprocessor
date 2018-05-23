from pyPowerLine import DataLogWriter


class DataLogFileWriter(DataLogWriter.DataLogWriter):
    def __init__(self, filename):
        DataLogWriter.DataLogWriter.__init__(self)

        self.out_file = open(filename, 'w')

    def put(self, line):
        self.out_file.write(line + '\n')

    def close(self):
        self.out_file.close()
