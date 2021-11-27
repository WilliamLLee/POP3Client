
from PyQt5.QtWidgets import QApplication, QComboBox,QLineEdit, QTextEdit,QWidget,QVBoxLayout,QHBoxLayout, QLabel,QPushButton
from PyQt5.QtGui import QFont, QIcon, QTextCursor
from PyQt5.QtCore import QRect, QSize

import threading



from config.config  import *
from tools import utls

# class PacketsAnalyzer(QDialog):
#     def __init__(self, main_window, results):
#         """
#         Initialization function
#         :param main_window: main windows object
#         """
#         super().__init__()
#         self.setWindowTitle('Packets Analysis')
#         self.main_window = main_window
#         self.table = QVBoxLayout()
#         self.results = results
#         self.__init_ui()

#     def __init_ui(self):
#         # Set window size
#         diglog_size = QSize(600,400)
#         self.setFixedSize(diglog_size)
#         # Set window icon
#         self.setWindowIcon(QIcon('icon.ico'))
        
#         # v Box Layout container
#         left_container = QVBoxLayout()
#         right_container = QVBoxLayout()
#         # Set information display
#         self.total_count, self.protocol_dic, self.service_dic = func.packet_count_func(self.results)
#         self.tcp_udp_count = 0
#         if 'TCP' in self.protocol_dic.keys():
#                 self.tcp_udp_count += self.protocol_dic['TCP']
#         if 'UDP' in self.protocol_dic.keys():
#                 self.tcp_udp_count += self.protocol_dic['UDP']
        
#         print(self.total_count, self.tcp_udp_count, self.protocol_dic, self.service_dic)
        
#         left_container.addWidget(QLabel("Count By Session Protocol:"))
#         left_container.addWidget(QLabel("Total Packet Count: {}".format(self.total_count)))
#         right_container.addWidget(QLabel("Count By Application Service:"))
#         right_container.addWidget(QLabel("Total TCP/UDP Count: {}".format(self.tcp_udp_count)))
#         for protocol in func.protocol_list:
#                 if protocol in self.protocol_dic.keys():
#                         left_container.addWidget(QLabel(protocol+":"+str(self.protocol_dic[protocol])+"(%.2f)"%(self.protocol_dic[protocol]/self.total_count)))
#                 else:
#                         left_container.addWidget(QLabel(protocol+":"+"0"))
#         for service in func.service_list:
#                 if self.tcp_udp_count!=0 and service in self.service_dic.keys():
#                         right_container.addWidget(QLabel(service+":"+str(self.service_dic[service])+"(%.2f)"%(self.service_dic[service]/self.tcp_udp_count)))
#                 else:
#                         right_container.addWidget(QLabel(service+":"+"0"))


#         total_container = QHBoxLayout()
#         total_container.addLayout(left_container)
#         total_container.addLayout(right_container)

#         self.table.addLayout(total_container)
#         self.setLayout(self.table)
#         self.adjustSize()
#         self.show()


