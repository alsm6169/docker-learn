import argparse


def echo_msg(msg, file_name = None):
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
