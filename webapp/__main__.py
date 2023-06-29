from webapp.spimex_parser import upload_file_from_spimex, read_spimex_file


def main() -> None:
    print('app started')
    upload_file_from_spimex()
    read_spimex_file()


if __name__ == '__main__':
    main()
