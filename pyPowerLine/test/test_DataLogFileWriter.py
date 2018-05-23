import unittest
import os.path
from pyPowerLine import DataLogFileWriter

class TestDataLogFileWriter(unittest.TestCase):

    def setUp(self):
        script_dir = os.path.dirname(__file__)
        self.scratch_path = os.path.join(script_dir, "scratch")

    def test_write_one_line(self):
        test_filename = os.path.join(self.scratch_path, "output1line.dat")

        writer = DataLogFileWriter.DataLogFileWriter(test_filename)
        target = "This is one line"
        writer.put(target)
        writer.close()

        expected = target + '\n'

        with open(test_filename, 'r') as in_file:
            actual = in_file.read()

        self.assertEqual(expected, actual)

    def test_write_two_lines(self):
        test_filename = os.path.join(self.scratch_path, "output2line.dat")

        writer = DataLogFileWriter.DataLogFileWriter(test_filename)
        target1 = "This is one line"
        target2 = "This is a second line"
        writer.put(target1)
        writer.put(target2)
        writer.close()

        expected = target1 + '\n' + target2 + '\n'

        with open(test_filename, 'r') as in_file:
            actual = in_file.read()

        self.assertEqual(expected, actual)
