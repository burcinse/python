
#-----------------------------------------

import os
from PIL import Image
from psd_tools2 import PSDImage

#-----------------------------------------

#Directory of EXE file
exe_dir = os.path.dirname(os.path.abspath(__file__))

#-----------------------------------------

def resize_images(dir):

    files = os.listdir(dir)
    files_list = [f for f in files if os.path.isfile(os.path.join(dir, f))]
    print(files_list)
    
    for m in files_list:
        file = os.path.join(dir, m)
        img = Image.open(file)
        w = img.width
        h = img.height
        print(file)
        print("w: " + str(w))
        print("h: " + str(h))
        #Resize all sizes larger than 1000 x 1000 px
        if w > 1000 or h > 1000:        
            #Considering that the aspect ratio is different, make it the larger criterion
            s = (1000, int(1000*h/w)) if w > h else (int(1000*w/h), 1000)
            print(s)
            img_resize = img.resize(s, Image.LANCZOS)
            img_resize.save(file) 
        print("-------------------------")   

#-----------------------------------------

#Taking the directory of the first hierarchy into consideration also takes it as the larger criterion

folder = os.path.join(exe_dir, "images")
dir_1 = os.listdir(folder)
files_dir1 = [f for f in dir_1 if os.path.isdir(os.path.join(folder, f))]

#print(files_dir1)

for i in files_dir1:
    #Directory acquisition of the second hierarchy
    dir_2 = os.listdir(os.path.join(folder, i))
    files_dir2 = [f for f in dir_2 if os.path.isdir(os.path.join(folder, i, f))]

    #print(files_dir2)
    
    for ii in files_dir2:
    
        target = os.path.join(folder, i, ii)
        resize_images(target)
    

#-----------------------------------------