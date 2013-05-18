.PHONY: install

SUPERVISORDIR=/etc/supervisor/conf.d
NGINXDIR=/etc/nginx

install:
	ln -sf `pwd`/supervisor/msgbrd.conf $(SUPERVISOR)
	supervisorctl reload
	cp -f ./nginx/msgbrd $(NGINXDIR)/sites-available
	ln -sf $(NGINXDIR)/sites-available/msgbrd $(NGINXDIR)/sites-enabled/
	service nginx restart

