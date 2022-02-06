from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

from pprint import pprint


driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://www.picktime.com/AFBL')
time.sleep(2)

next_hour_datetime = datetime.now() + timedelta(hours=1)
next_hour, am_pm = next_hour_datetime.strftime('%I').lstrip('0'), next_hour_datetime.strftime('%p')
next_hour_regex = f"{next_hour}\\s*{am_pm}"

slots = driver.find_elements(By.CSS_SELECTOR, '#booking-content > div.booking-body-cont.unselectable > div.booking-body.clearfix > div > ul > li')

for i, slot in enumerate(slots):
    if re.match(next_hour_regex, slot.text):
        print('------------------matched_____')
        #click_point = slot.find_element(By.CSS_SELECTOR, 'div.bl-center')
        driver.execute_script("arguments[0].click();", slot)

        time.sleep(2)
        af_center = driver.find_element(By.CSS_SELECTOR, '#booking-content > div.booking-body-cont.unselectable > div.booking-body.clearfix > div > ul > li')
        driver.execute_script("arguments[0].click();", af_center)

        time.sleep(2)
        this_slot_session = driver.find_element(By.CSS_SELECTOR, '#booking-content > div.booking-body-cont.unselectable > div.booking-body.clearfix > div > ul > li')
        driver.execute_script("arguments[0].click();", this_slot_session)

        time.sleep(2)
        # fill in the form and submit
        firstname = driver.find_element(By.CSS_SELECTOR, 'input.firstname')
        firstname.send_keys('Sachin')

        lastname = driver.find_element(By.CSS_SELECTOR, 'input.lastname')
        lastname.send_keys('Dangol')

        email = driver.find_element(By.CSS_SELECTOR, 'input.custemail')
        email.send_keys('sachindangol@gmail.com')

        mobile = driver.find_element(By.CSS_SELECTOR, 'input.custmobile')
        mobile.send_keys('90125510')

        keyfob = driver.find_element(By.CSS_SELECTOR, 'input.other_of0')
        keyfob.send_keys('1d81245')

        comment = driver.find_element(By.CSS_SELECTOR, 'textarea.bookingcomments')
        comment.send_keys(f"hello see you. \N{slightly smiling face}")

        time.sleep(4)
        book_appointment_btn = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
        book_appointment_btn.click()

        driver.quit()