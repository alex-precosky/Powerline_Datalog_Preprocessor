from pyPowerLine import DataProcessor
from pyPowerLine.TelemetryRecord import TelemetryRecord
from datetime import timedelta

from pyPowerLine.Anomaly import *


class PowerlineDataProcessor(DataProcessor.DataProcessor):

    def __init__(self, get_function, put_function):
        super().__init__(get_function, put_function)

        self.MVA_WINDOW_SECONDS = 5
        self.history = list()  # 0th element is the most recent

        self.single_value_anomaly_checkers = [PowerAnomalyChecker(),
                                              VoltageAnomalyChecker(),
                                              CurrentAnomalyChecker()]

    # keeps the self.history buffer full of at most MVA_WINDOW_SECONDS of data
    def append_history(self, telemetry_record):

        if len(self.history) == 0:
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
        time_gap_checker = TimeGapAnomalyChecker()
        time_gap_anomaly = time_gap_checker.check_telemetry_records(self.history[:2])
        if time_gap_anomaly is not None:
            anomalies.append(time_gap_anomaly)

        out_of_order_checker = OutOfOrderAnomalyChecker()
        out_of_order_anomaly = out_of_order_checker.check_telemetry_records(self.history[:2])
        if out_of_order_anomaly is not None:
            anomalies.append(out_of_order_anomaly)

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
            transformed_telemetry_line = f'{telemetry_line}, {kW_avg:.3f}, {V_avg:.3f}, {I_avg:.3f}'
        else:
            transformed_telemetry_line = f'{telemetry_line}, , ,'

        return f'{transformed_telemetry_line}', anomalies
