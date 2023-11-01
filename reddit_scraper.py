import os
import dotenv
import praw  # using PRAW- python reddit api wrapper
import csv
import time
import analyze_filter

def getPosts(CLIENT_ID, CLIENT_SECRET, subReddit):
    # 1: get authentication data
    user_agent = 'automation '
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=user_agent
    )

    # 2: retrive data
    posts = []
    for submission in reddit.subreddit(subReddit).new(limit=None):
        post = dict(post_txt=submission.title,created_utc=submission.created_utc,
                    upvote_ratio=submission.upvote_ratio,post_score=submission.score,
                    num_comments=submission.num_comments)
        posts.append(post)

    return list(posts)


def filterPostsByDate(posts):
    filter_date = float(os.getenv('Last_Run_Time_Reddit'))
    filtered_posts = []
    for post in posts:
        if post['created_utc'] > filter_date:
            filtered_posts.append(post)
    return filtered_posts


def storePostInCSV(posts):
    with open('data/reddit_data.csv', 'a', encoding="utf-8", newline='') as f:
        try:
            writer = csv.DictWriter(f, fieldnames=posts[0].keys())
            for post in posts:
                writer.writerow(post)
        except IndexError:
            print('list is empty!')


dotenv.load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


subreddits = ['CryptoMoonShots','altcoin','CryptoMarkets','crypto_currency','CoinBase','ledgerwallet',
              'CryptoCurrency','Crypto_com','CryptoCurrencyTrading','Crypto_General','defi','binance',
              'BitcoinBeginners','Bitcoin' ,'ethtrader','Ripple','ethereum','solana','Monero','Avax',
              'Crypto_Currency_News','CryptoCurrencyClassic','ethfinance','Arbitrum','CryptoCurrencyMoons',
              'XRP','SolanaLabs','0xPolygon','cosmosnetwork','cardano','CardanoTrading','litecoin','Chainlink',
              'BNBinance','NEO',
             ]

for subreddit in subreddits:
    posts = getPosts(CLIENT_ID, CLIENT_SECRET, subreddit)
    posts_filtered_date = filterPostsByDate(posts)
    if len(posts_filtered_date) == 0:
        print('no new posts available')
    else:
        filterd_posts = analyze_filter.filterPostsByCoin(posts_filtered_date)
        analyzed_posts = analyze_filter.analyzePosts(filterd_posts)
        storePostInCSV(analyzed_posts)

# set last run time
os.environ['Last_Run_Time_Reddit'] = str(time.time())
dotenv.set_key('.env', 'Last_Run_Time_Reddit',os.environ['Last_Run_Time_Reddit'])
