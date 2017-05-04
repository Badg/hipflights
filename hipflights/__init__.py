'''
LICENSING
-------------------------------------------------

Hipflights: Hipmunk flights API coding exercise

    The MIT license (MIT)

    Copyright 2017 Nick Badger.

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation files
    (the "Software"), to deal in the Software without restriction,
    including without limitation the rights to use, copy, modify, merge,
    publish, distribute, sublicense, and/or sell copies of the Software,
    and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
    BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
    ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

------------------------------------------------------
'''

# ###############################################
# Boilerplate
# ###############################################


from .hipflights import app


# Logging shenanigans
import logging
# Okay for Py2.7+
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())


# Control * imports.
__all__ = ['app', 'create_app']


def create_app(**config):
    ''' Configure the flask app for different environments, such as
    development/testing/production, etc.
    '''
    for key, value in config.items():
        app.config[key] = value
    
    app.app_context().push()
    return app
