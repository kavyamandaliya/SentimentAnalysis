from os import environ
from time import time, sleep

import requests
import requests.auth
from requests_oauthlib import OAuth1

from .exceptions import *


class API:
    def __init__(self, session=None):
        self.log_function = print
        self.retry_rate = 5
        self.num_retries = 5
        self.failed_last = False
        self.force_stop = False
        self.ignore_errors = False
        self.common_errors = (requests.exceptions.ConnectionError,
                              requests.exceptions.Timeout,
                              requests.exceptions.HTTPError)
        self.session = session

    def __str__(self):
        return pformat(vars(self))

    def log_error(self, e):
        """
        Print errors. Stop travis-ci from leaking api keys

        :param e: The error
        :return: None
        """

        if not environ.get('CI'):
            self.log_function(e)
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                self.log_function(e.response.text)

    def _sleep(self, seconds):
        """
        Sleep between requests, but don't force asynchronous code to wait

        :param seconds: The number of seconds to sleep
        :return: None
        """
        for _ in range(int(seconds)):
            if not self.force_stop:
                sleep(1)

    @staticmethod
    def merge_params(parameters, new):
        if new:
            parameters = {**parameters, **new}
        return parameters

    def get(self, *args, **kwargs):

        """
        An interface for get requests that handles errors more gracefully to
        prevent data loss
        """

        try:
            req_func = self.session.get if self.session else requests.get
            req = req_func(*args, **kwargs)
            req.raise_for_status()
            self.failed_last = False
            return req

        except requests.exceptions.RequestException as e:
            self.log_error(e)
            for i in range(1, self.num_retries):
                sleep_time = self.retry_rate * i
                self.log_function("Retrying in %s seconds" % sleep_time)
                self._sleep(sleep_time)
                try:
                    req = requests.get(*args, **kwargs)
                    req.raise_for_status()
                    self.log_function("New request successful")
                    return req
                except requests.exceptions.RequestException:
                    self.log_function("New request failed")

            # Allows for the api to ignore one potentially bad request
            if not self.failed_last:
                self.failed_last = True
                raise ApiError(e)
            else:
                raise FatalApiError(e)


class Reddit(API):
    def __init__(self, application_id, application_secret):
        super().__init__()
        self.retry_rate /= 2  # Because it will try reauthorise if failure

        self.application_id = application_id
        self.application_secret = application_secret

        self.url = "https://oauth.reddit.com"
        self.request_rate = 5
        self.user_agent = "SocialReaper"
        self.headers = {}
        self.token_expiry = 0
        self.requires_reauth = True

        self.auth()
        self.last_request = time()

    def auth(self):
        client_auth = requests.auth.HTTPBasicAuth('%s' % self.application_id,
                                                  '%s' % self.application_secret)
        post_data = {"grant_type": "client_credentials"}
        headers = {"User-Agent": self.user_agent}

        try:
            response = requests.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=client_auth, data=post_data,
                headers=headers)
        except requests.exceptions.RequestException as e:
            raise ApiError(e)

        rj = response.json()

        self.headers = {"Authorization": "bearer %s" % rj.get('access_token'),
                        "User-Agent": self.user_agent}
        self.token_expiry = time() + rj.get('expires_in', 0)

    def api_call(self, edge, parameters, return_results=True):

        if time() > self.token_expiry + 30:
            self.auth()

        time_diff = time() - self.last_request
        if time_diff < self.request_rate:
            sleep(self.request_rate - time_diff)

        self.last_request = time()

        try:
            req = self.get("%s/%s" % (self.url, edge), params=parameters,
                           headers=self.headers)
        except (ApiError, FatalApiError):
            try:
                self.auth()
            except ApiError:
                pass
            req = self.get("%s/%s" % (self.url, edge), params=parameters,
                           headers=self.headers)

        if return_results:
            return req.json()

    def search(self, query, count=100, order="new", page='',
               result_type="link", time_period="all", **params):

        parameters = {"show": "all",
                      "q": query,
                      "limit": count,
                      "sort": order,
                      "type": result_type,
                      "t": time_period,
                      "after": page}
        parameters = self.merge_params(parameters, params)

        return self.api_call('search.json', parameters)

    def subreddit(self, subreddit, count=100, category="new", page='',
                  time_period='all', **params):

        parameters = {"limit": count,
                      "t": time_period,
                      "after": page}
        parameters = self.merge_params(parameters, params)

        return self.api_call('r/%s/%s.json' % (subreddit, category), parameters)

    def user(self, user, count=100, order="new", page='',
             result_type="overview", time_period='all', **params):

        parameters = {"show": "all",
                      "limit": count,
                      "sort": order,
                      "type": result_type,
                      "t": time_period,
                      "after": page}
        parameters = self.merge_params(parameters, params)

        return self.api_call('user/%s/%s.json' % (user, result_type),
                             parameters)

    def thread_comments(self, thread, subreddit, order="top", sub_thread=None,
                        **params):

        parameters = {"depth": 50,
                      "showmore": True,
                      "sort": order}
        parameters = self.merge_params(parameters, params)

        path = None
        if sub_thread:
            path = 'r/%s/comments/%s/_/%s.json' % (
            subreddit, thread, sub_thread)
        else:
            path = 'r/%s/comments/%s.json' % (subreddit, thread)

        return self.api_call(path, parameters)

    def more_children(self, children, link_id, sort="new",
                      **params):
        parameters = {"api_type": "json",
                      "children": ",".join(children),
                      "link_id": link_id,
                      "sort": sort,
                      "limit_children": False
                      }
        parameters = self.merge_params(parameters, params)

        return self.api_call('api/morechildren', parameters)


