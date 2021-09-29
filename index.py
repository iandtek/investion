from flask import Flask, request, jsonify, render_template
from data_providers.TwitterClient import TwitterClient

app = Flask(__name__, template_folder='views')
client = TwitterClient()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/get-cardano-tweets')
def get_cardano_tweets():
    return {'tweets': client.get_tweets('#cardano -filter:retweets', 1)}

@app.route('/api/get-tweets', methods=["POST"])
def get_tweets():
    print(request.json)
    q = request.json['query']
    c = int(request.json['count'])
    return {'tweets': client.get_tweets(f'{q} -filter:retweets', c)}