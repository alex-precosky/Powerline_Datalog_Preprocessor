import unittest
from pyPowerLine.Anomaly import *
from pyPowerLine.TelemetryRecord import TelemetryRecord

class TestAnomaly(unittest.TestCase):

    def test_PowerAnomalyChecker(self):
        checker = PowerAnomalyChecker()
        record = TelemetryRecord("2018-01-08 14:54:42.630, 441.781, 477.470, 925.254")

        expected = None
        actual = checker.check_telemetry_record(record)

        self.assertIs(expected, actual)


    def test_PowerAnomalyChecker_zero(self):
        checker = PowerAnomalyChecker()
        record = TelemetryRecord("2018-01-08 14:54:42.630, 0.000, 477.470, 925.254")

        expected = None
        actual = checker.check_telemetry_record(record)

        self.assertIs(expected, actual)


    def test_PowerAnomalyChecker_negative(self):
        checker = PowerAnomalyChecker()
        record = TelemetryRecord("2018-01-08 14:54:42.630, -10.000, 477.470, 925.254")

        expected = None
        actual = checker.check_telemetry_record(record)

        self.assertIsNot(expected, actual)
