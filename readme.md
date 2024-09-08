# Data Scraping Project

## Introduction
Hi there! thank you for taking your time to look at my work.
This project is written to display data scraping ideas from different
kind of websites/ sources. I will be using pdm to install my requirements 
as opposed to common pip.

### Bitcoin rate
Our script uses simple requests module to get bitcoin rate in USD
in UTC time. the data is then stored in local influx db which is
optimal to save time series data.

### Entsoe transparency data
We are using paramiko to create a sftp client to entsoe
to get intraday capacity data from sftp server. we are using sqlite3
to store the data into the database.