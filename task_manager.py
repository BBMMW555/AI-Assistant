import subprocess
import psutil


        # 5. نظام إدارة المهام
class TaskManager:
    @staticmethod
    def open_program(name):
        try:
            subprocess.Popen(name)
            return True
        except Exception as e:
            return str(e)
    
    @staticmethod
    def close_program(name):
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == name:
                    proc.kill()
            return True
        except Exception as e:
            return str(e)
    
    @staticmethod
    def generate_code(task, instructions, previous_code="", error=""):
        return chain.run({
            "task": task,
            "instructions": instructions,
            "previous_code": previous_code,
            "error": error
        })
