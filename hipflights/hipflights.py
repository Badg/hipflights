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

import threading
import heapq
import flask
import requests


# ###############################################
# Boilerplate and helpers
# ###############################################


# Control * imports.
__all__ = ['app']


# Flask boilerplate
app = flask.Flask(__name__)
# What providers do we have?
PROVIDERS = [
    'expedia',
    'orbitz',
    'priceline',
    'travelocity',
    'united'
]
# What user agent should we use when requesting from the scrapers?
USER_AGENT = 'HipflightsService/0.1'
# Where are the scrapers running?
SCRAPER_HOST = 'http://127.0.0.1:9000'
# What's the URL prefix for the scrapers endpoint?
SCRAPER_PREFIX = '/scrapers/'
# How long before each scraper times out?
SCRAPER_TIMEOUT = 10
# We want to preserve our default headers, but replace the user agent.
HEADERS = requests.utils.default_headers()
HEADERS['User-Agent'] = USER_AGENT


# ###############################################
# Lib
# ###############################################


def get_single_scrape(target, results):
    ''' Performs a single request to the target scraper, adding its
    response to results.
    
    Args:
        target (str): the scraper provider name
        results (list): where to put the results (the list is mutated
            inplace)
    
    Returns:
        None
    '''
    # Issue the request to the scrapers API
    flights = requests.get(
        SCRAPER_HOST + SCRAPER_PREFIX + target,
        headers=HEADERS
    )
    # Convert it from json, and extract the actual response LIST into results.
    # Note that this is hard-coding the response format from the scraper API,
    # which is perhaps not the best approach.
    # Also note that order doesn't matter, but that if it did, we would need
    # to do something more to make this threadsafe
    results.append(flights.json()['results'])


@app.route('/flights/search/', methods=['GET'])
def search_flights():
    ''' Combine results from all providers, sorting by agony.
    
    Args:
        None
    
    Returns:
        Json of all merged results.
    '''
    # In python3, I would replace this with either a threadpoolexecutor or
    # asyncio; both would scale better than this, but we're definitely better
    # off making all of the requests concurrently, even if we need to use
    # threads directly (note that the GIL could still limit this though)
    
    # We need to actually retrieve the results from the threads, so we'll
    # create a results object for them to mutate. Sets are already threadsafe,
    # so we don't need to do anything special for it to work.
    results = []
    threads = []
    
    # Create and start a thread for each provider. In a more ideal world we
    # would add some limits to how many concurrent threads we have alive
    for provider in PROVIDERS:
        provider_thread = threading.Thread(
            target=get_single_scrape,
            args=(provider, results)
        )
        provider_thread.daemon = False
        threads.append(provider_thread)
        provider_thread.start()
        
    # Now we need to wait until all of the requests are finished.
    for provider_thread in threads:
        provider_thread.join(SCRAPER_TIMEOUT)
        
        # Check for a timeout. We don't have a way to kill threads if it did,
        # but we can at least abort the request.
        if provider_thread.isAlive():
            # Gateway timeout seems fairly appropriate here. This will exit the
            # request without running anything else below.
            flask.abort(504)
    
    # This creates an iterator for the merged result.
    merged = heapq.merge(*results)
    # Note that we're once again hard-coding the response format, which, again,
    # could probably be improved upon.
    return flask.jsonify(
        {
            # Note that iterators aren't natively serializable, so
            # unfortunately we need to collapse it into a list
            'results': list(merged)
        }
    )
