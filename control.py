# Author: Foster C. Williams
# Email: fosterclarksonwilliams@gmail.com
#github: github.com/fosdos


import time
import datetime

class twitter_timer(object):
  start_time = None
  user_screen_name = None
  def __init__(self, user_screen_name):
    self.start_time = datetime.datetime.now()
    self.user_screen_name = str(user_screen_name)
  def __str__(self):
    return "Timing " + str(self.user_screen_name) + ", started on: " + str(self.start_time)
  def time_check(self):
    if((datetime.datetime.now() - self.start_time).total_seconds() > 86400):
      return self.user_screen_name
    else:
      return False
  def time_test(self):
    return str(self.user_screen_name)
