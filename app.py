

#from ZZZ import *
import requests,random,json,time
from flask import Flask, request
#from waitress import serve
from telegram import *
from telegram.ext import *

app=Flask(__name__)
TOKEN="1135429462:AAEWJtFWqV_x5oUy10k83zHyHa8Cm2TZS_A"
URL="https://flaskos.herokuapp.com/"

dbot=Bot(TOKEN)
#s=dbot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))


keyboard2=[[InlineKeyboardButton("pp",callback_data="end")]]
dk=InlineKeyboardMarkup(keyboard2,resize_keyboard=True)
#dk.add()

keyboard=[[InlineKeyboardButton("آزمون",callback_id=""),InlineKeyboardButton("فايل",callback_id="")]]
dk0=ReplyKeyboardMarkup(keyboard,resize_keyboard=True)


channel_id="-1001417066339"

qs={0:["Khobi?",["Are.","Na."],0],1:["Mast Siahe?",["Are.","Na."],1],2:["Shab tarike?",["Are.","Na."],0],3:["To adami?",["Are.","Na."],0]}
nq=4

def user_vaz(user_id):
    if(user_id not in vaz):return ""
    return vaz[user_id]

def checkSub(user_id):
    resp=requests.get("https://api.telegram.org/bot"+TOKEN+"/getChatMember?chat_id="+channel_id+"&user_id="+str(user_id)).json()
    if(resp["ok"]==True and resp["result"]["status"] in ["member","creator"]):return True
    return False

def start(update, context):
    print("start",update.message.from_user["id"])
    update.message.reply_text("چي ميخواي؟",reply_markup=dk0)
    update.message.reply_photo(photo=open('HDP.png', 'rb'),caption="salam")
    update.message.reply_audio(audio=open('BRUH.ogg', 'rb'),caption="Bruuu")
    update.message.reply_document(document=open('22.py', 'rb'),caption="fil")
def reaction(update,context):
    print(update.message.from_user["id"])
    if(checkSub(update.message.from_user["id"])):
        if(user_vaz(update.message.from_user["id"])==""):
            if(update.message.text in diction):
                diction[update.message.text](update,context)
            else:
                print(update.message.text,list(update.message.text))
                update.message.reply_text("حاليم نيس چي ميگي!")
        else:
            vaz_dict[vaz[update.message.from_user["id"]]](update,context)
    else:
        update.message.reply_text("به نظر ميرسه مال اين اطراف نيستي...")
        update.message.reply_text("JOIN [HERE!](http://google.com)",parse_mode="Markdown")

def quizender(update,context):
    global users_quiz,quiz_ids,vaz
    chat_id=update.from_user["id"]
    print(users_quiz[chat_id])
    if(user_vaz(chat_id)=="quizing")and(chat_id in users_quiz):#agar karbar quiz dar hal ejra dare
        n=len(users_quiz[chat_id][0])#tedad solat quizi ke karbar dare mide
        correct=0
        wrong=0
        blank=0
        for x in range(n):#x ro az 0 ta n megdar mide va har bar code zir ejra mishe
            qid=users_quiz[chat_id][0][x]#id soali ke garare tas-hih she (na id quiz tele)
            ans=users_quiz[chat_id][1][x]#pasokh sabt shode karbar (too tabe javabdad sabtesh kardim)
            print(qid,ans)
            if(ans==-1):blank+=1#agar nazade bood
            elif(ans==qs[qid][2]):correct+=1#agar zade bood va barabar ba kilid soal bood
            else:wrong+=1#age hichkodoom halataye bala nabood
        users_quiz.pop(chat_id)#karbaro az list quiz haye faal hazf kon
        vaz[chat_id]=""#vaz karbar az quiz be halat adi taghieer mikone
        update.message.reply_text("Total: "+str(n)+"Correct: "+str(correct)+"Wrong: "+str(wrong)+"Blank: "+str(blank))#karname...
        update.message.reply_text("Score: "+str(correct/n*100))
        start(update,context)#bego badesh chi mikhad
    else:#age karbar quiz faal nadasht
        update.message.reply_text("چيزي براي تموم کردن نيست")
        #baraye etminan hamechi ro yedast tamiz mikonim
        if(chat_id in users_quiz):users_quiz.pop(chat_id)
        vaz[chat_id]=""
def button(update,context):
    update=update.callback_query
    if(update.data in button_dict):
        update.answer(text="Dokme zadi")
        button_dict[update.data](update,context)
    
def javabdad(update,context):
    global users_quiz,quiz_ids
    quizid=update.poll_answer.poll_id
    userans=update.poll_answer.option_ids[0]
    chat_id=update.poll_answer.user.id
    #print(quiz_ids[quizid] , users_quiz[chat_id])
    if(chat_id in users_quiz)and(quizid in quiz_ids)and(quiz_ids[quizid] in users_quiz[chat_id][0]):
        print(8989)
        qid=quiz_ids[quizid]
        #print(qid)
        ind=users_quiz[chat_id][0].index(qid)
        users_quiz[chat_id][1][ind]=userans
        quiz_ids.pop(quizid)
