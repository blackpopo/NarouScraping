
from scrapy import log
from scrapy.http import Request, Response

import twitter


class TwitterUserTimelineRequest(Request):

    def __init__(self, *args, **kwargs):
        self.screen_name = kwargs.pop('screen_name', None)
        self.count = kwargs.pop('count', None)
        self.max_id = kwargs.pop('max_id', None)
        super(TwitterUserTimelineRequest, self).__init__('http://twitter.com',
                                                         dont_filter=True,
                                                         **kwargs)


class TwitterStreamFilterRequest(Request):

    def __init__(self, *args, **kwargs):
        self.track = kwargs.pop('track', None)
        super(TwitterStreamFilterRequest, self).__init__('http://twitter.com',
                                                         dont_filter=True,
                                                         **kwargs)


class TwitterResponse(Response):

    def __init__(self, *args, **kwargs):
        self.tweets = kwargs.pop('tweets', None)
        super(TwitterResponse, self).__init__('http://twitter.com',
                                              *args,
                                              **kwargs)
