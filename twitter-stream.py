# coding: utf-8

import requests
import uuid
import sys
from datetime import datetime
from twitter import TwitterStream, OAuth
from elasticsearch import Elasticsearch
from config import ELASTICSEARCH, TWITTER_API


print('TWEPY - Twitter to Elasticsearch Interface with Python')

auth = OAuth(TWITTER_API["access_key"], TWITTER_API["access_secret"],
             TWITTER_API["consumer_key"], TWITTER_API["consumer_secret"])

stream = TwitterStream(auth=auth)
tweet_iter = stream.statuses.sample()
# pattern = re.compile("%s" % stream_term, re.IGNORECASE)

es = Elasticsearch([{'host': ELASTICSEARCH['host'], 'port': int(ELASTICSEARCH['port'])}])
session = requests.Session()

for tweet in tweet_iter:
    if 'delete' in tweet.keys():
        pass

    else:
        format = '%a %b %d %H:%M:%S %z %Y'
        # Tue Sep 01 17:30:12 +0000 2015
        timestamp = datetime.strptime(tweet['created_at'], format)

        hashtags = []
        if 'hashtags' in tweet['entities']:
            use_hashtag = True
            for hashtag in tweet['entities']['hashtags']:
                hashtags.append(hashtag['text'])

        if len(hashtags) == 0:
            hashtags = None
            use_hashtag = False

        user_mentions = []
        if 'user_mentions' in tweet['entities']:
            use_mention = True
            for users in tweet['entities']['user_mentions']:
                user_mentions.append(users['screen_name'])

        if len(user_mentions) == 0:
            user_mentions = None
            use_mention = False

        result = {
            'lang': tweet['lang'],
            'text': tweet['text'],
            'retweeted': tweet['retweeted'],
            'retweet_count': tweet['retweet_count'],
            '@timestamp': timestamp,
            'user': tweet['user']['screen_name'],
            'user_friends': tweet['user']['friends_count'],
            'user_lang': tweet['user']['lang'],
            'user_geo_enable': tweet['user']['geo_enabled'],
            'coordinates': tweet['coordinates'],
            'geo': tweet['geo'],
            'hashtags': hashtags,
            'user_mentions': user_mentions,
            'use_hashtag': use_hashtag,
            'use_mentions': use_mention,
            }

        sys.stdout.write('.')
        sys.stdout.flush()

        try:
            r = session.get('http://{}:{}'.format(ELASTICSEARCH['host'], ELASTICSEARCH['port']))
            if r.status_code == 200:
                es.create(index=ELASTICSEARCH['index'], doc_type=ELASTICSEARCH['doc_type'], id=uuid.uuid4().hex, body=result)
            else:
                raise Exception
        except Exception as exc:
            print('Error: {}'.format(exc))
