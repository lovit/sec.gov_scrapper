def load_txt(path):
    encodings = ['utf-8', 'latin-1', ]
    for encoding in encodings:
        try:    
            text = _load_txt(path, encoding)
            break
        except:
            text = ''
            continue
    if not text:
        print('text file is empty or failed to detect read (encoding): {}'.format(path))
    return text
    
def _load_txt(path, encoding):
    with open(path, encoding=encoding) as f:
        text = ''.join([line for line in f])
    return text

def parse_idx_date(path, date_type='yy'):
    """date_type = [yy, yy-mm, yy-mm-dd]"""
    idx, date = path.replace('\\','/').split('/')[-1][:-4].split('_')[:2]
    if date_type == 'yy':
        date = date[:4]
    elif date_type == 'yy-mm':
        date = date[:7]
    elif date_type == 'yy-mm-dd':
        date = date[:10]
    else:
        raise ValueError('date_type value error: {}'.format(date_type))
    return idx, date