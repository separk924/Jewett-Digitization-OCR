
"""
===================================================================================
Name: image_processing.py
Author: Madi Sanchez-Forman, Seung Park, Emilee Oquist, Ben Mcauliffe
Version: 5.18.23
Decription: This script uses OpenCV and NumPy to preprocess scans of Jewetts handwriting
Expects directory of images to use, will create a new dictionray of images
===================================================================================
"""
#************REQUIREMEMTS************#
# conda install -c conda-forge opencv (only needs to be done once)
# conda activate opencv-env
import numpy as np
import cv2 as cv
import glob
import os,sys 
#************ Paths to Files of Images, make sure to update this to your machines directory or your images ************#

path0 = '/Users/madisonforman/Desktop/jewettDigitization/data/fieldDiary1916/*.jpg' 
path1 = '/Users/madisonforman/Desktop/jewettDigitization/data/unprocessed_scans/may1940/*.jpg' 
path2 = '/Users/madisonforman/Desktop/jewettDigitization/data/fieldDiary1915/*.jpg' 

#************Paths to Files of Images, make sure to update this to your machines file************#

def load_images(path):
    """
    Load images takes a path name and reads in the list of images using cv.imread
    Params: path to image
    Returns: list of cv images
    """
    cv_imgs = []
    for img in glob.glob(path):
        i = cv.imread(img)
        cv_imgs.append(i)
    return cv_imgs

def remove_noise(image):
    """
    Removes noise from an image using Gaussian Blur
    Params: Image to remove noise from
    Returns: Image with noise removed
    """
    blur = cv.GaussianBlur(image,(3, 3),0)
    thresh = cv.threshold(blur, 200, 255, cv.THRESH_BINARY)[1]
    return thresh  

def preprocess_dirty_images(path, new_directory):
    """
    Used on dirty images, cleans them up and saves them to a new directory
    Params: Path to images, string name of new directory
    """
    image_list = load_images(path) #load all images as opencv images
    name_list = create_names(path) #create a list of strings to name
    assert len(image_list) == len(name_list)
    os.mkdir(new_directory)
    os.chdir(new_directory)
    for i in range(len(image_list)):
        image = image_list[i]
        name = name_list[i]
        print(name)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        image = remove_noise(gray)

        nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(~image, 4, cv.CV_32S) #find all connected components
        areas = stats[1:, cv.CC_STAT_AREA]
        result = np.zeros((labels.shape), np.uint8)
        for j in range(0, nlabels - 1):
            if areas[j] >= 100: #if we want to get rid this area (turn it black)
                result[labels == j + 1] = 255
        cv.imwrite(name, ~result) #save the image to new dir

        
def thresholding(img):
    """
    Returns thresholded image
    """
    ret, thresh = cv.threshold(img, 90,255, cv.THRESH_BINARY_INV)
    return thresh
    
def remove_dots(img):
    """
    Removes dotted lines on image and returns them
    """
    ret, bin_map = cv.threshold(img, 215 ,255, 0) #binarize the image
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(~bin_map, 4, cv.CV_32S) 
    
    areas = stats[1:, cv.CC_STAT_AREA] #list of all areas
    result = np.zeros((labels.shape), np.uint8) #empty numpy matrix to hold new image
    for j in range(0, nlabels - 1): #for each label found from connected components
        if areas[j] > 50: #decide if should be filtered
            result[labels == j + 1] = 255 #turn it black (becuase the image had to be inverted earlier)
    return result
    
def preprocess_clean_images(path, alpha, beta):
    cur = 0
    image_list = load_images(path)
    name_list = create_names(path)
    for i in range(len(image_list)):
        image = image_list[i]
        name = name_list[i]
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) 
 
        result = remove_dots(gray)
        result = ~result

def create_names(path):
    """
    Crate names outputs a list of strings that will be file names for the processed images 
    """
    # images = [f for f in os.listdir(dir)]
    lang = 'eng.'
    font = 'jewett'
    string = lang + font + ".exp"
    names = []
    i = 0
    for img in glob.glob(path):
        filename = string + str(i) + ".png"
        names.append(filename)
        i += 1
    return names

def change_names(path):
    name_list = create_names(path)
    image_list = load_images(path)
    # print(len(image_list))
    for i in range(len(image_list)):
        image = image_list[i]
        name = name_list[i]
        os.chdir('/Users/madisonforman/Desktop/jewettDigitization/data/1916_split') 
        cv.imwrite(name, image)

# preprocess_clean_images(path0, 1, 30)
preprocess_dirty_images(path1, "may1940_processed")
