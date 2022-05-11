# Ce script doit etre executé a partir de 16h.
import sys
import logging
from utils.extract import extract_url_dl
from utils.github import push, init_repo, get_remote_file
from datetime import date, timedelta, datetime
from utils.common import init_logger, MASSIFS

logger = init_logger()


if __name__ == '__main__':
    logger.info('Starting the extraction of urls...')
    new_urls = extract_url_dl(no_browser=True, start_date=date.today() + timedelta(days=-1), end_date=date.today() + timedelta(days=-1))

    branch = 'master'
    repo = init_repo()

    for massif in MASSIFS:
        file_path = f'app/data/{massif}/urls_list.txt'
        logger.info(f'Exporting the URL to Github for massif : {massif}   ...')
        push(repo, file_path, "Daily automatic file update", new_urls[massif], branch, update=True)
