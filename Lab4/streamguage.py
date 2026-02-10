import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class StreamGuage:
    time = []
    data = []
    units="ft"
    
    def __init__(self, fid, station_id, station_name, starttime):
        self.fid = fid 
        self.station_id = station_id
        self.station_name = station_name
        self.starttime = starttime

    def read_guage_file(self):
        """
        Read USGS Guage data and convert date and time to minutes since start

        parameters
        fid (str): path to data

        returns
        timestamps (list): minutes since 2024-09-01 00:00
        hgt (np.array): guage height in ft
        """
        date, time, hgt = np.loadtxt(self.fid, skiprows=28, usecols=[2,3,5], 
                                        dtype=str).T

        hgt = hgt.astype(float)
        days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
        hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
        mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

        timestamps = []
        for d, h, m in zip(days, hours, mins):
            timestamp = (d * 24 * 60) + (h * 60) + m
            timestamps.append(timestamp)

        self.time = timestamps
        self.data = hgt

    def plot(self):
        plt.figure(figsize=(10, 5))
        plt.title("Stream Guage <{}> <{}> <{}> <{}> <{}>".format(
            self.station_id, self.station_name, self.starttime, 
            max(self.data), self.units))
        plt.plot(self.time, self.data, c='k')
        datetime_object = datetime.strptime(self.starttime, '%Y-%m-%d %H:%M')

        # 2. Extract the month and year as integers
        month = datetime_object.month  # 10
        year = datetime_object.year

        plt.xlabel("Time (minutes since start of {}-{})".format(year, month))
        plt.ylabel("Guage Height ({})".format(self.units))
        plt.show()

    def convert(self):
        """
        Convert guage height from ft to m
        """
        self.data = self.data * 0.3048
        self.units = "m"

    def demean(self):
        """
        Demean the guage data
        """
        self.data = self.data - np.mean(self.data)
    
    def shift_time(self, shift):
        """
        Shift the time by a certain amount. 

        parameters
        shift (float): amount to shift time in minutes
        """
        self.time = [t + shift for t in self.time]

    def main(self):
        self.read_guage_file()   
        self.plot()   

        self.convert()   
        self.demean()   
        self.shift_time(-100)
        self.plot()   

class NOAAStreamGuage(StreamGuage):
    units="m"
    convert = False
    

if __name__ == "__main__":
    start = ["2024-09-07 00:00", "2024-10-07 00:00"]
    for i, fid in enumerate(["phelan_creek_stream_guage_2024-09-07_to_2024-09-14.txt",
                "phelan_creek_stream_guage_2024-10-07_to_2024-10-14.txt"]): 
        StreamGuage(fid=fid, station_id="15478040", 
                     station_name="PHELAN CREEK", 
                     starttime=start[i]).main()  