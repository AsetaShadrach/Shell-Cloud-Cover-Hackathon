import pandas as pd
import datetime
# Create a new CSV with re-ordered dates 

train_df = pd.read_csv("train\\train.csv")

def date_reorder(row):
    date_items = row.split("-")
    if date_items[0].isdigit():
        return date_items[1]+"-"+date_items[0]
    else:
        return row
    # Tmie colum = MST


train_df["DATE (MM/DD)"] = train_df["DATE (MM/DD)"].apply(date_reorder)
# Reorder the values by dates Jan 1 to Dec 31
train_array = sorted(train_df.values, 
                    key=lambda x: datetime.datetime.strptime("2020-"+x[0], 
                                                             "%Y-%b-%d" )
                    ) 
train_df = pd.DataFrame(train_array, columns= train_df.columns)

train_df.to_csv("train2.csv", index = False)


'''
This second part will combine 
the images df with the train data
'''
'''
train_data = pd.read_csv("train2.csv")

train_images_data = pd.read_csv("full_train_images.csv", 
                                index_col=False)
train_images_data = train_images_data.drop('Unnamed: 0',axis=1)

no_of_columns = len(train_images_data.columns) -2
# Add the first 2 columns
first_columns = ["DATE (MM/DD)","MST"]
# Re-order the remaining columns
other_columns = [i for i in range(no_of_columns)]
#Restructure_the columns_of the dataframe
train_images_data.columns =  first_columns + other_columns


final_df = pd.merge(train_data , train_images_data, 
                    how="inner", 
                    on=["DATE (MM/DD)","MST"])


final_df  =  final_df.dropna(how="any")

final_df.to_csv("final_train.csv")
'''