class MainFrameWindow(QWidget):
    '''
        design the main frame window
    '''
    def __init__(self,window_name,debug_flag=False,parent=None):
        super().__init__(parent)
        # the window title
        self.setWindowTitle(window_name)

        # the mails that get from the pop3 server
        self.mails = []

        # basic componet
        self.pop3_server = QComboBox()
        self.pop3_server.addItems(['pop.163.com','pop.qq.com','pop.gmail.com','pop.sina.com'])
        self.pop3_server.setEditable(False)
        self.pop3_port = QComboBox()
        self.pop3_port.addItems(['110','995'])
        self.pop3_port.setEditable(False)
        self.mail_address = QLineEdit()
        self.mail_address.setPlaceholderText("Input your email address")
        self.mail_password = QLineEdit()
        self.mail_password.setPlaceholderText("Input your email password")
        self.mail_password.setEchoMode(QLineEdit.Password)
        self.msg_arg = QLineEdit()
        self.msg_arg.setPlaceholderText("Input the mail number")
        self.cmd_info = QTextEdit()
        self.cmd_info.setReadOnly(True)
        self.mail_info = QTextEdit()
        self.mail_info.setReadOnly(True)
        self.state_info = QLabel()

        # get the resulotion of the screen
        self.screen_resolution = QApplication.desktop().screenGeometry()
        self.width = self.screen_resolution.width()
        self.height = self.screen_resolution.height()

        # get the size of the window
        self.window_width = self.width*0.5
        self.window_height = self.height*0.5
        # get the start position of the window
        self.window_start_x = self.width/2 - self.window_width/2
        self.window_start_y = self.height/2 - self.window_height/2
        # set the size  of the window
        self.window_rect = QRect(self.window_start_x,self.window_start_y,self.window_width,self.window_height)
        self.window_size = QSize(self.window_width,self.window_height)

        # set debug flag
        self.debug_flag = debug_flag

        # set the icon path
        self.icon_path = "icon.ico"

        # set the threading event
        self.thread_event = threading.Event()

        # init the ui of main frame window
        self.init_ui()

        # set the font
        self.font = QFont()
        self.font.setPointSize(12)
        self.font.setFamily("Consolas")

        # set the log_text
        self.log_text = ""

        if self.debug_flag:
            print("Debug mode is set now!")

    def init_ui(self):
        # set the size of the window
        self.setGeometry(self.window_rect)
        self.setFixedSize(self.window_size)

        # set icon of this window
        self.setWindowIcon(QIcon(self.icon_path))

        # set the layout
        total_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        top_layout_l1 = QHBoxLayout()
        top_layout_l2 = QHBoxLayout()
        middle_layout = QHBoxLayout()
        middle_layout_l1 = QVBoxLayout()
        middle_layout_l2 = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        # set the top layout
        top_layout_l1.addWidget(QLabel("POP3 Server:"))
        top_layout_l1.addWidget(self.pop3_server)
        top_layout_l1.addWidget(QLabel("POP3 Port:"))
        top_layout_l1.addWidget(self.pop3_port)
        top_layout_l1.addWidget(QLabel("Msg #:"))
        top_layout_l1.addWidget(self.msg_arg)
        top_layout_l2.addWidget(QLabel("Mail Address:"))
        top_layout_l2.addWidget(self.mail_address)
        top_layout_l2.addWidget(QLabel("Mail Password:"))
        top_layout_l2.addWidget(self.mail_password)
        
        
        STAT_button = QPushButton("STAT")
        STAT_button.clicked.connect(self.STAT_button_clicked)
        LIST_button = QPushButton("LIST")
        LIST_button.clicked.connect(self.LIST_button_clicked)
        RETR_button = QPushButton("RETR")
        RETR_button.clicked.connect(self.RETR_button_clicked)
        # start_button = QPushButton("Start")
        # start_button.clicked.connect(self.start_button_clicked)
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login_button_clicked)
        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.logout_button_clicked)
        
        top_layout_l1.addWidget(RETR_button)
        top_layout_l1.addWidget(STAT_button)
        top_layout_l1.addWidget(LIST_button)
        # top_layout_l2.addWidget(start_button)
        top_layout_l2.addWidget(login_button)
        top_layout_l2.addWidget(logout_button)

        top_layout.addLayout(top_layout_l1)
        top_layout.addLayout(top_layout_l2)

        # set the middle layout
        middle_layout_l1.addWidget(QLabel("Command Info:"))
        middle_layout_l1.addWidget(self.cmd_info)
        middle_layout_l2.addWidget(QLabel("Mail Info:"))
        middle_layout_l2.addWidget(self.mail_info)
        middle_layout.addLayout(middle_layout_l1)
        middle_layout.addLayout(middle_layout_l2)

        # set the bottom layout
        state_info_hint = QLabel("Running Status:",self)
        bottom_layout.addWidget(state_info_hint)
        bottom_layout.addWidget(self.state_info)

        # set the total layout
        total_layout.addLayout(top_layout)
        total_layout.addLayout(middle_layout)
        total_layout.addLayout(bottom_layout)

        # set the widget
        self.setLayout(total_layout)

        # show the window
        self.show()

    def start_button_clicked(self):
        # set the device 
        if self.debug_flag:
            print("Start button is clicked!")
        self.state_info.setText("Running...")
        if self.mail_address.text() == "" or self.mail_password.text() == "":
            if self.debug_flag:
                self.set_mail_address(MAILADDR)
                self.set_mail_password(MAILPASS)
            else:
                self.set_state_info("Please input the mail address and mail password!")
                raise Exception("Please input the mail address and mail password!")
        self.init_pop3_device()

    def login_button_clicked(self):
        if self.debug_flag:
            print("Login button is clicked!")
        try:
            self.start_button_clicked() 
        except Exception as e:
            self.set_state_info(str(e))
            return
        if self.device_valid == False:
            self.set_state_info("Please start the device first!")
            return
        if self.mail_address.text() == "" or self.mail_password.text() == "":
            self.state_info.setText("Please input the mail address and password!")
            return
        self.set_state_info("Login in...")
        self.log(">>>"+"USER %s" % self.mail_address.text())
        try:
            user_resp = self.pop3_device.user(self.mail_address.text())
        except Exception as e:
            self.set_state_info("Login failed: %s"%e)
            return 
        self.log("<<<"+user_resp)
        
        self.log(">>>"+"PASS %s" % self.mail_password.text())         
        try:
            pass_resp = self.pop3_device.pass_(self.mail_password.text())
        except Exception as e:
            self.set_state_info("Login failed: %s"%e)
            return
        self.log("<<<"+pass_resp)
        
        self.set_state_info("Login success!")

    def logout_button_clicked(self):
        if self.debug_flag:
            print("Logout button is clicked!")
        self.set_state_info("Logout...")
        self.log(">>>"+"QUIT")
        try:
            quit_resp = self.pop3_device.quit()
        except Exception as e:
            self.set_state_info("Logout failed: %s"%e)
            return
        self.log("<<<"+quit_resp)
        self.device_valid = False
        self.set_state_info("Logout success!")
        self.set_mail_info("You have logged out!")
        
    def STAT_button_clicked(self):
        if self.debug_flag:
            print("STAT button is clicked!")
        if self.device_valid == False:
            self.set_state_info("Please login first!")
            return
        self.set_state_info("STAT...")
        self.log(">>>"+"STAT")
        try:
            stat_resp = self.pop3_device.stat()
        except Exception as e:
            self.set_state_info("STAT failed: %s"%e)
            return
        self.log("<<<"+stat_resp)
        stat_resp_list = stat_resp.split(" ")
        self.set_mail_info("total mails (#): %s\nMemory size (bytes): %s"%(stat_resp_list[1], stat_resp_list[2]))
        self.set_state_info("STAT success!")
        

    def LIST_button_clicked(self):
        if self.debug_flag:
            print("LIST button is clicked!")
        if self.device_valid == False:
            self.set_state_info("Please login first!")
            return
        self.set_state_info("LIST...")
        if self.get_msg_arg()!= "":
            self.log(">>>"+"LIST %s" % self.get_msg_arg())
        else:
            self.log(">>>"+"LIST")
        try:
            if self.get_msg_arg() != "":
                list_resp = self.pop3_device.list(self.get_msg_arg())
            else:
                list_resp = self.pop3_device.list(None)
                
        except Exception as e:
            self.set_state_info("LIST failed: %s"%e)
            return
        
        if self.get_msg_arg() == "":
            self.log("<<<"+str(list_resp[0]))
            total_info = list_resp[0]
            self.set_mail_info("total mails (#): %s \tMemory size (bytes): %s"%(total_info[1], total_info[2]))
            for i in range(len(list_resp[1])):
                self.log(""+str(list_resp[1][i]))
                info_list = list_resp[1][i].split(" ")
                self.set_mail_info("mails No.%s \tMemory size (bytes): %s"%(info_list[0], info_list[1]),True)
            self.log(""+str(list_resp[2]))
            self.set_mail_info("response info lenght: %s byte(s)."%(list_resp[2]),True)
        else:
            self.log("<<<"+str(list_resp))
            list_resp_list = list_resp.split(" ")
            self.set_mail_info("total mails (#): %s\nMemory size (bytes): %s"%(list_resp_list[1], list_resp_list[2]))
        self.set_state_info("LIST success!")

    def RETR_button_clicked(self):
        if self.debug_flag:
            print("RETR button is clicked!")
        if self.device_valid == False:
            self.set_state_info("Please login first!")
            return
        if self.get_msg_arg()!= "":
            self.log(">>>"+"RETR %s" % self.get_msg_arg())
        else:
            self.set_state_info("Please input the mail No.!")
            return 
        self.set_state_info("RETR...")
        try:
            retr_resp = self.pop3_device.retr(self.get_msg_arg())
        except Exception as e:
            self.set_state_info("RETR failed: %s"%e)
            return
        # display the interaction with the server
        self.log("<<<"+str(retr_resp[0]))
        for i in range(len(retr_resp[1])):
            self.log(""+str(retr_resp[1][i]))
        self.log(""+str(retr_resp[2]))

        # display the mail content
        mail_content = ""
        for i in range(len(retr_resp[1])):
            mail_content += str(retr_resp[1][i]).strip('=\r\n')
        self.set_mail_info(mail_content)

        self.set_state_info("RETR success!")
        
            

    def get_mail_address(self):
        return self.mail_address.text()
    
    def get_mail_password(self):
        return self.mail_password.text()

    def get_pop3_server(self):
        return self.pop3_server.currentText()

    def get_pop3_port(self):
        return self.pop3_port.currentText()

    def get_msg_arg(self):
        return self.msg_arg.text()

    def set_cmd_info(self,info):
        self.cmd_info.setText(info)
        cursor = self.cmd_info.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.cmd_info.setTextCursor(cursor)

    def set_mail_info(self,info, add_flag=False):
        if add_flag:
            prev_info = self.mail_info.toPlainText()
            self.mail_info.setText(prev_info +'\n'+info)
        else:
            self.mail_info.setText(info)

    def set_state_info(self,state_info):
        self.state_info.setText(state_info)

    def set_mail_address(self,mail_address):
        self.mail_address.setText(mail_address)

    def set_mail_password(self,mail_password):
        self.mail_password.setText(mail_password)
    
    def log(self,info):
        self.log_text+=(info+"\n")
        self.set_cmd_info(self.log_text)


    def init_pop3_device(self):
        '''
        init the pop3 device
        '''
        self.pop3_device = utls.POP3(hostname = self.get_pop3_server(),port = self.get_pop3_port(),is_debug = self.debug_flag,encoding=encoding)
        self.set_state_info("POP3 device is initialized!")
        welcome_resp = self.pop3_device.getwelcome()
        self.log("<<<"+welcome_resp)
        self.set_mail_info(welcome_resp[4:])
        self.device_valid = True
        

if __name__ == "__main__":
    '''
        Test the function.
    '''
    
