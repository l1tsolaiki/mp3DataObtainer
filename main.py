import os
import mutagen

import write_tags
from constants import *


def process(filename, move=True):
    write_tags.clearGarbageTags(filename)
    write_tags.addTags(filename)
    if move:
        os.rename(SOURCE + filename, DESTINATION + filename)


def main():
    if input('Warning! You are going to change and possibly move files\n{} ---> {}. \n====Are you sure==== (y/n)? '
                     .format(SOURCE, DESTINATION)) != 'y':
        return 0

    for filename in os.listdir(SOURCE):
        try:
            # todo move handling of this exception to clearGarbageTags by adding headers manually in that func

            print("Processing", filename)
            process(filename)
        except mutagen.id3._util.ID3NoHeaderError:
            print("Error at", filename)


if __name__ == '__main__':
    main()
