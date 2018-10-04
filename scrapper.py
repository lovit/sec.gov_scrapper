import argparse
import os
import requests
import time
from bs4 import BeautifulSoup

# basic functions
def get_html_source(url):
    try:
        html_source = requests.get(url).text
        return html_source
    except:
        return None

def get_soup(url):
    try:
        html_source = requests.get(url).text
        soup = BeautifulSoup(html_source, 'lxml')
        return soup
    except:
        return None

def parse_html_link(soup):
    '''
    BeautifulSoup(html_source)로부터 끝에 htm이 들어간 링크들만 가져오기
    '''
    links = soup.find_all('a') 
    links = [link.attrs.get('href', '').strip() for link in links] 
    links = [link for link in links if '.htm' in link]
    return links

def parse_document_links(soup):
    links = soup.select('a[href^=/Archives/edgar/data/%d]' % company_id_int)
    links = [link.attrs.get('href', '').strip() for link in links]
    links = ['https://www.sec.gov'+link for link in links if '.htm' in link]
    return links

def parse_document_links_with_filling_date(soup):
    rows = soup.select('table[class=tableFile2] tr')
    if len(rows) <= 1:
        return []
    links_and_date = []
    for i, row in enumerate(rows):
        if i == 0:
            continue
        td = row.select('td')
        document_link = 'https://www.sec.gov' + td[1].select('a')[0].attrs.get('href', '')
        filling_date = td[3].text
        links_and_date.append((document_link, filling_date))        
    return links_and_date

# format (company_id, n_latest_html_per_company)
step1_base_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=def+14a&dateb=&owner=exclude&count={}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--company_path', type=str, default='company_list')
    parser.add_argument('--html_directory', type=str, default='./html/')
    parser.add_argument('--n_html_subdirectory', type=int, default=20)
    parser.add_argument('--n_latest_html_per_company', type=int, default=10)
    parser.add_argument('--period_begin', type=str, default='2017-01-01')
    parser.add_argument('--period_end', type=str, default='2018-01-01')
    parser.add_argument('--debug', dest='debug', action='store_true')

    args = parser.parse_args()
    company_path = args.company_path    
    html_directory = args.html_directory    
    n_html_subdirectory = args.n_html_subdirectory    
    n_latest_html_per_company = args.n_latest_html_per_company    
    period_begin = args.period_begin
    period_end = args.period_end
    debug = args.debug

    assert n_latest_html_per_company > 1
    assert period_begin < period_end

    # load company_list
    with open(company_path, encoding='utf-8') as f:
        # skip head
        next(f)
        company = [line[:-1] for line in f]

    company_list = [line.split('\t') for line in company]
    company_list = [line for line in company_list if line[2] != '']

    # create html tmp subdirectories
    if n_html_subdirectory > 0:
        for i in range(n_html_subdirectory):
            if not os.path.exists('{}/{}/'.format(html_directory, i)):
                os.makedirs('{}/{}/'.format(html_directory, i))
    else:
        if not os.path.exists('{}/'.format(html_directory)):
            os.makedirs('{}/'.format(html_directory))

    # main
    for num_company, company in enumerate(company_list):        
        if debug and num_company >= 30:
            break
        if num_company == 0:
            print('begin scrapper')
        elif ((num_company < 50) and (num_company % 5 == 0)):
            print('  .. scrapping (%d in %d)' % (num_company+1, len(company_list)))
        elif ((num_company < 500) and (num_company % 50 == 0)):
            print('  .. scrapping (%d in %d)' % (num_company+1, len(company_list)))
        elif num_company % 500 == 0:
            print('  .. scrapping (%d in %d)' % (num_company+1, len(company_list)))

        try:
            company_id = company[1]
            company_id_int = int(company[2])

            url = step1_base_url.format(company_id, n_latest_html_per_company)
            step1_soup = get_soup(url)

            if step1_soup == None:
                continue

            links = parse_document_links_with_filling_date(step1_soup)

            for num_dps, (step2link, filling_date) in enumerate(links):

                if not (period_begin <= filling_date <= period_end):
                    continue

                step2_soup = get_soup(step2link)
                if step2_soup == None:
                    continue

                table_rows = step2_soup.select('table[class=tableFile] tr')
                if len(table_rows) <= 1:
                    continue

                proxy_statement_link = table_rows[1].select('a')
                if len(proxy_statement_link) == 0:
                    continue

                proxy_statement_link = proxy_statement_link[0].attrs.get('href', '')
                proxy_statement_link = 'https://www.sec.gov' + proxy_statement_link 
                proxy_statement_link

                dps_html_source = get_html_source(proxy_statement_link)
                if dps_html_source == None:
                    continue

                if n_html_subdirectory > 0:
                    company_folder = num_company % n_html_subdirectory
                else:
                    company_folder = ''

                dps_html_fname = '{}/{}/{}_{}.html'.format(html_directory, company_folder, company_id, filling_date)
                with open(dps_html_fname, 'w', encoding='utf-8') as f:
                    f.write(dps_html_source)

            time.sleep(1)

        except Exception as e:
            print('error message = %s (num_company = %d)' % (str(e), num_company))

if __name__ == '__main__':
    main()