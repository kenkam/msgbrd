# README

Msgbrd is a simple a message board that uses [Flask](http://flask.pocoo.org/) and [Redis](http://redis.io) server for storing the messages. [Demo](http://flask.kennethkam.com)

## Quickstart

You'll need to have a redis server.

* Edit the ``settings.py`` as needed, then

```python
python app.py
```

This will start the server listening on port 5000, the default for Flask. By default, it will try to connect to the Redis server on ``127.0.0.1:6379``. For more on deployment, check out the [Flask docs](http://flask.pocoo.org/docs/deploying/).
