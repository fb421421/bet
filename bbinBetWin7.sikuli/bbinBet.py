#屏幕 1366*678 windows7 包裹浏览器地址栏，和下面桌面菜单栏
from datetime import datetime, date, time
import logging
import ConfigParser
import smtplib

config = ConfigParser.RawConfigParser()
config.read('config.properties')

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
    import random
    line=random.randint(1, 5)
    if line==1:
        click("1415471095183.png")
    elif line==2:
        click("1415471137742.png")
    elif line==3:
        click("1415471166215.png")
    elif line==4:
        click("1415471189433.png")
    elif line==5:
        click("1415471206482.png")
        
    wait(10)
    Region(300,538,114,49).inside().click("1415472178524.png")
    
    
    
    wait(10)
    Region(297,529,117,60).inside().click("1415472205466.png")
    
    
    print "切换线路："+str(line)
    
    

logging.basicConfig(filename='example.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%Y/%d/%m %H:%M:%S %p')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')        

Settings.MoveMouseDelay = 0

#赢的次数
winCount=int(config.get('WinLoseCount', 'winCount'));

#输的次数
loseCount=int(config.get('WinLoseCount', 'loseCount'));

print    winCount
print    loseCount
writeProperty(config,'winCount',str(winCount+1))

#检查是否可以下注
while(True):
    try:        
        #wait("1415469765357.png",FOREVER)
        
        
        #hasStart=wait("1415456736137.png",10*60)

        #if hasStart:
           #print "开始下注"     
        #else:
            #restart()
        
        #选择筹码
        click("1415458560817.png")
    
        #下注
        hover("1415459252324.png")
    
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
        click("1415456736137.png")
    
        hasStop=waitVanish("1415456736137.png",60*3)
        if hasStop:
           print "下注结束"     
        else:
            restart()
            
        #等待结果
        past = datetime.now()
        while(True):
            sleep(0.1)
            if exists("1415459624895.png",0):
            
                #统计输赢次数
                if exists("1415460987621.png",0):
                    winCount=winCount+1
                    loseCount=0
                    print "结果：赢"
                elif exists("1415460966925.png",0):
                    loseCount=loseCount+1
                    print "结果：输"
                break
            elif exists("1415456736137.png",0):
                print "结果：和"
                break
           
            now = datetime.now()
            pastSeconds=(now-past).seconds
            if pastSeconds>60*10:
                print "等待结算时间过长："+str(pastSeconds)
                restart()
            
            
    
       
        #处理结果
        print  "赢:"
        print  winCount
        print  "输:"
        print  loseCount
        
        if winCount==100:
            send_email("success!")
            break;
        
        #返回第一步重新开始
    except e:
        print e

    
send_email("failed!")

