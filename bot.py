import time
import tkinter
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from tkinter import *


class Bot():
    def __init__(self, email, password, attendance_link):
        self.email = email
        self.password = password
        self.attendance_link = attendance_link


    def google_login(self, bot, email, password):
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


    def log_into_lms(self,bot):
        # print("here1")
        bot.get(self.attendance_link)  # redirects to login page
        # sign into lms
        try:
            # print("here2")
            bot.implicitly_wait(10)
            bot.find_element(By.XPATH, "//*[@id='region-main']/div/div[2]/div/div/div/div/div/div[2]/div[3]/div/a").click()
        except:
            pass


    def binary_search(self, rows):
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

            if len(row.find_elements(By.TAG_NAME, 'a')) == 0:
                end = mid-1
            # print("here")
            # print(submit_attendance_button.text)
            else:
                submit_attendance_button = row.find_element(By.TAG_NAME, 'a')
                if "submit" in submit_attendance_button.text.lower():
                    return submit_attendance_button
                else:
                    end = mid - 1
        return False


    def show_error(self):
        root = Tk()
        texto = Toplevel(root)
        root.withdraw()
        root.after(20000, root.destroy)
        tkinter.messagebox.showerror(title="Something went wrong", message="Attendance NOT Marked", parent=texto)

    def show_info(self):
        root = Tk()
        texto = Toplevel(root)
        root.withdraw()
        root.after(20000, root.destroy)
        tkinter.messagebox.showinfo(title="Success", message="Attendance Marked Successfully", parent=texto)

    def mark_attendance(self):

        bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        self.google_login(bot, self.email, self.password)
        not_completed = True
        while not_completed:
            try:
                self.log_into_lms(bot)
                bot.implicitly_wait(10)

                # find the submit attendance button
                rows = bot.find_elements(By.TAG_NAME, 'tr')
                if len(rows) < 5:
                    # print("here3")
                    continue

                # print("submit_button not found")
                submit_attendance_button = self.binary_search(rows)
                # print("submit_button found" + str(submit_attendance_button))
                if submit_attendance_button == False:
                    marked = False
                else:
                    submit_attendance_button.click()
                    bot.implicitly_wait(10)
                    check = bot.find_elements(By.NAME, 'status')
                    while len(check) == 0:
                        bot.refresh()
                        bot.implicitly_wait(10)
                        check = bot.find_elements(By.NAME, 'status')
                    present_button = check[0]
                    # print(present_button.text)
                    present_button.click()
                    bot.implicitly_wait(10)
                    check = bot.find_elements(By.NAME, 'submitbutton')
                    while len(check) == 0:
                        bot.refresh()
                        bot.implicitly_wait(10)
                        check = bot.find_elements(By.NAME, 'submitbutton')
                    save_changes = check[0]
                    save_changes.click()
                    marked = True
                # print(marked)

                not_completed = False
                if not marked:
                    self.show_error()
                else:
                    self.show_info()
            except:
                #nothing
                pass
        bot.close()
