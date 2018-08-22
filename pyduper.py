import collections
import hashlib
import os
import pathlib
import sqlite3
import subprocess


HASH_COMMAND = 'sha1sum'
HASH_ALGORITHM = hashlib.sha1


_FileInfo = collections.namedtuple('_FileInfo', ['path', 'name', 'hash', 'size'])


class FileInfo(_FileInfo):
    pass


def get_fileinfos(folder):
    path_to_fileinfo = dict()
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        dir_files = []
        for filename in filenames:
            file_path = pathlib.Path(dirpath, filename)
            hash = subprocess.check_output(['sha1sum', str(file_path)]).split()[0].decode('utf-8')
            size = file_path.stat().st_size
            fileinfo = FileInfo(path=file_path, name=file_path.name, hash=hash, size=size)
            dir_files.append(fileinfo)
            path_to_fileinfo[file_path] = fileinfo
            yield fileinfo
        for dirname in dirnames:
            dir_files.append(path_to_fileinfo[pathlib.Path(dirpath, dirname)])
        sorted_dir_files = sorted(dir_files, key=lambda fi: fi.name)
        size = 0
        hash = HASH_ALGORITHM()
        for dir_file in sorted_dir_files:
            size += dir_file.size
            hash.update(dir_file.hash.encode('utf-8'))
        dirpath_path = pathlib.Path(dirpath)
        dir_fileinfo = FileInfo(path=dirpath_path, name=dirpath_path.name, hash=hash.hexdigest(), size=size)
        path_to_fileinfo[pathlib.Path(dirpath)] = dir_fileinfo
        yield dir_fileinfo


def build_database(folder, sqlite, tag):
    connection = sqlite3.connect(sqlite)
    cursor = connection.cursor()
    cursor.execute("""create table if not exists fileinfos(tag, path, name, hash, size)""")
    for fileinfo in get_fileinfos(folder):
        cursor.execute("""insert into fileinfos(tag, path, name, hash, size) values (?, ?, ?, ?, ?)""", (tag, str(fileinfo.path), fileinfo.name, fileinfo.hash, fileinfo.size))
    connection.commit()
    connection.close()
