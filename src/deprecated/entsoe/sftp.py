import paramiko
import os
import tempfile
import csv
import io
import logging

logger = logging.getLogger()

CONFIG = {
    'host': 'sftp-transparency.entsoe.eu',
    'username': os.environ.get('sftp_username'),
    'password': os.environ.get('sftp_password'),
    'directory': '/TP_export_2/2016/10/5/OfferedIntradayTransferCapacityImplicit/BZN|NL',
    'local_path': os.environ.get('local_path')
}

def run():
    """
    1. Creates  a connection to public rebex server.
    2. Lists all the files in the server
    3. gets data from a file
    :return: file data
    """
    sftp = connect_to_client()
    change_directory(sftp, CONFIG['directory'])

    # list all csv files
    file_list = get_file_list(sftp) # returns ['20161005_BZN|NL-BZN|BE.csv'] at the time of writing :)
    # get data for one file
    file = file_list[0]

    file_data = get_file_data(file,sftp)
    file_data = read_csv_data(file_data)
    sftp.close()
    return file_data

def connect_to_client():
    """
    Takes in hostname, username & password
    to connect to the client
    :return: SFTP client session object
    """
    client = paramiko.SSHClient()
    # to be used only for development. For Production get host keys from client
    client.set_missing_host_key_policy(policy=paramiko.client.AutoAddPolicy)
    client.connect(
        hostname=CONFIG['host'],
        username=CONFIG['username'],
        password=CONFIG['password']
    )
    logger.info('Connected to sftp')
    return client.open_sftp()

def change_directory(sftp, directory: str):
    """
    change directory to input directory
    :param sftp: SFTP object
    :param directory: String
    :return: None
    """
    sftp.chdir(directory)
    logger.info(f'Current working directory: {directory}')

def list_directories(sftp):
    """
    List all directories there is
    :param sftp: SFTP object
    :return: list of strings [String]
    """
    return sftp.listdir()


def get_file_list(sftp):
    """
    Find all files that are csv files
    :param sftp: SFTP object
    :return: list of file names List[String]
    """
    return [i.filename for i in sftp.listdir_attr() if '.csv' in i.filename.lower()]  # returns list of files

def read_csv_data(file_data):
    """
    Reads csv data and stores in a dictionary
    :param file_data: bytes object
    :return: list of dictionaries
    """
    reader = csv.reader(io.StringIO(file_data),delimiter='\t')
    columns = "DateTime	ResolutionCode	AllocationId	AllocationModeCode	UpdateDateTime	CapacityProductCode	OutAreaCode	OutAreaTypeCode	OutAreaName	InAreaCode	InAreaTypeCode	InAreaName	Capacity	UpdateTime".split('\t')
    next(reader)
    li = []
    for row in reader:
        dic = {}
        for i in range(len(row)):
            dic[columns[i]] = row[i]
        li.append(dic)
    return li

def get_file_data(file,sftp):
    """
    Reads data from the sftp and
    saves to a temporary file
    :param file: file name [String]
    :param sftp: SFTP object
    :return:
    """
    with tempfile.NamedTemporaryFile('wb', delete=False) as temp:
        sftp.getfo(file, temp)
    with open(temp.name, encoding='utf-8') as f:
        filedata = f.read()
    return filedata

if __name__ == '__main__':
    run()