import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

def filterPostsByCoin(posts):
    coin_patterns = {
        "BTC": [re.compile(r'(?i)Bitcoin'),re.compile(r'(?i)\bBitcoin\b'), re.compile(r'(?i)\bBTC\b')],
        "ETH": [re.compile(r'(?i)Ethereum'),re.compile(r'(?i)\bEthereum\b'), re.compile(r'(?i)\bETH\b'),re.compile(r'(?i)\bETHER\b')],
        "ETC": [re.compile(r'(?i)\bEthereum Classic\b'), re.compile(r'(?i)\bETC\b')],
        "Avalanche(AVAX)": [re.compile(r'(?i)Avalanche'),re.compile(r'(?i)\bAvalanche\b'), re.compile(r'(?i)\bAVAX\b')],
        "Solana(SOL)": [re.compile(r'(?i)Solana'),re.compile(r'(?i)\bSolana\b'), re.compile(r'(?i)\bSOL\b')],
        "Monero(XMR)": [re.compile(r'(?i)Monero'),re.compile(r'(?i)\bMonero\b'), re.compile(r'(?i)\bXMR\b'),re.compile(r'(?i)XMR')],
        "Optimism(OP)": [re.compile(r'(?i)Optimism'),re.compile(r'(?i)\bOptimism\b'), re.compile(r'(?i)\bOP\b')],
        "PAX Gold(PAXG)": [re.compile(r'(?i)paxgold'),re.compile(r'(?i)\bpaxgold\b'),re.compile(r'(?i)PAX Gold'),re.compile(r'(?i)\bPAX Gold\b'), re.compile(r'(?i)\bPAXG\b')],
        "Ripple(XRP)": [re.compile(r'(?i)Ripple'),re.compile(r'(?i)\bRipple\b'), re.compile(r'(?i)\bXRP\b')],
        "Arbitrum(ARB)": [re.compile(r'(?i)Arbitrum'),re.compile(r'(?i)\bArbitrum\b'), re.compile(r'(?i)\bARB\b')],
        "Binance(BNB)": [re.compile(r'(?i)BNB CHAIN'),re.compile(r'(?i)\bBNB CHAIN\b'),re.compile(r'(?i)Binance coin'),re.compile(r'(?i)\bBinance coin\b'), re.compile(r'(?i)\bBNB\b')],
        "Cardano(ADA)": [re.compile(r'(?i)Cardano'),re.compile(r'(?i)\bCardano\b'), re.compile(r'(?i)\bADA\b')],
        "Litecoin(LTC)": [re.compile(r'(?i)Litecoin'),re.compile(r'(?i)\bLitecoin\b'), re.compile(r'(?i)\bLTC\b')],
        "Cosmos(ATOM)": [re.compile(r'(?i)Cosmos'),re.compile(r'(?i)\bCosmos\b'), re.compile(r'(?i)\bATOM\b')],
        "Chainlink(LINK)":[re.compile(r'(?i)Chainlink'),re.compile(r'(?i)\bChainlink\b'), re.compile(r'(?i)\b\$LINK\b')],
        "Aave(AAVE)":[re.compile(r'(?i)Aave'), re.compile(r'(?i)\bAAVE\b')],
        "Polygon(MATIC)":[re.compile(r'(?i)Polygon'),re.compile(r'(?i)\bPolygon\b') ,re.compile(r'(?i)\bMATIC\b')],
        "Gas(GAS)":[re.compile(r'(?i)Gas'),re.compile(r'(?i)\bGas\b')],
        
    }

    filtered_posts = []

    for post in posts:
        post_text = post['post_txt']
        coin_name = None

        for name, patterns in coin_patterns.items():
            for pattern in patterns:
                if pattern.search(post_text):
                    coin_name = name
                    break
            if coin_name:
                break

        post['coin_name'] = coin_name if coin_name else 'not_coin'
        filtered_posts.append(post)

    return filtered_posts

def analyzePosts(posts):
    # 3: analyze data using nltk
    # nltk.download('vader_lexicon')
    sia = SIA()
    results = []

    for post in posts:
        pol_score = sia.polarity_scores(post['post_txt'])  # this will return dict

        # find post ins negitive=-1,postive=1 or neutral=0
        label = 0
        if pol_score['compound'] > 0.2:
            label = 1
        elif pol_score['compound'] < - 0.2:
            label = -1
        post['label'] = label
        results.append(post)

    return results