class Facebook(API):
    def __init__(self, api_key):
        super().__init__()

        self.key = api_key
        self.url = "https://graph.facebook.com/v"
        self.version = "2.9"
        self.request_rate = 1
        self.last_request = time()

    def api_call(self, edge, parameters, return_results=True):
        req = self.get("%s%s/%s" % (self.url, self.version, edge),
                       params=parameters)

        time_diff = time() - self.last_request
        if time_diff < self.request_rate:
            sleep(self.request_rate - time_diff)

        self.last_request = time()

        if return_results:
            return req.json()

    def node_edge(self, node, edge, fields=None, params=None):

        """

        :param node:
        :param edge:
        :param fields:
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"fields": fields,
                      "access_token": self.key}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s/%s' % (node, edge), parameters)

    def post(self, post_id, fields=None, **params):

        """

        :param post_id:
        :param fields:
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"fields": fields,
                      "access_token": self.key}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s' % post_id, parameters)

    def page_posts(self, page_id, after='', post_type="posts",
                   include_hidden=False, fields=None, **params):

        """

        :param page_id:
        :param after:
        :param post_type: Can be 'posts', 'feed', 'tagged', 'promotable_posts'
        :param include_hidden:
        :param fields:
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"access_token": self.key,
                      "after": after,
                      "fields": fields,
                      "include_hidden": include_hidden}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s/%s' % (page_id, post_type), parameters)

    def post_comments(self, post_id, after='', order="chronological",
                      filter="stream", fields=None, **params):

        """

        :param post_id:
        :param after:
        :param order: Can be 'ranked', 'chronological', 'reverse_chronological'
        :param filter: Can be 'stream', 'toplevel'
        :param fields: Can be 'id', 'application', 'attachment', 'can_comment',
        'can_remove', 'can_hide', 'can_like', 'can_reply_privately', 'comments',
        'comment_count', 'created_time', 'from', 'likes', 'like_count',
        'live_broadcast_timestamp', 'message', 'message_tags', 'object',
        'parent', 'private_reply_conversation', 'user_likes'
        :param params:
        :return:
        """
        if fields:
            fields = ",".join(fields)

        parameters = {"access_token": self.key,
                      "after": after,
                      "order": order,
                      "fields": fields,
                      "filter": filter}
        parameters = self.merge_params(parameters, params)

        return self.api_call('%s/comments' % post_id, parameters)


class Twitter(API):
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        super().__init__()

        self.app_key = api_key
        self.app_secret = api_secret
        self.oauth_token = access_token
        self.oauth_token_secret = access_token_secret

        self.url = "https://api.twitter.com/1.1"
        self.request_rate = 5

        self.auth = OAuth1(self.app_key, self.app_secret, self.oauth_token,
                           self.oauth_token_secret)
        self.last_request = time()

    def api_call(self, edge, parameters, return_results=True):
        req = self.get("%s/%s" % (self.url, edge), params=parameters,
                       auth=self.auth)

        time_diff = time() - self.last_request
        if time_diff < self.request_rate:
            sleep(self.request_rate - time_diff)

        self.last_request = time()

        if return_results:
            return req.json()

    def search(self, query, count=100, max_id='',
               result_type="mixed", include_entities=True,
               tweet_mode='extended', **params):

        count = 100 if count < 100 else count
        parameters = {"q": query,
                      "count": count,
                      "max_id": max_id,
                      "result_type": result_type,
                      "include_entities": include_entities,
                      "tweet_mode": tweet_mode}
        parameters = self.merge_params(parameters, params)

        return self.api_call("search/tweets.json", parameters)

    def user(self, username, count=200, max_id=None, exclude_replies=False,
             include_retweets=False, tweet_mode='extended', **params):
        parameters = {"screen_name": username,
                      "count": count,
                      "max_id": max_id,
                      "exclude_replies": exclude_replies,
                      "include_rts": include_retweets,
                      "tweet_mode": tweet_mode}
        parameters = self.merge_params(parameters, params)

        return self.api_call("statuses/user_timeline.json", parameters)
