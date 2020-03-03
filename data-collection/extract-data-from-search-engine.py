#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
import time

driver = webdriver.Chrome()
page = driver.get("https://www.paginebianche.it/")

# accept cookies
cookies = driver.find_element_by_xpath("//*[@class='gdpr_accept']")
cookies.click()


# In[197]:


place = "Pisa"
activity = "hotel"

# search something in the search bar
search_activity = driver.find_element_by_xpath("//*[@id='frmName']/div[1]/input")
search_activity.send_keys(activity)
search_place = driver.find_element_by_xpath("//*[@id='input_dove']")
search_place.send_keys(place)  
search = driver.find_element_by_xpath("//*[@id='frmNameSubmit']")
search.submit()

# wait for results
time.sleep(5)

n = 21 # 20 elements for each page 
hotels = []

# parse results
while True:
    for i in range(1,n):
        hotel = {}
        try:
            hotel['name'] = driver.find_element_by_xpath("//*[@id='co_" + str(i) + "']/div[1]/div[1]/div/h2/a").text
        except:
            break
        hotel['address'] = driver.find_element_by_xpath("//*[@id='co_" + str(i) + "']/div[1]/div[2]/div[1]/div/span/span[1]").text
        hotel['postal_code'] = driver.find_element_by_xpath("//*[@id='co_" + str(i) + "']/div[1]/div[2]/div[1]/div/span/span[2]").text
        hotel['locality'] = driver.find_element_by_xpath("//*[@id='co_" + str(i) + "']/div[1]/div[2]/div[1]/div/span/span[2]").text
        hotel['latitude'] = driver.execute_script("return document.querySelector('#addr_" + str(i) + " > div > div > span:nth-child(1)').textContent;")
        hotel['longitude'] = driver.execute_script("return document.querySelector('#addr_" + str(i) + " > div > div > span:nth-child(2)').textContent;")
        try:
            hotel['telephone'] = driver.find_element_by_xpath("//*[@id='co_" + str(i) + "']/div[1]/div[2]/div[3]/div/span[2]").text
        except:
            hotel['telephone'] = ''
        try:
            hotel['fax'] = driver.find_element_by_xpath("//*[@id='co_" + str(i) + "']/div[1]/div[2]/div[3]/div/span[4]").text
        except:
            hotel['fax'] = ''
        hotels.append(hotel)
    try:
        next_page = driver.find_element_by_xpath("//*[@id='container']/div[2]/div/div/div[4]/div[2]/div[22]/div/div/ul/li[4]/a")
        next_page.click()
    except:
        break
        
import csv

# save results into a csv file
keys = hotels[0].keys()
with open('hotels.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(hotels)



