# coding: utf-8

import requests
import uuid
import sys
from datetime import datetime
from twitter import TwitterStream, OAuth
from elasticsearch import Elasticsearch, client
from config import ELASTICSEARCH, TWITTER_API


def auth():
    auth = OAuth(
                 TWITTER_API["access_key"],
                 TWITTER_API["access_secret"],
                 TWITTER_API["consumer_key"],
                 TWITTER_API["consumer_secret"]
                 )
    return auth


def return_datetime(string):
    format = '%a %b %d %H:%M:%S %z %Y'
    return datetime.strptime(string, format)


def return_hashtags(tweet):
    hashtags = []
    if 'hashtags' in tweet['entities']:
        for hashtag in tweet['entities']['hashtags']:
            hashtags.append(hashtag['text'])
    return hashtags


def return_user_mentions(tweet):
    user_mentions = []
    if 'user_mentions' in tweet['entities']:
        for users in tweet['entities']['user_mentions']:
            user_mentions.append(users['screen_name'])
    return user_mentions


def contains_in_list(list):
    if len(list) == 0:
        return False
    else:
        return True


def connect_to_es():
    search = Elasticsearch([{'host': ELASTICSEARCH['host'], 'port': int(ELASTICSEARCH['port'])}])
    session = requests.Session()
    try:
        request = session.get('http://{}:{}'.format(ELASTICSEARCH['host'], ELASTICSEARCH['port']))
        if request.status_code == 200:
            return search
        else:
            return False
    except:
        return False


def send_to_es(body):
    connect = connect_to_es()
    if connect:
        connect.create(index=ELASTICSEARCH['index'], doc_type=ELASTICSEARCH['doc_type'], id=uuid.uuid4().hex, body=body)
    else:
        sys.stdout.write('E')
    sys.stdout.flush()


def template_es():
    # This function put mapping for create data structure
    print('Create mapping for Elasticsearch')
    connect = connect_to_es()
    interface = client.IndicesClient(connect)
    if connect:
        body = '{"order":0,"template":"*","settings":{},"mappings":{"_default_":{"dynamic_templates":[' \
                      '{"string_fields":{"mapping":{"index":"analyzed","type":"string","fields":{"raw":{' \
                      '"index":"not_analyzed","type":"string"}}},"match_mapping_type":"string","match":"*"}}]'\
                      ',"_all":{"enabled":true}}},"aliases":{}}'
        template = interface.exists_template(ELASTICSEARCH['template'],)
        if template:
            print('Mapping existis, using it.')
        else:
            print('Creating map for use!')
            interface.put_template(name=ELASTICSEARCH['template'], body=body)


if __name__ == '__main__':
    print('TWEPY - Twitter to Elasticsearch Interface with Python')
    stream = TwitterStream(auth=auth())
    tweet_iter = stream.statuses.sample()
    template_es()

    for tweet in tweet_iter:
        if 'delete' in tweet.keys():
            pass

        else:
            timestamp = return_datetime(tweet['created_at'])

            hashtags = return_hashtags(tweet)
            use_hashtags = contains_in_list(hashtags)

            user_mentions = return_user_mentions(tweet)
            use_mentions = contains_in_list(user_mentions)

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
                'use_hashtags': use_hashtags,
                'use_mentions': use_mentions,
                }

            send_to_es(result)
