#! /usr/bin/env python
from app import create_app

app = create_app()


"""
Inside templates you also have access to the 

1. request,
2. session,
3. g

objects as well as the `get_flashed_messages()` function.
"""