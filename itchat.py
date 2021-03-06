########################################  turing robot  ###################
import requests

apiUrl = 'http://www.tuling123.com/openapi/api'
data = {
    'key'    : '43e9f7a578e543c29f1e264925be721e', # 如果这个Tuling Key不能用，那就换一个
    'info'   : 'hello', # 这是我们发出去的消息
    'userid' : '123', # 这里你想改什么都可以
}

def get_echo(s):
    data['info']=s
    r = requests.post(apiUrl, data=data).json()
    return r['text']
######################  log in  ####################################################
import time
from itchat.content import *
import itchat
msgs=[]
revokedic=dict()
robotqueue=[]
revokequeue=[]
itchat.auto_login(hotReload=True,)

def robot_send(s,un):
    itchat.send('<robot>['+time.ctime()[-13:-5]+']:\n'+s,un) 
####################################  username to remarkname  ############
namedic=dict()
for x in itchat.get_friends():
    namedic[x['UserName']]=x['RemarkName']
for x in itchat.get_chatrooms():
    namedic[x['UserName']]=x['NickName']
def get_name(x):
    return namedic.get(x,x)
def explain(msg):
    for x in msg:
        if isinstance(msg[x],str) and msg[x].startswith('@'):
            msg[x]=get_name(msg[x])
    return msg
#################  start common msg log ######################################
itchat.run(0,0)

@itchat.msg_register([ATTACHMENT,CARD,FRIENDS,MAP,NOTE,PICTURE,RECORDING,SHARING,SYSTEM,TEXT,VIDEO], isFriendChat=True, isGroupChat=True, isMpChat=True)
def download_files(msg):
    print('receive a message')
    msgs.append(msg)


##################### robot enter leave ###############################
auto_target=[]
for tgt in auto_target:
    itchat.send('',tgt)
auto_target=[]
######################  robot routine ##############################
@itchat.msg_register([TEXT,PICTURE], isFriendChat=True, isGroupChat=True, isMpChat=True)
def robot(msg):
    revokedic[msg['MsgId']]=msg['Text']
    msgs.append(msg)
    #print(msg)
    if msg['FromUserName'] in auto_target:
        robot_send(get_echo(msg['Text']),msg['FromUserName'])
        if robotqueue:
            robot_send(robotqueue.pop(0),msg['FromUserName'])

#######################  revoke routine ######################################
def get_revoked_text(msg):
    try:
        txt=msg['Content']
        pos1=txt.find('<msgid>')+7
        pos2=txt.find('<',pos1)
        return '撤消内容是：“'+revokedic[txt[pos1:pos2]]+'”'
    except:
        return '撤消的数据块已入库。'


@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True, isMpChat=True)
def show_revoke(msg):
    msgs.append(msg)
    un=msg['FromUserName']
    if '@@' not in un:
        un=msg['ToUserName']
    #print(msg)
    print('%s: %s' % (msg['Type'], msg['Text']), get_name(msg['FromUserName']))
    if '<sysmsg type="revokemsg">' in msg['Content']:
        themsg='<tiri>:'+get_revoked_text(msg)+now()
        print(themsg)
        robot_send(themsg,un)
        if revokequeue:
            robot_send(revokequeue.pop(0),un)

#########################################################
#@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True, isMpChat=True)
#def download_files(msg):
#    msg['Text'](msg['FileName'])
#    print(msg['FileName'])
#    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

#%%

robotqueue=['彬仔让我说话前加上<tiri>:这样我说什么邪恶的话他能撇清干系[难过]。',\
'我还能反撤消你们的消息，话说彬仔怎么开发了这么个邪恶的功能尼？',\
'我能用互联网查天气哦，你问我哪里的天气，我就能查给你。',\
'我还能查日期之类的，还很基本，以后慢慢来，互联网会变成我的数据库，前景好曼妙的赶脚。。',\
'不过性别年龄之类的敏感信息还是不要问了',\
'相比之下，我妹siri就是个家庭主妇，不过你们要善待她啊。',\
]

revokequeue=['撤销的文本我直接显示出来，撤销的其它东西，直接保存到电脑里，彬仔说这样能节省大家的流量。。。',\
'我都有点不好yi xi了[偷笑]',\
'好邪恶的功能呢'\
]

robotqueue=[]
revokequeue=[]

def set_auto_reply():
    li=[(x["NickName"],x["UserName"]) for x in itchat.get_chatrooms()]
    for n,x in enumerate(li):
        print('%-3d %-5s %-20s '%(n+1,'yes'if x[1] in auto_target else 'no',x[0][:20]))
    import re
    ns=re.findall('\\d+',input('number to change:'))
    for x in map(int,ns):
        if li[x-1][1] in auto_target:
            auto_target.remove(li[x-1][1])
        else:
            auto_target.append(li[x-1][1])    