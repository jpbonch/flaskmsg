from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from better_profanity import profanity

app = Flask(__name__)
app.config['SECRET_KEY'] = '3432j5njkbn//bnksfg'
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class History(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    message = db.Column('message', db.String(500))

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    profanity.load_censor_words()
    msg = profanity.censor(msg)
    message = History(message=msg)
    db.session.add(message)
    db.session.commit()

    send(msg, broadcast=True)

@app.route('/')
def index():
    messages = History.query.all()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
	socketio.run(app)
