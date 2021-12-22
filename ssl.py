import socket
import ssl
import datetime
from time import sleep
import schedule


domains_url = {
"devnote.in":443,
"devnote_wrong.in":443,
"stackoverflow.com":443,
"stackoverflow.com/status/404":443
}

def ssl_expiry_datetime(hostname, port):
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

    conn.connect((hostname, port))
    ssl_info = conn.getpeercert()
    # Python datetime object
    #傳值ssl_info['notAfter']只要'notAfter'這段內容
    #ssl_dateformat 轉換格式(西元:年 月 日 時:分:秒)

    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_dateformat)  
    
  

def run_ssl():
    
    for key, value in domains_url.items():
        now = datetime.datetime.now()
        try:
            expire = ssl_expiry_datetime(key, value)
            diff = expire - now
            expire_new = expire.strftime("%Y-%m-%d")
            ssl = "Domain name: " + (str(value)) +  "Expiry Date: " + (str(expire_new)) + "Expiry Day: " +  (str(diff.days))
            print(ssl)
            
        except Exception as e:
            print (e)



"""
schedule.every(10).seconds.do(job)
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)
"""

if __name__ == "__main__":
    schedule.every(5).seconds.do(run_ssl) #schedule 輕量級定時排程  這邊是已5秒執行一次
    while True:
        schedule.run_pending()  #開始執行排程
        sleep(1)  #系統休息一秒
        
