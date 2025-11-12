#!/usr/bin/env python3
import pandas as pd
from pathlib import Path
import numpy as np
import datetime
from math import floor

def time_to_delat(t):
    """Convert datetime.time object with hour and minute to datetime.timedelta object"""
    dt = datetime.timedelta(hours=t.hour, minutes=t.minute)
    return dt
def trans_form_tostring(dt):
    hours = dt.seconds//3600
    minutes = (dt.seconds//60)%60
    seconds = dt.seconds%60
    return f"{hours}:{minutes}:{seconds}"

def main():
    # set path to csv
    path_to_csv = Path("Attendance.csv")
    # set names for the columns
    header = ['ID','Datetime']
    # read the csv as pandas dataframe
    df = pd.read_csv(path_to_csv, names = header,parse_dates=True)
    # Convert the column 'Date' to a datetime object
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Date'] = df['Datetime'].dt.date
    df['Time'] = df['Datetime'].dt.time

    for ID in df.ID.unique():
        # Iterate over every unique ID of employee and Filter for a single ID
        one_employee = df[df['ID']==ID].sort_values(by='Date')
        # Get the earliest start time of a day and the latest time of a day
        start_per_day = one_employee.groupby('Date')['Time'].min()
        end_per_day = one_employee.groupby('Date')['Time'].max()
        # Convert array of datetime.time objects to array of datetime.timedelta objects
        start_per_day_dt = np.array([time_to_delat(x) for x in start_per_day])
        end_per_day_dt = np.array([time_to_delat(x) for x in end_per_day])
        # get the duration for a single day
        delta_per_day = [trans_form_tostring(x) for x in (end_per_day_dt - start_per_day_dt)]
        # Create an empty list dates for the attendance
        attended_days = []
        for i,working_day in enumerate(one_employee.Date.unique()):
            if delta_per_day[i] == "0:0:0":
                delta_per_day[i] = "No Logout for this day"
            day = working_day.strftime("%d/%m/%Y")
            attended_days.append(f"{day}\t{delta_per_day[i]}")
        create_excel_output(ID,attended_days,Path("C:\Face-Recogntion-PyQt-master\Face_Detection_PyQt_Final"))

def create_excel_output(ID, dates,outpath=None):
    protocol_file = f"Attendance of ID-{ID} {datetime.date.today()}.txt"
    if outpath is not None:
        protocol_file = outpath / f"Attendance of ID-{ID} {datetime.date.today()}.txt"
    employee = f"Employee ID - {ID}"
    with open(protocol_file,'w') as txt:
        txt.write(employee+"\n\n")
        txt.write("Date\tDuration\n")
        for line in dates:
            txt.write(line)
            txt.write("\n")

if __name__ == '__main__':
    main()
