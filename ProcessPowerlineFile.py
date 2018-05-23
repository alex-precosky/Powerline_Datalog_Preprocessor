import argparse
import os.path
import sys
from pyPowerLine.DataLogFileLoader import DataLogFileLoader
from pyPowerLine.DataLogFileWriter import DataLogFileWriter
from pyPowerLine.PowerlineDataProcessor import PowerlineDataProcessor


def parse_arguments():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('input_filename', )
    parser.add_argument('output_filename', )

    return parser.parse_args()


if __name__ == "__main__":
    if sys.version_info < (3, 6):
        print('Must use at least python version 3.6')

    args = parse_arguments()

    if not os.path.exists(args.input_filename):
        print(f'Input file {args.input_filename} does not exist')

    loader = DataLogFileLoader(args.input_filename)
    writer = DataLogFileWriter(args.output_filename)

    processor = PowerlineDataProcessor(loader.get, writer.put)
    processor.run()

    loader.close()
    writer.close()
