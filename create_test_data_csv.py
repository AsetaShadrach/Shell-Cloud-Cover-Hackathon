import re
import os
import glob
import cv2
import pandas as pd

# Functions to sort file names exactly how they appear
def sort_digit(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ sort_digit(c) for c in re.split(r'(\d+)', text) ]


dir_name = os.path.join("Shell ML","test")
         
counter_for_files = 1 # Counter for all subdirectories

list_of_paths = sorted( filter( os.path.isdir,
                        glob.glob(dir_name + '/*') ),
                        key = natural_keys )
# Iterate over sorted list of files and print the file paths 
# one by one.
for file_path in list_of_paths:
    list_of_files = sorted( filter( os.path.isfile,
                        glob.glob(file_path + '/*') ),
                        key = natural_keys )

    # Store all image flat_lists in the subfolder
    img_vals_to_csv  = []
    
    for img_path in list_of_files[:-1] : # Leave out the csv file
        img_vals  = [] 
        image = cv2.imread(img_path)
        resized_image = cv2.resize( image,
                                    (24,28),
                                    interpolation=cv2.INTER_AREA)
        gray_image = cv2.cvtColor(  resized_image,
                                    cv2.COLOR_BGR2GRAY)
        
        # Flatten the list
        for pix_val_lists in gray_image :
            img_vals.extend(pix_val_lists)

        # Since the images are recorded every 10 mins
        for min in range(10):
            img_vals_to_csv.append(img_vals)


    weather_df = pd.read_csv(list_of_files[-1])
    images_df = pd.DataFrame(img_vals_to_csv[:-9])
    merged_df = pd.concat([ weather_df,images_df],
                            axis=1  )

    csv_name = "Shell ML\\combined_test_files\\"+str(counter_for_files)+"combined.csv"
    counter_for_files += 1

    merged_df.to_csv(csv_name, index = False)



dir_name = "Shell ML\\combined_test_files"

full_df = pd.DataFrame() # Initialize the df to concat to

list_of_files = sorted( filter( os.path.isfile,
                        glob.glob(dir_name+ '/*') ),
                        key = natural_keys )

for file in  list_of_files:
    df  = pd.read_csv(file)
    full_df  = pd.concat([full_df,df], ignore_index=True) 

full_df.to_csv("full_test_df.csv")

