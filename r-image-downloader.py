#-----------------------------------------
# r-image-downloader
# 
# 
#-----------------------------------------

import os
import re
import urllib.error
import urllib.request
import random
import pandas as pd

#-----------------------------------------

#Forced download flag
flag = "False"

#-----------------------------------------

#Execution file directory
exe_dir = os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------

#Reading Files
df = pd.read_csv(exe_dir + '/csv/list.csv', dtype='object', low_memory=False)
df = df.fillna('')

#-----------------------------------------

for i, row in df.iterrows():

    #Image acquisition from web
    imgs = [row['MainImage'], row['OtherImage1'], row['OtherImage2'], row['OtherImage3'], row['OtherImage4'], row['OtherImage5']]

    for index, url in enumerate(imgs):
        code = row['ID']
        dir_1 = code[0:3] #First three digits in the first level directory
        dir_2 = code[3:6] #The next three digits are placed in the second level directory

        if index > 0:
            filename = row['ID'] + "_" + str(index) + ".jpg"
        else:
            filename = row['ID'] + ".jpg"

        if url:
            dst_path = exe_dir + "/images/" + os.path.join(dir_1, dir_2, filename)
            stored_path = exe_dir + "/images-stored/" + os.path.join(dir_1, dir_2, filename)
            
            print(dst_path)

            #Download only when images are not acquired yet
            if flag == "True":
                try:
                    data = urllib.request.urlopen(url).read()
                    with open(dst_path, mode="wb") as f:
                        f.write(data)
                except urllib.error.URLError as e:
                    print(e)
                                
            elif not os.path.isfile(stored_path) and not os.path.isfile(dst_path):
                
                #Create a new folder if it does not exist
                if not os.path.isdir(os.path.join(exe_dir, "images", dir_1)):
                    os.mkdir(os.path.join(exe_dir, "images", dir_1))
                if not os.path.isdir(os.path.join(exe_dir, "images", dir_1, dir_2)):
                    os.mkdir(os.path.join(exe_dir, "images", dir_1, dir_2))
                                    
                try:
                    data = urllib.request.urlopen(url).read()
                    with open(dst_path, mode="wb") as f:
                        f.write(data)
                except urllib.error.URLError as e:
                    print(e)
            else:
                print(filename + "I already have one")


