import requests
import smtplib
import math

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_ENDPOINT = 'https://www.alphavantage.co/query'
ALPHA_API_KEY = '3PB0B1GDJP7N7Y3P'
NEWS_API_KEY = '7ffa52331634471cb94884eda66ec0ea'


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
params = {
	'function': 'TIME_SERIES_DAILY',
	'symbol': STOCK,
	'apikey': ALPHA_API_KEY
}


NEWS_ENDPOINT = 'https://newsapi.org/v2/everything/'
news_params = {
	'apiKey': NEWS_API_KEY,
	'q': 'tesla',	
	'pageSize': 3,
}

alpha_response = requests.get(url=ALPHA_ENDPOINT, params=params)
news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)


daily_list = [value for (key,value) in alpha_response.json()['Time Series (Daily)'].items()][:2]
yesterday_close_price = float(daily_list[0]['4. close'])
day_before_yesterday_close_price = float(daily_list[1]['4. close'])
daily_difference = yesterday_close_price - day_before_yesterday_close_price
percentage_rise_or_fall = (daily_difference/yesterday_close_price)*100


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
if percentage_rise_or_fall > 5:
	for articles in news_response.json()['articles']:
		print(f'{articles["title"]}\n\n{articles["content"]}')
elif percentage_rise_or_fall < -5 :
	for articles in news_response.json()['articles']:
		print(f'''TSLA: 🔻{math.floor(abs(percentage_rise_or_fall))}%
		Headline: {articles['title']} 
		Brief: {articles['content']}''')
		
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

