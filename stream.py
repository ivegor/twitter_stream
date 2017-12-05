import logging
from datetime import timezone
from functools import partial
from typing import Sequence

import tweepy

from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

log = logging.getLogger('twitter')


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, users: Sequence[int], file_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = set(users)
        self.file = partial(open, file=file_path, mode='a', encoding='utf-8')

    def on_status(self, status):
        if status.author.id in self.users:
            with self.file() as file:
                datetime = status.created_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
                print(datetime, status.author.name, sep=', ',  file=file)


if __name__ == '__main__':
    kremlin = 'KremlinRussia'
    trump = 'realDonaldTrump'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    kremlin_user = api.create_friendship(screen_name=kremlin)
    trump_user = api.create_friendship(screen_name=trump)

    while True:
        try:
            myStream = tweepy.Stream(
                auth=api.auth, listener=MyStreamListener(users=(kremlin_user.id, trump_user.id), file_path='temp.txt')
            )
            myStream.filter(follow=[str(trump_user.id), str(kremlin_user.id)])
        except Exception as e:
            log.error(e)
