import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv

from dht11 import DHT11

filename = "temperature.csv"
cnt = 12*6 + 1

def get_random_temperature():
    temperature = random.randint(0, 30)
    humidity = random.randint(0, 99)
    return temperature, humidity

def get_last_data(cnt=cnt):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        data = list(reader)
    
    last_data = data[-cnt:]
    x = [datetime.datetime.strptime(row[0], "%Y/%m/%d %H:%M:%S") for row in last_data]
    temp = [float(row[1]) for row in last_data]
    humi = [float(row[2]) for row in last_data]
    return x, temp, humi

def draw_graph(ax, line_temp, line_humi, dt_list, temp_list, humi_list):
    print(f"re-draw! {dt_list[-1]} {temp_list[-1]} {humi_list[-1]}")
    ax.set_xlim(dt_list[0], dt_list[-1]+datetime.timedelta(minutes=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    line_temp.set_xdata(dt_list)
    line_temp.set_ydata(temp_list) 
    line_humi.set_xdata(dt_list)
    line_humi.set_ydata(humi_list)
#    for i in range(cnt):
#        ax.annotate(f"{dt_list[i].strftime('%H:%M')}, {temp_list[i]}", xy=(dt_list[i], temp_list[i]),textcoords="offset points", xytext=(10,0), ha="center", rotation=45)
    

def main():
    dht11 = DHT11(pin=17)
    plt.ion()
    fig, ax = plt.subplots()

    dt_list, temp_list, humi_list = get_last_data()
    ax.set_xlim(dt_list[0], dt_list[-1])
    line_temp, = ax.plot(dt_list, temp_list, marker="o")
    line_humi, = ax.plot(dt_list, humi_list, marker="*")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    ax.set_ylim(0, 100)

    draw_graph(ax, line_temp, line_humi, dt_list, temp_list, humi_list)
    plt.draw()
    plt.pause(1)    

    previous_dt = datetime.datetime.now()
    
    while True:
        dt = datetime.datetime.now()
        dt = dt.replace(microsecond=0)
        str_dt = dt.strftime("%Y/%m/%d %H:%M:%S")

        if previous_dt.minute != dt.minute and dt.minute % 10 == 0:
            for _ in range(10):
                temperature, humidity = dht11.read_data()
                if humidity > 0:
                    break
            if humidity == 0 or temperature > 100:
                temperature = temp_list[-1]
                humidity = humi_list[-1]

            with open(filename, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([str_dt, temperature, humidity])
            print(str_dt, temperature, humidity)
            dt_list.append(dt)
            temp_list.append(temperature)
            humi_list.append(humidity)
            dt_list.pop(0)
            temp_list.pop(0)
            humi_list.pop(0)

            draw_graph(ax, line_temp, line_humi, dt_list, temp_list, humi_list)
            plt.draw()
            plt.pause(0.1)
        previous_dt = dt

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
