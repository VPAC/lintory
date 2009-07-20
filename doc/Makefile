all: build

stamp:

build: stamp
	ikiwiki --setup ikiwiki.setup --refresh

upload: build
	find html -type d | xargs chmod 755
	find html -type f | xargs chmod 644
	rsync --delete -avP html/ bmay,lintory@web.sourceforge.net:htdocs/
