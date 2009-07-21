# Build static html docs suitable for being shipped in the software
# package. This depends on ikiwiki being installed to build the docs.

ifeq ($(shell which ikiwiki),)
IKIWIKI=echo "** ikiwiki not found" >&2 ; echo ikiwiki
else
IKIWIKI=ikiwiki
endif

all:
	$(IKIWIKI) `pwd` html -v --wikiname Lintory \
		--plugin=goodstuff --plugin=graphviz \
		--exclude=html --exclude=Makefile \
		--exclude=ss \
		--no-usedirs

clean:
	rm -rf .ikiwiki html

upload: all
	find html -type d | xargs chmod 755
	find html -type f | xargs chmod 644
	rsync --delete -avP html/ bmay,lintory@web.sourceforge.net:htdocs/


ss/1:
	java -jar ~/schemaSpy_4.1.1.jar -dp /usr/share/java/mysql.jar -t mysql -host localhost -db r1 -u root -p abcdefg -o ss/1

ss/current:
	java -jar ~/schemaSpy_4.1.1.jar -dp /usr/share/java/mysql.jar -t mysql -host localhost -db r2 -u root -p abcdefg -o ss/current

ss: ss/1 ss/current
