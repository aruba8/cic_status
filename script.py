from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
import requests

app_number = os.getenv("APP_NUMBER")
surname = os.getenv("SURNAME")
dob = os.getenv("DOB")
country_id = os.getenv("COUNTRY_ID")
mailgun_api = os.getenv("MAIL_GUN_API")
mailgun_domain = os.getenv("MAIL_GUN_DOMAIN")


def send_simple_message(mailgun_api, mailgun_domain, text):
    return requests.post(
        "https://api.mailgun.net/v3/{0}/messages".format(mailgun_domain),
        auth=("api", mailgun_api),
        data={"from": "MAILGUN User <mailgun@{0}>".format(mailgun_domain),
              "to": ["biomaks@gmail.com"],
              "subject": "status check report",
              "text": text})

driver = webdriver.Firefox()
driver.get("https://services3.cic.gc.ca/ecas/security.do")
driver.find_element_by_id("agree").click()
driver.find_element_by_xpath("//input[@type='submit' and @value='Continue']").click()
select_id_type_elem = driver.find_element_by_id("idTypeLabel")
select_id_type = Select(select_id_type_elem)
select_id_type.select_by_value('3')
driver.find_element_by_id("idNumberLabel").send_keys(app_number)
driver.find_element_by_id("surnameLabel").send_keys(surname)
driver.find_element_by_id("dobDate").send_keys(dob)
select_cob_elem = driver.find_element_by_id("cobLabel")
select_cob = Select(select_cob_elem)
select_cob.select_by_value(country_id)
driver.find_element_by_xpath("//input[@type='submit' and @value='Continue']").click()

status_elem = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//a[@class='ui-link' and contains(@href, 'viewcasehistory.do')]")))
status = status_elem.text

status_elem.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Logout']")))
note_elems = driver.find_elements_by_xpath("//form/ol/li")

note_template = "{0}. {1}\n"
notes = "\n"
counter = 1
for note_el in note_elems:
    notes = notes + note_template.format(counter, note_el.text)
    counter = counter + 1

driver.close()
text = """
{0}
Today application status: {1}
notes: {2}
"""

if status != "In Process":
    text = text.format("Status changed!!!!!", status, notes)
else:
    text = text.format("Nothing changed", status, notes)

send_simple_message(mailgun_api, mailgun_domain, text)
