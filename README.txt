EasyHis is the final course project accomplished by Marichka Zlatohurska within the Python for Beginners course
from Beetroot Academy.
It resolves the author's daily routine tasks (statistic processing and data visualisation).

EasyHis is designed with using Python 3.8 on Ubuntu platform.
The PyQt5, matplotlib, numpy, scipy libraries are needed to be installed inside a working environment.
The program itself consists of three files that should be placed in the same directory:
- main.py - the main file for execution;
- graphical_widgets.py - the class for graphical widgets;
- mplwidget.py - the class for plot widget.

The following software packages are required to be installed on your computer:
Ubuntu (version >= 20.04)
Python (version >= 3.8)
PyQt5 (version >=5.15.2)
matplotlib (version >=3.3.4)
numpy (version >=1.20.0)
scipy (version >=1.6.0)

EasyHis takes a CSV format file as an input. The data should be arranged in single column without heading.
Outliers are eliminated from the data set using Inter Quartile Range method (https://kanoki.org/2020/04/23/how-to-remove-outliers-in-python/).
There are two options for data visualisation: the frequency distribution histogram and the box whiskers plot.
In the case of histogram the number of bins is 10 by default, but this parameter can be customized.
The output is the image in PNG format.

Save your time and enjoy using EasyHis.


