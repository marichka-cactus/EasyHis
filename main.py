# main EasyHis file for execution


from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import numpy as np
from scipy.stats import norm
from graphical_widgets import *


class MatplotlibWidget(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("EasyHis")
        self.ui.generate_his.clicked.connect(self.update_graph) # підключаємо функцію update_graph до сигналу натиснення кнопки
        self.addToolBar(NavigationToolbar(self.ui.MplWidget.canvas, self))
        self.ui.open_file.clicked.connect(self.import_data)
        self.ui.checkBox.clicked.connect(self.prepare_data)
        self.ui.generate_box_and_wisker.clicked.connect(self.box_and_wiskers)
        self.ui.save_figure.clicked.connect(self.save)
        self.isfileloaded = False




    def import_data(self):
        self.path = QFileDialog.getOpenFileName(self, "Open Data File", "", "CSV data files (*.csv)")
        filename = self.path[0]
        if filename:
            self.isfileloaded = True
            self.row_data = np.genfromtxt(filename, delimiter=',')
            self.my_data = self.row_data

    def data_upload_cheker(self):
        error = QMessageBox()
        error.setWindowTitle('Input data error')
        error.setText('The data file wasn\'t uploaded')
        error.exec_()


    def prepare_data(self):
        """
        remove outliers from the data using  IQR (Interquartile Range)
        """
        if not self.isfileloaded:
            self.data_upload_cheker()
        else:
            sorted_data = np.sort(self.my_data)
            Q1 = np.quantile(sorted_data, 0.25)
            Q3 = np.quantile(sorted_data, 0.75)
            IQR = Q3 - Q1
            low_lim = Q1 - 1.5 * IQR
            hig_lim = Q3 + 1.5 * IQR
            self.my_data = sorted_data[(sorted_data >= low_lim) & (sorted_data <= hig_lim)]




    def chekbox_cheker(self):
        if self.ui.checkBox.isChecked():
            self.prepare_data()
        else:
            self.my_data = self.row_data

    def tittle_text(self):
        """set tittle of the plot"""
        return self.ui.tittle_name.text()


    def y_axe_text(self):
        """set tittle of the Y axe"""
        return self.ui.y_axe.text()

    def x_axe_text(self):
        """set tittle of the X axe"""
        return self.ui.x_axe.text()


    def bin_number(self):
        """set bins number"""
        value = self.ui.spinBox.value()
        return value


    def update_graph(self):
        if not self.isfileloaded:
            self.data_upload_cheker()
        else:
            self.chekbox_cheker()
            tittle = self.tittle_text()
            y_label = self.y_axe_text()
            x_label = self.x_axe_text()

            self.ui.MplWidget.canvas.axes.clear()
            self.ui.MplWidget.canvas.axes.grid(True, c='lightgrey', alpha=0.5)


            mu, std = norm.fit(self.my_data)
            max = np.max(self.my_data)
            min = np.min(self.my_data)
            bins_number = self.bin_number()
            if bins_number == 0:
                bins_number = 10
            self.ui.MplWidget.canvas.axes.hist(self.my_data, bins_number, density=True, facecolor='blue', alpha=0.5)

            xmin = np.min(self.my_data) # визначення min значень на осі х
            xmax = np.max(self.my_data) # визначення max значень на осі х
            x = np.linspace(xmin, xmax, 100)  # возвращает одномерный массив из указанного количества элементов, значения которых равномерно распределенны внутри заданного интервала
            p = norm.pdf(x, mu, std)
            self.ui.MplWidget.canvas.axes.plot(x, p, 'k', linewidth=2)

            self.ui.MplWidget.canvas.axes.set_title(tittle + '\nmean = %.2f,  std = %.2f, min = %.2f, max = %.2f' % (mu, std, min, max), fontsize=12)
            self.ui.MplWidget.canvas.axes.set_xlabel(x_label, fontsize=12)
            self.ui.MplWidget.canvas.axes.set_ylabel(y_label, fontsize=12)

            self.ui.MplWidget.canvas.draw()

    def box_and_wiskers(self):
        if not self.isfileloaded:
            self.data_upload_cheker()
        else:
            self.chekbox_cheker()
            tittle = self.tittle_text()
            y_label = self.y_axe_text()
            x_label = self.x_axe_text()

            mu, std = norm.fit(self.my_data)
            max = np.max(self.my_data)
            min = np.min(self.my_data)

            self.ui.MplWidget.canvas.axes.clear()
            self.ui.MplWidget.canvas.axes.grid(True, c='lightgrey', alpha=0.5)
            self.ui.MplWidget.canvas.axes.set_title(tittle + '\nmean = %.2f,  std = %.2f, min = %.2f, max = %.2f' % (mu, std, min, max), fontsize=12)
            self.ui.MplWidget.canvas.axes.set_xlabel(x_label, fontsize=12)
            self.ui.MplWidget.canvas.axes.set_ylabel(y_label, fontsize=12)
            self.ui.MplWidget.canvas.axes.boxplot(self.my_data)
            self.ui.MplWidget.canvas.draw()

    def save(self):
        if not self.isfileloaded:
            self.data_upload_cheker()
        else:
            filepath = QFileDialog.getSaveFileName(self, 'Save Image', 'figure', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            self.ui.MplWidget.canvas.figure.savefig(filepath[0] + '.png')


if __name__ == '__main__':
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()