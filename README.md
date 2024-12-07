# Sentiment Analysis of Amazon Reviews 🛒

# Sentiment Analysis of Reviews
## Overview
This project is a sentiment analysis application that determines whether a review is positive, negative, or neutral. Users can input a single review or analyze reviews from an Amazon product URL to get detailed sentiment insights. The application is built using Python, Flask, and machine learning models.



## Project Structure

Sentiment_Analysis/
- *app.py*                                            # Main application file
- *requirements.txt*                                  # Project dependencies
- **static/**
- - *style.css*                                       # Static assets (CSS, JavaScript, etc.)
- **templates/**
- - *index.html*                                      # HTML templates
- **notebooks/**
- - *Preprocessing training model.ipynb*
- - *train.csv*                                       # Training dataset
- - *models.p*                                        # Trained ML model
- *web_scraping.py*                                   # Web scraping logic for Amazon reviews
- *README.md*                                         # Documentation
- **.gitignore**                                      # Ignored files and folders




## Dataset Used

The Amazon reviews full score dataset is constructed by randomly taking 6,00,000 training samples and 1,30,000 testing samples for each review score from 1 to 5. In total there are 30,00,000 training samples and 6,50,000 testing samples.

[Kaggle Link to the Dataset](https://www.kaggle.com/datasets/bittlingmayer/amazonreviews/data)


  

## Features
- Analyze the sentiment of a single review.
- Fetch and analyze reviews from an Amazon product page.
- Display sentiment distribution and average sentiment score.
- Supports multiple sentiment classification models:
- Logistic Regression
- Support Vector Machine (SVM)
- Random Forest
- User-friendly interface with responsive design.


## Technologies Used
- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Web Scraping: BeautifulSoup, Requests
- Data Processing: Pandas
- Visualization: Matplotlib
- Deployment: Heroku (or any cloud platform)
- Installation
- Prerequisites
- Python 3.7 or higher installed.
- Virtual environment (optional but recommended).
- Steps


## Clone the repository:

```bash
git clone https://github.com/ajaypahan91/Sentiment_Analysis.git
```
## Navigate to the project directory:
```bash
cd Sentiment_Analysis
```

## Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Install the dependencies:

```bash
pip install -r requirements.txt
```
## Train and Create the model
To train the model, run the following python file:

Preprocessing training model.ipynb 


## Run the application:
```bash
python app.py
```
Visit the link on {Terminal}: 

http://127.0.0.1:X000/


## Usage

### To analyze a single review
Enter a review in the input box.
Choose a sentiment classification model.
Click "Check Sentiment" to view the analysis.


### Analyze Reviews from an Amazon Product:

Enter the product URL in the input box.
Click "Check Reviews" to fetch and analyze reviews.
View sentiment distribution and detailed review analysis.


