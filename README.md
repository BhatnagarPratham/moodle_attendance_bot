# moodle_attendance_bot
A selenium bot for marking attendance in lms

Requirements: 

Latest version of python should be installed(preferably Python 3.10 or above)

Once python is installed, install selenium, which can be done by "pip install selenium" in the terminal

Similarlly install webdriver-manager by "pip install webdriver-manager"


How to use the bot:

Now simply make changes to the user_info_morning/evening.py
Enter your institute google email and google password in double quotes

In the attendance_link parameter enter the link of the site with the "Submit attendance" option, the page with all the dates and the logs of attendance.

Once this is done for both morning and evening attendance user_info, simply run the corresponding ._attendance_bot.py file.

The running of the attendance bot file can also be scheduled using windows task scheduler and can be made to run at a specific time everyday by creating "run task"
just make sure the properties are all correct, there is a need to uncheck field "run task only in system idle" and few others which can be taken in account.
