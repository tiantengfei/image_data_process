import image_word2vec_process
import sys
import os

def main(argv):
    model = image_word2vec_process.load_pre_train_word2vec()
    desc_data = image_word2vec_process.load_desc_files(argv[2])

    for d in os.listdir(argv[1]):
        image_word2vec_process.get_files(os.path.join(argv[1], d), model, desc_data, d)

if __name__ == '__main__':
    main(sys.argv)