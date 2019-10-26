from csv import DictWriter
from random import triangular
from time import sleep

tempo, sensor_1, sensor_2, sensor_3 = 0, 0, 0, 0


fieldnames = ["tempo", "sensor_1", "sensor_2", "sensor_3"]


with open('data.csv', 'w') as csv_file:
    csv_writer = DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "tempo": tempo,
            "sensor_1": sensor_1,
            "sensor_2": sensor_2,
            "sensor_3": sensor_3
        }

        csv_writer.writerow(info)
        print(tempo, sensor_1, sensor_2, sensor_3)

        tempo += 1
        sensor_1 = round(triangular(low=0.0, high=1500.0, mode=400.0),1)
        sensor_2 = round(triangular(low=-40.0, high=380.0, mode=0.0),1)
        sensor_3 = round(triangular(low=20.0, high=150.0, mode=60.0),1)

    sleep(0.1)
