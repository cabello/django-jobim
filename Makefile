clean:
	@find . -name "*.pyc" -delete

development:
	@pip install -r requirements/development.txt

environment:
	@pip install -r requirements/environment.txt

pep8:
	@pep8 -r .

test: clean
	@specloud --with-xunit --xunit-file=nose.xml --with-coverage --with-django --django-settings=settings --django-sqlite=use_sqlite --cover-erase --cover-package=jobim --verbosity=2 --where=jobim/tests
