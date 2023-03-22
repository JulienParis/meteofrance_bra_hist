import logging
import subprocess

from utils.bulletin import Bulletin
from utils.common import init_logger, MASSIFS
from utils.github import init_repo, update_file_content, \
    commit_many_files_and_push, add_file_to_commit

logger = init_logger(logging.DEBUG)

branch = 'master'
repo = init_repo()
files_to_commit = []

for massif in MASSIFS:
    # Lecture de la date de publication de notre fichier
    dates_ = subprocess.run(["cat", f"data/{massif}/urls_list.txt"],
                            capture_output=True).stdout.decode('utf-8').split(
        '\n')
    logger.debug(massif)
    new_data = []
    for date_ in dates_:
        if int(date_) >= 20181217143136:  ## Début des fichiers XML
            logger.debug(date_)
            bulletin = Bulletin(massif, date_)
            bulletin.download()

            try:
                bulletin.parse()
                new_data.append(bulletin.append_csv())
            except Exception as e:
                pass

    file_path = f'data/{massif}/hist.csv'
    logger.info(f'Exporting the BERA to Github for massif : {massif}   ...')

    # Update file already existing
    full_content = update_file_content(repo, file_path, branch, new_data,
                                       type_data='bera')

    # Add file in the tree to commit
    files_to_commit = add_file_to_commit(repo, full_content, file_path,
                                         files_to_commit)

logger.info('Compile all modified files in one commit  ...')
commit_many_files_and_push(repo, branch, "Daily automatic csv files update",
                           files_to_commit)
logger.info('Job succeeded  ...')
