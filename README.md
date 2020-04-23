## Mesh Viewer using pytorch3D

This code is implemented using Pytorch3D and PyQt5



### Installation

The code uses **Python 3.7** in **Ubuntu 18.04 LTS**

[Pytorch3D](https://github.com/facebookresearch/pytorch3d)

You can install Pytorch3D in upper link.

To install

~~~
git clone https://github.com/yeongjoonJu/Mesh-Viewer-using-pytorch3d.git
cd Mesh-Viewer-using-pytorch3d
mkdir data
pip install pyqt5
pip install pillow
~~~



### Run

~~~
python main.py
~~~

Rotate an object : dragging the mouse

Zoom in / out an object : wheeling the mouse 

Change the illumination position :<br>**W -  move to up, A - move to left, S - move to down, D - move to right**<br>
**Q - move to front, E - move to back**

### Examples

You can open .obj file after pressing file button.

![screenshot1](./example/screenshot1.png)

![](./example/screenshot2.png)

**Rotation**

You can rotate object through dragging mouse.

![](./example/screenshot3.png)

**Zoom in/out**

You can zoom in/out through wheeling.

![](./example/screenshot4.png)

**Change the illumination**

You can change the illumination using the keyboard.

![](./example/screenshot5.png)