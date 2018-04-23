from utils import load_txt

def count_sum_of_word_frequency(path):    
    doc = load_txt(path) # return type = str
    return len(doc.split())