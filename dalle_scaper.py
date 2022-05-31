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

def prompts_from_label(label, prompt_patterns):
	labels = []
	prompts = []

	return labels


def generate_prompts(word_list, prompt_patterns):
	labels = []
	prompts = []
	for idx, i in enumerate(word_list):
		for j in word_list[idx:]:
			for p in prompt_patterns:
				for p_iters in range(p[1]):
					#Forward 
					new_prompt = ""
					for c in list(p[0]):
						if(c=="1"):
							new_prompt+=i
						elif(c=="2"):
							new_prompt+=j
						else:
							new_prompt+=c
					prompts.append(new_prompt)

					if(i==j):
						labels.append(i+" "+i)
						continue

					#Backward
					new_prompt = ""
					for c in list(p[0]):
						if(c=="1"):
							new_prompt+=j
						elif(c=="2"):
							new_prompt+=i
						else:
							new_prompt+=c
					prompts.append(new_prompt)

					if(i<j):
						labels.append(i+" "+j)
						labels.append(i+" "+j)
					else:
						labels.append(j+" "+i)
						labels.append(j+" "+i)
					
						
	return labels, prompts

			


def dalle_scrape(prompts, output_dir, labels):
	#defining browser and adding the “ — headless” argument
	opts = Options()
	opts.add_argument(' — headless')
	driver = webdriver.Chrome('chromedriver', options=opts)

	#Step 1: Open Webpage
	url = 'https://huggingface.co/spaces/dalle-mini/dalle-mini'
	driver.maximize_window() #maximize the window
	

	for prompt_idx, prompt in enumerate(prompts):
		driver.get(url)          #open the URL
		driver.implicitly_wait(220) #maximum time to load the link

		#Give Dalle some time to open
		time.sleep(2)


		#Step 2: Switch to IFrame and get the elements 
		frame = driver.find_element_by_xpath('/html/body/div/main/iframe')
		driver.switch_to.frame(frame)

		prompt_box = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/div/label/input') 
		run_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/button')
	
	
	#Step 3: Loop through prompt list

		prompt_box.send_keys(Keys.CONTROL + "a")
		prompt_box.send_keys(Keys.DELETE)
		prompt_box.send_keys(prompt)
		driver.implicitly_wait(220)	
		
		run_button.click()
		driver.implicitly_wait(220)	
		time.sleep(2)

		#Get all the images

		for i in range(1, 10):
			img_element = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[3]/div[2]/div[3]/div/button['+str(i)+']/img')
			img_src = img_element.get_attribute('src');

			urllib.request.urlretrieve(img_src,"img.png")
			img = Image.open("img.png")

			image_folder_pth = output_dir+labels[prompt_idx]+"/"
			
			if(not os.path.exists(image_folder_pth)):
				os.makedirs(image_folder_pth)
			img.save(image_folder_pth+labels[prompt_idx]+str(len(os.listdir(image_folder_pth)))+".png")

		

def main():
	output_dir = "C:/Users/coles/Desktop/Dall-E/out_ims/"
	word_list = ["seashell", "dollar"]
	prompt_patterns = [("1 2, a", 1)]

	labels, prompts = generate_prompts(word_list, prompt_patterns)

	dalle_scrape(prompts, output_dir, labels)


if __name__ == '__main__':
	main()
