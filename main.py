import serial
import time
import db
import logging
import sys
import colorlog
from imagedata import Pixel, WarpImage


def printCursor(cursor):
    for record in cursor:
        logging.info(record, "\r\n")


def downloadImage(order_id: int):
    col = db.get_collection(db.DataBaseType.Order)
    # logging.debug(col)
    myquery = {"order_id": order_id}
    cursor = col.find(myquery)
    # printCursor(cursor)
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

    def send_pixel(self, pixel: Pixel):
        self.write(pixel.red)
        self.write(pixel.green)
        self.write(pixel.blue)

    def send_warpimage(self, warpimage: WarpImage):
        set_validation = False

        sec = warpimage.count_section()
        rad = warpimage.count_radius()
        print('Section'+str(sec))
        print('Radius'+str(rad))
        for s in sec:
            self.write(s)
            for r in rad:
                pix = warpimage.data[s][r]
                self.send_pixel(pix)
            self.write('\r\n')
            while len == 0:
                rxline = serial.readline()
                len = len(rxline)


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
        image = downloadImage(order_id=0)
        # print(image)
    except Exception as e:
        logging.error("Function 1 error", e)
        return

    # Function 2
    # Input ,image
    # Output pixarrayf
    logging.info("F2")
    warpimage = WarpImage()

    # Function 3 OK
    # Input pixarray
    # Output uart signal
    logging.info("F3")
    pp = PixelProgrammer('/dev/ttyUSB0')
    if not pp.is_open:
        logging.error("Serial port not open, quitting")
        return

    logging.info("Sending...")
    pp.write("hello\n".encode())
    pp.send_warpimage(warpimage)
    logging.info("Done")


if __name__ == "__main__":
    main()
