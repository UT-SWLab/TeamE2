#!/usr/bin/env python3
"""
collect.py
"""

# First party packages
import argparse
import os
import re
import sys
from time import sleep
import urllib

# Third party packages
from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_inputs():
    """
    Purpose:
        Gets inputs for collect.py
    Args:
        None
    Returns:
    """
    parser = argparse.ArgumentParser(description='Request information from an F1 API')
    parser.add_argument('-d', '--driver', dest='driver', action='store_true', help='Request driver data')
    parser.add_argument('-t', '--team', dest='constructor', action='store_true', help='Request team data')
    parser.add_argument('-c', '--circuit', dest='circuit', action='store_true', help='Request circuit data')
    args = parser.parse_args()
    return args.driver, args.constructor, args.circuit


def main():
    driver, constructor, circuit = get_inputs()
    root_path = os.path.dirname(os.path.abspath(__file__))
    
    if driver:
        get_images ('driver', root_path)
    if constructor:
        get_images ('constructor', root_path)
    if circuit:
        get_images ('circuit', root_path)
    return None


def change_dir(path):
    # Make data directory if it does not exist
    os.makedirs(path, exist_ok=True)

    # Change working directory to data directory
    os.chdir(path)


def get_images(type, root):
    # based on https://www.dataskunkworks.com/latest-posts/wikipedia-scraping-2020
    path = os.path.join(root, 'data')
    change_dir(path)
    file_path = os.path.join(path, f'{type}s.csv')
    df = pd.read_csv(file_path)
    df.fillna('', inplace=True)

    # print(df.head)'
    path = os.path.join(root, 'images', type)
    change_dir(path)

    fail_text = f'Could not find images for these {type}s with wikipedia pages:'

    # mask off entries with wiki url
    has_page = df['url'] != ''
    df_valid = df[has_page]
    ref_col = f'{type}Ref'
    for idx in df_valid.index:
        ref_id = df_valid[ref_col][idx]
        url = df_valid['url'][idx]

        # find all img tag from url with Beautiful Soup parser
        content = requests.get(url).content
        soup = BeautifulSoup(content,'lxml')
        image_tags = soup.findAll('img')

        # print out image urls
        success = False
        img_suffix = 0
        for image_tag in image_tags:
            # The first image on the page with the URL structure below is usually 
            # the image inside the infobox. We exlcude any .svg images, as they are 
            # vector graphics common to all Wikipedia pages
            link = image_tag.get('src')

            unwanted = ['flag', 'current', 'symbol', 'icon', 'quote', 'shackle', 'vip' \
                'ribbon', 'commons-logo']
            good_link = True
            for word in unwanted:
                good_link = good_link and not re.search(word, link, re.IGNORECASE)

            if re.search('wikipedia/.*/thumb/', link) and good_link:
                # Once the first image has been found, we break out of the loop and search the next page
                if '.jpg' in link or 'jpeg' in link:
                    file_ext = '.jpg'
                elif '.png' in link:
                    file_ext = '.png'
                elif '.svg' in link:
                    file_ext = '.svg'
                imagefile = open(f'{ref_id}{file_ext}-{img_suffix}', 'wb')
                img_suffix += 1

                imagefile.write(urllib.request.urlopen(f'https:{link}').read())
                imagefile.close()
                success = True

                # back off on requests
                if img_suffix % 4 == 0:
                    sleep(10)
                
        # if loop completes, add wiki url to list of failures and save as txt file
        if success:
            print(f'{ref_id}:\tSuccessfully downloaded {img_suffix} images from {url}')
        else:
            fail_text += url
            print(f'{ref_id}:\tFailed to download image')

        # be nice to the website
        sleep(1)
    

    # write failures to file
    with open("failed.txt", 'w') as file: # Use file to refer to the file object
        file.write(fail_text)
        file.write('\n=================================================================================\n')

    no_page = df['url'] == ''
    nan_text = f'These {type}s do not have wikipedia pages:\n'
    if df[no_page].size > 0:
        print(nan_text)
        print(df[no_page])
        with open("failed.txt", 'a') as file: # Use file to refer to the file object
            file.write(nan_text)
            file.write(str(df[no_page]))



if __name__ == '__main__':
    main()