#importing required libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium_move_cursor.MouseActions import move_to_element_chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import js
import json
import numpy as np
import time
import pandas as pd         #to save CSV file
from bs4 import BeautifulSoup
import ctypes         #to create text popup

import urllib.request
from PIL import Image

import os

import color_transfer
import cv2

import math
import os
from PIL import Image
from dask.diagnostics import ProgressBar
from imageio import imread
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import dask.array as da
import numpy as np
import matplotlib.pyplot as plt

#SRC: https://towardsdatascience.com/the-perils-of-palette-transfer-f2739b5e4d2c
class KMeansReducedPalette:
    ''' The K-means reduced palette class.

    Takes an image and performs k-means on all the RGB pixels of the image. The
    value of k is equal to `num_colors`.

    Args
    ---
        num_colors (int): the number of colors in the reduced palette.
    '''
    def __init__(self, num_colors):
        self.num_colors = num_colors
        self.kmeans = KMeans(num_colors, random_state=0xfee1600d)
        self.source_pixels = None

    def _preprocess(self, image):
        ''' Preprocess an image.

        Check that an image has exactly 3 color channels (RGB) and that the
        data type is numpy.uint8 (i.e. values between 0 and 255). Then, convert
        the image from W x H x C into WH x C.

        Args
        ---
            image (numpy.ndarray): the image to be preprocessed.

        Returns
        ---
            numpy.ndarray: the flattened image keeping all RGB pixels in the
                columns.
        '''
        assert image.shape[-1] == 3, 'image must have exactly 3 color channels'
        assert image.dtype == 'uint8', 'image must be in np.uint8 type'

        # Flatten pixels, if not already.
        if len(image.shape) > 2:
            return image.reshape(-1, 3)

        return image

    def fit(self, image):
        ''' The fit function for the palette.
        
        PPreprocesses the reference image and perform k-means clustering on the
        pixels. Then, find the distance of each pixel to the nearest centroid.

        Args
        ---
            image (numpy.ndarray): the reference image for this palette.
        '''
        image_cpy = image.copy()
        self.source_pixels = self._preprocess(image_cpy)
        self.kmeans.fit(self.source_pixels)
        
        # self.centroid_nearest_pixels = []

        # for ci in range(self.num_colors):
        #     pixels_ci = self.source_pixels[self.kmeans.labels_ == ci]
        #     distances_ci = np.sqrt(np.sum(np.square(
        #         pixels_ci - self.kmeans.cluster_centers_[ci]), axis=1))
        #     pixels_ci = pixels_ci[np.argsort(distances_ci)]

        #     self.centroid_nearest_pixels.append(pixels_ci)

    def recolor(self, image):
        ''' Transfer the reduced palette onto another image.

        Takes an image, applies k-means clustering on the pixels of the image,
        replace the predicted cluster center's color onto the image.

        Args
        ---
            image (numpy.ndarray): the input image for palette reduction.

        Returns
        ---
            numpy.ndarray: the recolored image based on this reduced palette.
        '''
        original_shape = image.shape
        image = self._preprocess(image)
        recolor_idx = self.kmeans.predict(image)
        recolor = self.kmeans.cluster_centers_[recolor_idx]
        recolor = np.round(recolor).astype(np.uint8)  # Round back to 0-255.

        return recolor.reshape(original_shape)

#Set outline to new color
def recolor_outline(img):
	img[np.all(img == 0, axis=-1)] = 255
	return img

def color_transfer(img_dir, out_dir, palette_pth):
	
	palette_to_match = KMeansReducedPalette(320)
	palette_img = np.asarray(Image.open(palette_pth).convert('RGB'))

	#print("unique", np.unique(palette_img, axis=0).shape)
	palette_to_match.fit(palette_img)
	print(palette_to_match.kmeans.cluster_centers_.shape)
	#palette_to_match.kmeans.cluster_centers_[]


	for filename in os.listdir(img_dir):
		img = np.asarray(Image.open(img_dir+filename).convert('RGB'))
		#img = recolor_outline(img)

		alpha = Image.open(img_dir+filename).convert('RGBA').split()[-1]

		#palette_to_change = KMeansReducedPalette(64)
		
		#palette_to_change.fit(img)
		#reduced_img =  palette_to_change.recolor(img)
		recolored_img = Image.fromarray(palette_to_match.recolor(img)).convert('RGBA')
		recolored_img.putalpha(alpha)



		image_out_dir = out_dir+filename
		recolored_img.save(image_out_dir)


