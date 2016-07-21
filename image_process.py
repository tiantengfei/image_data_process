import os
from PIL import Image
import sys
import numpy as np
from random import shuffle


def get_files(from_dir, dir_name):
    """Get files under from_dir/dir_name"""
    dir_file_in = os.path.join(from_dir, dir_name)
    files = os.listdir(dir_file_in)

    return [os.path.join(dir_file_in, fi) for fi in files]


def write_image_file(from_dir, to_dir):
    """Write image data from from_dir to to_dir.

    Args:
        from_dir:directory where images are. Under from_dir, there may be more than one directory,
                 and each directory deposit a kind of images.
        to_dir: directory to which images data wil write
    """
    images_data = get_images_data(from_dir)

    if not os.path.isdir(to_dir):
        os.mkdir(to_dir, 0755)
    example_num_per_file = len(images_data) / 4 + 10

    shuffle(images_data)

    print('Total example for train is {}'.format(len(images_data)))
    files = []
    os.chdir(to_dir)

    files = [open('image_%s.bin' % i, 'wb') for i in range(1, 5)]
    for label, im, _, _ in images_data:
        files[count / example_num_per_file].write(label)
        files[count / example_num_per_file].write(im)
        count = count + 1
    for f in files:
        f.close()


def write_image_file_onefile(from_dir, to_dir, index):
    """Write image data from from_dir to to_dir.

    Args:
        from_dir:directory where images are. Under from_dir, there may be more than one directory
                 and each directory deposit a kind of images.
        to_dir: directory to which images data wil write
        index: the ascii sort order of this kind of image among the all kinds of images under from_dir.
    """
    images_data = get_images_data(from_dir)

    if not os.path.isdir(to_dir):
        os.mkdir(to_dir, 0755)

    shuffle(images_data)

    ls_name = from_dir.split('/')

    print('current: get image_data for {}. The bin file_name is {}.'.format(from_dir, ls_name[-1]))
    print('Total example for train is {}'.format(len(images_data)))
    # os.chdir(to_dir)
    path = os.path.join(to_dir, 'image_%d.bin' % index)
    with open(path, 'wb') as f:
        for label, im, _, _ in images_data:
            f.write(label)
            f.write(im)


def get_images_data(from_dir):
    """ get generated data for this kind of image under from_dir. There is at least a directory under the from_dir.

    Args:
        from_dir: this kind of images placed in this directory.

    """

    dirs = os.listdir(from_dir)
    dirs = sorted(dirs)
    dir_num = len(dirs)
    dir_files = [get_files(from_dir, dir_name) for dir_name in dirs]
    ims = []
    for i in range(dir_num):
        for im in dir_files[i]:
            # print('{} is a kind of {}.'.format(im, i + 1))
            ims.append((i, im, Image.open(im)))


            # ims = [(i, im, Image.open(im)) for i in range(dir_num) for im in dir_files[i]]

            # for im in ims:
            #   print('{} is a kind of {}.'.format(im[1], im[0]))

    data_list = [get_image_with_lable(ims[i], ims[j])
                 for i in range(len(ims)) for j in range(i + 1, len(ims))
                 if get_shape(ims[i][2]) == get_shape(ims[j][2])
                 ]
    return data_list


def get_image_with_lable(im1, im2):
    """generate a sample by im1 and im2. The label is zero if im1 and im2 are the same category or else one.

    Args:
        im1: the first image.
        im2: the second image.

    """
    category_1, name_1, image_1 = im1
    category_2, name_2, image_2 = im2

    #image_1 = image_1.resize((120, 120))
    #image_2 = image_2.resize((120, 120))

    #box = (10, 10, 110, 110)
    #image_1 = image_1.crop(box)
    #image_2 = image_2.crop(box)

    image1_data = image_1.resize((64, 64))
    image2_data = image_2.resize((64, 64))

    # print np.array(image1_data).shape, np.array(image2_data).shape
    m1 = np.transpose(np.array(image1_data), (1, 0, 2))
    m2 = np.transpose(np.array(image2_data), (1, 0, 2))

    # print m1.shape, m2.shape
    m3 = np.concatenate((m1, m2), axis=0)

    print m3.shape
    label = '0' if category_1 == category_2 else '1'

    if category_1 == category_2:
        print('{} and {} are the same category.'.format(name_1, name_2))
        print('the label is {}'.format(label))
    return label, m3.tostring(), name_1[-8:-4], name_2[-8:-4]


def get_shape(image):
    """ return the arg's shape.
    Args:
        image: the arg whose shape we want to know.

    Returns:
        the arg's shape.
    """
    image_1 = image.resize((64, 64))
    im1 = np.array(image_1)
    return im1.shape


def generate_train_data(from_dir, to_dir, dir_num):
    """generate data of original images and place the data in the directory of to_dir.

    """
    dir_list = (os.listdir(from_dir))
    dir_list.sort()
    dir_list = dir_list[:dir_num]

    dir_list.sort()

    for i in range(len(dir_list)):
        write_image_file_onefile(os.path.join(from_dir, dir_list[i]), to_dir, i)

    print('dirs is {}.'.format(dir_list))


def main(argv):
    """ get args from commandline.


      Args:
         argv[1]: directory that original images place.
         argv[2]: directory that images processed place.
         argv[3]: the numbers of directories in the directory of argv[1]

    """

    from_dir = argv[1]
    to_dir = argv[2]
    dir_num = int(argv[3])
    # write_image_file_onefile(from_dir, to_dir, index)
    # write_image_file_onefile(from_dir, to_dir, dir_num)
    generate_train_data(from_dir, to_dir, dir_num)


if __name__ == '__main__':
    main(sys.argv)
