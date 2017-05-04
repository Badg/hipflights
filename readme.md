# HipFlights: Hipmunk flights API coding exercise

## Requirements

Requires Python. Tested on both python 2.7 and python 3.5.

3rd-party python deps (```flask``` and ```requests```) are handled by ```setup.py```.

## Installation and usage

Within a virtualenv of your choosing:

```
    git clone https://github.com/Badg/hipflights.git
    pip install -e ./hipflights
    python -m hipflights
```

## Notes

+ Normally, I would version the API endpoint, for example using ```GET /flights/v1/search``` or ```GET /v1/flights/search```, etc; since this would break the test script (not to mention violate the spec sheet!) I didn't.
+ This isn't really focused on scalability; I was more concerned with "shipping fast" and "write clean code". In a more perfect world, I would either mirror the scraperapi's use of tornado, or move to ```async```/```await``` in python 3
+ Furthermore, if I were **really** concerned about performance, I might set the whole thing up as a streaming system: read from each socket, parse each json result as you go, and merging on the fly, writing each result to the output socket immediately. The only problem there is you'd have to wait for all of the receiving sockets' buffers from the scrapers api call to have data, so if one of them went down, you might accumulate a bunch of junk in the socket buffers, potentially causing issues with backpressure (not to mention, effectively leaking memory)
+ I used ```heapq.merge``` to merge the sorted lists, rather than writing my own merge function, purely out of time constraints. Realistically speaking, I've seen benchmarks suggesting that it's actually fastest to ```.extend()``` and then ```.sort()```, even when the input lists are sorted, for ```n < ~100000```. This is a result of the list operations being written in C, whereas the ```heapq.merge``` call is implemented in pure Python
+ In a more perfect world, the API would implement some kind of pagination, instead of returning all results at once
+ This is geared towards simplicity; if you wanted to do anything more with the API than just merge results from different providers, I would very likely cast the parsed json into dedicated ```Result``` objects
+ (Hopefully obviously) in a production environment I would write more tests, particularly ones that do a better job of mocking the scraper APIs than simply running them locally. Given that the code exercise ships with its own test suite, and that the code is so simple, I instead opted to just test it locally several times.
+ I considered setting up Travis for this to make it easier to test against both python 2 and python 3, but it seemed like overkill, so I just tested it locally.
