from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import dotenv
import os
import time
import datetime
import calendar
import csv
import analyze_filter


def convertToUnixtime(js_time):
    year = int(js_time.split('-')[0])
    month = int(js_time.split('-')[1])
    date = int(js_time.split('-')[2].split('T')[0])
    hours = int(js_time.split('-')[2].split('T')[1].split(':')[0])
    mins = int(js_time.split('-')[2].split('T')[1].split(':')[1])
    secs = int(js_time.split('-')[2].split('T')[1].split(':')[2].split('.')[0])

    t = datetime.datetime(year, month, date, hours, mins, secs)
    epotch_t = calendar.timegm(t.timetuple())
    return epotch_t


def convertToInt(val: str):
    if ',' in val:
        val = val.replace(',', '')
    if val.endswith('K'):
        return int(float(val[:val.find('K')])*1000)
    elif val.endswith('M'):
        return int(float(val[:val.find('M')])*1000000)

    return val


def route_intercept(route):
    if route.request.resource_type == "image":
        return route.abort()
    if route.request.resource_type == "video":
        return route.abort()
    if route.request.resource_type == "media":
        return route.abort()
    return route.continue_()


def scraper(profile_urls):
    dotenv.load_dotenv()
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        stealth_sync(page)  # to hide bot data
        page.set_default_timeout(60000)
        page.route("**/*", route_intercept)  # block images

        # login
        page.goto('https://twitter.com/i/flow/login')
        page.wait_for_selector('h1[id="modal-header"]')
        page.locator('input[autocomplete="username"]').fill('anuruddaSriyan')
        page.wait_for_selector('text=Next')
        page.locator('text=Next').click()
        page.wait_for_selector('h1#modal-header')
        page.locator('input[name="password"]').click()
        page.keyboard.type('niggasriyan123')
        page.locator('div[data-testid="LoginForm_Login_Button"]').click()
        # wait untill home page is loaded
        page.wait_for_selector('a[aria-label="X"]')

        def getPosts():
            # wait for tweets to loads
            page.wait_for_selector('div[data-testid="tweetText"]')
            posts = page.query_selector_all(
                'div[data-testid="cellInnerDiv"]')  # posts
            if page.locator('path[d="M7 4.5C7 3.12 8.12 2 9.5 2h5C15.88 2 17 3.12 17 4.5v5.26L20.12 16H13v5l-1 2-1-2v-5H3.88L7 9.76V4.5z"]').is_visible():
                posts.pop(0)  # remove pinned post
            return posts

        data = list()  # all the data is stored here

        for url in profile_urls:
            page.route("**/*", route_intercept)  # block images
            page.goto(url)  # go to this page

            # wait until specific page is loaded
            page.wait_for_selector(
                'span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')
            tweets = set()
            # load last run time
            filter_date = float(os.getenv('Last_Run_Time_Twitter'))
            breakOuterLoop = False

            while True:
                for post in getPosts():
                    if post.query_selector("time"):
                        unixTime = convertToUnixtime(
                            post.query_selector("time").get_attribute('datetime'))
                        if unixTime < filter_date:
                            breakOuterLoop = True
                            break

                    tweet = post.query_selector('div[data-testid="tweetText"]')
                    if tweet:  # check if post is a tweet
                        tweet_txt = tweet.text_content()
                        if tweet_txt not in tweets:
                            tweet_data = {
                                'post_txt': tweet_txt.replace('\n', ''),
                                'like_count': convertToInt(post.query_selector('div[data-testid="like"]').text_content()),
                                'reply_count': convertToInt(post.query_selector('div[data-testid="reply"]').text_content()),
                                'view_count': convertToInt(post.query_selector('a[aria-label*="analytics"]').text_content()),
                                'retweet_count': convertToInt(post.query_selector('div[data-testid="retweet"]').text_content()),
                                'posted_time': unixTime
                            }
                            tweets.add(tweet_txt)
                            data.append(tweet_data)

                if breakOuterLoop:  # if there is no new posts
                    break
                page.mouse.wheel(0, 4000)  # scroll page
                time.sleep(3)
            print("done scraping:"+url)

    return data


def storePostInCSV(posts):
    with open('data/twitter_data.csv', 'a', encoding="utf-8", newline='') as f:
        try:
            writer = csv.DictWriter(f, fieldnames=posts[0].keys())
            for post in posts:
                writer.writerow(post)
        except IndexError:
            print('list is empty!')


urls = [
    'https://twitter.com/Cryptobullmaker',
    'https://twitter.com/ethereum',
    'https://twitter.com/ForbesCrypto',
    'https://twitter.com/DocumentingBTC',
    'https://twitter.com/solana',
    'https://twitter.com/SolanaStatus',
    'https://twitter.com/AltcoinDailyio',
    'https://twitter.com/avax',
    'https://twitter.com/arbitrum',
    'https://twitter.com/Ashcryptoreal',
    'https://twitter.com/binance',
    'https://twitter.com/chainlink',
    'https://twitter.com/cosmos',
    'https://twitter.com/Cardano',
    'https://twitter.com/cryptojack',
    'https://twitter.com/coinbureau',
    'https://twitter.com/CoinDesk',
    'https://twitter.com/crypto',
    'https://twitter.com/CoinMarketCap',
    'https://twitter.com/cryptofeednews',
    'https://twitter.com/CryptoBoomNews',
    'https://twitter.com/CryptoNetWire',
    'https://twitter.com/CryptoClub06',
    'https://twitter.com/cryptobull2020',
    'https://twitter.com/cryptobull',
    'https://twitter.com/TCryptoCurrency',
    'https://twitter.com/litecoin',
    'https://twitter.com/monero',
    'https://twitter.com/MultiTpark',
    'https://twitter.com/OptimismHub',
    'https://twitter.com/Paxos',
    'https://twitter.com/0xPolygonLabs',
    'https://twitter.com/Ripple',
    'https://twitter.com/100trillionUSD',
    'https://twitter.com/WuBlockchain',
    'https://twitter.com/whale_alert',
    'https://twitter.com/Neo_Blockchain',
    'https://twitter.com/NEOnewstoday',
]

query_posts = scraper(urls)
filtered_posts = analyze_filter.filterPostsByCoin(query_posts)
analyzed_posts = analyze_filter.analyzePosts(filtered_posts)
storePostInCSV(analyzed_posts)

# set last run time
os.environ['Last_Run_Time_Twitter'] = str(time.time())
dotenv.set_key('.env', 'Last_Run_Time_Twitter',
               os.environ['Last_Run_Time_Twitter'])
