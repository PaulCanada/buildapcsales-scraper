import logging

import praw


class Scraper(object):

    def __init__(self, settings, category=None, product=None, subreddit=None):
        self.category = category or ""
        self.product = product or ""
        self.subreddit = subreddit or "buildapcsales"
        self.reddit_client = None
        self.settings = settings
        self.current_subreddit = None

        if not self.settings:
            logging.critical("No settings information loaded. Exiting.")
            exit(2)

        self.category_list = [
            "CPU",
            "CPU Cooler",
            "Cooler",
            "GPU",
            "SSD",
            "HDD",
            "PSU",
            "Monitor",
            "Prebuilt",
            "Case",
            "Motherboard",
            "Mobo"
        ]

        if not self.category.startswith("[") and not self.category.endswith("]"):
            self.category = "[" + self.category + "]"

        if not product:
            logging.warning("WARNING: No product specified. All posts may be returned.")

        self._load_reddit_client()

    def _load_reddit_client(self):
        self.reddit_client = praw.Reddit(client_id=self.settings.client_id, client_secret=self.settings.client_secret,
                                         user_agent=self.settings.client_agent)

    def _load_subreddit(self):
        self.current_subreddit = self.reddit_client.subreddit(self.subreddit)

    def get_new(self, count=10):
        self._load_subreddit()

        return [submission for submission in self.current_subreddit.new(limit=count)]

    def check_for_product(self, submission):
        found = False
        if self.product.lower() in submission.title.lower():
            logging.debug("Product {0} found in {1}".format(self.product, submission.title))
            found = True
        # else:
        #     print("Product {0} not found in {1}".format(self.product, submission.title))

        return found

    def check_for_category(self, submission):
        found = False

        submission_category = submission.title[submission.title.find("["):submission.title.find("]") + 1]
        logging.debug(submission_category)

        if self.category.lower() in submission_category:
            logging.debug("Category {0} found in {1}".format(self.category, submission.title))
            found = True
        # else:
        #     print("Category {0} not found in {1}".format(self.category, submission.title))

        return found

    def check_for_deal(self):
        submission_list = self.get_new(count=30)
        found_one = False

        for submission in submission_list:
            category_found = self.check_for_category(submission)

            if not category_found:
                continue

            product_found = self.check_for_product(submission)

            if product_found:
                found_one = True
                logging.info("{0} was found: {1}".format(self.product, submission.shortlink))

        if not found_one:
            logging.info("No product deals were found for {0}.".format(self.product))

    def print_description(self):
        print(self.current_subreddit.description)

