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
    # Function 1
    # Input OrderId

    # Setup UART
    logging.info("F1")
    logging.info("UARTs")
    print(serial_ports())
    uart = PixelProgrammer(serial_ports()[0])

    # db.list_collection(db.DataBaseType.Order)
    try:
        #TTC
        # crop = db.download_image(order_id='61f4b5083fdf222d1cb3ce25')
        crop = db.download_image(order_id='620a2ba26a74fd1cdb7872fc')
        # print(image)
        # tool.show(crop, wait_time=1000, label='downloaded crop')
    except Exception as e:
        logging.error("Function 1 error", e)
        return
    profile = SpinnerProfile()
    logging.info("F2")
    strip = tool.deround(crop, profile)
    tool.show(strip, wait_time=1000)
    logging.info("F3")
    # final = tool.hold(tool.reround(strip, profile))
    # logging.info("F4")

    # send every 2 lines
    line_per_message = 2
    msg = []
    counter=0


    for sec in strip:
        for pixel in sec:
            # RGB
            msg.append(pixel[0])
            msg.append(pixel[1])
            msg.append(pixel[2])

        if len(msg) >= line_per_message * profile.led_count * 3:
            counter+=1
            logging.info("Transfering %d of %d", counter, profile.angle_count/line_per_message)
            # print(msg)
            uart.write(msg)
            val = uart.read(size=4)
            if len(val)<4:
                logging.error('no reply')
            else:
                print(val)
            msg.clear()
            time.sleep(0.01)

    # x,y,z = strip.size()


if __name__ == "__main__":

    main()
