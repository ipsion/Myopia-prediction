import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QListWidget, QVBoxLayout,
                             QWidget, QSplitter, QGraphicsView, QGraphicsScene,
                             QFileDialog, QApplication, QListWidgetItem, QGraphicsPixmapItem)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot
import pydicom



def load_dicom_as_pixmap(file_path):
    try:
        dataset = pydicom.dcmread(file_path)
        # 这里需要根据实际数据集来调整
        # 例如，将像素值缩放到0-255
        image_array = dataset.pixel_array.astype(np.uint8)
        # 假设图像是灰度图
        height, width = image_array.shape
        bytes_per_line = width
        qimage = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap
    except Exception as e:
        print(f"Error loading DICOM file: {file_path}, {e}")
        return None





class DicomViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.last_selected_folder = None  # 初始化文件夹路径变量
        self.initUI()

    def initUI(self):

        self.setWindowTitle('DICOM Viewer')
        self.setGeometry(100, 100, 800, 600)

        # 创建左右布局
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # 上传按钮和dicom文件列表
        self.upload_button = QPushButton('Upload DICOM Dataset', self)
        self.dicom_list = QListWidget(self)

        # 连接信号和槽
        self.upload_button.clicked.connect(self.upload_dicom)
        self.dicom_list.itemClicked.connect(self.show_dicom)

        # 布局设置
        left_layout.addWidget(self.upload_button)
        left_layout.addWidget(self.dicom_list)
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        # 创建视图和场景
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)

        # 连接下一个分析页面的按钮
        self.analyze_button = QPushButton('Analyze', self)
        self.analyze_button.clicked.connect(self.analyze_clicked)
        right_layout.addWidget(self.graphics_view)
        right_layout.addWidget(self.analyze_button, alignment=Qt.AlignRight)
        right_widget.setLayout(right_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        self.setCentralWidget(splitter)

    def show_dicom(self,item):
        if self.last_selected_folder:
            file_path = os.path.join(self.last_selected_folder,item.text())
            load_and_display_dicom(self.graphics_view,file_path)

    @pyqtSlot(QListWidgetItem)
    def show_dicom(self, item):
        if self.last_selected_folder:
            file_path = os.path.join(self.last_selected_folder, item.text())
            pixmap = load_dicom_as_pixmap(file_path)
            if pixmap is not None:
                self.scene.clear()
                item = QGraphicsPixmapItem(pixmap)
                self.scene.addItem(item)
                self.graphics_view.fitInView(item,Qt.KeepAspectRatio)
            else:
                print(f"Failed to load dicom as QPixmap: {file_path}")

    def upload_dicom(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select folder')
        if folder_path:
            self.last_selected_folder = folder_path
            self.dicom_list.clear()
            dicom_files = self.list_dicom_files(folder_path)
            for file in dicom_files:
                self.dicom_list.addItem(os.path.basename(file))

    def list_dicom_files(self, folder_path):
        dicom_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.dcm', '.dicom')):  # 检查是否为DICOM文件
                    dicom_files.append(os.path.join(root, file))
        return dicom_files

    def show_dicom(self, item):
        if self.last_selected_folder:
            file_path = os.path.join(self.last_selected_folder, item.text())
            load_and_display_dicom(self.graphics_view, file_path)

    def analyze_clicked(self):
        print("Analyze button clicked")
        # 在这里添加跳转到下一个页面的逻辑

    def upload_dicom(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.last_selected_folder = folder_path
            self.dicom_list.clear()
            dicom_files = self.list_dicom_files(folder_path)
            for file in dicom_files:
                self.dicom_list.addItem(os.path.basename(file))

                # 列出文件夹中的DICOM文件名

    def load_and_display_dicom(graphics_view, file_path):
        # 假设 load_dicom_as_pixmap 是您用来加载DICOM为QPixmap的函数
        pixmap = load_dicom_as_pixmap(file_path)
        if pixmap is not None:
            scene = QGraphicsScene()
            pixmap_item = scene.addPixmap(pixmap)
            graphics_view.setScene(scene)
            graphics_view.fitInView(pixmap_item, Qt.KeepAspectRatio)


    def list_dicom_files(self, folder_path):
        dicom_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.dcm'):  # 检查是否为DICOM文件
                    dicom_files.append(os.path.join(root, file))
        return dicom_files




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DicomViewer()
    ex.show()
    sys.exit(app.exec_())