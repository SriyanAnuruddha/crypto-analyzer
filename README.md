# Crypto Analyzer

*Crypto Analyzer* is a Python program designed to gather and analyze trends in the cryptocurrency market. It collects data from social platforms like Twitter and Reddit, performs sentiment analysis, and organizes this information to gain insights into cryptocurrency trends.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Script Overview](#script-overview)


## Features

- **Social Media Sentiment Analysis**: Categorizes user sentiment as positive, neutral, or negative for various cryptocurrencies.
- **Data Collection from Twitter and Reddit**: Scrapes posts, comments, likes, and other metrics to analyze public opinion on cryptocurrencies.
- **Data Storage in Excel**: Stores processed data in an Excel sheet for easy review and analysis.
- **Pandas-Based Analysis**: Uses Jupyter Notebook with various Pandas code segments for comprehensive data analysis.

## Installation

### Prerequisites
- **Python 3.x** (ensure it’s installed and added to PATH)
- Dependencies in `requirements.txt`

### Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/username/crypto-analyzer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd crypto-analyzer
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the **Twitter scraper** to collect tweets, likes, views, and comments about cryptocurrencies:
    ```bash
    python twitter_scraper.py
    ```

2. Run the **Reddit scraper** to gather posts and comments about various cryptocurrencies:
    ```bash
    python reddit_scraper.py
    ```

3. Analyze data in **Jupyter Notebook** using the coded Pandas segments for processing and visualization:
    ```bash
    jupyter notebook main.ipynb
    ```

## Technologies Used

- **Programming Language**: Python
- **Web Scraping**: Tweepy for Twitter, PRAW for Reddit
- **Sentiment Analysis**: TextBlob
- **Data Analysis**: Pandas in Jupyter Notebook
- **Data Storage**: Excel (via openpyxl)

## Script Overview

- **twitter_scraper.py**: Scrapes Twitter data (tweets, likes, views, comments) and performs sentiment analysis to categorize posts.
- **reddit_scraper.py**: Similar to the Twitter scraper, collects Reddit data to analyze cryptocurrency sentiment.
- **analysis.ipynb**: Jupyter Notebook containing various Pandas code segments for detailed analysis and visual representation of the collected data.

