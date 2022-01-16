import serial
import time
import db
import logging
import sys
import colorlog


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
    # Output pixarray
    print("F2")
    # Function 3
    # Input pixarray
    # Output uart signal
    print("F3")
    try:
        print("Helloworld")
        ser = serial.Serial(
            port="/dev/ttyUSB0",
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=2  # seconds     # <-- HERE
        )
    except Exception as e:
        logging.error("No UART found")
        return

    logging.info("Serial status: " + str(ser.isOpen()))
    db.list_collection(db.DataBaseType.Order)

    logging.info("Sending...")
    ser.write("hello\n".encode())
    time.sleep(1)


if __name__ == "__main__":
    main()
