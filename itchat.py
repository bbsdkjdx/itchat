
import requests

apiUrl = 'http://www.tuling123.com/openapi/api'
data = {
    'key'    : '43e9f7a578e543c29f1e264925be721e', # 如果这个Tuling Key不能用，那就换一个
    'info'   : 'hello', # 这是我们发出去的消息
    'userid' : 'wechat-robot', # 这里你想改什么都可以
}

def get_echo(s):
    data['info']=s
    r = requests.post(apiUrl, data=data).json()
    return r['text']
# 让我们打印一下返回的值，看一下我们拿到了什么



from itchat.content import *
import itchat
msgs=[]
msgdic=dict()

itchat.auto_login(hotReload=True,)
####################################username to remarkname
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
#######################################################
itchat.run(0,0)

for x in itchat.get_chatrooms():
    print(x["NickName"])
    print(x["UserName"])
    print()

auto_target=[]
for tgt in auto_target:
    itchat.send('大家好，我是siri她哥，我叫tiri，主人手机刚设置静音，应该是休息了，我可以陪大家聊天哦！[呲牙]',tgt)

for tgt in auto_target:
    itchat.send('大家好，我是tiri，主人又让我出来了，如果嫌我吵，@我哦',tgt)

for tgt in auto_target:
    itchat.send('主人的静音取消了，应该是刚被开完会，再聊哦，tiri会想念大家的，么么哒',tgt)
auto_target=[]

@itchat.msg_register([TEXT,PICTURE], isFriendChat=True, isGroupChat=True, isMpChat=True)
def robot(msg):
    msgdic[msg['MsgId']]=msg['Text']
    msgs.append(msg)
    print(msg['Text'])
    if msg['FromUserName'] in auto_target:
        itchat.send(get_echo(msg['Text']),msg['FromUserName'])
   # print('%s: %s' % (msg['Type'], msg['Text']), msg['FromUserName'])
    #print(get_name(msg['FromUserName']),':',msg.get('ActualNickName',''),'->',get_name(msg['ToUserName']),msg['Text'])


#############################################################
def get_revoked_text(msg):
    try:
        txt=msg['Content']
        pos1=txt.find('<msgid>')+7
        pos2=txt.find('<',pos1)
        return '撤消内容是：“'+msgdic[txt[pos1:pos2]]+'”'
    except:
        return '撤销的消息非文字，我把附件存到电脑了，以防耗费大家流量，需要的话找我主人要。'


@itchat.msg_register([NOTE], isFriendChat=True, isGroupChat=True, isMpChat=True)
def show_revoke(msg):
    msgs.append(msg)
    un=msg['FromUserName']
    if '@@' not in un:
        un=msg['ToUserName']
    #print(msg)
    print('%s: %s' % (msg['Type'], msg['Text']), get_name(msg['FromUserName']))
    if '<sysmsg type="revokemsg">' in msg['Content']:
        themsg=get_revoked_text(msg)
        print(themsg)
        itchat.send(themsg,un)
        #itchat.send(txt,un)
#########################################################
#@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True, isMpChat=True)
#def download_files(msg):
#    msg['Text'](msg['FileName'])
#    print(msg['FileName'])
#    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register([ATTACHMENT,CARD,FRIENDS,MAP,NOTE,PICTURE,RECORDING,SHARING,SYSTEM,TEXT,VIDEO], isFriendChat=True, isGroupChat=True, isMpChat=True)
def download_files(msg):
    print('msg received.')
    msgs.append(msg)
#%%

