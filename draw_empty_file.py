import os
import argparse
from glob import glob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html_directory', type=str, default='./tmp/')
    parser.add_argument('--txt_directory', type=str, default='./txt/')
    parser.add_argument('--debug', dest='debug', action='store_true')

    args = parser.parse_args()
    html_directory = args.html_directory
    txt_directory = args.txt_directory
    debug = args.debug

    paths = (glob('{}/*.html'.format(html_directory)) 
             + glob('{}/*/*.html'.format(html_directory)))

    if debug:
        paths = paths[:30]

    for path in paths:
        txt_path = path.replace(html_directory, txt_directory)
        txt_path = txt_path[:-5] + '.txt'
        dirname = os.path.dirname(txt_path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('')

if __name__ == '__main__':
    main()