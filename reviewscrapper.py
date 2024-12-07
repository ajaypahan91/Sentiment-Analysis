import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# Header to set the requests as a browser request
headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

# Function to grab HTML data from Amazon review page
def reviewsHtml(url, len_page):
    soups = []
    for page_no in range(1, len_page + 1):
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            soups.append(soup)
        else:
            print(f"Failed to fetch page {page_no}: {response.status_code}")
    return soups

# Function to extract reviews from HTML data
def getReviews(html_data):
    data_dicts = []
    boxes = html_data.select('div[data-hook="review"]')

    for box in boxes:
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except:
            name = 'N/A'
        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except:
            stars = 'N/A'
        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except:
            title = 'N/A'
        try:
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except:
            date = 'N/A'
        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except:
            description = 'N/A'

        data_dict = {
            'Name': name,
            'Rating': stars,
            'Title': title,
            'Date': date,
            'Review': description
        }
        data_dicts.append(data_dict)

    return data_dicts

# Web Scrapper Function
def web_scrapper(url_review, len_page=4):
    if "amazon" not in url_review.lower():
        raise ValueError("Invalid URL: Please provide a valid Amazon product review URL.")

    # Grab all HTML pages
    html_datas = reviewsHtml(url_review, len_page)

    reviews = []
    # Iterate through all HTML pages and extract reviews
    for html_data in html_datas:
        review = getReviews(html_data)
        reviews += review

    # Create a DataFrame with the reviews data
    Review = pd.DataFrame(reviews)
    Review['Review'] = Review['Review'].str.replace(r'\nRead more$', '', regex=True)
    # Remove duplicate reviews based on all columns
    Review = Review.drop_duplicates(keep='first').reset_index(drop=True)
    return Review

# Example usage:
# df = web_scrapper('https://www.amazon.in/Prestige-Electric-Kettle-PKOSS-1500watts/dp/B01MQZ7J8K/ref=pd_rhf_dp_s_vtp_ses_clicks_nonshared_d_sccl_2_4/261-5943901-0306121?pd_rd_w=WEFZC&content-id=amzn1.sym.bbc929e6-0703-4254-ace1-2b3564aa1f3a&pf_rd_p=bbc929e6-0703-4254-ace1-2b3564aa1f3a&pf_rd_r=A9P4G8K637NNSDRA7W7H&pd_rd_wg=90L6P&pd_rd_r=281801ab-53e2-4cdf-8780-c2825a408acd&pd_rd_i=B01MQZ7J8K&th=1', len_page=4)
# print(df)
