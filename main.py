from haps_shared.structure import SpinnerProfile
import haps_shared.database as db
import inspect
import os
import logging
import time
import serial
import cv2
import haps_shared.tool as tool


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


def main():
    tool.init_log()
    # logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.info("HAPS #2")
    # Function 1
    # Input OrderId
    # Output image
    logging.info("F1")

    # db.list_collection(db.DataBaseType.Order)
    try:
        crop = db.download_image(order_id='61f4b5083fdf222d1cb3ce25')
        # print(image)
        tool.show(crop, wait_time=1000, label='downloaded crop')
    except Exception as e:
        logging.error("Function 1 error", e)
        return
    profile = SpinnerProfile()
    logging.info("F2")
    strip = tool.deround(crop, profile)
    tool.show(strip, wait_time=1000)
    logging.info("F3")
    final = tool.hold(tool.reround(strip, profile))
    logging.info("F4")


if __name__ == "__main__":

    main()
