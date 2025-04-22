from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    balance = db.Column(db.Float, default=0)
    energy = db.Column(db.Integer, default=100)
    last_click = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('index.html', user=user)
    return redirect('/login')

@app.route('/click', methods=['POST'])
def click():
    if 'user_id' not in session:
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    now = datetime.utcnow()

    # energiyani tiklash
    if user.energy == 0 and (now - user.last_click) > timedelta(hours=1):
        user.energy = 100

    if user.energy > 0:
        user.balance += 0.001
        user.energy -= 1
        user.last_click = now
        db.session.commit()
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
