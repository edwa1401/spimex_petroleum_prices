import logging

from webapp.spimex_parser import download_file_from_spimex, read_spimex_file

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info('app started')
    download_file_from_spimex()
    read_spimex_file()


if __name__ == '__main__':
    main()
