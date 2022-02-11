from haps_shared.structure import SpinnerProfile
import haps_shared.database as db
import inspect
import os
import logging
import time
import serial
import cv2
import haps_shared.tool as tool

import sys
import glob
import serial


def printCursor(cursor):
    for record in cursor:
        logging.info(record, "\r\n")


class PixelProgrammer(serial.Serial):
    def __init__(self, port):
        try:
            super().__init__(
                port=port,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2  # seconds
            )
        except Exception as e:
            logging.warning("No UART found")
            return None


def serial_ports():
    # list USB serial ports
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        if "USB" in port:
            result.append(port)
    return result


def main():
    tool.init_log()
    # logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("HAPS #2")
    # test send uart
    uart = PixelProgrammer(serial_ports()[0])
    uart.write(str.encode('hello'));


if __name__ == "__main__":
    main()
