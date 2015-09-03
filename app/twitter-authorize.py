# coding: utf-8

from config import TWITTER_API

"""
twitter-authorize:
 - step through the process of creating and authorization a
   Twitter application.

Based on: https://github.com/ideoforms/python-twitter-examples
"""

import twitter
import time

print("1. Create a new Twitter application here: https://apps.twitter.com")
print("When you have created the application, enter:")
print("   your application name: "),
app_name = input()

if TWITTER_API['consumer_key']:
    consumer_key = TWITTER_API['consumer_key']
else:
    print("   your consumer key: "),
    consumer_key = input()

if TWITTER_API['consumer_secret']:
    consumer_secret = TWITTER_API['consumer_secret']
else:
    print("   your consumer secret: "),
    consumer_secret = input()

print("2. Now, authorize this application.")
print("You'll be forwarded to a web browser in two seconds.")
print()

time.sleep(2)

try:
    access_key, access_secret = twitter.oauth_dance(app_name, consumer_key, consumer_secret)
except Exception as e:
    print("Error: {}".format(e))

print("Done.")
print("Now, replace the credentials in config.py with the below:")
print()

print("consumer_key = {}".format(consumer_key))
print("consumer_secret = {}".format(consumer_secret))
print("access_key = {}".format(access_key))
print("access_secret = {}".format(access_secret))
