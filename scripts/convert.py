# Pythono3 code to rename multiple  
# files in a directory or folder 
# and convert all .jpg to .png
# Drop this script in the same
# directory that you want to convert
# images for
  
# importing os module 
import os 
from PIL import Image
  
# Function to rename multiple files 
def main():

    for filename in os.listdir("."):
        if filename[-2] == '-':
            os.rename(filename, filename[:-2])
        elif filename[-3] == '-':
            os.rename(filename, filename[:-3])

        is_jpg = filename[-4:] == '.jpg'
        png_exists = os.path.exists(filename[:-4]+'.png')
        if is_jpg and not png_exists:
            im1 = Image.open(filename)
            im1.save(filename[:-4]+'.png')
            os.remove(filename)
        elif is_jpg and png_exists:
            os.remove(filename)


if __name__ == '__main__': 
    main() 

