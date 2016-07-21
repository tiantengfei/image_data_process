import os
from random import shuffle
import sys
import image_process
import numpy as np


def write_test_image_to_file(from_dir, to_dir):
    image_data = image_process.get_images_data(from_dir)

    if not os.path.isdir(to_dir):
        os.mkdir(to_dir, 0755)
    shuffle(image_data)

    print('the number of image for test is {}'.format(len(image_data)))
    with open(os.path.join(to_dir, 'image_test.bin'), 'wb') as f:
        for label, im, _, _ in image_data:
            f.write(label)
            f.write(im)


def write_test_image_with_name(from_dir, to_dir, index):
    image_data = image_process.get_images_data(from_dir)

    if not os.path.isdir(to_dir):
        os.mkdir(to_dir, 0755)
    shuffle(image_data)

    print('the number of image for test is {}'.format(len(image_data)))
    with open(os.path.join(to_dir, 'image_test_%d.bin' % index), 'wb') as f:
        for label, im, image_name_1, image_name_2 in image_data:
            # print image_name_1, image_name_2
            f.write(label)
            f.write(image_name_1)
            f.write(image_name_2)
            f.write(im)


def generate_train_data(from_dir, to_dir, dir_num):
    dir_list = (os.listdir(from_dir))
    dir_list.sort()
    dir_list = dir_list[:dir_num]

    dir_list.sort()

    for i in range(len(dir_list)):
        write_test_image_with_name(os.path.join(from_dir, dir_list[i]), to_dir, i)

    print('dirs is {}.'.format(dir_list))


def read_test_image(fromdir):
    with open(fromdir, "rb") as f:

        while True:
            label = f.read(1)
            if label == '':
                break

            name_1 = f.read(4)
            name_2 = f.read(4)
            im = f.read(24576)
            im = np.fromstring(im, dtype=np.uint8).reshape(128, 64, 3)
            print('label is {}, name_1 is {}, name_2 is {}, shape is {}.'.format(label, name_1, name_2, im.shape))


def main(argv):
    if len(argv) < 3:
        print('You must input the from_dir and to_dir.')
        sys.exit(-1)
    # write_test_image_to_file(argv[1], argv[2])
    #write_test_image_with_name(argv[1], argv[2], int(argv[3]))
    generate_train_data(argv[1], argv[2], int(argv[3]))


if __name__ == '__main__':
    main(sys.argv)
    # read_test_image('/home/ttf/image_data_test/image_test.bin')

