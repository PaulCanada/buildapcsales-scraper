import logging

from src.dev.classes.Scraper import Scraper
from src.dev.classes.Settings import Settings


logging.getLogger().setLevel(logging.INFO)


def main():
    s = Settings()
    scrap = Scraper(s, product="GTX 1080", category="GPU")

    # scrap.print_description()

    scrap.check_for_deal()


if __name__ == '__main__':
    main()