def pixelate(img_dir, out_dir, recolor=False, palette_pth=""):
	#defining browser and adding the “ — headless” argument
	opts = Options()
	opts.add_argument(' — headless')
	driver = webdriver.Chrome('chromedriver', options=opts)

	#Step 1: Open Webpage
	url = 'https://pixel-me.tokyo/en/'
	driver.maximize_window() #maximize the window

	driver.get(url)          #open the URL
	driver.implicitly_wait(220) #maximum time to load the link
	time.sleep(2)

	in_img_elem = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/section[3]/div/div/div[2]/div/div[2]/form/input")

	#SELECT TRANSPARENT BACKGORUND
	#----------------------------
	test_im_path = "C:/Users/coles/Desktop/Dall-E/img.png"
	in_img_elem.send_keys(test_im_path)
	driver.implicitly_wait(220)
	time.sleep(10)
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight,)")
	time.sleep(2)

	#Select the transparent background
	driver.find_element_by_xpath("/html/body/div[1]/div/div/div/section[4]/div/div/div[2]/div/div[2]/div[2]").click()
	driver.implicitly_wait(220)
	time.sleep(2)
	driver.find_element_by_xpath('//*[@id="__layout"]/div/div/section[4]/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]').click()
	driver.implicitly_wait(220)
	time.sleep(2)
	driver.find_element_by_xpath("/html/body/div[1]/div/div/div/section[4]/div/div/div[2]/div/div[2]/div/div[2]/div/div[4]/div[32]/div").click()
	time.sleep(2)



	image_sizes = [128, 64, 48, 32]
	#Step 2: Loop through images
	for filename in os.listdir(img_dir):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight,)")

		f = os.path.join(img_dir, filename)
		
		in_img_elem.send_keys(f)
		driver.implicitly_wait(220)
		time.sleep(10)


		for i in range(1, 5):
			img_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/section[4]/div/div/div[2]/div/div[2]/div[1]/div/div/div/div["+str(i)+"]")
			img_button.click()
			print("CLICKED IMAGE")
			driver.implicitly_wait(220)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight,)")
			time.sleep(2) 

			download_button = driver.find_element_by_xpath('//*[@id="__layout"]/div/div/section[5]/div/div[2]/div[1]/div/div[1]/div/div[4]')
			download_button.click()
			print("CLICKED DOWNLOAD")
			driver.implicitly_wait(220)
			time.sleep(2)

			img_to_save = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/section[5]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div[2]/img')
			#img_to_save = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/section[5]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div[2]/img')


			img_src = img_to_save.get_attribute('src');
			time.sleep(1)
			urllib.request.urlretrieve(img_src,"img.png")
			#print("SOURCE   ", img_src)
			img = Image.open("img.png")

			image_out_dir = out_dir+"original_color/"+str(image_sizes[i-1])+"/"
			if(not os.path.exists(image_out_dir)):
	 			os.makedirs(image_out_dir)

			image_out_dir = image_out_dir+filename
			#Resize image to correct size
			img = img.resize((image_sizes[i-1], image_sizes[i-1]), Image.NEAREST)
			img.save(image_out_dir)


			if(recolor):
				rec_image_out_dir = out_dir+"recolored/"+str(image_sizes[i-1])+"/"

				if(not os.path.exists(rec_image_out_dir)):
	 				os.makedirs(rec_image_out_dir)
				rec_image_out_dir = rec_image_out_dir+filename
				img.save(recolored(img, palette_pth))



			#16 bit one 
			# image_out_dir = os.path.join(out_dir, str(16))
			# if(not os.path.exists(image_out_dir)):
	 	#  		os.makedirs(image_out_dir)
			# image_out_dir = os.path.join(image_out_dir, filename.split(".")[0]+" "+str(image_sizes[i-1])+".png")
			# img = img.resize((16, 16), Image.NEAREST)
			# img.save(image_out_dir)


			close_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/section[5]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div[3]/div/span/span')
			close_button.click()
			driver.implicitly_wait(220)
			time.sleep(1)

			





	# 	for i in range(1, 10):
	# 		img_element = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/div/button['+str(i)+']/img')
	# 		img_src = img_element.get_attribute('src');

	# 		urllib.request.urlretrieve(img_src,"img.png")
	# 		img = Image.open("img.png")

	# 		image_folder_pth = output_dir+labels[prompt_idx]+"/"
			
	# 		if(not os.path.exists(image_folder_pth)):
	# 			os.makedirs(image_folder_pth)
	# 		img.save(image_folder_pth+labels[prompt_idx]+str(len(os.listdir(image_folder_pth)))+".png")

		

def main():
	img_dir = "C:/Users/coles/Desktop/Dall-E/to_pixelate/"
	out_dir = "C:/Users/coles/Desktop/Dall-E/pixelated/"
	palette_pth  = "C:/Users/coles/Desktop/Dall-E/AliceTheAljemistPalette.png"
	#palette_pth  = "C:/Users/coles/Desktop/Dall-E/lil_witch.jpg"
	#pixelate(img_dir, out_dir, recolor=True, palette_pth =palette_pth)

	img_dir = "C:/Users/coles/Desktop/Dall-E/NPC_torecolor/"
	out_dir = "C:/Users/coles/Desktop/Dall-E/NPC_recolored/"
	color_transfer(img_dir, out_dir, palette_pth)


if __name__ == '__main__':
	main()
