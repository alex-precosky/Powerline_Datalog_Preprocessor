from abc import ABC, abstractmethod


class DataProcessor(ABC):
    def __init__(self, get_function, put_function):
        super().__init__()

        self.get_function = get_function
        self.put_function = put_function

    @abstractmethod
    def process_line(self, telemetry_line):
        """Returns a line of processed telemetry and a list of anomaly messages"""
        pass

    def run(self):
        while True:
            telemetry_line = self.get_function()
            if telemetry_line is None:
                break
            transfomred_line, anomalies = self.process_line(telemetry_line)
            self.put_function(transfomred_line)
            for anomaly in anomalies:
                self.put_function(anomaly)
