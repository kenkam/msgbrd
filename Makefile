.PHONY: install

SUPERVISORDIR=/etc/supervisor/conf.d
NGINXDIR=/etc/nginx/sites-available

install:
	ln -sf `pwd`/supervisor/msgbrd.conf $(SUPERVISOR)
	supervisorctl reload
	ln -sf `pwd`/nginx/msgbrd $(NGINXDIR)
	service nginx restart

env:
	virtualenv --no-site-packages env
	pip install -r requirements.txt --target env
