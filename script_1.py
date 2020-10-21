import os
import datetime
import hashlib
import shutil
import sqlite3

ROOT_DIR = '.'
SITE_DIR = './site'
BCAKUP_DIR = './backup_dir'

def get_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()

def get_info():
    all_paths = []
    for root, dirs, files in os.walk(SITE_DIR):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            mtime = os.path.getatime(file_path)
            last_modified_date = datetime.datetime.fromtimestamp(mtime).replace(microsecond=0)
            md5_sum = get_md5(file_path)

            now = datetime.datetime.now()

            all_paths.append([file_name, md5_sum, file_path, last_modified_date, now])
    return all_paths

def write_db(data):

    try:
        conn = sqlite3.connect('db_dirs.db')
        c = conn.cursor()
        c.execute('insert into dirs(name, md5, backup_name, edit_datetime, backup_datetime) '
                  'values (?,?,?,?,?)', data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def back_up(file_path):
    print(file_path)

    date = str(datetime.datetime.now())[:16].replace(' ', '_')
    CURRENT_DIR = os.path.join(BCAKUP_DIR, date)
    os.makedirs(CURRENT_DIR, exist_ok=True)

    directory_tree = ('/').join( file_path.split(os.sep)[2:-1] )
    os.makedirs(os.path.join(CURRENT_DIR, directory_tree), exist_ok=True)
    destanation = os.path.join(CURRENT_DIR, directory_tree)
    shutil.copy(file_path, destanation)

class Main:
    for row in get_info():
        back_up(row[2])
        write_db(row)

if __name__ == '__main__':
    Main()

# files = [f for f in os.listdir('.') if os.path.isfile(f)]
# print((len(path) - 1) * '---', os.path.basename(root))
# path = root.split(os.sep)
# name = file_path.split(os.sep)[-1]
