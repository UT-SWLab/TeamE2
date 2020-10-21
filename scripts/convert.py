
# Pythono3 code to rename multiple  
# files in a directory or folder 
# and convert all .jpg to .png
  
# importing os module 
import os 
  
# Function to rename multiple files 
def main():

    for filename in os.listdir("."):
        if filename[-2] == '-':
            os.rename(filename, filename[:-2])
        elif filename[-3] == '-':
            os.rename(filename, filename[:-3])

  
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 

