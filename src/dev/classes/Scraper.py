import logging

import praw
import pprint
import re


class Scraper(object):

    def __init__(self, settings, category=None, product=None, subreddit=None, count=10, skip_oos=False, max_price=None):
        self.category = category or ""
        self.product = product or ""
        self.subreddit = subreddit or "buildapcsales"
        self.reddit_client = None
        self.settings = settings
        self.current_subreddit = None
        self.search_count = count
        self.skip_oos = skip_oos
        self.max_price = max_price

        if not self.settings:
            logging.critical("No settings information loaded. Exiting.")
            exit(2)

        # if not self.category.startswith("[") and not self.category.endswith("]"):
        #     self.category = "[" + self.category + "]"

        if not product:
            logging.warning("WARNING: No product specified. All posts may be returned.")

        self._load_reddit_client()

    def _load_reddit_client(self):
        self.reddit_client = praw.Reddit(client_id=self.settings.client_id, client_secret=self.settings.client_secret,
                                         user_agent=self.settings.client_agent)

    def _load_subreddit(self):
        self.current_subreddit = self.reddit_client.subreddit(self.subreddit)

    def _get_new(self, count=10):
        self._load_subreddit()

        return [submission for submission in self.current_subreddit.new(limit=count)]

    def _check_for_product(self, submission):
        found = False
        if self.product.lower() in submission.title.lower():
            logging.debug("Product {0} found in {1}".format(self.product, submission.title))
            found = True
        # else:
        #     print("Product {0} not found in {1}".format(self.product, submission.title))

        return found

    def _check_for_category(self, submission):
        found = False
        post = submission.title
        self._find_price(submission)

        # Check for expired post.
        if submission.link_flair_text and any(flair in submission.link_flair_text for flair in ['Expired', 'Out Of Stock', 'OOS']) and self.skip_oos:
            logging.debug("Deal: '{0}' is expired.".format(post))
            return False

        else:
            submission_category = submission.link_flair_text or post[post.find("["):post.find("]") + 1]

        logging.debug("Category: {0}".format(submission_category))

        if self.category.lower() in submission_category.lower():
            logging.debug("Category {0} found in {1}".format(self.category, submission.title))
            found = True
        # else:
        #     print("Category {0} not found in {1}".format(self.category, submission.title))

        return found

    def check_for_deal(self):
        submission_list = self._get_new(count=self.search_count)
        found_one = False

        for submission in submission_list:
            if self._check_for_category(submission) and self._check_for_product(submission):
                found_one = True
                logging.info("{0} was found: {1}\n{2}".format(self.product, submission.shortlink, submission.title))
                # pprint.pprint(vars(submission))

        if not found_one:
            logging.info("No product deals were found for {0}.".format(self.product))

    @staticmethod
    def _find_price(submission):
        m = re.search(r"\$\d+(?:\.\d+)?", submission.title)
        if m:
            logging.debug("Submission: {0} ### Price: {1}".format(submission.title, m.group()))
        else:
            logging.debug("Bad format: {0}".format(submission.title))

    def print_description(self):
        print(self.current_subreddit.description)

