# Import selenium package
import sqlite3
import os
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException


# Creates an 'instance' of your driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)
links_browser = webdriver.Chrome(chrome_options=chrome_options)

# getting to the desired url
browser.get("http://github.com/search?utf8=%E2%9C%93&q=selenium&type=")

# calculating the time for the performance Performance Timing Events flow
# navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd
# -> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd
# -> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd

navigationStart = browser.execute_script("return window.performance.timing.navigationStart")
responseStart = browser.execute_script("return window.performance.timing.responseStart")
domComplete = browser.execute_script("return window.performance.timing.domComplete")
totalPerformance = domComplete - navigationStart

right_title = 'Search · selenium · GitHub'

# checking that we are indeed in the right page
live_title = browser.title

# getting the desired data by xpath, i is the result number (first result => i=1 and so on),getting the first 5 results
# saving the results in a 2d array data[i] == result [i] . data[0][0] == title of first link and so on
items, links = 6, 5
# entering zeroes so i can tell where there is no value
data = [[0 for x in range(items)] for y in range(links)]
# time performance for each link
time_prfmnce = [0, 0, 0, 0, 0]

# different table for tags, in data we put flag to know if there are any tags
tags_table = [[0 for x in range(8)] for y in range(links)]

for i in range(0, 5):
    # description
    description_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/p" % (i+1))
    data[i][1] = description_element.text
    # tags
    # - checking if there are any tags
    try:
        # checking for NoSuchElementException - by first tag element
        flag_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/div[1]/a[1]"% (i + 1))
        # there are no exception we can get all elements
        tag_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/div[1]"% (i + 1))
        tags_table[i] = tag_element.text.split("\n")
        # in order to keep single format
        while len(tags_table[i]) < 8:
            tags_table[i].append(0)
        # this is the flag for tags ; 1 == there are tags. 0 == there arent any tags
        data[i][2] = 1
    except NoSuchElementException:
        pass
    # time
    # - checking if there is a license - if there is going to p[2] else p
    #  then checking format div or div[2], no other patterns discovered may be one more
    try:
        time_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/div[2]/p[2]/relative-time" % (i + 1))
        data[i][3] = time_element.text
    except NoSuchElementException:
        try:
            time_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/div[2]/p/relative-time" % (i + 1))
            data[i][3] = time_element.text
        except NoSuchElementException:
            try:
                time_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/div/p[2]/relative-time" % (i + 1))
                data[i][3] = time_element.text
            except NoSuchElementException:
                try:
                    time_element = browser.find_element_by_xpath("// *[ @ id = \"js-pjax-container\"] / div / div[1] / div[2] / div /ul/div[%d]/div[1]/div[2]/p/ relative - time" % (i + 1))
                    data[i][3] = time_element.text
                except NoSuchElementException:
                    time_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/div/p/relative-time" % (i + 1))
                    data[i][3] = time_element.text
    # lang
    lang_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[2]" % (i+1))
    data[i][4] = lang_element.text
    # stars
    stars_element = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[3]/a" % (i+1))
    data[i][5] = stars_element.text
    # title
    # checking if the link is active + measuring time
    URL = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/h3/a" % (i+1)).get_attribute('href')
    request = requests.get(URL)
    if request.status_code == 404:
        print('Web Page is not active')
        exit(1)
    links_browser.get(URL)
    link_navigationStart = links_browser.execute_script("return window.performance.timing.navigationStart")
    link_domComplete = links_browser.execute_script("return window.performance.timing.domComplete")
    time_prfmnce[i] = link_domComplete - link_navigationStart
    title_elem = browser.find_element_by_xpath("//*[@id=\"js-pjax-container\"]/div/div[1]/div[2]/div/ul/div[%d]/div[1]/h3/a" % (i+1))

    data[i][0] = title_elem.text
    # key for two tables == title
    tags_table[i].append(title_elem.text)
browser.close()
links_browser.close()

# printing time to text file
text_file = open("Search_query_time.txt", "w")
text_file.write("Search query took: %.2f ms" %totalPerformance)
text_file.close()

text_file2 = open("Links_time.txt", 'w')
for i in range(0, 5):
    text_file2.write("Link number %.f took: %.2f ms," % (i+1 , time_prfmnce[i]))
text_file2.close()

# Inserting records into the data table
sql1 = """INSERT OR REPLACE INTO DATA(TITLE, DESCRIPTION, TAGS_FLAG, TIME, LANGUAGE, STARS) VALUES(:TITLE, :DESCRIPTION, :TAGS_FLAG, :TIME, :LANGUAGE, :STARS)"""
sql2 = """INSERT OR REPLACE INTO TAGS(TAG1, TAG2, TAG3, TAG4, TAG5, TAG6, TAG7, TAG8, TITLE) VALUES(:TAG1, :TAG2, :TAG3, :TAG4, :TAG5, :TAG6, :TAG7, :TAG8, :TITLE)"""

# Setting up connection
conn = sqlite3.connect('data_db.db')
try:
    conn.execute('''CREATE TABLE DATA(TITLE STRING PRIMARY KEY, DESCRIPTION STRING, TAGS_FLAG INTEGER, TIME STRING, LANGUAGE STRING, STARS STRING)''')
    conn.commit()
    conn.execute('''CREATE TABLE TAGS(TAG1 INTEGER, TAG2 INTEGER, TAG3 INTEGER, TAG4 INTEGER, TAG5 INTEGER, TAG6 INTEGER, TAG7 INTEGER, TAG8 INTEGER, TITLE STRING PRIMARY KEY)''')
    conn.commit()
except:
    pass
for i in range(0, 5):
    conn.execute(sql1, data[i])
    conn.commit()
    conn.execute(sql2, tags_table[i])
    conn.commit()

conn.close()