from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Define file paths for pickle files
base_dir = '/Users/srinivasareddypadala/Desktop/book recommender system/archive-2/book-recommender-system'
popular_path = os.path.join(base_dir, 'model/popular.pkl')
pt_path = os.path.join(base_dir, 'model/pt.pkl')
books_path = os.path.join(base_dir, 'model/books.pkl')
similarity_scores_path = os.path.join(base_dir, 'model/similarity_scores.pkl')

# Load pickle files
try:
    popular = pickle.load(open(popular_path, 'rb'))
    pt = pickle.load(open(pt_path, 'rb'))
    books = pickle.load(open(books_path, 'rb'))
    similarity_scores = pickle.load(open(similarity_scores_path, 'rb'))
except FileNotFoundError as e:
    print(f"Error loading pickle file: {e}")
    # Handle the error appropriately, such as logging or notifying the user.
    raise  # Optional: re-raise the exception to terminate the application if files are critical.

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_ratings'].values),
                           rating=list(popular['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Check if user_input exists in pt.index
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        return render_template('recommend.html', data=data)
    else:
        return render_template('recommend.html', error="User input not found in index")

if __name__ == '__main__':
    app.run(debug=True, port=5001)


