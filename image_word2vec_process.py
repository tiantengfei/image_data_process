import os
import sys
from PIL import Image
from random import shuffle

import gensim
import numpy as np
import tensorflow as tf


class Image_with_desc:
    pass


def load_pre_train_word2vec(model_location='/home/ttf/applications/GoogleNews-vectors-negative300.bin'):
    print('loading the pretrained model. It will takes a few minutes')
    model = gensim.models.Word2Vec.load_word2vec_format(model_location, binary=True)
    print('successfully load the model! \n start to generate training set.')

    return model


def get_files(dir, model, desc_data, filename):
    """ get all data from dir which consists all kind of images that will be used. The description of image
       wiil be read from the json file for the kind of image.


       Args:
           dir: directory that all kind of images places.

     Returns:
         all data of images in the directory.

    """


    dirs = os.listdir(dir)
    image_data = []
    count = 0
    for d in dirs:
        image_files = get_files_for_one_category(os.path.join(dir, d))
        # with open(os.path.join(json_dir, d + '.json')) as f:
        #     json_data = json.load(f)

        for image in image_files:
            if desc_data.has_key(image.number):
                image.desc, image.desc_list = get_image_desc(desc_data, image.number)
                desc_vector = np.zeros((300,), dtype=np.float32)
                for s in image.desc_list:
                    if model.__contains__(s):
                        desc_vector += model[s]
                image.desc_vector = desc_vector
                image_data.append(image)
                count += 1

    shuffle(image_data)
    # write_image_data_to_file(image_data)
    conver_to(image_data, filename)
    print('total number of images is %d .' % count)


def get_image_desc(desc_data, image_number):
    """ get description for the image whose number is image_number.

    Args:
        desc_data: a dictionary that includes the number of image and the corresponding desc.
        image_number: the number of the image.

    Returns:
        image_desc: the description for the image.
        image_number: the number of the image.
    """

    image_desc = desc_data[image_number]
    image_desc_list = (image_desc[:-1]).strip().split(' ')

    return image_desc, image_desc_list


def get_image_desc_for_json(jsondata, image_name):
    """ get image description from jsondata according to image_name.

        Args:
            jsondata: json file that image descriptions are saved.
            image_name: the SHA-1 file name.

        Returns:
            image description for given image name.
    """
    raw_desc = [image_desc['title'] for image_desc in jsondata if
                image_desc['images'][0]['path'] == 'full/' + image_name]
    # print(raw_desc)
    desc_list = raw_desc[0].split('-')
    desc = ' '.join(s for s in desc_list if s != '')

    return desc, desc_list


def get_files_for_one_category(dir):
    """ get data for a kind of image. The data don't include the description about the image.

        Args:
            dir:directory that a kind of images place.
        Returns:
             only data about images, not the description.

    """
    dirs = os.listdir(dir)
    image_in_dir = []
    for d in dirs:
        files = os.listdir(os.path.join(dir, d))
        for f in files:
            image = Image_with_desc()
            image.data = Image.open(os.path.join(dir, d + '/' + f)).resize((64, 64))
            image.number = f[:-4]
            if np.array(image.data).shape == (64, 64, 3):
                image_in_dir.append(image)
            else:
                print("image number is {}. And shape is {}.".format(image.number, np.array(image.data).shape))
            # print(image.name)

    return image_in_dir


def write_image_data_to_file(image_data):
    """ write images' data to disk.

    Args:
        image_data: images' data will be writed to disk.

    """
    if not os.path.isdir('train_set'):
        os.mkdir('train_set', 0755)
    with open('train_set/image_data.bin', 'wb') as f:
        for image in image_data:
            f.write((image.desc_vector).tostring())
            f.write((image.data).tostring())


def test():
    with open('train_set/image_data.bin', 'rb') as f:
        image_size = 64 * 64 * 3
        count = 1
        while True:
            image_vector = f.read(300 * 4)
            if image_vector == '':
                break
            image_data = f.read(image_size)
            im_data = np.fromstring(image_data, dtype=np.uint8).reshape(64, 64, 3)
            im_vector = np.fromstring(image_vector, dtype=np.float32).reshape(300)
            count += 1
            print(im_data.shape)
            print(im_vector.shape)


def conver_to(image_data, save_file_name='image_0'):

    file_name = os.path.join('train_set', save_file_name + '.tfrecords')
    writer = tf.python_io.TFRecordWriter(file_name)

    for image in image_data:
        # print("label shape is {}. image shape is {}.".format(np.array((image.desc_vector)).shape,
        #                                                      np.array((image.data)).shape))
        image_raw = (image.data).tostring()
        label_raw = (image.desc_vector).tostring()
        example = tf.train.Example(features=tf.train.Features(feature={
            'label': _bytes_feature(label_raw),
            'image_raw': _bytes_feature(image_raw)}))

        writer.write(example.SerializeToString())

    writer.close()


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def load_desc_files(desc_file):
    print('loading desc file.....')
    image_desc = {}
    with open(desc_file, 'r') as f:
        for line in f:
            image_num, desc = line.split('\t')
            image_desc[image_num] = desc

    print('successfully load desc data!')
    return image_desc


def main(argv):
    dir = argv[1]
    json_dir = argv[2]
    model = load_pre_train_word2vec()
    desc_data = load_desc_files("/home/ttf/Desktop/product_info.txt")

    get_files(dir, model, desc_data)
    # test()


if __name__ == '__main__':
    main(sys.argv)
