#屏幕 1440*900 windows7 包裹浏览器地址栏，和下面桌面菜单栏
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
         Region(186,607,287,186).inside().click("1415556959371.png")
    elif line==2:
         Region(186,607,287,186).inside().click("1415556982408.png")
    elif line==3:
         Region(186,607,287,186).inside().click("1415557005501.png")
    elif line==4:
         Region(186,607,287,186).inside().click("1415557039003.png")
    elif line==5:
         Region(186,607,287,186).inside().click("1415557058484.png")
        
    wait(10)
    Region(339,621,68,70).inside().click("1415557394923.png")
    
    
    
    wait(10)
    Region(339,621,68,70).inside().click("1415557434527.png")
    
    
    logging.info("切换线路："+str(line))
    
#读取配置文件，设置日志系统    
config = ConfigParser.RawConfigParser()
config.read('config.properties')
logging.basicConfig(filename='example.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%Y/%d/%m %H:%M:%S %p')
       
#禁止鼠标移动延时
Settings.MoveMouseDelay =0.5
Settings.SlowMotionDelay=0.5

#赢的次数
winCount=int(config.get('WinLoseCount', 'winCount'));
#输的次数
loseCount=int(config.get('WinLoseCount', 'loseCount'));
name=config.get('WinLoseCount', 'name')

logging.info("初始化参数winCount:"+str(winCount))
logging.info("初始化参数loseCount:"+str(loseCount))


#检查是否可以下注
flag=0
while(True):
    try:

        logging.info("检查是否符合开局结果")
        past = datetime.now()
        while(True):
                if Region(960,321,43,57).inside().exists(Pattern("1415595384222.png").similar(0.80),3):
                    break
                
                  
                elif Region(960,321,43,57).inside().exists(Pattern("1415596000971.png").similar(0.80),0):
                    break
               
                now = datetime.now()
                pastSeconds=(now-past).seconds
                if pastSeconds>60*3:
                    logging.info("等待结算时间过长")
                    loseCount=0
                    break
        
        
        logging.info("等待下注")
        try:
           Region(898,548,212,212).inside().wait("1415556232362.png",10*60)
        except:     
           logging.info("等待开局失败，切换线路")     
           restart()
        
        #选择筹码
        logging.info("选择筹码")
        Region(445,574,471,153).inside().click("1415556359027.png")
       
    
        #下注
        logging.info("下注")
        Region(337,453,189,168).inside().hover("1415556570732.png")
      
        
        betCount=0
        if loseCount==0:
            mouseDown(Button.LEFT)
            mouseUp()
        else:
            #规避风险，可以多翻一倍
            #if(loseCount>=1):
             #   betCount=loseCount-1
             #   if loseCount==1:
              #      winCount=winCount-1
            #else:
            betCount=loseCount
                
            for x in range(2**betCount):
                wait(0.1)
                mouseDown(Button.LEFT)
                mouseUp()
    
        #点击确认下注
        logging.info("确认下注："+str(2**betCount))
        Region(898,548,212,212).inside().click("1415556232362.png")


        logging.info("等待下注结束")
    
        hasStop=Region(898,548,212,212).inside().waitVanish("1415556232362.png",60*3)
        if not hasStop:
           logging.info("等待下注失败，切换线路")     
           restart()
            
        #等待结果
        logging.info("等待发牌结束")
        past = datetime.now()
        while(True):
            if Region(464,488,523,267).inside().exists("1415556682240.png",0):
            
                #统计输赢次数
                if Region(464,488,523,267).inside().exists("1415556801768.png",0):
                    winCount=winCount+1
                    loseCount=0
                    logging.info("结果：赢")
                elif Region(464,488,523,267).inside().exists("1415557766219.png",0):
                    loseCount=loseCount+1
                    logging.info("结果：输")
                break
            elif Region(898,548,212,212).inside().exists("1415556232362.png",0):
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

        if loseCount>7:
            loseCount=0;
        
        if winCount==100:
            logging.info("恭喜你，今天任务完成！")
            send_email("恭喜你"+name+"，今天任务完成！")
            break;
        
        #返回第一步重新开始
    except:
        logging.info(name+"出现错误")
        send_email(name+"出现错误"+traceback.format_exc())
        logging.error(traceback.format_exc())
        
        

