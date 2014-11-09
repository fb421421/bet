#屏幕 1366*678 windows7 包裹浏览器地址栏，和下面桌面菜单栏
from datetime import datetime, date, time
import logging
import ConfigParser
import smtplib
import random
import traceback
import sys

def send_email(content):
            gmail_user = "fb421421@gmail.com"
            gmail_pwd = "uuyy880211"
            FROM = 'fb421421@gmail.com'
            TO = ['fb421421@gmail.com'] #must be a list
            SUBJECT = "Testing sending using gmail"
            TEXT = content

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
                print 'successfully sent the mail'
            except:
                print "failed to send mail"

def writeProperty(config, name , value):
    config.set('WinLoseCount', name,value);
    with open('config.properties', 'wb') as configfile:
        config.write(configfile)

def restart():
    line=random.randint(1, 5)
    if line==1:
         Region(256,571,202,66).inside().click("1415471095183.png")
    elif line==2:
         Region(256,571,202,66).inside().click("1415471137742.png")
    elif line==3:
         Region(256,571,202,66).inside().click("1415471166215.png")
    elif line==4:
         Region(256,571,202,66).inside().click("1415471189433.png")
    elif line==5:
         Region(256,571,202,66).inside().click("1415471206482.png")
        
    wait(10)
    Region(300,538,114,49).inside().click("1415472178524.png")
    
    
    
    wait(10)
    Region(297,529,117,60).inside().click("1415472205466.png")
    
    
    logging.info("切换线路："+str(line))
    
#读取配置文件，设置日志系统    
config = ConfigParser.RawConfigParser()
config.read('config.properties')
logging.basicConfig(filename='example.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%Y/%d/%m %H:%M:%S %p')
       
#禁止鼠标移动延时
Settings.MoveMouseDelay = 0
#赢的次数
winCount=int(config.get('WinLoseCount', 'winCount'));
#输的次数
loseCount=int(config.get('WinLoseCount', 'loseCount'));
name=config.get('WinLoseCount', 'name')

logging.info("初始化参数winCount:"+str(winCount))
logging.info("初始化参数loseCount:"+str(loseCount))


#检查是否可以下注
while(True):
    try:

        logging.info("检查是否符合开局结果")

        try:
            Region(210,613,419,108).inside().wait("1415469765357.png",60*10)
        except:
            logging.info("等待结算时间过长")
            restart()
        
        
        logging.info("等待下注")
        hasStart=Region(760,413,392,265).inside().wait("1415456736137.png",10*60)
        if not hasStart:
           logging.info("等待开局失败，切换线路")     
           restart()
        
        #选择筹码
        logging.info("选择筹码")
        Region(467,503,373,111).inside().click("1415458560817.png")
    
        #下注
        logging.info("下注")
        Region(328,362,236,226).inside().hover("1415459252324.png")
        
        betCount=0
        if loseCount==0:
            mouseDown(Button.LEFT)
            mouseUp()
        else:
            #规避风险，可以多翻一倍
            if(loseCount>=1):
                betCount=loseCount-1
            else:
                betCount=loseCount;
                
            for x in range(2**betCount):
                wait(0.1)
                mouseDown(Button.LEFT)
                mouseUp()
    
        #点击确认下注
        logging.info("确认下注："+str(2**betCount))
        Region(838,438,288,195).inside().click("1415456736137.png")


        logging.info("等待下注结束")
    
        hasStop=Region(838,438,288,195).inside().waitVanish("1415456736137.png",60*3)
        if not hasStop:
           logging.info("等待下注失败，切换线路")     
           restart()
            
        #等待结果
        logging.info("等待发牌结束")
        past = datetime.now()
        while(True):
            sleep(0.1)
            if Region(472,431,456,190).inside().exists("1415459624895.png",0):
            
                #统计输赢次数
                if Region(466,432,445,190).inside().exists("1415460987621.png",0):
                    winCount=winCount+1
                    loseCount=0
                    logging.info("结果：赢")
                elif Region(466,432,445,190).inside().exists("1415460966925.png",0):
                    loseCount=loseCount+1
                    logging.info("结果：输")
                break
            elif Region(786,416,359,266).inside().exists("1415456736137.png",0):
                logging.info("结果：和")
                break
           
            now = datetime.now()
            pastSeconds=(now-past).seconds
            if pastSeconds>60*10:
                logging.info("等待结算时间过长："+str(pastSeconds))
                restart()
            
       
        #处理结果
        writeProperty(config,'winCount',str(winCount))
        writeProperty(config,'loseCount',str(loseCount))
        logging.info("赢:"+str(winCount))
        logging.info("输:"+str(loseCount))
        
        if winCount==100:
            logging.info("恭喜你，今天任务完成！")
            send_email("恭喜你"+name+"，今天任务完成！")
            break;
        
        #返回第一步重新开始
    except:
        logging.info(name+"出现错误")
        send_email(name+"出现错误"+traceback.format_exc())
        logging.error(traceback.format_exc())
        
        

