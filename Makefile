
all: webber.conf
	./webber

profile:
	./webber --profile

lint:
	pylint \
		--include-ids=y \
		--reports=n \
		--disable-msg=W0312,C0103 \
		webber.py plugins

clean:
	rm -f *.pyc plugins/*.pyc

realclean: clean
	rm -rf out

# Automatically create webber.conf:
ifeq ($(wildcard webber.conf),)
webber.conf: in/webber.conf
	ln -s in/webber.conf
endif
