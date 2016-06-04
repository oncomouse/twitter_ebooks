# twitter_ebooks-REDIS

This is an update to https://github.com/patrickt/twitter_ebooks, which is an update to postcasio's version, which is an update to thom's version.

Non-standard twitter dependencies:
* python-Levenshtein - http://pypi.python.org/pypi/python-Levenshtein/
* cobe - https://github.com/pteichman/cobe
* twitter - https://pypi.python.org/pypi/twitter
* yaml – http://pyyaml.org
* redis-py
* simplejson

Use `pip` and `virtualenv` and you can install them all automatically and without clobbering existing features.

This version uses REDIS for data storage instead of a series of .txt files and an SQLite3 database for state and history storage. Doing so means you can run this _ebooks account on Heroku, if you want.

###REQUIREMENTS

- Any decent linux distro. OS X works too.
- A new twitter account 
- The files from this package. Just unzip them into a folder in your user folder (here on out referred to as the ebooks folder)

###PREPARING TWEETS

- Download your Twitter archive. There will be a `tweets.csv` file present therein. Move that into the twitter_ebooks folder. 
- Run `cobe brain init; process.py`.

###CREATE APP

- Log into dev.twitter.com with your bot account. Then clicky: https://dev.twitter.com/apps
- Click create new application and fill out everything but callback url.
- Click on your new application and go into settings. Here, change the application type to Read and Write. Update settings and return the details tab. Here, scroll to the bottom and click 'create my access token'.
- Copy these four values: 
  - consumer key 
  - consumer secret 
  - access token 
  - access token secret 
- Verify that access level is 'read and write'.

###INSTALL PYTHON DEPENDENCIES

(This will assume that you have installed python-distribute through your package manager.)
  - Now download twitter_ebooks https://github.com/patrickt/twitter_ebooks/tarball/master 
  - Make sure you have 'pip', the python distribution manager installed.
    - `pip install -r requirements.txt`
  - You may need gcc and python-devel. Get them from your package manager.

###CREATE YOUR ROBOT 

- Edit the YAML file in the botrc file.
- Put the values you saved from your application earlier in the 'api' bit.
- Follow the instructions for the remainder of the config file. It's well commented 

###DO THIS IN ORDER

2. `python learn.py` (This is only necessary if you enabled auto-learning. This sets the initial "last tweet learned" so you do not feed the bot a tweet twice. on arch this must be python2 learn.py) 
4. `cobe learn tweetfile.txt` (this creates a new brain, using the file you prepared earlier as training) 

Your bot is now ready! test it locally (this won't tweet anything) with:
`python twert.py -o`

When this is to your liking, you can do a final 'live' test by doing:
`python twert.py`

### UPLOAD TO HEROKU

You can now upload your bot to Heroku.

###AUTOMATE YOUR ROBOT

Use the [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler) to run `python twert.py` every hour and `python reply.py` every 10 minutes in order to handle tweeting and replying.