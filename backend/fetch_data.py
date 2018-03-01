import shutil
import zipfile

import io

import just
import os

import re
import requests

repos = {"https://github.com/HoraApps/LeafPic/archive/dev.zip",
         'https://github.com/SimpleMobileTools/Simple-Calendar/archive/master.zip',
         'https://github.com/TeamAmaze/AmazeFileManager/archive/master.zip',
         }


def download_repos():
    for repo in repos:
        print('Download repo - ' + repo)
        r = requests.get(repo)
        print('Zipping response')
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print('Extract file')
        z.extractall('data-android/')


def parse_data(dir):
    for file in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, file)):
            parse_data(os.path.join(dir, file))
        elif file.endswith(".java"):
            shutil.copy(os.path.join(dir, file), 'data-java/%s.txt' % file.replace('.java', ''))
        else:
            os.remove(os.path.join(dir, file))


def get_data():
    files = list()
    for file in list(just.multi_read("data-java/**/*.txt").values()):
        new_file = ''
        for line in file.split('\n'):
            if line.strip().startswith('@') or \
                    line.strip().startswith('/') or \
                    line.strip().startswith('import') or \
                    line.strip().startswith('package') or \
                    line.strip().startswith('*'):
                line = line.replace(line, '')
            new_file += line + '\n'
        files.append(re.sub(r'\n\s*\n', '\n', new_file))
    return files


parse_data('data-android')
data = get_data()
print(len(data))