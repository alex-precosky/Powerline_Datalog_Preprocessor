from pyPowerLine import DataProcessor
from pyPowerLine.TelemetryRecord import TelemetryRecord
import datetime
from datetime import timedelta
from abc import ABC, abstractmethod

class PowerlineDataProcessor(DataProcessor.DataProcessor):

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

                if delta > datetime.timedelta(seconds=1, microseconds = 500000):
                    return f'* Anomaly - time gap detected > 1.5 s ({delta.seconds + delta.microseconds/1e6} s)'

            return None

    def __init__(self, get_function, put_function):
        super().__init__(get_function, put_function)

        self.MVA_WINDOW_SECONDS = 5
        self.history = list()  # 0th element is the most recent

        self.single_value_anomaly_checkers = [PowerlineDataProcessor.PowerAnomalyChecker(),
                                              PowerlineDataProcessor.VoltageAnomalyChecker(),
                                              PowerlineDataProcessor.CurrentAnomalyChecker()]


    # keeps the self.history buffer full of at most MVA_WINDOW_SECONDS of data
    def append_history(self, telemetry_record):

        if len(self.history) == 0 :
            self.history.append(telemetry_record)
            return

        if len(self.history) == 1:
            self.history = [telemetry_record] + [self.history[0]]
            return

        # If there aren't MVA_WINDOW_SECONDS of data in the buffer, then append this record
        delta = telemetry_record.timestamp - self.history[-2].timestamp

        if delta < timedelta(seconds=self.MVA_WINDOW_SECONDS):
            self.history = [telemetry_record] + self.history
        # Otherwise, let the oldest record get pushed out
        else:
            self.history = [telemetry_record] + self.history[:-1]


    def calc_mva(self):
        kW_avg, V_avg, I_avg = 0.0, 0.0, 0.0
        for telemetry_record in self.history:
            kW_avg += telemetry_record.power
            V_avg += telemetry_record.voltage
            I_avg += telemetry_record.current

        kW_avg /= len(self.history)
        V_avg /= len(self.history)
        I_avg /= len(self.history)

        return kW_avg, V_avg, I_avg

    def process_line(self, telemetry_line):
        """Returns a line of processed telemetry and a list of Anomalies"""
        super().process_line(telemetry_line)
        telemetry_record = TelemetryRecord(telemetry_line)

        # keeps the buffer self.history full of at most MVA_WINDOW_SECONDS of history data
        self.append_history(telemetry_record)

        kW_avg, V_avg, I_avg = self.calc_mva()

        anomalies = list()

        for checker in self.single_value_anomaly_checkers:
            anomaly = checker.check_telemetry_record(telemetry_record)
            if anomaly is not None:
                anomalies.append(anomaly)

        # check for a time gap in the two most recent measurements so that
        # the anomoly can be logged
        time_gap_checker = PowerlineDataProcessor.TimeGapAnomalyChecker()
        time_gap_anomaly = time_gap_checker.check_telemetry_records(self.history[:2])
        if time_gap_anomaly is not None:
            anomalies.append(time_gap_anomaly)


        # check for a time gap in the moving average time (i.e. what is in self.history)
        # so that no averaging can be output
        time_gap_anomaly = time_gap_checker.check_telemetry_records(self.history)
        if time_gap_anomaly is not None:
            output_mva = False
        else:
            output_mva = True

        # also disable averaging output if there aren't enough samples yet
        delta = self.history[0].timestamp - self.history[-1].timestamp
        if delta.seconds < 5:
            output_mva = False


        if output_mva is True:
            transformed_telemetry_line = f'{telemetry_line}, {kW_avg}, {V_avg}, {I_avg}'
        else:
            transformed_telemetry_line = f'{telemetry_line}, , ,'

        return f'{transformed_telemetry_line}', anomalies
