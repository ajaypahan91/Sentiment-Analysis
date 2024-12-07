import pickle
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request
from reviewscrapper import web_scrapper  

app = Flask(__name__)

# Load the trained models and vectorizer
with open("notebooks/models.p", 'rb') as model_file:
    models_data = pickle.load(model_file)

logreg_model = models_data['logreg']
svm_model = models_data['svm']
vect = models_data['vectorizer']
rf_model = models_data['rf']

# Preprocessing function for text data
def preprocess_text(text):
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer

    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+|\[.*?\]|[^a-zA-Z\s]+|\w*\d\w*', ' ', text)
    text = re.sub(r'\n', ' ', text)

    stop_words = set(stopwords.words("english"))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    text = ' '.join(filtered_words).strip()

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lem_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(lem_tokens)

# Function to predict sentiment for a list of reviews
def predict_sentiment_for_reviews(reviews, model, vectorizer):
    results = []
    for review in reviews:
        preprocessed_review = preprocess_text(review)
        review_vector = vectorizer.transform([preprocessed_review])
        sentiment = model.predict(review_vector)
        results.append(sentiment[0])
    return results

# Function to create a sentiment distribution chart
def create_sentiment_chart(sentiments):
    import pandas as pd
    import io
    import base64

    # Count sentiment occurrences
    sentiment_counts = pd.Series(sentiments).value_counts()
    labels = sentiment_counts.index
    sizes = sentiment_counts.values

    # Plot sentiment distribution
    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#1ba307', '#f8de7e', '#fa3232'])
    plt.title('Sentiment Distribution')

    # Save the chart to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the chart to base64
    chart_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Close the plot
    plt.close()
    return chart_base64

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'single_review' in request.form:
            review_text = request.form['single_review']
            model_choice = request.form['model_choice']
            review_text = preprocess_text(review_text)

            if model_choice == 'Logistic Regression':
                model = logreg_model
            elif model_choice == 'Support Vector Machine (SVM)':
                model = svm_model
            elif model_choice == 'Random Forest':
                model = rf_model

            input_test = vect.transform([review_text])
            result = model.predict(input_test)
            return render_template('index.html', result=result[0], review=review_text, model=model_choice, show_result=True)

        elif 'url_review' in request.form:
            product_url = request.form['url_review']
            df_reviews = web_scrapper(product_url)
            
            # Check if the necessary columns exist
            if 'Name' not in df_reviews.columns or 'Rating' not in df_reviews.columns or 'Review' not in df_reviews.columns:
                return render_template('index.html', error_message="The required columns ('Name', 'Rating', 'Review') were not found in the scraped data. Please check the URL or try again.", show_error=True)
      
            # Predict sentiment for each review
            sentiments = predict_sentiment_for_reviews(df_reviews['Review'], logreg_model, vect)  # Use the appropriate model and vectorizer

            # Add the sentiment column to the DataFrame
            df_reviews['Sentiment'] = sentiments

            # Calculate sentiment distribution and average sentiment score
            sentiment_chart = create_sentiment_chart(sentiments)
            avg_sentiment = sentiments.count("Positive") - sentiments.count("Negative")

            df_reviews = df_reviews[['Name', 'Rating', 'Review', 'Sentiment']]
            return render_template(
                'index.html',
                reviews=df_reviews.to_html(classes='table table-bordered'),
                sentiment_chart=sentiment_chart,
                avg_sentiment=avg_sentiment,
                show_reviews=True
            )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
