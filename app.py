from flask import Flask, abort, jsonify, render_template, redirect, request, url_for
from datetime import datetime, timedelta
import redis
import signal
import sys

app = Flask(__name__)

from settings import *
# TODO: errors
KEY_NUM = 'count'
TIME_STORE_FORMAT = '%Y-%m-%d %H:%M'
TIME_DISPLAY_FORMAT = '%d %b, %Y %H:%M'

# setup redis
r = redis.Redis(host=HOST, port=PORT, db=1)
# check the count is there
try:
    if r.get(KEY_NUM) == None:
        r.set(KEY_NUM, 0)
except:
    sys.stderr.write("Cannot connect to redis server\n")
    sys.exit(1)

"""
Redis based functions
"""
def has_entries():
    if int(r.get(KEY_NUM)) > 0:
        return True
    return False
    
def get_count():
    return int(r.get(KEY_NUM))

def delete_message(n):
    n = int(n)
    # pop it out of the list
    if (r.lrem('messages', n, 0) != True):
        return False
    m = "m:%d:body" % n
    d = "m:%d:date" % n
    # delete the keys for said message
    r.delete(m)
    r.delete(d)  
    return True  

def get_message(n):
    n = int(n)
    # does it exist
    m = "m:%d:body" % n
    d = "m:%d:date" % n
    date = datetime.strptime(r.get(d), TIME_STORE_FORMAT) + timedelta(hours=GMT_OFFSET)
    date = date.strftime(TIME_DISPLAY_FORMAT)
    return (n, r.get(m).decode('utf-8'), date)
    
def get_messages(start=0, end=9):
    """
    Returns a list of messages back
    """
    msgs = None
    if has_entries():
        msgs = []
        for n in r.lrange('messages', start, end):
            msgs.append(get_message(n))
    return msgs

def save_message(msg):
    """
    Saves the message into redis and returns the msg id
    """
    # increment
    r.incr(KEY_NUM)
    n = int(r.get(KEY_NUM))
    m = "m:%d:body" % n
    d = "m:%d:date" % n
    # save into database
    r.set(m, msg)
    r.set(d, datetime.now().strftime(TIME_STORE_FORMAT))
    r.lpush('messages', n)
    return n

"""
Flask based routes
"""
@app.route('/')
def index():
    # get messages
    # in the format of (body, datetime)
    texts = get_messages()
    return render_template('index.html', texts=texts)

@app.route('/_get')
def _get():
    # get 10 more messages
    n = request.args.get('n', -1, type=int)
    if n < 0:
        abort(404)
    # an ajax request, this one is
    # n is the number of list items already loaded. so we need n..n+9 more
    start = n
    end = start + 9
    texts = get_messages(start, end)
    return jsonify(msgs=texts)

@app.route('/post', methods=['POST'])
def post():
    error = ""
    if request.method == 'POST':
        # make sure request is not empty
        m = request.form['text'].strip()
        if len(m) > 140 or m == "":
            # message too long or empty message
            pass
        else:
            save_message(request.form['text'])
            return redirect('/')
    # redirect back to html
    return redirect('/' + error)
    
@app.route('/_post', methods=['POST'])
def _post():
    """
    AJAX version of post()
    """
    if request.method == 'POST':
        # make sure request is not empty
        m = request.form['text'].strip()
        if len(m) > 140 or m == "":
            abort(400)
        n = save_message(request.form['text'])
        msg = get_message(n)
        return jsonify(id=msg[0],
                       body=msg[1],
                       date=msg[2])

@app.route('/delete/<int:n>', methods=['GET'])
def delete(n):
    if request.method == 'GET':
        if delete_message(n) != True:
            abort(404)
    return redirect('/')
    
    
def sigint_handler(signal, frame):
    r.save()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    app.debug = True
    app.run()
