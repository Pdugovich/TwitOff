"""Retreive tweets, embeddings, and persist in the database"""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

# OLD TERRIBLE CODE
# def add_user_and_tweets(twitter_handle):
#     twitter_user = TWITTER.get_user(twitter_handle)
#     tweets=twitter_user.timeline(
#         count=200,
#         exclude_replies=True,
#         include_rts=False,
#         tweet_mode='extended'
#         )
#     db_user = User(
#         id=twitter_user.id,
#         name=twitter_user.screen_name,
#         newest_tweet_id=tweets[0].id
#         )
#     for tweet in tweets:
#         embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
#         db_tweet = Tweet(
#             id=tweet.id, 
#             text=tweet.full_text[:500], 
#             embedding=embedding
#             )
#         db_user.tweets.append(db_tweet)
#         DB.session.add(db_tweet)
#     DB.session.commit()

def add_or_update_user(username):
    """Add or update a user and their tweets, or return error"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user=(User.query.get(twitter_user.id) or
        User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        tweets=twitter_user.timeline(count=200, exclude_replies=True,
                                     include_rts=False, 
                                     tweet_mode='extended', 
                                     since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # Calc embeedding on full tweet
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], 
                             embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username,e))
        raise e
    else:
        DB.session.commit()