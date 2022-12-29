import csv
import time
import datetime
import serial
from serial.tools import list_ports


log_period = 5  # sec


class DataLogger:
    def __init__(self, filename, row_names=list[str]):
        self.filename = filename
        self.file = open(self.filename, 'a')
        self.writer = csv.writer(self.file)
        self.writer.writerow(row_names)

    def log(self, value: list):
        self.writer.writerow(value)
        self.file.flush()

    def close(self):
        self.file.close()


class SerialReader:
    def __init__(self, baudrate, port: str = None):
        if port is not None:
            self.port = port
        else:
            ports = list(list_ports.comports())
            port_name = ""
            for port in ports:
                if "usb" in port.name:
                    port_name = port.name
                    break
            if port_name == "":
                for port in ports:
                    print(f"{port.name}: {port.description}")
                raise Exception("Please select serial port manualy.")
            self.port = "/dev/" + port_name
        self.baudrate = baudrate
        self.serial = serial.Serial(self.port, self.baudrate)

    def read(self) -> str:
        line = self.serial.readline()
        if line != b'':
            try:
                return line.decode("utf-8").strip()
            except UnicodeDecodeError:
                return ""
        return ""

    def close(self) -> None:
        self.serial.close()


ser = SerialReader(115200, 'COM12')

date = datetime.datetime.now()
date = date.strftime("%Y-%m-%d_%H-%M-%S")
data_logger = DataLogger(f"logs/{date}.csv", ['sec', 'electric_power'])

pre_time = time.time() - 100
cnt = 0
while True:
    try:
        electric_power = ser.read()
        try:
            electric_power = float(electric_power)
        except ValueError:
            continue
        if time.time() - pre_time > log_period:
            print(f"electric_power: {electric_power}")
            pre_time = time.time()
            data_logger.log([cnt*log_period, str(electric_power)])
            cnt += 1
    except KeyboardInterrupt:
        data_logger.close()
        ser.close()
        exit(0)
