# README

This project contains a message board that uses [Flask](http://flask.pocoo.org/) and [Redis](http://redis.io) server for storing the messages.

## Quickstart

You'll need to have a redis server.

* Edit the ``settings.py`` as needed, then

```python
python app.py
```

This will start the server listening on port 5000, the default for Flask. For deployment, check out the [Flask docs](http://flask.pocoo.org/docs/deploying/).
