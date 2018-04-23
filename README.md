## Scrapping

Scrapping proxy statement documents from www.sec.gov.

### Requires

Python libraries

	beautifulsoup4 >= 4.6.0
	requests >= 2.14.2
	argparse >= 1.1

Input file. company idx list. Tap separated file format. First line is header. 

	Company Name	CIK	CIK Number
	01 COMMUNIQUE LABORATORY INC	0	
	1347 CAPITAL CORP	0001606163	1606163
	1347 PROPERTY INS HLDGS INC	0001591890	1591890
	1-800-FLOWERS.COM	0001084869	1084869
	1PM INDUSTRIES INC	0000859747	859747
	1ST CAPITAL BANK	0000000000	
	1ST CENTURY BANCSHARES INC	0001420525	1420525
	...

### script

Python 3 script

	python scrapper.py [--arguments]

Examples

	python scrapper.py --debug --period_begin 2017-01-01 --period_end 2018-01-01 --html_directory /Users/myname/secgov/tmp/

Arguments

| argument | default value | description |
| --- | --- | --- |
| --company_path | 'company_list' | company list file. see above example for formatting |
| --html_directory | './tmp/' | directory for saving html |
| --n_html_subdirectory | 20 | number of sub-directories. ./tmp/0/file, ... ./tmp/19/file. It should be larger than 1|
| --n_latest_html_per_company | 10 | number of latest proxy statement (eagar search) |
| --period_begin | '2017-01-01' | begin of filling date |
| --period_end | '2018-01-01' | end of filling date |
| --debug | False | if you use --debug, then activate debug mode |


## Draw empty table

Row corresponds (company, date). Two columns are separated with tap.

### Scripts

Python 3 script

	python draw_table.py
	python draw_table.py --table_path MY_DIRECTORY/TABLE.TXT
	python draw_table.py --html_directory MY_HTMLDIRECTORY

Arguments

| argument | default value | description |
| --- | --- | --- |
| --html_directory | './tmp/' | directory for saving html |
| --table_path | './empty_table.txt' | table file path |
| --date_type | 'yy' | choices = [yy, yy-mm, yy-mm-dd] |
| --debug | False | nothing |
