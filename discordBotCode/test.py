from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)

    sentiment_polarity = blob.sentiment.polarity

    

