from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Debug: Print the current working directory
print("Current working directory:", os.getcwd())

# Paths to the model files
model_files = {
    "books": "model/books.pkl",
    "popular": "model/popular.pkl",
    "pt": "model/pt.pkl",
    "similarity_scores": "model/similarity_scores.pkl"
}

# Function to load the model
def load_model(path):
    try:
        with open(path, 'rb') as file:
            model = pickle.load(file)
        print(f"Model {path} loaded successfully")
        return model
    except FileNotFoundError:
        print(f"File {path} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading {path}: {e}")
        return None

# Load all models
models = {name: load_model(path) for name, path in model_files.items()}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        book_name = request.form['book_name']
        # Assuming you have a function to get recommendations based on the loaded models
        recommendations = get_recommendations(book_name, models)
        return render_template('result.html', recommendations=recommendations)
    else:
        return render_template('index.html')

def get_recommendations(book_name, models):
    # Add your logic to get recommendations using the loaded models
    # This is a placeholder function
    return ["Book1", "Book2", "Book3"]

if __name__ == '__main__':
    app.run(debug=True)



