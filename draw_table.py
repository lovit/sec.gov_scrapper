import os
import argparse
from glob import glob
from utils.utils import parse_idx_date

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html_directory', type=str, default='./tmp/')
    parser.add_argument('--table_path', type=str, default='./empty_table.txt')    
    parser.add_argument('--date_type', choices=['yy', 'yy-mm', 'yy-mm-dd'], default='yy-mm-dd')
    parser.add_argument('--debug', dest='debug', action='store_true')

    args = parser.parse_args()
    html_directory = args.html_directory
    table_path = args.table_path
    date_type = args.date_type
    debug = args.debug

    table_directory = os.path.dirname(table_path)
    if not os.path.exists(table_directory):
        os.makedirs(table_directory)

    paths = (glob('{}/*.html'.format(html_directory)) 
             + glob('{}/*/*.html'.format(html_directory)))

    entries = {'{}\t{}'.format(*parse_idx_date(path, date_type)) for path in paths}

    with open(table_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write('{}\n'.format(entry))

if __name__ == '__main__':
    main()