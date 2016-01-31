#!/usr/bin/python3

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  Copyright (C) 2016 Tyler Cromwell <tyler@csh.rit.edu>

  This file is part of Cerebrum.

  Cerebrum is free software: you can redistribute it and/or modify
  it under Version 2 of the terms of the GNU General Public License
  as published by the Free Software Foundation.

  Cerebrum is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Cerebrum.
  If not, see <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

print('Importing libraries...')

""" Python libraries """
import configparser
import re
import readline
import sys
import time

""" OpenCV library """
import cv2

""" Readline settings """
readline.parse_and_bind('tab: complete')

""" Global constants """
CAMERA_DEFAULT = 0

""" Global variables """
config = None


"""
Searches for faces in the given frame.
"""
def detectFaces(frame, scaleFactor, minNeighbors, minSize, maxSize):
    faceCascade = cv2.CascadeClassifier(sys.argv[2])
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        grayscale,
        scaleFactor = scaleFactor,
        minNeighbors = minNeighbors,
        flags = 0,
        minSize = tuple(map(int, minSize)),
        maxSize = tuple(map(int, maxSize))
    )

    if len(faces) > 1:
        print(len(faces), 'faces found')

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Face', (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        print('Face of size (%dx%d) found at (%d, %d)' % (w, h, x, y))

    return faces


"""
Main "function".
"""
if __name__ == '__main__':
    flags = 0
    windowName = 'Camera %d' % (CAMERA_DEFAULT)

    """ Parse face detection options """
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    scaleFactor = float(config.get('Faces', 'scaleFactor'))
    minNeighbors = int(config.get('Faces', 'minNeighbors'))
    minSize = re.split('\s*,\s*', config.get('Faces', 'minSize'))
    maxSize = re.split('\s*,\s*', config.get('Faces', 'maxSize'))

    """ """
    camera = cv2.VideoCapture(CAMERA_DEFAULT)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(config.get('Faces', 'width')))
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(config.get('Faces', 'height')))

    print('Capture Resolution: %dx%d' %
        (camera.get(cv2.CAP_PROP_FRAME_WIDTH), camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )

    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    
    if not camera.isOpened():
        camera.open(CAMERA_DEFAULT)

    while True:
        start = time.time()
        retval, frame = camera.read()

        """ Check flags """
        if flags & 1:
            detectFaces(frame, scaleFactor, minNeighbors, minSize, maxSize)

        end = time.time()
        fps = 1 // (end - start)

        cv2.putText(frame, 'FPS: %d' % (fps), (0, 12), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv2.imshow(windowName, frame)

        key = cv2.waitKey(1)

        """ Determine action """
        if key == 27:
            cv2.destroyWindow(windowName)
            cv2.waitKey(1); cv2.waitKey(1);
            cv2.waitKey(1); cv2.waitKey(1);
            camera.release()
            break
        elif key == ord('f'):
            flags = flags ^ 1
