# Author: Foster C. Williams
# Email: fosterclarksonwilliams@gmail.com
#github: github.com/fosdos
import tweepy, sys, time
from control import twitter_timer
class bot(object):
  """
  Fosdos easy twitter bot driver
  """
  keys = []
  my_following = []
  my_followers = []
  leech_list = []
  def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
    keys = []
    self.my_follow_list = []
    self.keys.append(consumer_key)
    self.keys.append(consumer_secret)
    self.keys.append(access_key)
    self.keys.append(access_secret)
    self.my_follow_list = []
    self.my_followers = []
    self.leech_list = []


  def gen_follow_lists(self):
    api = self.authenticate()
    me = api.me().screen_name
    follow_list_pages = []
    print("Generating list of followed users...")
    try:
      for follower in tweepy.Cursor(api.friends).items():
        self.my_following.append(follower.screen_name.encode('ascii','ignore'))
    except:
      print("failed to generate following list")
      return
    print("Success...")
    print("Generating list of followers...")
    try:
      for follower in tweepy.Cursor(api.followers).items():
        self.my_followers.append(follower.screen_name.encode('ascii','ignore'))
    except:
      print ("failed to generate follower list")
    print ("Success...")
    return

  def authenticate(self):
    CONSUMER_KEY = self.keys[0]
    CONSUMER_SECRET = self.keys[1]
    ACCESS_KEY = self.keys[2]
    ACCESS_SECRET = self.keys[3]
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    toReturn = tweepy.API(auth, wait_on_rate_limit=True)
    try:
      auth_test = toReturn.me().screen_name
      return toReturn
    except:
      return False
  def follow_user(self, twitter_screen_name):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        api.create_friendship(twitter_screen_name)
        return True
      except:
        return False
  def unfollow_user(self,twitter_screen_name):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        api.destroy_friendship(twitter_screen_name)
        return True
      except:
        return False
  def id_to_screenname(self,twitter_id):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        screen_name = api.get_user(twitter_id).screen_name
        return screen_name
      except:
        return False
  def get_user_follower_count(self,twitter_screen_name):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        count = api.get_user(twitter_screen_name).followers_count
        return count
      except:
        return False
    return int(follower_counter)
  def get_user_following_count(self,twitter_screen_name):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        count = api.get_user(twitter_screen_name).friends_count
        return count
      except:
        return False
  def get_follower_count(self):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        count = api.me().followers_count
        return count
      except:
        return False
  def get_following_count(self):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      try:
        count = api.me().friends_count
        return count
      except:
        return False
  def following_me(self,twitter_screen_name):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    ids = self.my_followers
    if twitter_screen_name in ids:
      return True
    else:
      return False
  def generate_long_leech_list(self,twitter_names):
    toReturn = []
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    try:
      for x in range(len(twitter_names)):
        counter = 0
        for follower in tweepy.Cursor(api.followers, screen_name=twitter_names[x]).items():
          if counter > 15:
            break
          if(follower.followers_count <= follower.friends_count):
            if(self.following_me(follower.screen_name.encode('ascii','ignore'))!=True):
              if( follower.screen_name.encode('ascii','ignore') not in self.my_following):
                if(follower.followers_count>50):
                  toReturn.append(follower.screen_name.encode('ascii','ignore'))
                  counter = counter + 1
      self.leech_list = toReturn
      return toReturn
    except Exception as ex:
      template = "An exception of type {0} occured. Arguments:\n{1!r}"
      message = template.format(type(ex).__name__, ex.args)
      print(message)
      return False

  def generate_leech_list(self,twitter_name):
    toReturn = []
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    try:
      counter = 0
      for follower in tweepy.Cursor(api.followers, screen_name=twitter_name).items():
        toReturn.append(follower.screen_name.encode('ascii','ignore'))
        counter = counter + 1
        if (counter>=100):
          break
      return toReturn
    except:
      return False
  def get_user_name(self):
    api = self.authenticate()
    if(api == False):
      self.auth_failed()
      return False
    else:
      return api.me().screen_name.encode('ascii','ignore')
  def auth_failed(self):
    return "Shit something failed"
  def start(self):
    timers = []
    prey = self.leech_list
    amount_of_timers = 10
    for x in range(amount_of_timers):
      timers.append(twitter_timer("set"))
    counter = 0
    print("Made timer list just fine...")
    tester = 0
    print("Started outside loop")
    while(counter < len(prey)):
      print("Started inside loop")
      for x in range(len(timers)):
        if(timers[x].user_screen_name=="set"):
          timers[x] = twitter_timer(prey[counter])
          print ("Trying to Follow Someone")
          self.follow_user(prey[counter])
          counter = counter + 1
          time.sleep(3600)
        check = timers[x].time_check()
        if (check != False):
          user = timer[x].time_check()
          self.unfollow_user(user)
          time.sleep(3600)
          timers[x] = twitter_timer(prey[counter])

          self.follow_user(prey[counter])
          counter = counter + 1
          time.sleep(3600)
        time.sleep(300)
