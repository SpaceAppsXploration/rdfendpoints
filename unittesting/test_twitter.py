import unittest
import twitter
import json


from config.tw_secret import token, token_key, con_secret, con_secret_key
from flankers.textsemantics import find_related_concepts

__author__ = 'Lorenzo'


class TwitterTests(unittest.TestCase):
    #twitter_lists = ['nasa-tech', 'astronomy-space-only', 'nasa-social', 'esa']

    api = twitter.Api(consumer_key=con_secret,
                      consumer_secret=con_secret_key,
                      access_token_key=token,
                      access_token_secret=token_key)
                      #cache=None)

    def runTest(self):
        def request_list_members(cursor=-1, lst=None):
            """
            Return members in a list of the Twitter account
            :param cursor: status of the cursor (-1 = start)
            :param lst: slug of the list
            :param count: number of returning objects
            :return: a complete Twitter API object as dict()
            """
            if not lst:
                lst = self.twitter_lists[0]
            return self.api.GetListMembers(slug=lst, cursor=cursor)

        def get_all_users_from_list(users=list(), cursor=-1, lst=None):
            """
            Recursevely return all the members' screen names of a list
            :param users: store the outcome
            :param cursor: status of the cursor (-1 = start)
            :return: a list() of screen names
            """
            members = request_list_members(lst=self.twitter_lists[0], cursor=cursor) \
                if lst is None \
                else request_list_members(lst=lst, cursor=cursor)
            print members[len(members) - 1]
            if members[len(members) - 1][1] == 0:
                return users
            print[u.__dict__['screen_name'] for u in members[0]]
            return get_all_users_from_list([u.__dict__['screen_name'] for u in members[0]],
                                           cursor=members[len(members) - 1][1])

        twitter_lists = self.api.GetLists(screen_name='XplorationApp')

        def lists_ids():
            """
            Return id and slug of the lists
            :return: a list() of tuple(id, slug)
            """
            twitter_lists = self.api.GetLists(screen_name='XplorationApp')
            return [(l.__dict__['_id'], l.__dict__['_name']) for l in twitter_lists]

        def list_timeline(targs):
            """
            Return the timeline for a given list
            :param targs: a tuple(id, slug) of a list
            :return: a list() of Tweets objects
            """
            _id, _slug = targs[0], targs[1]
            pub_list = self.api.GetListTimeline(list_id=_id, slug=_slug)
            return pub_list

        for twt in list_timeline(lists_ids()[1]):
            if isinstance(twt, list):
                print twt
                break
            print 'https://twitter.com/' + str(twt.GetUser().screen_name) + '/status/' + str(twt.GetId())
            print twt.media[0]['media_url'] if isinstance(twt.media, list) and len(twt.media) != 0 else None
            print twt.media['media_url'] if isinstance(twt.media, dict) and 'media_url' in twt.media.keys() else None
            print twt.urls[0].__dict__

        else:
            print None

            print twt.urls[0].url if len(twt.urls) != 0 else None


        def pick_info_from_twt(twt):
                """
                Extract text, url and image url from a Tweet object
                :param twt: the Tweet object from Twitter API
                :return: tuple: text, url of the Tweet, url of the image in the Tweet
                """
                txt = twt['text'].encode('ascii', 'replace')
                url = twt['entities']['urls'][0]['url'] if len(twt['entities']['urls']) != 0 else None
                media = twt['entities']['media'][0]['media_url'] if 'media' in twt['entities'].keys() else None
                #c = find_related_concepts(txt)
                return txt, url, media

        def lists_ids(self):
            """
            Return id and slug of the lists
            :return: a list() of tuple(id, slug)
            """
            twitter_lists = self.api.GetLists(screen_name='XplorationApp')
            return [(l.__dict__['_id'], l.__dict__['_name']) for l in twitter_lists]




        def get_all_users_from_list(self, users=list(), cursor=-1, lst=None):
            """
            Recursevely return all the members' screen names of a list
            :param users: store the outcome
            :param cursor: status of the cursor (-1 = start)
            :return: a list() of screen names
            """
            members = self.request_list_members(lst=self.twitter_lists[0], cursor=cursor) \
                if lst is None \
                else self.request_list_members(lst=lst, cursor=cursor)
            if members['next_cursor'] == 0:
                return users
            return self.get_all_users_from_list([u['screen_name'] for u in members['users']],
                                                cursor=members['next_cursor_str'])
        #print list_timeline(lists_ids()[0])


        '''from flankers.tweetStore import get_all_users_from_list, request_list_members

        def get_counted(count=1):
            return request_list_members(count=count)



        # print get_all_users_from_list()

        # five = get_counted()['users'][0]['screen_name']

        for user in get_all_users_from_list()[0:4]:
            print user
            twts = t.statuses.user_timeline(screen_name=user, count=5)
            for tw in twts:
                i = pick_info_from_twt(tw)
                print i
            # s = storeIndexer()
            # s.execute_task(q, q.key)
'''
        #
        # Tweet structure:
        # users.0.screen_name > twitter name
        # text > text of the tweet
        # entities.urls.0.url > url of the tweet
        # entities.media.0.media_url
        #