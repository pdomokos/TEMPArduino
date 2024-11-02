from datetime import datetime

import serial


def writeTemp(row):
   with open("temp_data.txt","a") as f:
      f.write(row)




with serial.Serial('/dev/ttyACM0', 115200, timeout=300) as ser:
   while True:
      line = ser.readline()
      now = datetime.now()
      strd = now.strftime("%Y-%m-%d %H:%M:%S")
      x = line.decode("utf-8").split("#")
      writeTemp(strd+"#"+line.decode("utf-8"))


