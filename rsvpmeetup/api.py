from .errors import *
import requests
import time
from datetime import date, timedelta
import json
import sys
from .helper import *


class Session(requests.Session):
    """
    requests.session object ,
    with error handling inbuilt,
    config Files

    """

    # Override
    def request(self, method, url, **kwargs):
        r = super().request(method, url, **kwargs)
        time.sleep(2)  # Respecting site rate limits , and to not get banned
        r.raise_for_status()
        return r

    def login(self):

        user = get_config_data('secret.json')
        self.headers = get_headers('initial')
        r = self.get('https://secure.meetup.com/login/')

        self.headers = get_headers('login')
        data = {
            'email': user['email'],
            'password': user['password'],
            'rememberme': 'on',
            'token': getToken(r.text),
            'submitButton': 'Log in',
            'returnUri': 'https://www.meetup.com/',
            'op': 'login',
            'apiAppClientId': ''
        }
        loginResponse = self.post('https://secure.meetup.com/login/', data=data)
        if loginResponse.text.find("Your email or password was entered incorrectly") != -1:
            raise AuthError()
        print("Authorized Succesfully!")

    def rsvp_groups(self):

        groups = get_config_data('groups.json')

        for config_group in groups['groups']:

            if 'endDate' in config_group.keys():
                group = Group(urlname=config_group['urlname'], session=self, endDate=config_group['endDate'])
            else:
                group = Group(urlname=config_group['urlname'], session=self)
            if not group.invalid:  # If urlname provided is valid
                group.get_events(session=self)
class Group:
    def __init__(self, urlname: str, session: Session, endDate=date.today() + timedelta(days=30)):
        self.name = ''
        self.invalid = 0
        self.urlname = urlname
        self.endDate = str(endDate)
        try:
            session.get(self.getUrl())
        except requests.exceptions.HTTPError as e:
            print('Invalid Group name configured! Skipping' + "--> " + self.urlname)
            self.invalid = 1

    def get_events(self, session: Session):
        """
        Gets all events from a group till configured date , and rsvps to them
        if not configured , queried till a month later
        """
        startDate = str(date.today())
        session.headers = get_headers('standard')
        session.headers['referer'] = self.getUrl() + 'events/calendar/'
        session.headers[
            'x-meetup-activity'] = 'standardized_url=%2Furlname%2Fevents%2Fcalendar%2Fdate&standardized_referer=%2Furlname%2Fevents'

        queryStr = '(endpoint:members/self,meta:(method:get),params:(fields:\'memberships, privacy\'),ref:self,type:member),(endpoint:noop,flags:!(facebook_login_active,feature_microtargets_MUP-16377,nwp_event_template_MUP-16782,wework-announce,feature_google_tag_manager_MUP-19169),meta:(metaRequestHeaders:!(unread-notifications,unread-messages,admin-privileges,tos-query,facebook-auth-url,google-auth-url),method:get),params:(),ref:headers,type:headers),'+\
                   '(endpoint:'+self.urlname+',meta:(flags:!(feature_app_banner_MUP-16415,feature_new_group_event_home_MUP-16376,feature_new_group_home_sharing_MUP-16516,feature_twitter_group_sharing_MW-2381),method:get),params:(country:in,fields:\'category,city_link,fee_options,join_info,leads,localized_location,membership_dues,member_sample,other_services,past_event_count,draft_event_count,proposed_event_count,pending_members,photo_count,photo_sample,photo_gradient,plain_text_description,plain_text_no_images_description,profile,self,topics,nominated_member,nomination_acceptable,member_limit,leader_limit,last_event,welcome_message,pro_rsvp_survey\',state:\'\'),ref:group,type:group),'+\
                   '(endpoint:'+self.urlname+'/events,list:' \
                   + '(dynamicRef:\'list_events_for_period_'+self.urlname+"_" + startDate + 'T00:00:00.000_' + self.endDate + 'T00:00:00.000\'),meta:(method:get),params:(fields:\'comment_count,event_hosts,featured_photo,plain_text_no_images_description,series,self,rsvp_rules,rsvp_sample,venue,venue_visibility\',' \
                   + 'no_earlier_than:\'' + startDate + 'T00:00:00.000\',' \
                   + 'no_later_than:\'' + self.endDate + 'T00:00:00.000\',status:\'past,cancelled,upcoming\'),ref:\'' \
                   + 'events_for_period_'+self.urlname+"_"  + startDate + 'T00:00:00.000_' + self.endDate + 'T00:00:00.000\')'

        params = (
            ('queries', queryStr),
        )

        response = session.get('https://www.meetup.com/mu_api/urlname/events/calendar/date', params=params)
        response = json.loads(response.text)
        self.name = response['responses'][2]['value']['name']
        events = response['responses'][3]['value']
        events.sort(key=lambda event: event['created'])
        events.reverse()  # Reverse sorting via date
        print("RSVPing for ", self)
        for event in events:
            groupEvent = Event(json=event, group=self)

            print("---" + str(groupEvent) + "---")
            if not groupEvent.rsvp_done:#Checking to see if previousy RSVPD/WaitListed
                try:
                    groupEvent.rsvp(session=session)
                    print("RSVP Successful!")
                except FullRSVP as e:
                    print(e.message)
                    groupEvent.waitlist(session=session)
                    print("WaitList Successful!")
            else:
                print("Event already RSVP'd /Waitlisted before")




    def getUrl(self):
        """
        Return the Url of Group
        """
        return 'https://www.meetup.com/' \
               + self.urlname + '/'

    def __str__(self):
        return "Group name : " + self.name


