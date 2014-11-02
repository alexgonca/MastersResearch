# coding=utf-8
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import MySQLdb as myDB
import ConfigParser
from jdcal import gcal2jd
import datetime

first_day = datetime.datetime(2013, 12, 07)
number_of_days = 1
search_term = u"shopping itaquera"

config = ConfigParser.ConfigParser()
config.read('info.config')
con = myDB.connect(config.get('db', 'host'), config.get('db', 'username'),
                   config.get('db', 'password'), config.get('db', 'schema'))
con.set_character_set('utf8')
cur = con.cursor()
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

date_list = [first_day + datetime.timedelta(days=x) for x in range(0, number_of_days)]

for date in date_list:
    ranking = 1

    julian_date = int(gcal2jd(date.year, date.month, date.day)[0] +
                      gcal2jd(date.year, date.month, date.day)[1] + 0.5)

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.private.browsing.autostart", True)
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get("http://www.google.com.br/")

    inputElement = driver.find_element_by_name("q")
    inputElement.send_keys(search_term + " daterange:" + str(julian_date) + "-" + str(julian_date))
    inputElement.submit()

    wait = WebDriverWait(driver, 100)
    wait.until(EC.title_contains(search_term+ " daterange:"))

    more_pages = True
    start_parameter = '10'
    while more_pages:
        google_links = driver.find_elements_by_xpath("//ol[@id='rso']/div/li/div/h3/a")
        google_blurbs = driver.find_elements_by_xpath("//ol[@id='rso']/div/li/div/div/div")
        for i in range (0, len(google_links)):
            cur.execute('INSERT INTO google '
                        '(url, title, ranking, date, query, blurb) '
                        'values (%s, %s, %s, %s, %s, %s)',
                        (google_links[i].get_attribute("href"), google_links[i].text, ranking,
                         str(date.year) + "-" + str(date.month) + "-" + str(date.day),
                         search_term, google_blurbs[i].text))
            ranking += 1

        next_page = driver.find_elements_by_xpath("//a[@id='pnnext']")
        if len(next_page) == 0:
            more_pages = False
        else:
            next_page[0].click()
            can_move = False
            while not can_move:
                next_page = driver.find_elements_by_xpath("//a[@id='pnnext']")
                if len(next_page) == 0:
                    can_move = True
                else:
                    try:
                        initial_index = next_page[0].get_attribute("href").find("&start=") + 7
                        final_index = next_page[0].get_attribute("href").find("&", initial_index)
                        if final_index == -1:
                            final_index = len(next_page[0].get_attribute("href"))
                        current_start_parameter = next_page[0].get_attribute("href")[initial_index:final_index]
                        if start_parameter == current_start_parameter:
                            time.sleep(0.1)
                        else:
                            start_parameter = current_start_parameter
                            can_move = True
                    except selenium.common.exceptions.StaleElementReferenceException as e:
                        time.sleep(0.1)
    con.commit()
    driver.quit()