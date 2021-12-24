import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QGuiApplication
import pyotp
import paramiko
import datetime
import time
import configparser
import socket
import ssl
import schedule

config = configparser.ConfigParser()
now = datetime.datetime.now().strftime("%Y%m%d")    #設定當下時間(年月日)
local_path = ( './rdlog.log' 
                + '-' 
                +  now
                +  '_' )#本地位置

remote_path = '/var/log/nginx/rdlog.log-' + now + '.gz'    #遠端linux主機  


"""
color:	white rgb(110,110,110) #eb7350	前景颜色，字体颜色
background:	transparent	背景为透明
background-color:	white rgb(110,110,110) #eb7350	背景颜色
background-position:	left right center top bottom	设定图片的位置
background-image:url()	./img/back.jpg	背景图片 ，不缩放图片大小
border-image:url()	./img/back.jpg	背景图片，会对图片进行拉伸，平铺
border-style:	outset inset	边框样式，按下是inset
border-width:	px	边框大小
border-radius:	px	边框弧度
border:3px solid red	px color	边框宽度以及颜色
border-color: rgba(255, 225, 255, 30);	color	边框颜色
font-family	微软雅黑	设定字体所属家族
font: bold 14px	bold px	字体大小并加粗
font-size:	px	字体大小
font-style:	inset	字体样式
font-weight:	px	字体深浅
selection-color:	color	设定选中时候的颜色
————————————————
原文链接：https://blog.csdn.net/qq_42250189/article/details/105199339
"""

class MainWindow(QMainWindow):
        def __init__(self):
                super(MainWindow, self).__init__()
                self.resize(400, 300)
                self.setStyleSheet('background-image:url(./img/bluesky.jpg); background-position: bottom')
                # Button
                self.button1 = QPushButton('OTP')
                self.button2 = QPushButton('EQ_RDLOG')
                self.button3 = QPushButton('監控SSL')
                self.text1 = QTextEdit()
                self.text1.setReadOnly(True)

                self.button1.setStyleSheet('background:	transparent; background-color: #FFA823; color: #805300; font: bold 30px')
                self.button2.setStyleSheet('background:	transparent; background-color: #FFA823; color: #805300; font: bold 30px')
                self.button3.setStyleSheet('background:	transparent; background-color: #FFA823; color: #805300; font: bold 30px')


        # frame
                self.layout = QGridLayout()
                self.layout.addWidget(self.button1, 0, 0) #x, y, 佔據幾行, 幾列
                self.layout.addWidget(self.button2, 1, 0)
                self.layout.addWidget(self.button3, 2, 0, 1, 3)
                self.layout.addWidget(self.text1, 3, 0, 2, 3)

                self.main_frame = QWidget()
                self.main_frame.setLayout(self.layout)
                self.setCentralWidget(self.main_frame)


        # Sub Window
                self.sub_window = TextEditDemo()
                self.sub2_window = App()
                self.sub3_window = SSLDemo()

        
        # Button Event
                self.button1.clicked.connect(self.sub_window.show)
                self.button2.clicked.connect(self.sub2_window.show)
                self.button3.clicked.connect(self.sub3_window.show)
                
                		
class TextEditDemo(QWidget):
        def __init__(self):
                super().__init__()
                self.resize(400, 300)
                self.btnPress1 = QPushButton('CU')
                self.btnPress2 = QPushButton('ET')
                self.btnPress3 = QPushButton('AMG')
                self.btnPress1.setStyleSheet('font-size:30px')
                self.btnPress2.setStyleSheet('font-size:30px')
                self.btnPress3.setStyleSheet('font-size:30px')

                layout = QHBoxLayout()
                layout.addWidget(self.btnPress1)   
                layout.addWidget(self.btnPress2)
                layout.addWidget(self.btnPress3)    		
                self.setLayout(layout)

                self.btnPress1.clicked.connect(self.btnPress4_Clicked)
                self.btnPress2.clicked.connect(self.btnPress5_Clicked)
                self.btnPress3.clicked.connect(self.btnPress6_Clicked)

        def btnPress4_Clicked(self):
       
                self.opt = config.read('otp.ini')
                cu = config['OTP']['CU']
                self.totp1 = pyotp.TOTP(cu)
                self.clipboard = QApplication.clipboard()
                self.clipboard.setText(self.totp1.now())

        def btnPress5_Clicked(self):
       
                self.opt = config.read('otp.ini')
                et = config['OTP']['ET']
                self.totp2 = pyotp.TOTP(et)
                self.clipboard = QApplication.clipboard()
                self.clipboard.setText(self.totp2.now())
        
        def btnPress6_Clicked(self):
       
                self.opt = config.read('otp.ini')
                amg = config['OTP']['AMG']
                self.totp3 = pyotp.TOTP(amg)
                self.clipboard = QApplication.clipboard()
                self.clipboard.setText(self.totp3.now())


