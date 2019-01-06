# ListFetcher

ListFetcher is designed to get the programs list for different Radio station
(currently supported: [radiko](http://radiko.jp/)). ListFetcher supports various
features including:

* Get a full programs schedule

    `$python main.py {STATION_NAME} [--keyword YOUR_KEYWORD] [--output True] [--save YOUR_PATH]`

* Only Search for the keyword through all programs and highlight related programs in the schedule.

    `$python main.py {STATION_NAME} --keyword YOUR_KEYWORD --output False [--save YOUR_PATH]`

* Search for the keyword through all programs with highlights and pick out the related programs and show up all details for those programs on the second sheet.

    `$python main.py {STATION_NAME} --keyword YOUR_KEYWORD [--output True] [--save YOUR_PATH]`

** Note: `{}` indicates this argument is mandatory, `[]` indicates the argument is optional. The default save path is `.\output\STATION_NAME_DATE`

## Reuqired

* Python 3.4 or above

* [Pandas](https://pandas.pydata.org/) 0.20.3 or above

    `pip install pandas`

* [argParser](https://docs.python.org/3/library/argparse.html)

    `pip install argparser`

* [pathLib](https://docs.python.org/3/library/pathlib.html)

    `pip pathlib`

* [xmltodict](https://pypi.org/project/xmltodict/)

    `pip install xmltodict`

* [requests](http://docs.python-requests.org/en/master/)

    `pip install requests`

---

## To Be Developed

* Keyword Machine Learning develop

* User Interface

* Server for keyword mapping

* More Radio stations
