import discord
from time import sleep
token = 'Njg4MzIyMDQxODM2NzMyNTY4.Xm3lxA.pDaNSl5ImMOtl-lyM_TpXI0r3Mw'

'''class MyClient inherit discord.Client create a connection to Bot and we
can easily use Python to send command through discord Server'''
bot = discord.Client()
HPC = 688332663098048532

COUNTRIES = ['VIETNAM', 'IRAQ']


##############################
voting_Count = 0             #
voteYes = 0                  # Table of something  Idc
voteNo = 0                   #
whiteVote = 0                #
messageNeedToVote = None     #
##############################

##############################
raiseList = []               #
raiseMessage = None           #
##############################
def validCountry(country):
    if COUNTRIES.count(country) > 0: return True
    return False

def setRegisterationResquest(message,country,role):
    pass


@bot.event
async def on_ready():
    print('Ok connected ')

@bot.event
async def on_message(message):
    global voting_Count,voteNo,voteYes,messageNeedToVote
    mess = message.content  
    roleList = message.guild.roles
    DEL = None
    CHAIR = None
    
    for i in roleList:
        if i.name == '@delegate': DEL = i
        if i.name == '@chair': CHAIR = i
    del_Nums = len(DEL.members)
    
    if mess.startswith('$'):
        ######################################################################################
        if mess.startswith('$regis'):
            try:
                country = mess.split(' ')[1].upper()
                if validCountry(country):
                    member = message.author
                    if member.roles.count(DEL) > 0:
                        await message.channel.send('UNVALID ACTIVITY\n{} have already registered as {}'.format(member.name,member.nick))
                    else:
                        await member.edit(nick = country,roles = [DEL], reason = None)
                        await message.channel.send('Succesfully registered as {}'.format(country))
                        

            except Exception as e:
                await message.channel.send('Invalid Country or Invalid Guild\'s Input')
                raise e
                #send message, invalid country
        ######################################################################################
        elif mess.startswith('$startraise') and message.author.roles.count(CHAIR) > 0:
            print('Update message to raising hand')
            time = 30
            try:
                time = float(mess.split(' ')[1])
            except Exception as e:
                await message.channel.send('Error with time, automatic time is 15 seconds for voting stuff')
                time = 30
            global raiseMessage
            raiseMessage = message
            sleep(time)
            notification = 'Numbers of Delegates want to raise hand: {}'.format(len(raiseList))
            for i in raiseList:
                notification += '\n{}'.format(i.nick)
            await message.channel.send(notification)
            
        ######################################################################################
        elif mess.startswith('$startvote') and message.author.roles.count(CHAIR) > 0:
            voteYes = 0
            voteNo = 0
            voting_Count = 0
            
            messageNeedToVote = message
            print('Update new message that need to vote')
            #đặt lại số lượng người biểu quyết
        ######################################################################################
        elif mess.startswith('$send'):
            #$send <message> to <country>
            #gửi private message cho thằng quỷ <country>
            pass


@bot.event
async def on_reaction_add(reaction, user):
    roleList = reaction.message.guild.roles
    DEL = None
    CHAIR = None
    #print('Got an reaction from guild! ')
    for i in roleList:
        if i.name == '@delegate': DEL = i
        if i.name == '@chair': CHAIR = i
    del_Nums = len(DEL.members)
    #print('numbers of del: {}'.format(del_Nums))

    global voteNo,voteYes,voting_Count, whiteVote,raiseList

    #print(messageNeedToVote, str(reaction.emoji))
    #print(str(reaction.emoji) == '👍') 
    if  str(reaction.emoji) == '👍' and reaction.message == messageNeedToVote and user.roles.count(DEL) > 0:
        #print(1111)
        voteYes += 1
        voting_Count += 1
    elif  str(reaction.emoji) == '👎'and reaction.message == messageNeedToVote and user.roles.count(DEL) > 0:
        #print(111)
        voteNo += 1
        voting_Count += 1
    elif str(reaction.emoji) == '😃' and reaction.message == messageNeedToVote and user.roles.count(DEL) > 0:
        whiteVote += 1
        voting_Count += 1
    elif str(reaction.emoji) == '👍' and reaction.message == raiseMessage and user.roles.count(DEL) > 0:
        raiseList.append(user)

    if voting_Count == del_Nums:
        await reaction.message.channel.send('Numbers of agree: {}\nNumbes of disagree: {}\nNumbers of white-vote: {}'.format(voteYes,voteNo,whiteVote))
@bot.event
async def on_reaction_remove(reaction,user):
    roleList = reaction.message.guild.roles
    DEL = None
    #print('Got an reaction from guild! ')
    for i in roleList:
        if i.name == '@delegate': DEL = i
        if i.name == '@delegate': CHAIR = i
    #print('numbers of del: {}'.format(del_Nums))

    global voteNo,voteYes,voting_Count, whiteVote, raiseList

    #print(messageNeedToVote, str(reaction.emoji))
    #print(str(reaction.emoji) == '👍') 
    if  str(reaction.emoji) == '👍' and reaction.message == messageNeedToVote and user.roles.count(DEL) > 0:
        #print(1111)
        voteYes -= 1
        voting_Count -= 1
    elif  str(reaction.emoji) == '👎'and reaction.message == messageNeedToVote and user.roles.count(DEL) > 0:
        #print(111)
        voteNo -= 1
        voting_Count -= 1
    elif str(reaction.emoji) == '😃' and reaction.message == messageNeedToVote and user.roles.count(DEL) > 0:
        whiteVote -= 1
        voting_Count -= 1
    elif str(reaction.emoji) == '👍' and reaction.message == raiseMessage and user.roles.count(DEL) > 0:
        raiseList.remove(user)
        ####################################



@bot.event 
async def on_member_join(member):
    if len(member.role) == 0:
        pass
        #sent through bot TextChannel that something went wrong
        
# @bot.event
# async def on_member_join(member):
#         print(member.name)

bot.run(token)