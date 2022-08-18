import argparse


def echo_msg(msg: str, file_name: str = None) -> None:
    """Simple echo of input message either on console or input file.

    This is line two of the description.

    This is line three of description

    Parameters
    ----------
    msg: message to display on console / write to file
    file_name: name of the file where to write the message

    Returns
    -------
    None
    """

    print(f'{msg}')
    if file_name is not None:
        text_file = open(file_name, "wt")
        n = text_file.write(msg)
        text_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('msg', type=str, nargs='?',
                        default='Hi from ArgumentParser',
                        help='echo back the input message')

    parser.add_argument('-f', '--file',
                        help='echo to file')

    args = parser.parse_args()
    msg = args.msg if args.msg else 'Hi, PyCharm'
    file_name = args.file if args.file else None

    echo_msg(msg, file_name)
