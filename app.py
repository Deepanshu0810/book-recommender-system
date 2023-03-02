from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd



app = Flask(__name__)

popular_books = pickle.load(open('popular_books.pkl','rb'))
rating_table = pickle.load(open('final_rating_table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


@app.route("/")
def index():
    return render_template('index.html',
                           book_name = list(popular_books['Book-Title'].values),
                           book_author = list(popular_books['Book-Author'].values),
                           image = list(popular_books['Image-URL-L'].values),
                           votes = list(popular_books['Total-Ratings'].values),
                           rating = list(popular_books['Avg-Rating'].values) 
                           )


@app.route("/recommend")
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    suggestions=list()
    index = np.where(rating_table.index==user_input.lower())[0][0]
    items = sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:7]
    for i in items:
        item = list()
        temp = books[books['Book-Title'].apply(lambda x: x.lower())==rating_table.index[i[0]].lower()]
        temp.drop_duplicates('Book-Title',inplace=True)
        item.append(temp['Book-Title'].values[0])
        item.append(temp['Book-Author'].values[0])
        item.append(temp['Image-URL-L'].values[0])
        suggestions.append(item)

    return render_template('recommend.html',data=suggestions)

if __name__=="__main__":
    app.run(debug=True)

