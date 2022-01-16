import serial
import time
import db
import logging
import sys
import colorlog
from typing import List


def printCursor(cursor):
    for record in cursor:
        print(record, "\r\n")


def downloadImage(order_id: int):
    col = db.get_collection(db.DataBaseType.Order)
    print(col)
    myquery = {"order_id": order_id}
    cursor = col.find(myquery)
    printCursor(cursor)
    result = 0
    return result


def initLog():
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('my_log_info.log')
    sh = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
    fh.setFormatter(formatter)
    sh.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S'))
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def initSerial(port: str):
    logging.info("setting up serial")
    try:
        ser = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2  # seconds     # <-- HERE
        )
        return ser
    except Exception as e:
        logging.error("No UART found")
        return None


class PixArrayConfig:
    resolution: int = 8  # bits
    length: int = 16
    angle: int = 72


class Pixel:
    red = 255
    green = 255
    blue = 255

    def shift(self, bits: int):
        self.red >> bits
        self.green >> bits
        self.blue >> bits


def generatePixArray(config: PixArrayConfig, image) -> List[List[Pixel]]:
    arr = [[Pixel()]*config.length]*config.angle
    # fill in the array with data
    Pixel
    bitshift = 8 - config.resolution  # number of bits to be shifted
    return arr


def txPixArray(serial, pixarray: List[List[Pixel]]):
    for index, angle in enumerate(pixarray):
        # angle element
        logging.info("Sending "+str(index))
        serial.write(index)
        # TODO: Define parser within Pixel class
        # serial.write(angle)


def main():
    initLog()
    # logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("HAPS #2")
    # Function 1
    # Input OrderId
    # Output image
    logging.info("F1")

    db.list_collection(db.DataBaseType.Order)
    try:
        order_id = 0
        image = downloadImage(order_id)
        print(image)
    except Exception as e:
        logging.error("Function 1 error", e)
        return

    # Function 2
    # Input ,image
    # Output pixarrayf
    logging.info("F2")
    image = "Something"
    config = PixArrayConfig()
    pixarr = generatePixArray(config, image)

    # Function 3
    # Input pixarray
    # Output uart signal
    logging.info("F3")
    serial = initSerial("/dev/ttyUSB0")
    logging.info("Serial status: " + str(serial.isOpen()))

    logging.info("Sending...")
    serial.write("hello\n".encode())

    txPixArray(serial, pixarr)
    logging.info("Done")


if __name__ == "__main__":
    main()
