import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from voice_interaction import Voic

class AIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.voice_interaction = Voic()

    def initUI(self):
        self.setGeometry(100, 100, 100, 100)  # حجم النافذة الصغير بحجم الأيقونة
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WA_TranslucentBackground)  # إزالة إطار النافذة وتفعيل الخلفية الشفافة
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('')
        
        central_widget = QWidget(self)
        central_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(central_widget)

        # إعداد الأيقونة
        self.chat_icon = QLabel(central_widget)
        pixmap = QPixmap("C:/Users/bassam/Desktop/mine_project/Pngtree—social icon_4421694.png")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)  # تعديل حجم الأيقونة
        self.chat_icon.setPixmap(scaled_pixmap)
        self.chat_icon.setAlignment(Qt.AlignCenter)
        self.chat_icon.mousePressEvent = self.toggle_chat_frame

        layout = QVBoxLayout()
        layout.addWidget(self.chat_icon)
        central_widget.setLayout(layout)

        # إطار مربع المحادثة
        self.chat_frame = QFrame(central_widget)
        self.chat_frame.setGeometry(0, 0, 300, 300)
        self.chat_frame.setStyleSheet("background-color: rgba(255, 255, 255, 200); border: 1px solid gray; border-radius: 10px;")  # استخدام rgba لتحقيق الشفافية
        self.chat_frame.hide()

        # مربع النص للمحادثة
        self.chat_box = QTextEdit(self.chat_frame)
        self.chat_box.setGeometry(10, 10, 280, 150)
        self.chat_box.setStyleSheet("background-color: rgba(255, 255, 255, 200); border: 1px solid gray; border-radius: 5px;")  # استخدام rgba لتحقيق الشفافية
        self.chat_box.setReadOnly(True)

        # إطار لإدخال النص وإرساله
        input_frame = QFrame(self.chat_frame)
        input_frame.setGeometry(10, 180, 280, 40)
        input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 200); border: 1px solid gray; border-radius: 5px;")

        # مربع نص للإدخال
        self.input_box = QLineEdit(input_frame)
        self.input_box.setGeometry(0, 0, 180, 30)
        self.input_box.setStyleSheet("background-color: rgba(255, 255, 255, 200); border: 1px solid gray; border-radius: 5px;")

        # زر الإرسال
        self.send_button = QPushButton("إرسال", input_frame)
        self.send_button.setGeometry(190, 0, 80, 30)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("background-color: lightblue; border: 1px solid gray; border-radius: 5px;")

        # زر التحدث
        self.talk_button = QPushButton("تحدث", self.chat_frame)
        self.talk_button.setGeometry(10, 230, 80, 30)
        self.talk_button.clicked.connect(self.start_voice_interaction)
        self.talk_button.setStyleSheet("background-color: lightgreen; border: 1px solid gray; border-radius: 5px;")

        # زر التحديث
        self.update_button = QPushButton("تحديث", self.chat_frame)
        self.update_button.setGeometry(100, 230, 80, 30)
        self.update_button.clicked.connect(self.update)
        self.update_button.setStyleSheet("background-color: yellow; border: 1px solid gray; border-radius: 5px;")

        # زر الإغلاق النهائي
        self.close_button = QPushButton("إغلاق", self.chat_frame)
        self.close_button.setGeometry(190, 230, 80, 30)
        self.close_button.clicked.connect(self.close_app)
        self.close_button.setStyleSheet("background-color: red; border: 1px solid gray; border-radius: 5px;")

        self.chat_icon.mousePressEvent = self.toggle_chat_frame

    def toggle_chat_frame(self, event):
        if self.chat_frame.isHidden():
            self.chat_frame.show()
            self.setGeometry(100, 100, 320, 320)  # تكبير النافذة لتناسب مربع المحادثة
        else:
            self.chat_frame.hide()
            self.setGeometry(100, 100, 100, 100)  # تصغير النافذة لعرض الأيقونة فقط

    def send_message(self):
        message = self.input_box.text()
        self.add_message(message, "user")
        self.input_box.clear()
        response = self.voice_interaction.respond(message)
        self.add_message(response, "assistant")

    def add_message(self, message, sender):
        color = "green" if sender == "user" else "blue"
        self.chat_box.append(f'<p style="color:{color}; border-radius: 5px; padding: 5px;">{message}</p>')

    def start_voice_interaction(self):
        self.voice_interaction.start()

    def update(self):
        # قم بإضافة وظيفة التحديث هنا
        pass

    def close_app(self):
        self.close()

    def leaveEvent(self, event):
        if not self.chat_frame.isHidden():
            QTimer.singleShot(500, self.minimize_chat_frame)

    def enterEvent(self, event):
        if self.chat_frame.isHidden():
            self.chat_frame.show()
            self.setGeometry(100, 100, 320, 320)  # تكبير النافذة لتناسب مربع المحادثة

    def minimize_chat_frame(self):
        if not self.underMouse():
            self.chat_frame.hide()
            self.setGeometry(200, 200, 100, 100)  # تصغير النافذة لعرض الأيقونة فقط

if __name__ == '__main__':
    app = QApplication(sys.argv)
    assistant = AIAssistant()
    assistant.show()
    sys.exit(app.exec_())
