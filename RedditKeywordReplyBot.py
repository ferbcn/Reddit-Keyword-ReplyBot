#!/usr/bin/python

import praw
import re
import os
import time

from config import ID, SECRET, PASSWORD, AGENT, USERNAME

#SUBS = ['eth', 'cryptocurrencies', 'ethereum']
KEYWORDS = ['future', 'bright', 'crypto']

SUBS = ['cryptocurrencies']
LIMIT = 100

reddit = praw.Reddit (client_id=ID, client_secret=SECRET, password=PASSWORD, user_agent=AGENT, username=USERNAME)
reddit.read_only = False

while (True):
    for SUB in SUBS:
        print ('###', SUB, '###')
        print ('Checking submissions for keywords ...')
        subreddit = reddit.subreddit (SUB)
        # Have we run this code before? If not, create an empty list
        if not os.path.isfile ("posts_replied_to.txt"):
            posts_replied_to = []

        # If we have run the code before, load the list of posts we have replied to
        else:
            # Read the file into a list and remove any empty values
            with open ("posts_replied_to.txt", "r") as f:
                posts_replied_to = f.read ()
                posts_replied_to = posts_replied_to.split ("\n")
                posts_replied_to = list (filter (None, posts_replied_to))

        # Get the top LIMIT values from our subreddit
        for submission in subreddit.hot (limit=LIMIT):
            ReplyToPost = False
            print ("Title: ",submission.title)

            # If we haven't replied to this post before
            if submission.id not in posts_replied_to:

                # CONDITIONS FOR THE BOT
                # Do a case insensitive search where all keywords need to appear in order our bot to reply
                #print (submission.selftext)
                for keyword in KEYWORDS:
                    if re.search (keyword, submission.selftext, re.IGNORECASE):
                        # Set flag for replying to the post
                        ReplyToPost = True
                    else:
                        ReplyToPost = False

                # REPLY ACTIONS
                if ReplyToPost:
                    print ("\n>Bot replying to:", submission.title, "(", submission.id, ")")
                    reply = "Hi, I am a bot! Wow, such future, everyone clueless, beep boooooooop!"

                    # Store the current id into our list
                    posts_replied_to.append (submission.id)
                    # Write our updated list back to the file
                    with open ("posts_replied_to.txt", "w") as f:
                        for post_id in posts_replied_to:
                            f.write (post_id + "\n")
                    print (reply)

                    # Post Reply
                    try:
                        submission.reply (reply)
                        # submission.downvote ()
                    except Exception as e:
                        print(e)

                    print ('>Bot is waiting for 10 sec.\n')
                    # time.sleep (541)
                    time.sleep (10)

    print ('\n>All done! Bot will sleep for 5 min. Zzzz...\n')
    time.sleep (300)
