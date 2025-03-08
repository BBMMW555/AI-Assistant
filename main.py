import os
import sys
import json
import time
import sqlite3
from datetime import datetime

# استيراد مكتبات PyQt5 لإنشاء واجهة المستخدم
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QFrame, QVBoxLayout, QWidget, QMessageBox,
    QProgressBar, QSplashScreen, QSystemTrayIcon
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QTranslator, QLocale

# استيراد الملفات الأخرى من المشروع
from voice_interaction import Voic
from speech_recognition import Spee
from adaptive_learner import AdaptiveLearner
from task_manager import TaskManager
from event_handler import EventHandler

# استيراد مكتبة transformers لاستخدام نموذج AraGPT
from transformers import pipeline

# المسار الأساسي للمشروع
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# تحميل نموذج AraGPT للردود الذكية
chatbot = pipeline("text-generation", model="aubmindlab/aragpt2-base")

# تهيئة المساعد الصوتي
voice_interaction = Voic()

# تهيئة التعرف على الكلام باستخدام نموذج Vosk
speech_recognition = Spee(os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0"))


# تعريف الكلاس الرئيسي للتطبيق
class AIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.show_splash_screen()  # عرض شاشة الترحيب
        self.initUI()  # تهيئة واجهة المستخدم
        self.sound_enabled = True  # تفعيل الصوت افتراضيًا
        self.drag_pos = None  # متغير لتتبع موقع النافذة عند السحب
        self.chat_frame_visible = False  # حالة إطار الدردشة (ظاهر أم مخفي)
        self.interaction_timer = QTimer()  # مؤقت لمراقبة التفاعل
        self.interaction_timer.timeout.connect(self.check_interaction)  # ربط المؤقت بالدالة
        self.adaptive_learner = AdaptiveLearner()  # تهيئة نظام التعلم التكيفي
        self.task_manager = TaskManager()  # تهيئة مدير المهام
        self.event_handler = EventHandler()  # تهيئة معالج الأحداث
        self.check_required_files()  # التحقق من وجود الملفات المطلوبة
        QTimer.singleShot(3000, self.welcome_message)  # عرض رسالة الترحيب بعد 3 ثوانٍ

    def check_required_files(self):
        """التحقق من وجود الملفات المطلوبة"""
        required_files = [
            os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0", "ivector", "final.ie"),
            os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0", "graph", "HCLG.fst"),
            os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0", "graph", "words.txt"),
            os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0", "graph", "phones", "word_boundary.int"),
            os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0", "rescore", "G.fst"),
            os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0", "rescore", "G.carpa"),
            os.path.join(BASE_DIR, "splash.png"),
            os.path.join(BASE_DIR, "icon.png"),
            os.path.join(BASE_DIR, "Pngtree—social icon_4421694.png")
        ]
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        if missing_files:
            error_message = "الملفات التالية ناقصة:\n" + "\n".join(missing_files)
            QMessageBox.critical(self, "خطأ", error_message)
            sys.exit(1)  # إغلاق التطبيق بشكل أنيق

    def show_splash_screen(self):
        """عرض شاشة الترحيب"""
        splash_pix = QPixmap(os.path.join(BASE_DIR, "splash.png"))  # صورة شاشة الترحيب
        if splash_pix.isNull():
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على صورة شاشة الترحيب (splash.png).")
            return
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.show()
        QTimer.singleShot(3000, splash.close)  # إخفاء شاشة الترحيب بعد 3 ثوانٍ

    def initUI(self):
        """تهيئة واجهة المستخدم"""
        # تحديد حجم وموقع النافذة
        self.setGeometry(100, 100, 100, 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('')

        # إنشاء واجهة مركزية شفافة
        central_widget = QWidget(self)
        central_widget.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(central_widget)

        # إضافة أيقونة الدردشة
        self.chat_icon = QLabel(central_widget)
        pixmap = QPixmap(os.path.join(BASE_DIR, "Pngtree—social icon_4421694.png"))
        if pixmap.isNull():
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على أيقونة الدردشة (Pngtree—social icon_4421694.png).")
            return
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        self.chat_icon.setPixmap(scaled_pixmap)
        self.chat_icon.setAlignment(Qt.AlignCenter)
        self.chat_icon.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                border-radius: 50px;
                padding: 10px;
            }
            QLabel:hover {
                background-color: rgba(255, 255, 255, 200);
            }
        """)
        self.chat_icon.mousePressEvent = self.toggle_chat_frame
        self.chat_icon.mouseMoveEvent = self.move_window
        self.chat_icon.enterEvent = self.toggle_chat_frame

        # إنشاء تخطيط عمودي وإضافة الأيقونة
        layout = QVBoxLayout()
        layout.addWidget(self.chat_icon)
        central_widget.setLayout(layout)

        # إنشاء إطار الدردشة
        self.chat_frame = QFrame(central_widget)
        self.chat_frame.setGeometry(20, 20, 300, 300)
        self.chat_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid gray;
                border-radius: 10px;
            }
        """)
        self.chat_frame.hide()

        # إنشاء مربع الرسائل
        self.chat_box = QTextEdit(self.chat_frame)
        self.chat_box.setGeometry(10, 10, 280, 150)
        self.chat_box.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.chat_box.setReadOnly(True)

        # إنشاء إطار الإدخال
        input_frame = QFrame(self.chat_frame)
        input_frame.setGeometry(10, 180, 280, 40)
        input_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid gray;
                border-radius: 5px;
            }
        """)

        # إنشاء مربع الإدخال (QTextEdit بدلاً من QLineEdit)
        self.input_box = QTextEdit(input_frame)
        self.input_box.setGeometry(5, 5, 180, 30)
        self.input_box.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.input_box.setLineWrapMode(QTextEdit.WidgetWidth)  # تفعيل الانتقال التلقائي للسطر التالي

        # ربط حدث الضغط على المفاتيح
        self.input_box.keyPressEvent = self.keyPressEvent

        # إنشاء زر الإرسال
        self.send_button = QPushButton("إرسال", input_frame)
        self.send_button.setGeometry(194, 5, 80, 30)
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffda03;
            }
        """)

        # إنشاء زر التحدث
        self.talk_button = QPushButton("🎤 تحدث", self.chat_frame)
        self.talk_button.setGeometry(10, 228, 80, 30)
        self.talk_button.clicked.connect(self.start_voice_interaction)
        self.talk_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffda03;
            }
        """)

        # إنشاء زر الإغلاق
        self.close_button = QPushButton("إغلاق", self.chat_frame)
        self.close_button.setGeometry(10, 265, 80, 30)
        self.close_button.clicked.connect(self.close_app)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #ffda03;
            }
        """)

        # إنشاء شريط التقدم
        self.progress_bar = QProgressBar(self.chat_frame)
        self.progress_bar.setGeometry(10, 300, 280, 20)
        self.progress_bar.setValue(0)

        # إنشاء أيقونة النظام
        self.tray_icon = QSystemTrayIcon(self)
        icon_pix = QIcon(os.path.join(BASE_DIR, "icon.png"))
        if icon_pix.isNull():
            QMessageBox.critical(self, "خطأ", "لم يتم العثور على أيقونة التطبيق (icon.png).")
            return
        self.tray_icon.setIcon(icon_pix)
        self.tray_icon.show()

        # تحميل ملف الترجمة
        translator = QTranslator()
        locale = QLocale.system().name()
        translator.load(f":/translations/{locale}.qm")
        QApplication.installTranslator(translator)

    def toggle_chat_frame(self, event):
        """فتح/إغلاق إطار الدردشة عند النقر على الأيقونة"""
        if self.chat_frame.isHidden():
            self.chat_frame.show()
            self.setGeometry(self.x(), self.y(), 320, 320)  # تغيير حجم النافذة
            self.chat_frame_visible = True
        else:
            self.chat_frame.hide()
            self.setGeometry(self.x(), self.y(), 100, 100)  # إعادة النافذة إلى حجمها الأصلي
            self.chat_frame_visible = False

    def move_window(self, event):
        """سحب النافذة عند النقر والسحب"""
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def check_interaction(self):
        """مراقبة التفاعل وإغلاق مربع الدردشة عند عدم التفاعل لفترة معينة"""
        current_time = QTimer().remainingTime()
        if current_time - self.last_interaction_time > 5000:  # 5 ثواني بدون تفاعل
            self.chat_frame.hide()
            self.setGeometry(self.x(), self.y(), 100, 100)
            self.chat_frame_visible = False

    def keyPressEvent(self, event):
        """التعامل مع حدث الضغط على المفاتيح"""
        if event.key() == Qt.Key_Return and event.modifiers() & Qt.ShiftModifier:
            # إضافة سطر جديد عند الضغط على Shift + Enter
            self.input_box.insertPlainText("\n")
        elif event.key() == Qt.Key_Return:
            # إرسال الرسالة عند الضغط على Enter
            self.send_message()
        else:
            super().keyPressEvent(event)

    def send_message(self):
        """إرسال الرسالة التي قام المستخدم بكتابتها في مربع الإدخال"""
        message = self.input_box.toPlainText().strip()  # الحصول على النص من QTextEdit
        if message:  # التأكد من أن النص غير فارغ
            self.add_message(message, "user")
            self.input_box.clear()  # مسح مربع الإدخال

            if hasattr(self, 'voice_interaction'):
                response = self.voice_interaction.respond(message)  # الحصول على الرد
                self.add_message(response, "assistant")  # إضافة رد المساعد

    def add_message(self, message, sender):
        """إضافة رسالة إلى مربع الدردشة"""
        color = "green" if sender == "user" else "blue"
        self.chat_box.append(f'<p style="color:{color}; border-radius: 5px; padding: 5px;">{message}</p>')

    def start_voice_interaction(self):
        """بدء التفاعل الصوتي"""
        recognizer = Spee(os.path.join(BASE_DIR, "vosk-model-ar-0.22-linto-1.1.0"))
        print("يُرجى التحدث الآن...")
        try:
            text = recognizer.listen()
            print(f"تم التعرف على النص: {text}")
            self.add_message(f"لقد قلت: {text}", "user")
            response = self.voice_interaction.respond(text)
            self.add_message(response, "assistant")
        except Exception as e:
            print(f"حدث خطأ: {e}")
            self.add_message("حدث خطأ أثناء التعرف على الكلام.", "assistant")

    def close_app(self):
        """إغلاق التطبيق عند النقر على زر الإغلاق"""
        self.close()

    def save_interaction(self, interaction_type):
        """حفظ التفاعل في قاعدة بيانات SQLite"""
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'interactions.db'))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('INSERT INTO interactions (type) VALUES (?)', (interaction_type,))
        conn.commit()
        conn.close()


# تشغيل التطبيق
if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = AIAssistant()
    assistant.show()
    sys.exit(app.exec_())