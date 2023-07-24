======
Zero Python SDK
======
Python SDK for `Zero <https://tryzero.com>`_. Provides a clear and simple interface for the secrets manager GraphQL API.

Installation
------------

.. code:: sh

    poetry add zero-python-sdk

Usage
-----

Fetch your vendor secrets by passing your ``zero`` token:

.. code:: python

    import os
    from zero_sdk import zero

    ZERO_TOKEN = os.getenv("ZERO_TOKEN")

    # {'aws': {'secret': 'value', 'secret2': 'value2'}, 'googleCloud': {...}}
    print(zero(token=ZERO_TOKEN, pick=["aws", "googleCloud"], caller_name="stagingcluster").fetch())
