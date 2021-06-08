from datetime import datetime
from ftplib import FTP
import os
import time
import os.path
from os import path

ftpHost = ""
ftpUser = ""
ftpPassword = ""

HOST = ''
PORT = '3306'
DB_USER = ''
DB_PASS = ''
database_name = ''


def get_dump(database):
    filestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    pathname = 'backups/' + time.strftime('%Y-%m-%d')
    print(pathname)
    # C:/xampp/mysql/bin/mysqldump for xampp windows
    filename = database + "_" + filestamp

    if not path.exists('backups'):
        os.mkdir('backups')

    if not path.exists(pathname):
        os.mkdir(pathname)

    os.popen("mysqldump --single-transaction -h %s -P %s -u %s -p%s %s > %s.sql" % (
        HOST, PORT, DB_USER, DB_PASS, database, pathname + '/' + database + "_" + filestamp))

    print("\n|| Database dumped to " + pathname + '/' + filename + ".sql || ")
    time.sleep(5)
    while 1:
        if path.exists(pathname + '/' + filename + '.sql'):
            with open(pathname + '/' + filename + '.sql') as myfile:
                if 'Dump completed' in myfile.read():
                    print('Jest!')
                    break
                else:
                    print('Nie ma :(')
                    time.sleep(3)

    print(pathname + '/' + filename + '.sql')
    save_to_ftp(pathname, filename + '.sql')


def save_to_ftp(path, file_name):
    with FTP(ftpHost) as ftp:

        ftp.login(user=ftpUser, passwd=ftpPassword)
        print(ftp.getwelcome())

        ftp.cwd('/htdocs/')
        if not 'sql' in ftp.nlst():
            ftp.mkd('sql')

        with open(path + '/' + file_name, 'rb') as f:
            ftp.cwd('/htdocs/sql/')
            new_dir = str(datetime.now().date())
            if str(new_dir) not in ftp.nlst():
                ftp.mkd(str(new_dir))

            ftp.storbinary('STOR ' + str(new_dir) + '/' + file_name, f)

        ftp.quit()

        print('Backup done!')


if __name__ == "__main__":
    while 1:
        get_dump(str(database_name))
        time.sleep(3600)
