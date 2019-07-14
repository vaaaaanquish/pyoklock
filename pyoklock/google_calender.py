import datetime
import unicodedata
import pickle
from os.path import exists
from os.path import expanduser
from prompt_toolkit.formatted_text import FormattedText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_east_asian_width_count(text):
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    return count


class GCalender():
    def __init__(self, events_top, today_flag, color):
        # OAuth
        self.events_top = events_top
        self.today_flag = today_flag
        self.color = color
        self.credential = None
        self._make_credential()
        self.service = build('calendar', 'v3', credentials=self.credential)
        self.events = []
        self._parse_calender()

    def _make_credential(self):
        if exists(expanduser('~/.pyoklock/token.pickle')):
            with open(expanduser('~/.pyoklock/token.pickle'), 'rb') as token:
                self.credential = pickle.load(token)
        if not self.credential or not self.credential.valid:
            if self.credential and\
                    self.credential.expired and self.credential.refresh_token:
                self.credential.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    expanduser('~/.pyoklock/credentials.json'), SCOPES)
                self.credential = flow.run_local_server()
            with open(expanduser('~/.pyoklock/token.pickle'), 'wb') as token:
                pickle.dump(self.credential, token)

    def _get_cal_events(self, maxResults=250):
        now = datetime.datetime.utcnow()
        now = now - datetime.timedelta(minutes=now.minute + now.hour * 60)
        now = now.isoformat() + 'Z'
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=maxResults,
            singleEvents=True,
            orderBy='startTime').execute()
        return events_result.get('items', [])

    def _parse_calender(self):
        for event in self._get_cal_events():
            e = {
                'title': event['summary'],
                'month': None,
                'day': None,
                'hour': None,
                'minute': None
            }
            d = event['start'].get('dateTime', None)
            if d is None:
                d = event['start']['date']
                d = datetime.datetime.strptime(d, "%Y-%m-%d")
                e['month'] = d.month
                e['day'] = d.day
            else:
                # 2017-08-07T07:09:31+00:00 -> 2017-08-07T07:09:31+0000
                d = d.split('+')
                d[1] = d[1].replace(':', '')
                d = datetime.datetime.strptime('+'.join(d),
                                               "%Y-%m-%dT%H:%M:%S%z")
                e['month'], e['day'], e['hour'], e[
                    'minute'] = d.month, d.day, d.hour, d.minute
            self.events.append(e)

    def get_calender_text(self):
        text = ''
        count = 0
        today = datetime.datetime.utcnow() if self.today_flag else None
        events = [
            x for x in self.events
            if x['month'] == today.month and x['day'] == today.day
        ] if self.today_flag else self.events

        if len(events) == 0:
            return 'not found events!'
        for e in events:
            text += '{:2d}/{:02} {} > {}\n'.format(
                e['month'], e['day'],
                '     ' if e['hour'] is None else '{:2d}:{:02}'.format(
                    e['hour'], e['minute']), e['title'])
            count += 1
            if count >= self.events_top:
                break
        return text

    def get_calender_text_formatted(self):
        text = []
        count = 0
        today = datetime.datetime.now()
        events = [
            x for x in self.events
            if x['month'] == today.month and x['day'] == today.day
        ] if self.today_flag else self.events

        if len(events) == 0:
            return 'not found events!'
        for e in events:
            t = '{:2d}/{:02} {} > {}\n'.format(
                e['month'], e['day'],
                '     ' if e['hour'] is None else '{:2d}:{:02}'.format(
                    e['hour'], e['minute']), e['title'])
            # formatted
            if e['month'] == today.month and e['day'] == today.day and e[
                    'hour'] is not None and self.color:
                d = (e['hour'] * 60 + e['minute']) - (
                    today.hour * 60 + today.minute)
                if d <= 5 and d > 0:
                    text.append(('#FF0000', t))
                elif d <= 0 and d >= -15:
                    text.append(('#008000', t))
                else:
                    text.append(('#ffffff', t))
            else:
                text.append(('#ffffff', t))
            count += 1
            if count >= self.events_top:
                break
        return FormattedText(text)

    def get_max_length(self):
        return max([
            get_east_asian_width_count(x)
            for x in self.get_calender_text().split('\n')
        ])
