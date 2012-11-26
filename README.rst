========
Adworks
========

A simple Django application to manage ad banner design and approval processes.


Requirements
============

* Python 2.7+
* Django 1.4+

Installation
============

Install using pip: ::

    $ pip install django-adworks
    
Or install from source code: ::

    $ python setup.py install

Usage
=====

Add ``adworks`` to your ``INSTALLED_APPS`` ::

    INSTALLED_APPS = (
        ...
        'adworks',
    )
    
Include ``adworks`` in your ``urls.py`` ::

    url('adworks', include('adworks.urls')),
    
Create necessary database tables ::

    $ python manage.py syncdb
    
or ::

    $ python manage.py migrate adworks


    