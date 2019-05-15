from glob import glob
from os.path import join


class DirectoryIterator:
    def __init__(self, directory_filepath):
        self.__filenames = glob(join(directory_filepath, '*'))
        self.__total_files = len(self.__filenames)
        self.__current_index = 0

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        return self.next()

    def next(self):
        if len(self.__filenames) == 0:
            return None

        current_index = self.__current_index
        self.__current_index = (self.__current_index + 1) % self.__total_files

        return self.__filenames[current_index]
