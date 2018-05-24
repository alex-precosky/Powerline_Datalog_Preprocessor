import datetime
from abc import ABC, abstractmethod


class SingleValueAnomalyChecker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    # Returns None for no anomaly, and a message if there is one
    def check_telemetry_record(self, telemetry_record):
        pass


class MultiValueAnomalyChecker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    # checks a collection of telemetry records for an anomaly that happens over time
    # Returns None for no anomaly, and a message if there is one
    def check_telemetry_records(self, telemetry_records):
        pass


class PowerAnomalyChecker(SingleValueAnomalyChecker):
    def __init__(self):
        super().__init__()

    def check_telemetry_record(self, telemetry_record):
        super().check_telemetry_record(telemetry_record)
        if telemetry_record.power < float(0.0):
            return f'* Anomaly - kW < 0.0 (kW = {telemetry_record.power})'
        else:
            return None


class VoltageAnomalyChecker(SingleValueAnomalyChecker):
    def __init__(self):
        super().__init__()

    def check_telemetry_record(self, telemetry_record):
        super().check_telemetry_record(telemetry_record)
        if (telemetry_record.voltage >= 475) and (telemetry_record.voltage <= 485):
            return None
        else:
            return f'* Anomaly - V outside range of 480 V +/- 5.0V (V={telemetry_record.voltage})'


class CurrentAnomalyChecker(SingleValueAnomalyChecker):
    def __init__(self):
        super().__init__()

    def check_telemetry_record(self, telemetry_record):
        super().check_telemetry_record(telemetry_record)
        if telemetry_record.current < 0.0:
            return f'* Anomaly - I < 0.0 (I = {telemetry_record.current})'
        else:
            return None


class TimeGapAnomalyChecker(MultiValueAnomalyChecker):
    def __init__(self):
        super().__init__()

    def check_telemetry_records(self, telemetry_records):
        super().check_telemetry_records(telemetry_records)

        # Can't have a time gap if there aren't at least two records
        if len(telemetry_records) < 2:
            return None

        for a,b in zip(telemetry_records, telemetry_records[1:]):
            delta = a.timestamp - b.timestamp

            max_delta = datetime.timedelta(seconds=1, microseconds=500000)
            if (delta >  max_delta) and (delta > datetime.timedelta(seconds=0)):
                return f'* Anomaly - time gap detected > 1.5 s ({delta.seconds + delta.microseconds/1e6} s)'

        return None


class OutOfOrderAnomalyChecker(MultiValueAnomalyChecker):
    def __init__(self):
        super().__init__()

    def check_telemetry_records(self, telemetry_records):
        super().check_telemetry_records(telemetry_records)

        # Can't have a time gap if there aren't at least two records
        if len(telemetry_records) < 2:
            return None

        for a, b in zip(telemetry_records, telemetry_records[1:]):
            delta = a.timestamp - b.timestamp

            if delta < datetime.timedelta(seconds=0):
                return f'* Anomaly - time stamps out of order'

        return None
