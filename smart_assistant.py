import tkinter as tk
from tkinter import ttk

class SmartAssistantUI:
    def __init__(self, master):
        self.master = master
        master.title("الذكي - واجهة التفعيل")
        master.geometry("300x400")
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        
        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.pack(expand=True, fill='both')
        
        self.create_widgets()
    
    def create_widgets(self):
        self.activate_btn = ttk.Button(
            self.main_frame,
            text="تفعيل الذكي 🚀", 
            command=self.activate
        )
        self.activate_btn.pack(pady=10, fill='x')
        
        self.auto_learn_btn = ttk.Button(
            self.main_frame,
            text="تعليم تلقائي 🤖", 
            command=self.auto_learn
        )
        self.auto_learn_btn.pack(pady=10, fill='x')
        
        self.ask_btn = ttk.Button(
            self.main_frame,
            text="اسألني سؤال ❓", 
            command=self.ask_question
        )
        self.ask_btn.pack(pady=10, fill='x')
        
        self.knowledge_btn = ttk.Button(
            self.main_frame,
            text="ماذا تعلمت؟ 🧠", 
            command=self.show_knowledge
        )
        self.knowledge_btn.pack(pady=10, fill='x')
        
        self.result_label = ttk.Label(
            self.main_frame,
            text="...أنا جاهز لمساعدتك",
            font=('Arial', 10),
            wraplength=250
        )
        self.result_label.pack(pady=20)
    
    def activate(self):
        self.result_label.config(text="✅ تم التفعيل بنجاح!\nأنتظر أوامرك...")
    
    def auto_learn(self):
        self.result_label.config(text="🔍 جاري البحث التلقائي...\nسيتم تحديث المعرفة تلقائيًا")
    
    def ask_question(self):
        self.result_label.config(text="📩 يمكنك طرح سؤالك الآن في حقل الدردشة")
    
    def show_knowledge(self):
        self.result_label.config(text="📚 المعرفة الحالية:\n- أساسيات الذكاء\n- تحليل البيانات\n- التعرف على الأنماط")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAssistantUI(root)
    root.mainloop()