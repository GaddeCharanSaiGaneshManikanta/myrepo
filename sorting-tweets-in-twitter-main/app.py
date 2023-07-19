import streamlit as st
import API_KEYS as api
from tweepy import API,OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt

authentication=OAuthHandler(api.api_key,api.api_secret)
tapi=API(authentication)
st.title('sorting of specific tweets on twitter')
tweet_input=st.text_input('Enter a word to search')

def clean_tweets(tweet):
    tweet_words=str(tweet).split(' ')
    clean_words=[word for word in tweet_words if not word.startswith('#')]
    return ' '.join(clean_words)

positive_tweets=[]
negative_tweets=[]

if st.button('sort tweets'):
    print(tweet_input)
    public_tweets=tapi.search_tweets(tweet_input,count=100)
    
    cleaned_tweets=[clean_tweets(tweet.text) for tweet in public_tweets]
    for tweet in cleaned_tweets:
        tweet_polarity=TextBlob(tweet).sentiment.polarity
        if tweet_polarity<0:
            negative_tweets.append(tweet)
        else:
            positive_tweets.append(tweet)
    st.success(len(positive_tweets))
    st.warning(len(negative_tweets))
    labels=['positive','negative']
    share=[len(positive_tweets),len(negative_tweets)]
    fig,ax=plt.subplots()
    ax.pie(share,labels=labels)
    st.pyplot(fig)

    col1,col2=st.columns(2)
    col1.header('positive tweets')
    col1.write(positive_tweets)
    col2.header('negative tweets')
    col2.write(negative_tweets)

    #st.write(public_tweets)