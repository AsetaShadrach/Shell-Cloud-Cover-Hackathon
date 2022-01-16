import os
import glob
import pandas as pd
import re


def sort_digit(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ sort_digit(c) for c in re.split(r'(\d+)', text) ]

dir_name = "test"

list_of_paths= sorted(filter(os.path.isdir, 
                            glob.glob(dir_name+'/*')),
                            key = natural_keys)

df = pd.DataFrame()

for path in list_of_paths:
    csv_path = path+"\\weather_data.csv"

    data = pd.read_csv(csv_path)

    df = pd.concat([df , data], ignore_index =True)


df.to_csv("test_data.csv", index=False)

