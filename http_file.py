import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QFontMetrics
from PyQt5.QtWidgets import *
from requests_toolbelt import MultipartEncoderMonitor
from requests_toolbelt.downloadutils import stream

import http_login
import http_main
from http_request import Requests
from utils import Setting, delete_user_info, url_upload


def print_info(function_name):
    print("=" * 50 + function_name + "=" * 50)


class MyLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.ElideRight, self.width())

        painter.drawText(self.rect(), self.alignment(), elided)


class Window_file(QMainWindow):

    def __init__(self, parent=None):
        super(Window_file, self).__init__(parent)
        # self.cwd = os.getcwd() # 获取当前程序文件位置
        self.user = None
        self.filename = None
        self.ui_main = None
        self.ui_login = http_login.Window()

        self.pic_full_path = None
        self.txt_full_path = None

        self.formGroupBox = QGroupBox()
        self.setWindowTitle('选择文件')
        self.resize(450, 300)  # 设置窗体大小
        self.widget = QWidget(parent)

        self.init_ui()

    def setUser(self, val):
        print_info(sys._getframe().f_code.co_name)
        self.user = val
        print(val)

    def init_ui(self):

        self.btn_logout = QPushButton()
        self.btn_logout.setText("注销")
        self.btn_logout.setFixedWidth(100)
        self.btn_logout.setStyleSheet('''color: rgb(255, 0, 0);;''')

        # btn 1选择图片
        self.btn_choosePic = QPushButton(self)
        self.btn_choosePic.setObjectName("btn_choosePic")
        self.btn_choosePic.setText("选择图片")
        self.btn_choosePic.setFixedSize(100, 40)

        self.label_choosed_pic_name = QLabel(self)
        self.label_choosed_pic_name.setAlignment(Qt.AlignCenter)
        self.label_choosed_pic_name.setFixedWidth(250)

        # btn 2选择txt
        self.btn_chooseTxt = QPushButton(self)
        self.btn_chooseTxt.setObjectName("btn_chooseTxt")
        self.btn_chooseTxt.setText("选取txt文件")
        self.btn_chooseTxt.setFixedSize(100, 40)

        self.label_choosed_txt_name = QLabel(self)
        self.label_choosed_txt_name
        self.label_choosed_txt_name.setAlignment(Qt.AlignCenter)
        self.label_choosed_txt_name.setFixedWidth(250)

        formLayout = QFormLayout()
        formLayout.addRow(self.btn_choosePic, self.label_choosed_pic_name)
        formLayout.addRow(self.btn_chooseTxt, self.label_choosed_txt_name)
        self.formGroupBox.setLayout(formLayout)

        # btn 3 提交
        self.btn_emit = QPushButton(self)
        self.btn_emit.setObjectName("btn_emit")
        self.btn_emit.setText("提交")
        self.btn_emit.setFixedSize(100, 40)

        self.setCentralWidget(self.widget)
        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_logout, alignment=Qt.AlignRight)
        layout.addWidget(self.formGroupBox, alignment=Qt.AlignCenter)
        layout.addWidget(self.btn_emit, alignment=Qt.AlignHCenter)  # 单元格居中

        self.widget.setLayout(layout)  # 设置窗口总布局

        # 设置信号
        self.btn_choosePic.clicked.connect(self.slot_btn_choosePic)
        self.btn_chooseTxt.clicked.connect(self.slot_btn_chooseTxt)
        self.btn_emit.clicked.connect(self.slot_btn_emit)
        self.btn_logout.clicked.connect(self.slot_btn_logout)

    def slot_btn_choosePic(self):
        print_info(sys._getframe().f_code.co_name)

        self.pic_full_path, filetype = QFileDialog.getOpenFileName(self,
                                                                   "选取文件夹",
                                                                   # self.cwd,
                                                                   "All Files (*);;Image files(*.jpg *.gif *.png)g")  # 设置图片扩展名过滤，用双分号间隔

        if self.pic_full_path == "":
            print("\n取消选择")
            return

        imgname = self.pic_full_path.split("/")[-1]

        print("\n你选择的图片为:")
        print(imgname)
        self.label_choosed_pic_name.setText(imgname)
        print("文件筛选器类型: ", filetype)

    def slot_btn_chooseTxt(self):
        print_info(sys._getframe().f_code.co_name)

        self.txt_full_path, filetype = QFileDialog.getOpenFileName(self,
                                                                   "选取文件",
                                                                   # self.cwd,
                                                                   "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

        if self.txt_full_path == "":
            print("\n取消选择")
            return
        txtname = self.txt_full_path.split("/")[-1]

        print("\n你选择的txt为:")
        print(txtname)
        self.filename = txtname.split(".")[0]
        self.label_choosed_txt_name.setText(txtname)
        print("文件筛选器类型: ", filetype)

    # 将图片和txt一起请求后端api，点击发送请求并返回值存放在本地目录内存中，发送和返回显示出进度条，到达100%跳转到第三个窗口
    def slot_btn_emit(self):
        img_name = self.label_choosed_pic_name.text()
        txt_name = self.label_choosed_txt_name.text()

        if img_name and txt_name:
            # 进度条初始化
            self.progress = QProgressDialog(self)
            self.progress.setWindowTitle("正在导入")
            self.progress.setCancelButtonText("取消")
            self.progress.setFixedWidth(400)
            self.progress.setMinimumDuration(2)
            self.progress.setMaximum(100)

            if self.progress.wasCanceled():
                QMessageBox.warning(self, "提示", "上传文件失败!")
            self.progress.show()

            self.construct_upload_multipart(txt_name, img_name)
        else:
            QMessageBox.information(self, "Message",
                                    "请先选择图片和文字",
                                    QMessageBox.Ok)

    def slot_btn_logout(self):
        delete_user_info(self.user)
        self.user = None
        self.ui_login.show()
        self.hide()

    # 更新进度条
    def update_progressbar(self, val):
        print(val)
        self.progress.setValue(val)
        if val == 100:
            self.progress.close()

    def construct_upload_multipart(self, txt_name, img_name):
        print_info(sys._getframe().f_code.co_name)

        # if txt_name is not None and img_name is not None:
        print(txt_name, img_name)

        imgname, imgtype = img_name.split(".")
        txtname, txttype = txt_name.split(".")

        m = MultipartEncoderMonitor.from_fields(
            fields={"image": (imgname + "." + imgtype, open(self.pic_full_path, 'rb'), 'image/' + imgtype),
                    "text": (txtname + "." + txttype, open(self.txt_full_path, 'rb'), 'text/plain')
                    })

        monitor = MultipartEncoderMonitor(m, self.on_upload_callback)
        header = {"Authorization": self.user.get_header_type() + " " + self.user.get_access_token(),
                  "Content-Type": monitor.content_type
                  }
        request = Requests()
        request.post_request(url_upload, monitor, header, self.onSuccess, self.onFail)

    # 上传进度监控
    def on_upload_callback(self, monitor):

        progress = (int(monitor.bytes_read / monitor.len * 100))
        print("已上传" + str(progress) + "%")

        self.progress.setValue(progress)
        QCoreApplication.processEvents()
        if progress >= 100:
            self.progress.close()

    def onSuccess(self, result):
        print_info(sys._getframe().f_code.co_name)

        setting = Setting()
        if 'error_code' in result:
            print('fail', result)
            setting.resolve_response_data(result)
            erro_info = setting.get_error_info()
            print(erro_info)
            QMessageBox.warning(self,
                                "警告",
                                erro_info,
                                QMessageBox.Yes)
        else:
            print('success', result)
            if not os.path.exists(QDir.currentPath() + "/tmp/"):
                os.mkdir(QDir.currentPath() + "/tmp/")

            font_file = QDir.currentPath() + "/tmp/" + self.filename + ".ttf"

            with open(font_file, 'wb') as fd:
                filename = stream.stream_response_to_file(result, path=fd)
            print('file saved to %s' % filename)

            self.label_choosed_txt_name.clear()
            self.label_choosed_pic_name.clear()

            self.ui_main = http_main.User(font_file, self.txt_full_path)
            self.ui_main.setUser(self.user)
            self.ui_main.show()
            self.close()

    def onFail(self, error_info):
        print_info(sys._getframe().f_code.co_name)

        QMessageBox.warning(self,
                            "错误",
                            error_info,
                            QMessageBox.Yes)

    # 绘制水平线
    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.begin(self)
        painter.drawLine(200, 135, 350, 135)
        painter.drawLine(200, 178, 350, 178)
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_file = Window_file()
    window_file.show()
    sys.exit(app.exec_())
