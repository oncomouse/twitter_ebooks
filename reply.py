import twitter, os
import config
from simplejson import loads, dumps
from cobe.brain import Brain

def smart_truncate(content, length=140):
	    if len(content) <= length:
	        return content
	    else:
	        return content[:length].rsplit(' ', 1)[0]

b = Brain(os.path.join(os.path.dirname(__file__), 'cobe.brain'))

try:
	state = loads(open(os.path.join(os.path.dirname(__file__), '.state'), 'r').read())
except:
	state = {}

if 'last_reply' not in state:
	state['last_reply'] = 0

api = twitter.Api(**config.api)

def check_names(rp):
	for name in config.screen_name:		
		if rp.user.screen_name.lower() == name.lower():
			return True
	return False

if config.replies:
	print "Performing replies"
	
	last_tweet = long(state['last_reply'])

	replies = api.GetReplies(since_id=last_tweet)

	for reply in replies:
		if check_names(reply):
			continue
		try:
			reply_tweet = smart_truncate('@%s %s' % (reply.user.screen_name.encode('utf-8', 'replace'), b.reply(reply.text.encode('utf-8', 'replace')).encode('utf-8', 'replace')))
			api.PostUpdate(reply_tweet, in_reply_to_status_id=reply.id)
		except:
			print 'Error posting reply.'
		last_tweet = max(reply.id, last_tweet)

	state['last_reply'] = str(last_tweet)

print "Saving state"

open(os.path.join(os.path.dirname(__file__), '.state'), 'w').write(dumps(state))