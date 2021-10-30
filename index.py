from flask import Flask, request, jsonify, render_template
from data_providers.TwitterClient import TwitterClient

app = Flask(__name__, template_folder='views', static_folder='static', static_url_path='')
client = TwitterClient()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tweets_sentiment_analysis')
def tweet_sentiment_analysis():
    return render_template('tweets_sentiment_analysis.html')    

@app.route('/api/get-tweets', methods=["POST"])
def get_tweets():
    print(request.json)
    q = request.json['query']
    c = int(request.json['count'])
    return {'tweets': client.get_tweets(f'{q} -filter:retweets', c)}

if __name__ == "__main__":
    app.run(debug=True)