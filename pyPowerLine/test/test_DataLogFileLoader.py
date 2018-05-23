import unittest
import os.path
from pyPowerLine import DataLogFileLoader


class TestDataLogFileLoader(unittest.TestCase):

    def setUp(self):
        script_dir = os.path.dirname(__file__)
        self.test_data_path = os.path.join(script_dir, "data")

    def test_load_missing_file(self):
        self.assertRaises(FileNotFoundError,
                          DataLogFileLoader.DataLogFileLoader,
                          "/imaginary.dat")

    def test_load_one_line(self):

        test_filename = os.path.join(self.test_data_path, "telemetry[1].dat")
        loader = DataLogFileLoader.DataLogFileLoader(test_filename)

        expected = "2018-01-08 14:54:42.630, 441.781, 477.470, 925.254"
        actual = loader.get()

        self.assertEqual(expected, actual)
        loader.close()

    def test_load_second_line(self):

        test_filename = os.path.join(self.test_data_path, "telemetry[1].dat")
        loader = DataLogFileLoader.DataLogFileLoader(test_filename)

        expected = "2018-01-08 14:54:43.784, 320.249, 475.942, 672.873"
        loader.get()
        actual = loader.get()

        self.assertEqual(expected, actual)
        loader.close()


    def test_load_end_of_file(self):
        test_filename = os.path.join(self.test_data_path, "twolines.dat")
        loader = DataLogFileLoader.DataLogFileLoader(test_filename)

        loader.get()
        loader.get()
        actual = loader.get()

        self.assertIs(actual, None)
        loader.close()

    def test_load_after_end_of_file(self):
        test_filename = os.path.join(self.test_data_path, "twolines.dat")
        loader = DataLogFileLoader.DataLogFileLoader(test_filename)

        loader.get()
        loader.get()
        loader.get()
        actual = loader.get()

        self.assertIs(actual, None)
        loader.close()
