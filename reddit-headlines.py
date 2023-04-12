import subprocess
import re
from bs4 import BeautifulSoup

# execute the curl command and get the HTML content of the Reddit homepage
curl_output = subprocess.check_output(['curl', '-s', '--request', 'GET', 'https://www.reddit.com/r/news/'])
html_content = curl_output.decode('utf-8')

# parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# find all the headlines using the appropriate tag and class
headlines = soup.find_all("h3")

# create a list of headlines
headlines_list = [headline.text for headline in headlines]

# save the headlines to a text file
with open('/home/pi/static/reddit/reddit_headlines.txt', 'w') as file:
    for headline in headlines_list:
        file.write("From /r/news: " + headline + '\n')
