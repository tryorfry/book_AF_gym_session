import re
import os
import time
from datetime import datetime, timedelta
import pytz

from selenium import webdriver
from selenium.webdriver.common.by import By

def book_next_hour_slot():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    driver.get('https://www.picktime.com/AFBL')
    time.sleep(2)

    # heroku may run in different location. Hence just enforce timezone so that we book correctly
    sg_now = datetime.datetime.now(pytz.timezone('Asia/Singapore'))

    next_hour_datetime = sg_now + timedelta(hours=1)
    next_hour, am_pm = next_hour_datetime.strftime('%I').lstrip('0'), next_hour_datetime.strftime('%p')
    next_hour_regex = f"{next_hour}\\s*{am_pm}"

    slots = driver.find_elements(By.CSS_SELECTOR, '#booking-content > div.booking-body-cont.unselectable > div.booking-body.clearfix > div > ul > li')

    for i, slot in enumerate(slots):
        if re.match(next_hour_regex, slot.text):
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
            firstname.send_keys(os.environ['firstname'])

            lastname = driver.find_element(By.CSS_SELECTOR, 'input.lastname')
            lastname.send_keys(os.environ['lastname'])

            email = driver.find_element(By.CSS_SELECTOR, 'input.custemail')
            email.send_keys(os.environ['email'])

            mobile = driver.find_element(By.CSS_SELECTOR, 'input.custmobile')
            mobile.send_keys(os.environ['mobile'])

            keyfob = driver.find_element(By.CSS_SELECTOR, 'input.other_of0')
            keyfob.send_keys(os.environ['key'])

            comment = driver.find_element(By.CSS_SELECTOR, 'textarea.bookingcomments')
            #comment.send_keys(f"hello see you. \N{slightly smiling face}")
            # emoji causes problem when running in  headless mode("Chromedriver only supports characters in the BMP")
            # remove for now
            comment.send_keys(f"Hello see you.")

            #time.sleep(4)
            book_appointment_btn = driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
            book_appointment_btn.click()

            driver.quit()

            return {"message", "Successfully booked gym slot"}

if __name__ == '__main__':
    book_next_hour_slot()
