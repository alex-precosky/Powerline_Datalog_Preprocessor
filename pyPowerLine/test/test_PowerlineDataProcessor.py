import unittest
from pyPowerLine.PowerlineDataProcessor import PowerlineDataProcessor
from pyPowerLine.TelemetryRecord import TelemetryRecord

class TestPowerlineDataProcessor(unittest.TestCase):
    def setUp(self):
        TestPowerlineDataProcessor.__abstractmethods__ = set()

    def null_write_callback(self, write_str):
        pass

    def null_read_callback(self):
        pass

    def test_append_history_longer_than_mva(self):
        # makes sure that we don't keep values around that aren't
        # needed for MVA calculation anymore, to save memory
        #
        # inserts 7 records, but only 6 should be retained

        processor = PowerlineDataProcessor(self.null_read_callback, self.null_write_callback)

        processor.append_history( TelemetryRecord('2018-01-08 14:55:40.152, 1, 2, 3'))
        processor.append_history( TelemetryRecord('2018-01-08 14:55:41.152, 1, 2, 3'))
        processor.append_history( TelemetryRecord('2018-01-08 14:55:42.152, 2, 3, 4'))
        processor.append_history( TelemetryRecord('2018-01-08 14:55:43.152, 4, 5, 6'))
        processor.append_history( TelemetryRecord('2018-01-08 14:55:44.152, 4, 5, 6'))
        processor.append_history( TelemetryRecord('2018-01-08 14:55:45.152, 4, 5, 6'))
        processor.append_history( TelemetryRecord('2018-01-08 14:55:46.152, 4, 5, 6'))

        expected = 6
        actual = len(processor.history)

        self.assertEqual(expected, actual)

    def test_calc_mva(self):

        processor = PowerlineDataProcessor(self.null_read_callback, self.null_write_callback)

        processor.history.append( TelemetryRecord('2018-01-08 14:55:45.152, 4, 5, 6'))
        processor.history.append( TelemetryRecord('2018-01-08 14:55:44.152, 4, 5, 6'))
        processor.history.append( TelemetryRecord('2018-01-08 14:55:43.152, 4, 5, 6'))
        processor.history.append( TelemetryRecord('2018-01-08 14:55:42.152, 2, 3, 4'))
        processor.history.append( TelemetryRecord('2018-01-08 14:55:41.152, 1, 2, 3'))
        processor.history.append( TelemetryRecord('2018-01-08 14:55:40.152, 1, 2, 3'))

        kW_mva, V_mva, I_mva = processor.calc_mva()

        self.assertAlmostEqual(kW_mva, 2.6666666666)
        self.assertAlmostEqual(V_mva, 3.6666666666)
        self.assertAlmostEqual(I_mva, 4.6666666666)
