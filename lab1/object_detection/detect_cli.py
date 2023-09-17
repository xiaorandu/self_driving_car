# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main script to run the object detection routine."""
import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils


def run(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:
  """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    camera_id: The camera id to be passed to OpenCV.
    width: The width of the frame captured from the camera.
    height: The height of the frame captured from the camera.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """

  # Variables to calculate FPS
  counter, fps = 0, 0
  start_time = time.time()
  fps_avg_frame_count = 10

  # Start capturing video input from the camera cv2.CAP_GSTREAMER
  cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2, (cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY))
  #print(cv2.getBuildInformation())
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
  #print(cv2.getBuildInformation())

  # Initialize the object detection model
  base_options = core.BaseOptions(
    file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
  detection_options = processor.DetectionOptions(
    max_results=3, score_threshold=0.3)
  options = vision.ObjectDetectorOptions(
    base_options=base_options, detection_options=detection_options)
  detector = vision.ObjectDetector.create_from_options(options)

  # Continuously capture images from the camera and run inference
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      sys.exit(
        'ERROR: Unable to read from webcam. Please verify your webcam settings.'
      )

    counter += 1
    image = cv2.flip(image, -1) # -1 flips the image horizontally and vertically. 1 flips horizontally. 0 flips vertically.

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)

    # Calculate the FPS
    if counter % fps_avg_frame_count == 0:
      end_time = time.time()
      fps = fps_avg_frame_count / (end_time - start_time)
      start_time = time.time()

    # Show the FPS
    fps_text = 'FPS = {:.1f}'.format(fps)
    print(fps_text)

    # Detect specific objects
    for detection in detection_result.detections:
      category = detection.categories[0]
      category_name = category.category_name

      # PERSON
      if category.index == 0 and category.score > .75:
        # stop until person is no longer detected
        print('Car detects a person.')

      # TRAFFIC LIGHT
      if category.index == 9 and category.score > .75:
        pass

      # STOP SIGN
      if category.index == 12 and category.score > .75:
        #sees a stop sign. 
        print('Car detects a stop sign.')
        # stop for N seconds before continuing.

  cap.release()


def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
    '--model',
    help='Path of the object detection model.',
    required=False,
    default='efficientdet_lite0.tflite') # lite-model_efficientdet_lite0_detection_metadata_1.tflite
  parser.add_argument(
    '--cameraId', help='Id of camera.', required=False, type=int, default=0)
  parser.add_argument(
    '--frameWidth',
    help='Width of frame to capture from camera.',
    required=False,
    type=int,
    default=640)
  parser.add_argument(
    '--frameHeight',
    help='Height of frame to capture from camera.',
    required=False,
    type=int,
    default=480)
  parser.add_argument(
    '--numThreads',
    help='Number of CPU threads to run the model.',
    required=False,
    type=int,
    default=4)
  parser.add_argument(
    '--enableEdgeTPU',
    help='Whether to run the model on EdgeTPU.',
    action='store_true',
    required=False,
    default=False)
  args = parser.parse_args()

  run(args.model, int(args.cameraId), args.frameWidth, args.frameHeight,
    int(args.numThreads), bool(args.enableEdgeTPU))

if __name__ == '__main__':
  main()