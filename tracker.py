import datetime
import time
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


os.environ['TZ'] = "Asia/Kathmandu"

def notify(inputs):
    print(f"Sending notification {inputs}")
    # Email credentials
    sender_email = "emailbotforall@gmail.com"

    email_list = ["hssaka7@gmail.com", "cva.acharya8@gmail.com","lwagun1@gmail.com"]
    a = ["basnetaakash97@gmail.com", "hssaka7@gmail.com"]
    receiver_email = ', '.join(a)
    password = "lyzs omgg uqfs btdb"

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Passport Date tracker"

    # Add body to email
    _b = ""
    for inp in inputs:
        if "might have dates for" in inp:
            _b = _b + inp + "\n"

    if bool(_b):
        body = _b + "Plese check here: https://emrtds.nepalpassport.gov.np/ "
        message.attach(MIMEText(body, "plain"))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, a, message.as_string())

        print("Email sent successfully!")
    else:
        print("No available dates so not sending email")

def check_dates(location):
    result = None
    print(f"checking for {location}")
    try:
        notice = driver.find_element(By.XPATH, '//*[@id="home"]/app-root/app-appointment/section[2]/div/div[2]/div[1]/div[1]/div[4]/lib-citizen-appointment/div/div/div[2]/p').text
        notice  = f"{notice} : {location}"
        if "There are no available slots at the moment" in notice:
            result = notice
        else:
            result = f"might have dates for {location}"

    except Exception as e:
        print(e)
        result = f"might have dates for {location} as something has changed"
    finally:
        print(result)
        # TODO add the attachments to the results
        return result



def run(url, driver):
    results = []
    driver.get(url)
    time.sleep(2)

    print("selecting passport renewal....")
    driver.find_element(By.XPATH, '//*[@id="services"]/div/div[2]/div/div/div[2]').click() # passport renewal
    time.sleep(1)


    print("selecting ordinary 34 page....")
    driver.find_element(By.XPATH, '//*[@id="home"]/app-root/app-request-service/section[2]/div/div/div[1]/div/form/div/div/div[2]/div[1]/div[1]/label').click() # ordinary 34 page
    time.sleep(1)

    print("selecting proceed and i agree....")
    driver.find_element(By.XPATH, '//*[@id="home"]/app-root/app-request-service/section[2]/div/div/div[1]/div/form/div/div/div[3]/div[2]/a').click()  #proceed
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="mat-dialog-0"]/app-consent-dialog/div/div[3]/a[1]').click() # i agree
    time.sleep(1)

    print("selecting other ....")
    driver.find_element(By.XPATH, '//*[@id="mat-select-0"]/div/div[2]').click() #dropdown 
    driver.find_element(By.XPATH, '//*[@id="mat-option-1"]/span').click() #selecting "Other" 
    time.sleep(1)

    print("selecting washington dc ....")
    driver.find_element(By.XPATH, '//*[@id="mat-select-1"]/div/div[2]').click() #dropdown 
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="mat-option-36"]').click() #selecting "washington dc"
    time.sleep(1)
    results.append(check_dates('washington dc'))


    # select newyork
    print("selecting newyork ....")
    driver.find_element(By.XPATH, '//*[@id="mat-select-1"]/div/div[2]').click() #dropdown 
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="mat-option-31"]').click() #selecting "newyork"
    time.sleep(1)
    results.append(check_dates('newyork'))

    time.sleep(2)
    driver.close()
    return results


if __name__ == "__main__":
    #Date and timezone check"
    current_time = datetime.datetime.now()
    timezone_info = current_time.astimezone().tzinfo
    print("Timezone: ", timezone_info)
    print("Current time: ", current_time)

    base_url = "https://emrtds.nepalpassport.gov.np/"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    results = run(base_url, driver)
    notify(results)
