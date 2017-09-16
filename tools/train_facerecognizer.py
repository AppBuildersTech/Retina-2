#!/usr/bin/env python3

#######################################################################
# Copyright (C) 2016 Tyler Cromwell <tjc6185@gmail.com>
#
# This file is part of Cerebrum.
#
# Cerebrum is free software: you can redistribute it and/or modify
# it under Version 2 of the terms of the GNU General Public License
# as published by the Free Software Foundation.
#
# Cerebrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cerebrum.
# If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
#######################################################################

import getopt
import os
import sys

import numpy
from PIL import Image
import cv2

sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import opt
from modules import pathname
from modules import recognition


def print_usage():
    """
    Displays program usage information.
    """
    print('Usage:\t./train_facerecognizer.py --label=NAME')
    print('  --help\t\tPrints this text')
    print('  --label=NAME\t\tThe name of the person\'s face to recognize')
    exit(0)


def main():
    """
    Main function.
    """
    label = None

    try:
        short_opts = ['']
        long_opts = ['help', 'label=']
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError as error:
        print('Invalid argument: \"{}\"\n'.format(str(error)))
        print_usage()

    if len(opts) == 0:
        print_usage()

    for o, a in opts:
        if o == '--help':
            print_usage()
        elif o == '--label':
            label = opt.validate_training_dataset(a)

    if not label:
        print('\n  Label not specified!\n')
        print_usage()

    # Initialize variables
    recognizer_path = pathname.get_recognizer_file(label)
    recognizer = cv2.face.createLBPHFaceRecognizer()
    filename = label + '.lbph.xml'
    images = []

    # Get the absolute path of each image
    print('Collecting training images... ', end='')
    image_paths = pathname.get_training_images(label)
    print('DONE')

    # Add each of the persons images to the training set
    print('Preparing images and labels... ', end='')
    labels = [recognition.hash_label(label)] * len(image_paths)
    for path in image_paths:
        image_pil = Image.open(path)
        image = numpy.array(image_pil)
        (w, h) = image_pil.size
        images.append(image[0: h, 0: w])
    print('DONE')

    # Train
    print('Training recognizer... ', end='')
    recognizer.train(images, numpy.array(labels))
    print('DONE')

    # Save the newly trained recognizer
    print('Saving recognizer: {}...'.format(filename), end='')
    os.makedirs(pathname.get_recognizer_root(), exist_ok=True)
    recognizer.save(recognizer_path)
    print('DONE')


if __name__ == '__main__':
    """
    Program entry.
    """
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
