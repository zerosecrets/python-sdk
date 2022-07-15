======
Zero Python SDK
======
Python SDK for `Zero <https://tryzero.com>`_. Provides a clear and simple interface for the secrets manager GraphQL API.

Installation
--------

.. code:: sh

    poetry add zero-sdk

Usage
--------

Fetch your vendor secrets by passing your ``zero`` token

.. code:: python

    import os
    from zero_sdk import zero

    ZERO_TOKEN = os.getenv("ZERO_TOKEN")

    # {'aws': {'secret': 'value', 'secret2': 'value2'}}
    print(zero(token=ZERO_TOKEN, pick=["aws"]).fetch())

    # {'aws': {'secret': 'value', 'secret2': 'value2'}, 'googleCloud': {...}}
    print(zero(token=ZERO_TOKEN, pick=["aws", "googleCloud"]).fetch())

    try:
        # empty token
        print(zero(token="", pick=[]).fetch())
    except AssertionError as exception:
        print(exception)  # Apis should be a list of strings

    try:
        # apis is not a list of string
        print(zero(token=ZERO_TOKEN, pick=[0]).fetch())
    except AttributeError as exception:
        print(exception)  # Apis should be a list of strings
