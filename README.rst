=============================
django_internal_external_comments
=============================

.. image:: https://badge.fury.io/py/django-internal-external-comments.svg
    :target: https://badge.fury.io/py/django-internal-external-comments

.. image:: https://travis-ci.org/ortkin/django-internal-external-comments.svg?branch=master
    :target: https://travis-ci.org/ortkin/django-internal-external-comments

.. image:: https://codecov.io/gh/ortkin/django-internal-external-comments/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ortkin/django-internal-external-comments

Extends the django.contrib.comments to allow internal and external comments

Documentation
-------------

The full documentation is at https://django-internal-external-comments.readthedocs.io.

Quickstart
----------

Install django_internal_external_comments::

    pip install django-internal-external-comments

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'internal_external_comments.apps.InternalExternalCommentsConfig',
        ...
    )

Add django_internal_external_comments's URL patterns:

.. code-block:: python

    from internal_external_comments import urls as internal_external_comments_urls


    urlpatterns = [
        ...
        url(r'^', include(internal_external_comments_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
