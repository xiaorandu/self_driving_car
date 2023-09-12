# TensorFlow Lite Python object detection example with Raspberry Pi

## Lab 1B: Step 6: Object Detection

### Quick setup steps (bruffridge)

#### Prerequisites

`sudo raspi-config`    
Interface Options -> Enable legacy camera support    
Reboot Rasberry Pi

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install libatlas-base-dev

#installed this but might not have needed to
sudo apt-get install libv4l-dev

# for opencv 4.8.0 hardware optimized
wget https://github.com/prepkg/opencv-raspberrypi/releases/latest/download/opencv.deb
sudo apt install -y ./opencv.deb
rm -rf opencv.deb

# for opencv 4.8.0 hardware optimized
wget https://github.com/prepkg/opencv-raspberrypi/releases/latest/download/opencv.deb
sudo apt install -y ./opencv.deb
rm -rf opencv.deb

#The article claims these are required for opencv but I didn't need them.
sudo apt-get install gfortran
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libfontconfig1-dev libcairo2-dev
sudo apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt-get install libgtk2.0-dev libgtk-3-dev

sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install python3-dev
```

#### Running Object Detection sample

```
cd self_driving_car/lab1/object_detection
# The script install the required dependencies and download the TFLite models.
sh setup.sh
```

Run the example. If you have your Pi connected to a monitor in desktop mode it will open a window showing the camera with bounding boxes around detected objects:
```
python3 detect.py --model efficientdet_lite0.tflite
```

### Running Object Detection in headless mode

This mode is used for programmable smart car object detection. It won't display a window showing the camera feed and bounding boxes.
```
python3 detect_cli.py --model efficientdet_lite0.tflite
```

### Hardware acceleration

I get 6.7 FPS. It will likely be higher when running in headless mode without displaying the camera feed window and bounding boxes.
OpenCV hardware acceleration: https://pyimagesearch.com/2017/10/09/optimizing-opencv-on-the-raspberry-pi/
TensorFlow can be improved with Coral Edge TPU USB Accelerator: https://towardsdatascience.com/3-ways-to-install-tensorflow-2-on-raspberry-pi-fe1fa2da9104


## Original Documentation

This example uses [TensorFlow Lite](https://tensorflow.org/lite) with Python on
a Raspberry Pi to perform real-time object detection using images streamed from
the Pi Camera. It draws a bounding box around each detected object in the camera
preview (when the object score is above a given threshold).

At the end of this page, there are extra steps to accelerate the example using
the Coral USB Accelerator to increase inference speed.

## Set up your hardware

Before you begin, you need to
[set up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
with Raspberry Pi OS (preferably updated to Buster).

You also need to
[connect and configure the Pi Camera](https://www.raspberrypi.org/documentation/configuration/camera.md)
if you use the Pi Camera. This code also works with USB camera connect to the
Raspberry Pi.

And to see the results from the camera, you need a monitor connected to the
Raspberry Pi. It's okay if you're using SSH to access the Pi shell (you don't
need to use a keyboard connected to the Pi)—you only need a monitor attached to
the Pi to see the camera stream.

## Download the example files

First, clone this Git repo onto your Raspberry Pi like this:

```
git clone https://github.com/tensorflow/examples --depth 1
```

Then use our script to install a couple Python packages, and download the
EfficientDet-Lite model:

```
cd examples/lite/examples/object_detection/raspberry_pi

# The script install the required dependencies and download the TFLite models.
sh setup.sh
```

In this project, all you need from the TensorFlow Lite API is the `Interpreter`
class. So instead of installing the large `tensorflow` package, we're using the
much smaller `tflite_runtime` package. The setup scripts automatically install
the TensorFlow Lite runtime.

## Run the example

```
python3 detect.py \
  --model efficientdet_lite0.tflite
```

You should see the camera feed appear on the monitor attached to your Raspberry
Pi. Put some objects in front of the camera, like a coffee mug or keyboard, and
you'll see boxes drawn around those that the model recognizes, including the
label and score for each. It also prints the number of frames per second (FPS)
at the top-left corner of the screen. As the pipeline contains some processes
other than model inference, including visualizing the detection results, you can
expect a higher FPS if your inference pipeline runs in headless mode without
visualization.

For more information about executing inferences with TensorFlow Lite, read
[TensorFlow Lite inference](https://www.tensorflow.org/lite/guide/inference).

## Speed up model inference (optional)

If you want to significantly speed up the inference time, you can attach an
[Coral USB Accelerator](https://coral.withgoogle.com/products/accelerator)—a USB
accessory that adds the
[Edge TPU ML accelerator](https://coral.withgoogle.com/docs/edgetpu/faq/) to any
Linux-based system.

If you have a Coral USB Accelerator, you can run the sample with it enabled:

1.  First, be sure you have completed the
    [USB Accelerator setup instructions](https://coral.withgoogle.com/docs/accelerator/get-started/).

2.  Run the object detection script using the EdgeTPU TFLite model and enable
    the EdgeTPU option. Be noted that the EdgeTPU requires a specific TFLite
    model that is different from the one used above.

```
python3 detect.py \
  --enableEdgeTPU
  --model efficientdet_lite0_edgetpu.tflite
```

You should see significantly faster inference speeds.

For more information about creating and running TensorFlow Lite models with
Coral devices, read
[TensorFlow models on the Edge TPU](https://coral.withgoogle.com/docs/edgetpu/models-intro/).
