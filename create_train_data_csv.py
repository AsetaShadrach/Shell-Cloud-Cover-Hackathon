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


def date_from_dir(dir):
    # Create the date from the folder name
    month, day = dir[-4:-2], dir[-2:]
    date = '2020-'+month+'-'+day
    date = pd.to_datetime(date)
    month_day = str(date.strftime("%b"))+"-"+day

    return month_day


def time_from_dir(img_path , min):
    #Add the time as a string
    actual_minutes = int(img_path[-8:-6])+min
    # Format to allow for :01, :02 etc
    if actual_minutes < 10:
        actual_minutes = '0'+str(actual_minutes)
    else:
        actual_minutes= str(actual_minutes)
        
    return [img_path[-10:-8]+":"+ actual_minutes]


def get_file_list( condition, dir):
    # Get file/directory list
    file_list = sorted( filter( condition,
                    glob.glob(dir + '/*') ),
                    key = natural_keys )

    return file_list


dir_name = ("train")
         
counter_for_files = 1 # Counter for all subdirectories

# Get the list of folders
list_of_paths = get_file_list(os.path.isdir,dir_name )

# Iterate over sorted list of folders
for file_path in list_of_paths:
    '''
     Make date to use a list
     so that you can concat with the 
     other details in other lists
    '''
    date_to_use = [date_from_dir(file_path)]

    if glob.glob(file_path + '/*'): # Check if the folder has anything
        list_of_files = get_file_list(os.path.isfile,file_path )

        # Store all image flat_lists in the subfolder
        img_vals_to_csv  = []
        co = 0
        for img_path in list_of_files: 
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
                img_time_str = time_from_dir(img_path , min)
                total_list = date_to_use + img_time_str + img_vals
                img_vals_to_csv.append(total_list)


        images_df = pd.DataFrame(img_vals_to_csv[:-9])
        
        csv_name = "combined_train_files\\"+str(counter_for_files)+"combined.csv"
        counter_for_files += 1

        images_df.to_csv(csv_name, index = False)


    else: # If the images folder has nothing
        pass



# Combine all the data into 1 csv
dir_name = "combined_train_files"

# Initialize the df to concat to
full_df = pd.DataFrame() 

list_of_files = sorted( filter( os.path.isfile,
                        glob.glob(dir_name+ '/*') ),
                        key = natural_keys )

for file in  list_of_files:
    df  = pd.read_csv(file,index_col= False )
    full_df  = pd.concat([full_df,df], ignore_index=True) 

full_df.to_csv("full_train_images.csv")
