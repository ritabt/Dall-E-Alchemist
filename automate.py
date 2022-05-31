from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pdb


path = "C:\\Users\\ritat\\OneDrive\\Desktop\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)
# to maximize the browser window
driver.maximize_window()
url = "https://huggingface.co/spaces/dalle-mini/dalle-mini"
driver.get(url)

# Let website load

#identify text box
# text_cl"ss_name = "block gr-box gr-input w-full gr-text-input  !rounded-tl-lg !rounded-tr-none !rounded-br-none !rounded-bl-lg !mt-0 !mr-0 !mb-0 !ml-0 !border-r-0"
# # <input type="text" class="block gr-box gr-input w-full gr-text-input  !rounded-tl-lg !rounded-tr-none !rounded-br-none !rounded-bl-lg !mt-0 !mr-0 !mb-0 !ml-0 !border-r-0" placeholder="">
# # <div id="6" class="w-full overflow-hidden border-solid border border-gray-200 rounded-lg gr-panel form gr-box-unrounded !p-0 !m-0 !border-0 !shadow-none overflow-visible"><div class="absolute inset-0 z-10 flex flex-col justify-center items-center bg-white dark:bg-gray-800 pointer-events-none transition-opacity svelte-cyw4c6 opacity-0"></div> <label class="block w-full"><span class="text-gray-600 text-[0.855rem] mb-2 block dark:text-gray-200 relative z-40 sr-only h-0 !m-0">Enter your prompt</span> <input type="text" class="block gr-box gr-input w-full gr-text-input  !rounded-tl-lg !rounded-tr-none !rounded-br-none !rounded-bl-lg !mt-0 !mr-0 !mb-0 !ml-0 !border-r-0" placeholder=""></label></div>
# l = driver.find_element_by_class_name(text_class_name)
# # inputElement = driver.find_element_by_id("6")
# #send input
# l.send_keys("coconut crab")
# pdb.set_trace()
# //*[@id="6"]/label/input

sleep(10)
print("Pressing Run")
# button_xpath = "//*[@id=\"7\"]"
# button_xpath = "/html/body/div[1]/div[2]/div/div[3]/div[1]/div/button"
# ttt = '"7"'
# button_xpath = "//*[@id=%s]" % ttt
button_xpath = '//*[@id="7"]'
button = driver.find_element(By.XPATH, button_xpath)
# button = driver.find_element_by_id("7")
button.click()
# sleep(30)

#to close the browser
driver.quit()