class App(QWidget):

        def __init__(self):
                super().__init__()
                self.initUI()
                

        def initUI(self):
                self.setWindowTitle('EQ_RDlog下載')
                self.resize(400, 300)
                self.nameLb1 = QLabel("<font color='blue' size='4' face='Arial'>輸入使用者帳號 : </font>", self)
                self.nameEd1 = QLineEdit(self)
                self.nameLb2 = QLabel("<font color='blue' size='4' face='Arial'>輸入使用者密碼 : </font>", self)
                self.nameEd2 = QLineEdit(self)
                self.nameEd2.setEchoMode(QLineEdit.Password)  #設定密文
                #self.log_thread = AppThread()  #類的實例化,也可以在此處實例化,但如過在此處實例化的話,就不會獲得控鍵的值了,傳遞至run()線程中,因此在start()中實例化。
                self.textEdit = QTextEdit()
                self.textEdit.setReadOnly(True)   #設定唯讀,介面是無法輸入的
                self.btnOk = QPushButton("下載")
                self.btnCancel = QPushButton("清除帳密")
                self.Clr = QPushButton("清除內容")

        #設置位置

                mainLayout = QGridLayout(self)
                mainLayout.addWidget(self.nameLb1, 0,0)
                mainLayout.addWidget(self.nameEd1, 0,1)
                mainLayout.addWidget(self.nameLb2, 1,0)
                mainLayout.addWidget(self.nameEd2, 1,1)
                mainLayout.addWidget(self.btnOk, 1,2)
                mainLayout.addWidget(self.btnCancel, 0,2)
                mainLayout.addWidget(self.Clr, 3,2)
                mainLayout.addWidget(self.textEdit, 2,0,1,0)

                
        # self.setLayout(mainLayout)  主要布局(格子)
        #按鈕動作
                self.btnCancel.clicked.connect(self.nameEd1.clear)
                self.btnCancel.clicked.connect(self.nameEd2.clear)
                self.btnOk.clicked.connect(self.start)  #按下載中連置start() 
                self.Clr.clicked.connect(self.textEdit.clear)

        

        def start(self):
                username = self.nameEd1.text() #獲得帳號
                password = self.nameEd2.text() #獲得密碼
                print(username)
                self.log_thread = AppThread(username,password) #在此實例化是為了讓run()線程中得到參數
                self.log_thread.start()  #開始線程
                self.log_thread.update.connect(self.log)  #信號連接槽函數
                self.log_thread.error.connect(self.error) #信號連接槽函數

        def log(self, i):
                self.textEdit.append(f"<font color='blue' size='6' face='DFKai-sb'> {i} </font>")
                #self.log_thread.update.connect(self.log) 信號連接槽,傳入數值(i)這可以隨意設變數,主要是發射那邊參數是甚麼
                #也能在裡面新增其他self.textEdit.append,照著下面發射的for迴圈逐一顯示

        def error(self, e):
                self.textEdit.append(f"<font color='red' size='6' face='DFKai-sb'> {e} </font>")

class SSLDemo(QWidget):
        def __init__(self):
                super().__init__()
                
                self.resize(400, 300)
                self.ssltext = QTextEdit()
                self.sslbtn = QPushButton('檢測')
                self.ssltext.setReadOnly(True)

                layout = QVBoxLayout()
                layout.addWidget(self.ssltext)
                layout.addWidget(self.sslbtn)    		
                self.setLayout(layout)

                #啟動
                self.sslbtn.clicked.connect(self.start)
        
        def start(self):
                self.log_thread = SllThread() #在此實例化是為了讓run()線程中得到參數
                self.log_thread.start()  #開始線程
                self.log_thread.update.connect(self.ap)  #信號連接槽函數
                self.log_thread.error.connect(self.err) #信號連接槽函數

        def ap(self, ssl):
                self.ssltext.append(f"<font color='blue' size='6' face='DFKai-sb'> {ssl} </font>")
                #self.log_thread.update.connect(self.log) 信號連接槽,傳入數值(i)這可以隨意設變數,主要是發射那邊參數是甚麼
                #也能在裡面新增其他self.textEdit.append,照著下面發射的for迴圈逐一顯示

        def err(self, e):
                self.ssltext.append(f"<font color='red' size='6' face='DFKai-sb'> {e} </font>")               

   
        
