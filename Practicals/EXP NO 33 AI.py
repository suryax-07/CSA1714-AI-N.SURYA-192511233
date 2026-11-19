
from textblob import TextBlob

text = input("Enter a sentence: ")

analysis = TextBlob(text)
score = analysis.sentiment.polarity

if score > 0:
    print("Sentiment: Positive")
elif score < 0:
    print("Sentiment: Negative")
else:
    print("Sentiment: Neutral")
