import os
import re

import sys


def rename_images(directory):
    """Rename files' name to num.extension in  the directory.

    Recommendation: it is better to use absolute path for  the directoy.

    Args:
        directory: directory where files are.
    """

    if not os.path.isdir(directory):
        print('{} is not exists.'.format(directory))
        sys.exit(-1)
    files = os.listdir(directory)
    num = 1
    os.chdir(directory)
    print('current work directory is {}'.format(os.getcwd()))
    for file in files:
        nnum_for_file_name = str(num) if num > 9 else '0' + str(num)
        os.rename(file, nnum_for_file_name + '.' + re.split('\.', file)[-1])
        print('befor change is {}, after is {}'.format(file, nnum_for_file_name + '.' + re.split('\.', file)[-1]))
        num += 1
    print('The number of files name changed is {}'.format(num) )


def rename_batch_dirs(directory):
    dirs = [os.path.join(directory, dir_name) for dir_name in os.listdir(directory)]

    for dir_name in dirs:
        rename_images(dir_name)


def main(argv):
    if len(argv) < 1:
        print('please add a argument for the directory in which the file name will be modified!')
        sys.exit(-1)
    directory = sys.argv[1]
    rename_batch_dirs(directory=directory)


if __name__ == '__main__':
    main(sys.argv)