class AppThread(QThread):   

        update  = pyqtSignal(str)  #定義str信號槽
        error = pyqtSignal(str)    #定義str信號槽     
        global local_path     #變成全域變數
        global remote_path    #變成全域變數  
        def __init__(self, username, password):  #初始化
            super().__init__()
            self.username = username    #屬性
            self.password = password    #屬性

        #def __del__(self):
                #self.wait()
       
        def run(self):
                #print(self.username)
                #print(self.password)
                for i in range(191,199):
                        log  = "下載完成"    #定義信號內容,也可空值
                        err = "!!!ERR!!!"  #定義信號內容
                        
                        try:
                                self.update.emit(f"<font color='green' size='6' face='Arial'>================= </font>")
                                self.update.emit(f"{i}正在下載")
                                transport = paramiko.Transport(('10.11.2.' + str(i), 22))
                                transport.connect(username=self.username, password=self.password)   #使用者登入帳密
                                sftp = paramiko.SFTPClient.from_transport(transport)
                                sftp.get(remote_path, local_path  + str(i) + '.gz')  # 將遠端檔案下載到本地並重新命名 
                                transport.close()
                                self.update.emit(str(i) + log)  #emit 發射信號
                        except Exception as e:
                                self.error.emit(err)
                                print(e)
                                time.sleep(1) 
class SllThread(QThread):
        #QThread 使用這模組範例
        """
        class Thread(QThread):
            def __init__(self):
            super(Thread,self).__init__()
            def run(self):
        """
        update  = pyqtSignal(str)  #定義str信號槽
        error = pyqtSignal(str)    #定義str信號槽   
        def __init__(self):  #初始化
            super().__init__()           
        
        
        def ssl_expiry_datetime(self, hostname, port):
                ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'
                #%b 本地简化的月份名称
                #%d 月内中的一天（0-31）
                #%H 24小时制小时数（0-23）
                #%M 分钟数（00=59）
                #%S 秒（00-59）
                #%Y 四位数的年份表示（000-9999）
                #%Z 当前时区的名称
                #datetime.datetime.strptime(ssl_info['notAfter'] 輸出來的時間 'Sep  9 12:00:00 2016 GMT' 
                #strptime 接收以時間元組，並返回以可讀字符串表示的當地時間，格式由參數format 決定。 2021-10-12 09:07:45

                context = ssl.create_default_context()  #這個例子創建了一個SSL 上下文並使用客戶端套接字的推薦安全設置，包括自動證書驗證:
                context.check_hostname = False   #是否要啟用主機名檢查

                conn = context.wrap_socket(
                        socket.socket(socket.AF_INET),
                        server_hostname=hostname,
                        )
                # 5 second timeout
                conn.settimeout(5.0)   
                port = int(port)
                conn.connect((hostname, port))
                ssl_info = conn.getpeercert()
                # Python datetime object
                #傳值ssl_info['notAfter']只要'notAfter'這段內容
                #ssl_dateformat 轉換格式(西元:年 月 日 時:分:秒)

                return datetime.datetime.strptime(ssl_info['notAfter'], ssl_dateformat)
        
        def run(self):
                config.read(r'C:\Users\kai.hsu\Desktop\KAI\python\python3\IT3\config.ini')
                for key, value in config.items('SSL'):
                        now = datetime.datetime.now()
                        try:
                                expire = self.ssl_expiry_datetime(key, value)
                                diff = expire - now
                                expire_new = expire.strftime("%Y-%m-%d")
                                ssl = "域名": " + (str(key)) + "  Expiry Date: " + (str(expire_new)) + "  Expiry Day: " +  (str(diff.days))
                                self.update.emit(ssl)
                                print(ssl)
                                
                                
                        except Exception as e:
                                self.error.emit(e)
                                print (e)     


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
