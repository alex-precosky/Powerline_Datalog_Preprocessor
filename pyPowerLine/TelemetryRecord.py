import dateutil.parser

class TelemetryRecord:
    def __init__(self, telemetry_line):
        tokens = telemetry_line.split(',')
        self.timestamp = dateutil.parser.parse(tokens[0])
        self.power = float(tokens[1])
        self.voltage = float(tokens[2])
        self.current = float(tokens[3])
