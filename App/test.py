import discord
import asyncio
import data
token = data.token
nations = data.nations
#Njg4MzIyMDQxODM2NzMyNTY4.Xm87hA.QkYgsyYUGQ3dsxkCj9r1CggbItw
'''class MyClient inherit discord.Client create a connection to Bot and we
can easily use Python to send command through discord Server'''
bot = discord.Client()





##############################
voting_Count = 0             #
voteYes = 0                  # Table of something  Idc
voteNo = 0                   #
whiteVote = 0                #
messageNeedToVote = None     #
##############################

##############################
raiseList = []               #
raiseMessage = None          #
##############################


'''roll call box'''
##############################
rollCallMessage = None       #
memberNeedtoReply = None     #
isReplyTheRollCall = False   #
##############################


def validCountry(country):
    if nations.count(country) > 0: return True
    return False

def setRegisterationResquest(message,country,role):
    pass


@bot.event
async def on_ready():
    print('Ok connected')




@bot.event
async def on_message(message):
    print(message.content   )
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
            global raiseList
            raiseList = []
            time = 30
            try:
                time = float(mess.split(' ')[1])
                await message.channel.send('You got {} seconds to raise your hand by reacting 👍 to $startraise message', time)
            except Exception as e:
                await message.channel.send('Error with time, automatic time is 15 seconds to raise your hand by reacting 👍 to $startraise message')
                time = 15
            global raiseMessage
            raiseMessage = message
            await asyncio.sleep(time)
            notification = 'Numbers of Delegates want to raise hand: {}'.format(len(raiseList))
            for i in raiseList:
                notification += '\n{}'.format(i.mention)
            await message.channel.send(notification)
            
        ######################################################################################
        elif mess.startswith('$startvote') and message.author.roles.count(CHAIR) > 0:
            voteYes = 0
            voteNo = 0
            whiteVote = 0
            voting_Count = 0
            messageNeedToVote = message
            print('Update new message that need to vote')
            try:
                time = float(mess.split(' ')[1])
            except Exception as e:
                await message.channel.send('Error with time, automatic time is 20 seconds for voting stuff')
                time = 20
            await asyncio.sleep(time)
            await message.channel.send('Numbers of agree: {}\nNumbes of disagree: {}\nNumbers of white-vote: {}\nUnvoted: {}'.format(voteYes,voteNo,whiteVote,del_Nums - voteYes - voteNo - whiteVote))
            #đặt lại số lượng người biểu quyết
        ######################################################################################
        elif mess.startswith('$rollcall') and message.author.roles.count(CHAIR) > 0:
            global memberNeedtoReply,rollCallMessage, isReplyTheRollCall
            roleList = message.guild.roles
            DEL = None
            CHAIR = None
            absentList = []
            onlineList = []
            for i in roleList:
                if i.name == '@delegate': DEL = i
                if i.name == '@chair': CHAIR = i
            delList = DEL.members

            for i in delList:
                memberNeedtoReply = i
                await message.channel.send('$call {}. You have 5 seconds to react 👍 on this message'.format(i.mention))
                await asyncio.sleep(5)
                if isReplyTheRollCall:
                    onlineList.append(i)
                else:
                    absentList.append(i)
                isReplyTheRollCall = False
   
            roll = 'Absent delegate(s):'
            for i in absentList: roll += '\n{}'.format(i.mention)
            roll+='\nOnline delegate(s):'
            for i in onlineList: roll += '\n{}'.format(i.mention)
            print(roll)
            await message.channel.send(roll)
        elif mess.startswith('$call'):
            rollCallMessage = message
            print('\n\n\n\nrollcall messageeeeeeeeeeeeeeeee changed:\n\n\n\n')

        elif mess.startswith('$invite') and message.author.roles.count(CHAIR) > 0:
            try:
                memberMentioned = message.mentions[0]
            except:
                await message.channel.send('Invalid Invitation because no one was found on $invite message')
                return 
            voiceChannelList = message.guild.voice_channels
            mainVoiceChannel = None
            for i in voiceChannelList:
                if i.name.upper() == message.channel.name.upper(): mainVoiceChannel = i
            memberList = mainVoiceChannel.members
            if memberMentioned in memberList:
                await memberMentioned.edit(mute = False, reason = None)
        elif (mess.startswith('$over')  or mess.startswith('$muteall')) and  message.author.roles.count(CHAIR) > 0:
            try:
                await message.mentions[0].edit(mute = True, reason = None)
                await message.channel.send('Over speech of {}'.format(message.mentions[0].nick))
            except:
                print('Mute all confirmed')
                await message.channel.send('Mute all')
                for member in message.guild.members:
                    if member.roles.count(CHAIR) == 0:
                        await member.edit(mute = True, reason = None)
        
                
            

            
           


            

@bot.event
async def on_reaction_add(reaction, user):
    try:
        roleList = reaction.message.guild.roles
    except:
        await reaction.message.channel.send('Something went wrong!')
        return
    DEL = None
#    CHAIR = None
    #print('Got an reaction from guild! ')
    for i in roleList:
        if i.name == '@delegate': DEL = i
#        if i.name == '@chair': CHAIR = i
#    del_Nums = len(DEL.members)
    global isReplyTheRollCall
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
    elif str(reaction.emoji) == '👍' and reaction.message == rollCallMessage and user == memberNeedtoReply:
        isReplyTheRollCall = True
        
@bot.event
async def on_reaction_remove(reaction,user):
    roleList = reaction.message.guild.roles
    DEL = None
    #print('Got an reaction from guild! ')
    for i in roleList:
        if i.name == '@delegate': DEL = i
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


bot.run(token)