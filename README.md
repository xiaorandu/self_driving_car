## PiCar-4WD 

### Lab 1B: Step 6: Object Detection

For more information about the code this was derived from: https://github.com/tensorflow/examples/blob/master/lite/examples/object_detection/raspberry_pi/README.md

#### Prerequisites

`sudo raspi-config`
Interface Options -> Enable legacy camera support
Reboot Rasberry Pi

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install libatlas-base-dev

#installed but might not have needed to
sudo apt-get install libv4l-dev

#haven't installed these yet. The article claims they are required for opencv.
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

### Running Object Detection sample

```
cd self_driving_car/lab1/object_detection
# The script install the required dependencies and download the TFLite models.
sh setup.sh
```

Run the example. If you have your Pi connected to a monitor in desktop mode it will open a window showing the camera with bounding boxes around detected objects:
```
python3 detect.py --model efficientdet_lite0.tflite
```

PiCar-4WD 

Quick Links:

 * [About PiCar-4WD](#about_this_module)
 * [Update](#update)
 * [About SunFounder](#about_sunfounder)
 * [License](#license)
 * [Contact us](#contact_us)

<a id="about_this_module"></a>
### About PiCar-4WD:



<a id="update"></a>
### Update:
 - picar-4wd is the 4WD car that is built based on the Raspberry Pi, with the functions, including line following, following, obstacle avoidance, speed testing,  remote control, radar testing and use the web page to control the picar-4wd
2019-09-21:
 - New Release

----------------------------------------------
<a id="about_sunfounder"></a>
### About SunFounder
SunFounder is a technology company focused on Raspberry Pi and Arduino open source community development. Committed to the promotion of open source culture, we strives to bring the fun of electronics making to people all around the world and enable everyone to be a maker. Our products include learning kits, development boards, robots, sensor modules and development tools. In addition to high quality products, SunFounder also offers video tutorials to help you make your own project. If you have interest in open source or making something cool, welcome to join us!

----------------------------------------------
<a id="license"></a>
### License
This is the code for PiCar-4WD.
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied wa rranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

PiCar-4WD comes with ABSOLUTELY NO WARRANTY; for details run ./show w. This is free software, and you are welcome to redistribute it under certain conditions; run ./show c for details.

SunFounder, Inc., hereby disclaims all copyright interest in the program 'PiCar-4WD' (which makes passes at compilers).

Mike Huang, 21 August 2015

Mike Huang, Chief Executive Officer

Email: service@sunfounder.com, support@sunfounder.com

----------------------------------------------
<a id="contact_us"></a>
### Contact us:
website:
	www.sunfounder.com

E-mail:
	service@sunfounder.com, support@sunfounder.com