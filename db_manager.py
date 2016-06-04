import datetime
import os
import redis
import sys
from simplejson import loads, dumps
from botconfig import config

if "REDIS_SERVER" in os.environ:
    r = redis.from_url(os.environ["REDIS_SERVER"])
else:
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

def filter_lambda(t):
    t = loads(t)
    return t[2] == False or datetime.datetime.now() - datetime.datetime.strptime(t[1],"%Y-%m-%dT%H:%M:%S.%f") > datetime.timedelta(hours = config['log_time'])

def get_tweets():
    tweets_from_db = filter(filter_lambda, r.lrange('twets.db', 0, -1))
    
    txt_tweets = []
    for f in config['brain_tweets']:
        #shove those pieces of shit into a list
        txt_tweets += [line.strip() for line in openfile(f)]
        
    return tweets_from_db + txt_tweets

def insert_tweet(content, ours=True):
    t = [content, datetime.datetime.now(), ours]
    r.rpush('twets.db', dumps(t, default=datetime.datetime.isoformat))

def openfile(path):
    #note: i don't actually know if you have to close + reopen a file to change the mode soooo
    if(len(config['brain_tweets'][0]) == 0):
        return ['']
    if os.path.exists(os.path.join(os.path.dirname(__file__), path)) == False:
        txtfile = open(os.path.join(os.path.dirname(__file__), path), "w")
        txtfile.close
    #open for read and write
    txtfile = open(os.path.join(os.path.dirname(__file__), path), "r+")
    return txtfile