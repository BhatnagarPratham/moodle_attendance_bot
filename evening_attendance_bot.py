import time
import tkinter
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from tkinter import *
import user_info_evening as user


def google_login(email, password):
    bot.get(
        "https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
    )
    bot.implicitly_wait(5)
    enter_username = bot.find_element(By.NAME, "identifier")
    enter_username.send_keys(email + '\n')
    # enter_username.send_keys(Keys.RETURN)
    # driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button/span").click()
    bot.implicitly_wait(5)
    enter_password = bot.find_element(By.NAME, "password")
    enter_password.send_keys(password + '\n')
    # enter_password.send_keys(Keys.RETURN)
    # driver.find_element(By.XPATH, "//*[@id='passwordNext']/div/button/span").click()
    time.sleep(4)


def log_into_lms():
    bot.get(user.attendance_link)  # redirects to login page
    # sign into lms
    bot.implicitly_wait(10)
    bot.find_element(By.XPATH, "//*[@id='region-main']/div/div[2]/div/div/div/div/div/div[2]/div[3]/div/a").click()


def binary_search(rows):
    start = 2
    end = len(rows) - 4

    while start <= end:

        mid = (start + end) // 2
        row = rows[mid]
        cols = row.find_elements(By.TAG_NAME, 'td')
        # print(cols[0].text)
        if "Present" in cols[2].text:
            start = mid + 1
            continue
        try:
            submit_attendance_button = row.find_element(By.TAG_NAME, 'a')
            # print("here")
            # print(submit_attendance_button.text)
            if "submit" in submit_attendance_button.text.lower():
                return submit_attendance_button
            else:
                end = mid - 1
        except Exception:
            end = mid-1
            continue

    return False

def show_error():
    root = Tk()
    texto = Toplevel(root)
    root.withdraw()
    root.after(20000, root.destroy)
    tkinter.messagebox.showerror(title="Something went wrong", message="Attendance NOT Marked", parent=texto)


bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

google_login(user.email, user.password)

log_into_lms()
bot.implicitly_wait(10)

#find the submit attendance button
rows = bot.find_elements(By.TAG_NAME, 'tr')
submit_attendance_button = binary_search(rows)

marked = False

if(submit_attendance_button == False):
    marked = False
else:
    submit_attendance_button.click()
    present_button = bot.find_element(By.NAME, 'status')
    # print(present_button.text)
    present_button.click()
    save_changes = bot.find_element(By.NAME, 'submitbutton')
    save_changes.click()
    marked = True

if ~marked :
    show_error()