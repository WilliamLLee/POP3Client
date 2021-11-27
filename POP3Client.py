import sys


from ui.FrameWindow import *
from config import *
from config import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # if you want to set the debug_flag to True, you must set the email address and password in config.py
    win = MainFrameWindow(WINDOW_NAME,debug_flag=False)  
    sys.exit(app.exec_())
    
    