class Event:
    def __init__(self, uniqueId:str, group: Group, name:str):
        """
        Manually Creating the event
        """
        self.uniqueId = uniqueId
        self.name = name
        self.rsvp_done = 0
        self.group = group
        self.waitlisted = 0
        self.time=''
        self.rsvp_limit=0
        self.yes_rsvp_count=0

    def __init__(self, json:dict, group:Group):
        """
        Directly creates event from json response
        """

        self.uniqueId = json['id']
        self.name = json['name']
        self.group = group

        try:
            self.rsvp_limit=json['rsvp_limit']
        except:
            self.rsvp_limit=100000 #No limit on rsvp Case
        self.yes_rsvp_count=json['yes_rsvp_count']
        self.rsvp_done = 0
        self.waitlisted = 0
        self.time=json['local_date']+' '+json['local_time']
        try:
            if (json['self']['rsvp']['response']=='yes'):#Means it has already been RSVP'd previously
                self.rsvp_done=1
        except:
            self.rsvp_done=0



    def getUrl(self):
        """
        Returns the Url of the Event
        """
        return self.group.getUrl() + \
               "events/" + self.uniqueId + "/"

    def rsvp(self, session: Session) -> str:
        if not self.waitlisted and self.is_full():
            raise FullRSVP
        session.headers = get_headers('standard')

        session.headers = {
            'authority': 'www.meetup.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.132 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        params = (
            ('action', 'rsvp'),
            ('response', 'yes'),
        )

        response = session.get(self.getUrl(), params=params)
        # idk(s)

        referer = self.getUrl() + '?action=rsvp&response=yes'  # referer in header
        session.headers = get_headers('rsvp')
        session.headers['referer'] = referer
        session.headers['x-mwp-csrf'] = session.cookies['x-mwp-csrf-header']
        queryStr = '(endpoint:' \
                   + self.group.urlname + "/events/" + self.uniqueId + "/rsvps" \
                   + ',meta:(method:post),' \
                   + 'params:(eventId:' + self.uniqueId \
                   + ',fields:rsvp_counts,response:yes,' \
                   + 'self.group.urlname:' + self.group.urlname + ')' \
                   + ',ref:rsvpAction' + "_" + self.group.urlname + '_' + self.uniqueId + ')'


        data = {
            'queries': queryStr
        }
        response = session.post('https://www.meetup.com/mu_api/urlname/events/eventId', data=data)
        if not self.waitlisted: self.rsvp_done = 1
        return "OK"
    def waitlist(self, session: Session):
        self.waitlisted=1
        self.rsvp(session)
    def __str__(self):
        return "Event Name :" + self.name+"\n"\
                "Timing of event! : "+self.time

    def is_full(self):
        return self.rsvp_limit == self.yes_rsvp_count


