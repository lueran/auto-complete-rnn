import shutil
import zipfile

import io

import just
import os

import re
import requests

repos = {"https://github.com/HoraApps/LeafPic/archive/dev.zip",
         'https://github.com/TeamAmaze/AmazeFileManager/archive/master.zip',
         "https://github.com/dkim0419/SoundRecorder/archive/master.zip",
         "https://github.com/javiersantos/MLManager/archive/master.zip",
         "https://github.com/afollestad/photo-affix/archive/master.zip",
         "https://github.com/esoxjem/MovieGuide/archive/master.zip",
         "https://github.com/1hakr/AnExplorer/archive/master.zip",
         "https://github.com/avjinder/Minimal-Todo/archive/master.zip"
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
            dest = 'data-java/%s/' % dir
            if not os.path.exists(dest):
                os.makedirs(dest)
            shutil.copy(os.path.join(dir, file), 'data-java/%s/%s.txt' % (dir, file.replace('.java', '')))
        else:
            os.remove(os.path.join(dir, file))


def get_data():
    files = list()
    post_data_dir = "data-java-post"
    if os.path.exists(post_data_dir):
        shutil.rmtree(post_data_dir)
        os.mkdir(post_data_dir)
    else:
        os.mkdir(post_data_dir)
    for i, file in enumerate(list(just.multi_read("data-java/**/*.txt").values())):
        new_file = os.path.join(post_data_dir, "j%s.txt" % i)
        new_line = ''
        with open(new_file, 'w') as post:
            for line in file.split('\n'):
                if line.strip().startswith('@') or \
                        line.strip().startswith('/') or \
                        line.strip().startswith('import') or \
                        line.strip().startswith('package') or \
                        line.strip().startswith('*'):
                    line = line.replace(line, '')
                line = re.sub(r'(class) (\S+)', r'\1 ^C^', line)
                line = re.sub(r"if.?\(([a-zA-Z\.\(\)\!0-9]+).[\)|=|<|>|!|&|\|]?", 'if (^E^ ', line)
                line = re.sub(r"(static final int) ([A-Z0-9_]+)", r"\1 ^P^", line)
                line = re.sub(r"(static final String) ([A-Z0-9_]+)", r"\1 ^P^", line)

                # if m is not None:
                #     print(m.group(1))
                new_line += line + '\n'
            post.write(re.sub(r'\n\s*\n', '\n', new_line))


download_repos()
parse_data('data-android')
get_data()
# print(len(data))
