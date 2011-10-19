django-jobim
============

A virtual store that wants to make your life easier when you think about
selling some personal stuff. You don't need intermediate people or to pay
fees. It's informal, simple and focus on the main goal: sale.

Running the project
-------------------

It's very easy to use django-jobim.

Clone the repository, install the requirements, synchronize the database and fire up the server:

    git clone git://github.com/cabello/django-jobim.git
    cd django-jobim
    make environment
    python manage.py syncdb
    python manage.py runserver

When you are done, you will have your store available at http://localhost:8000
and the administrative section at http://localhost:8000/admin, you are ready
to add new products and to visit your store.

Requirements to host the project
--------------------------------

Just run `make environment` and wait the installation. I recommend you to use [virtualenv][2].

**Note**: Mac OS X doesn't have libjpeg installed by default and your PIL won't
recognize JPEG images if you don't install the libjpeg library.

Requirements to developers
--------------------------

Just run `make development` and wait the installation. I **still** recommend the use of [virtualenv][2].

Running the tests
-----------------

If you already ran `make development` you just need to run:

    make test

And you will see a pretty nice output. :D


License
-------

The django-jobim project follows the [GNU Affero General Public License][1].

[1]: http://www.gnu.org/licenses/agpl-3.0.html
[2]: http://www.virtualenv.org
