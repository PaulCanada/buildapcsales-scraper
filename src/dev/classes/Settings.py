import simplejson
import logging


class Settings(object):

    def __init__(self):
        self.client_id = ""
        self.client_secret = ""
        self.client_agent = ""

        self.load_settings()

    def load_settings(self):
        try:
            with open('./client_info.json', 'r') as file:
                client_info = simplejson.loads(file.read())

        except FileNotFoundError:
            logging.error("Failed to find client_info.json. Exiting.")
            exit(3)

        try:
            self.client_id = client_info['client_id']
            self.client_secret = client_info['client_secret']
            self.client_agent = client_info['client_agent']

        except KeyError as ke:
            logging.critical("Failed to extract client information: {0}".format(ke))
