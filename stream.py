import tweepy

from secret import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, users, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = set(users)
        self.file = open(file_path, 'a')

    def on_status(self, status):
        if status.user in self.users:
            self.file.write(status.text)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    kremlin = 'KremlinRussia'
    trump = 'realDonaldTrump'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    kremlin_user = api.create_friendship(screen_name=kremlin)
    trump_user = api.create_friendship(screen_name=trump)

    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(users=(kremlin_user, trump_user), file_path='temp.txt'))
    myStream.filter(follow=[str(trump_user.id), str(kremlin_user.id)])
