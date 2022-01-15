import serial
import time
import db

def main():
    try:
        print("Helloworld")
        ser = serial.Serial(
            port = "/dev/ttyUSB1",
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout  = 2 # seconds     # <-- HERE
        )
    except:
        print("No UART found")
        return
    print("Serial status: " + str(ser.isOpen()))
    db.list_collection(db.DataBaseType.Order)
    image_64_decode = base64.decodebytes(image_64_encode)

        
    print("Sending...")
    ser.write("hello\n".encode())
    time.sleep(1)

if __name__ == "__main__":
    main()
