=====
Usage
=====

To use django_internal_external_comments in a project, add it to your `INSTALLED_APPS`:

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
