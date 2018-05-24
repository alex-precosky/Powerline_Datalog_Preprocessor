import unittest
from unittest.mock import MagicMock
from pyPowerLine.DataProcessor import DataProcessor


class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        # allow instantiation of an ABC for testing
        DataProcessor.__abstractmethods__ = set()

        self.read_count = 0

    def one_line_read_callback(self):

        if self.read_count == 0:
            return_line = "1, 2, 3"
        else:
            return_line = None
        self.read_count += 1
        return return_line

    def null_write_callback(self, write_str):
        pass

    def test_write_callback_called(self):
        write_callback = MagicMock()

        def null_processor(x): return x, []
        processor = DataProcessor(self.one_line_read_callback, write_callback)
        processor.process_line = null_processor

        processor.run()

        write_callback.assert_called_once_with("1, 2, 3")

    def test_process_called(self):
        mock_process = MagicMock(return_value=("1, 2, 3", []))

        processor = DataProcessor(self.one_line_read_callback, self.null_write_callback)

        processor.process_line = mock_process
        processor.run()

        mock_process.assert_called()