def quizi(update,context):
    global users_quiz,quiz_ids
    n=3#tedad soal hayee ke mikhaim
    qids=random.sample(list(qs),n)#entekhab n ta az kilid heye dictionary qs random (entekhat id soalat)
    update.message.reply_text("آزمون شروع شد")
    users_quiz[update.message.from_user["id"]]=[qids,[-1]*n]#be karbar ba id ye quiz nesbat midim [list id soalat,list vaz pasokhgoyee (-1=nazade)]
    for x in qids:#ye halgast. be tartib azaye qids ro too x mizare va baraye hakodom code ziro ejra mikone
        dpoll=update.message.reply_poll(open_period=10+random.randint(5,15),question=qs[x][0],options=qs[x][1],correct_option_id=qs[x][2],type="quiz",is_anonymous=False)#ersal quiz ba id x
        quiz_ids[dpoll.poll.id]=x#Har soal quiz ye id ekhtesasi too telegram dare. Ma ham vase khodemoon id darim bara soala.In dictionary mige kodom id quiz tele bara kodom id soale

    update.message.reply_text("موفق باشي",reply_markup=dk)
    print(users_quiz)
def quizing (update,context): 
    update.message.reply_text("اول بايد امتحانو تموم کني")
    
def quiz (update, context):
    global vaz
    chat_id = update.message.from_user["id"]
    file = open("vip.txt", "r")
    codes = json.loads(file.read())
    file.close()
    users = list (codes.values())
    if (chat_id in users):
        vaz[chat_id]="quizing"
        quizi(update, context)
    else:
        update.message.reply_text("بايد وي آي پي شي. کدتو بده.")
        vaz[chat_id]="check"

def vipcheck(update, context):
    global vaz
    chat_id = update.message.from_user["id"]

    file = open("vip.txt","r")   
    codes = json.loads(file.read())
    file.close()
    if (update.message.text in codes) and (codes[update.message.text]==0):
        codes[update.message.text] = chat_id
        file = open("vip.txt","w")
        file.write(json.dumps(codes))
        file.close()
        update.message.reply_text("ثبت نام با موفقيت انجام شد!")
        start(update,context)
    elif(update.message in codes)and(codes[update.message.text]==chat_id):
        update.message.reply_text("gablan vip shodi!")
    else:
        update.message.reply_text("کد وارد شده صحيح نمي باشد! \n براي پيگيري از ادمين اقدام کنيد")
    vaz[chat_id]=""

def file(update,context):
    update.message.reply_text("سوال چيه ديگه؟")

karbara=[986010208]
def repoll(update,context):
    tp=update.message.poll
    chat_id=update.message.from_user["id"]   
    if(chat_id==518848442):
        pp=update.message.reply_poll(question=tp.question,options=list(map(lambda x:x.text,tp.options)))
        for x in karbara:pp.forward(x)

def vidit(update,context):
    print(234)
    dd=update.to_dict()
    vid_id=dd["channel_post"]["message_id"]#Ba zakhire in id badan mitooni be video dastresi dashte bashi
    print(dd["channel_post"]["chat"]["id"],channel_id)
    if(str(dd["channel_post"]["chat"]["id"])==channel_id):
        print("sent!")
        dbot.forwardMessage(518848442,channel_id,vid_id)

diction={"آزمون":quiz,"فايل":file}
vaz={}
vaz_dict={"check":vipcheck,"quizing":quizing}

button_dict={"end":quizender}

users_quiz={}
quiz_ids={}
updater = Updater(TOKEN,use_context=True)

@app.route('/'+TOKEN,methods=['POST'])
def respond():
    update=Update.de_json(request.get_json(force=True),dbot)

    #chat_id=update.message.chat.id
    #msg_id=update.message.message_id

    #text = update.message.text
    #print("got text message :", text)
    updater.dispatcher.process_update(update)

    return 'ok'
@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    print("set")
    s = dbot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
@app.route('/')
def index():
    print("!")
    return 'I feel alive!'




strt=CommandHandler('start',start)
reactH=MessageHandler(Filters.text,reaction)
reactP=MessageHandler(Filters.poll,repoll)
reactV=MessageHandler(Filters.video,vidit)
updater.dispatcher.add_handler(strt)
updater.dispatcher.add_handler(reactH)
updater.dispatcher.add_handler(reactP)
updater.dispatcher.add_handler(reactV)
updater.dispatcher.add_handler(PollAnswerHandler(javabdad))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

if __name__ == '__main__':app.run() #serve(app,host="0.0.0.0",port=80)#updater.idle()  #app.run()


