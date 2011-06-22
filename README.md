django-jobim
============

A virtual store that wants to make your life easier when you to think about
selling some personal stuff. You don't need intermediate people or to pay
fees. It's informal, simple and focus in the main goal: to sell.

Requirements
------------

- Django 1.3
- Markdown
- PIL (Python Imaging Library)
- [django-stdimage][1]

Note: Mac OS X doesn't have libjpeg installed by default and your PIL won't
recognize JPEG images if you don't install the libjpeg library.

Requirements to run the tests
-----------------------------

- coverage
- django_coverage

Note: this packages are available via `easy_install` or `pip`.

Installation
============

It's very easy to install django-jobim, once you have all requirements
satisfied.

Clone the repository, synchronize the database and fire up the server:

    git clone git://github.com/cabello/django-jobim.git
    cd django-jobim
    python manage.py syncdb
    python manage.py runserver

When you are done, you will have your store available at http://localhost:8000
and the administrative section on http://localhost:8000/admin, you are ready
to add new products and to visit the site.

License
=======

The django-jobim project follows the BSD license, equal to Django.

[1]: http://code.google.com/p/django-stdimage/