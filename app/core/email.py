import os

from django.contrib.auth import get_user_model
from django.apps import apps

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Email(object):
    """
    Constructs a transaction email and message
    to one user based on system events.
    """
    def __init__(self, template_name, to_emails):
        self.api_key = (
            'SG.IjdbYqf4R0G3L5cHp1JxCQ.VhvjRtUSx'
            'X5BAH39hKuVGpYi_lhpRZW-t9st6mxEGvA'
        )
        if template_name == 'welcome_user':
            self.from_email = 'welcome@liveleague.events'
            self.template_id = 'd-02c660b9b23c45ed992fc601dec8fd3f'
            self.subject = 'Welcome to Live League!'
            self.text = '''
                        Congratulations!\n
                        You've just signed up to the UK's biggest underground
                        music competition. As a new user, you can look forward
                        to:\n
                        - Exclusive online offers\n
                        - Chances to win great prizes\n
                        - Voting for your favourite artists\n
                        Be sure to follow us on social media for the latest
                        news and competition results:\n
                        - https://www.facebook.com/liveleague.events\n
                        - https://www.instagram.com/_liveleague/\n
                        - https://www.twitter.com/_liveleague/\n
                        '''
        elif template_name == 'welcome_artist':
            self.from_email = 'welcome@liveleague.events'
            self.template_id = 'd-f73543b6aed34417ae4f4c5a6db5a98f'
            self.subject = 'Welcome to Live League!'
            self.text = '<insert welcome_artist message here>'
        elif template_name == 'welcome_promoter':
            self.from_email = 'welcome@liveleague.events'
            self.template_id = 'd-80b7e3003a534a4686976de701710fdc'
            self.subject = 'Welcome to Live League!'
            self.text = '<insert welcome_promoter message here>'
        elif template_name == 'verified_promoter':
            self.from_email = 'support@liveleague.events'
            self.template_id = 'd-d2abe65f88754c63891c162c5340cc0e'
            self.subject = 'Your account has been verified'
            self.text = '<insert verified_promoter message here>'
        elif template_name == 'ticket':
            self.from_email = 'sales@liveleague.events'
            self.template_id = 'd-5089e73b4c8644d4be176c24cd1b18d7'
            self.subject = 'Your ticket has been purchased!'
            self.text = '<insert ticket message here>'
        elif template_name == 'artist_added':
            self.from_email = 'support@liveleague.events'
            self.template_id = 'd-9eb52223f95248228a9e6c37bdf20a25'
            self.subject = "You've been added to an event"
            self.text = '<insert artist_added message here>'
        elif template_name == 'artist_removed':
            self.from_email = 'support@liveleague.events'
            self.template_id = 'd-cdab3d850b7f4188ba2d86209cdb7b34'
            self.subject = "You've been removed from an event"
            self.text = '<insert artist_removed message here>'
        elif template_name == 'vote':
            self.from_email = 'sales@liveleague.events'
            self.template_id = 'd-e62412bc6e6f492390d83a2284a6bd24'
            self.subject = 'Your vote has been cast!'
            self.text = '<insert vote message here>'
        if isinstance(to_emails, list):
            self.to_emails = to_emails
        else:
            self.to_emails = to_emails.split()
        self.Message = apps.get_model('core', 'Message')
        self.ReadFlag = apps.get_model('core', 'ReadFlag')

    def send(self):
        """Sends an email and creates a message and read flag."""
        for address in self.to_emails:
            email = Mail(
                from_email=self.from_email,
                to_emails=address,
            )
            email.template_id = self.template_id
            try:
                sg = SendGridAPIClient(self.api_key).send(email)
                print('Email(s) sent to:', self.to_emails)
            except Exception as e:
                print('Email(s) failed:', str(e))
            message = self.Message.objects.create_message(
                self.subject, self.text
            )
            recipient = get_user_model().objects.get(email=address)
            readflag = self.ReadFlag.objects.create_readflag(
                message, recipient
            )
