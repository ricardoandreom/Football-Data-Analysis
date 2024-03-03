import tweepy

bearer_token = '...'
consumer_key = '...'
consumer_secret = '...'
access_token = '...'
access_token_secret = '...'


api = tweepy.Client(bearer_token=bearer_token,
                    access_token=access_token,
                    access_token_secret=access_token_secret,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret)

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

data_download_loc = "C:/Users/Admin/Downloads"
match = 'SL Benfica 1 - 0 FC Porto'

oldapi = tweepy.API(auth)
media1 = oldapi.media_upload(f'{data_download_loc}/{match}.png')

api.create_tweet(text='Test match report post',media_ids=[media1.media_id])