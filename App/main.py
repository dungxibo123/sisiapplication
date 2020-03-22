import discord,asyncio, data
from commitee import Commitee as commitee
from discord.ext import commands
token = data.token
bot = commands.Bot(command_prefix = '$')

commiteeDict = {}
@bot.event
async def on_message(message):
    print(message.content)
    mess = message.content
    if message.channel.name.upper() == 'BOT' and mess.startswith('$help'):
            await asyncio.sleep(1.23456)
            files = [discord.File('HELP.txt')]
            embed.title = 'Please read the following files!'
            await message.channel.send(content = None, files = files,embed = embed)
            return
    if not message.channel.name.upper() in commiteeDict.keys():
        newCom = commitee(message.channel.name.upper(), message.guild)
        temp = {message.channel.name.upper(): newCom}
        commiteeDict.update(temp)
    if message.channel.name.upper() in commiteeDict.keys():
        com = commiteeDict[message.channel.name.upper()]
        dele, chair, admin = com.getRoleList()

        if mess.startswith('$hello') and admin in message.author.roles:
            await com.hello(message)
        ######################################################################################
        elif mess.startswith('$regis') and dele in message.author.roles:
            await com.register(message)

        elif mess.startswith('$startraise') and message.author.roles.count(chair) > 0:
            await com.startraise(message)
        ######################################################################################
        elif mess.startswith('$startvote') and message.author.roles.count(chair) > 0:
            await com.startvote(message)
        ######################################################################################
        elif mess.startswith('$rollcall') and message.author.roles.count(chair) > 0:
            await com.rollcall(message)
        elif mess.startswith('$call'):
            com.setRollCallMessage(message)

        elif mess.startswith('$invite') and message.author.roles.count(chair) > 0:
            await com.invite(message)

        elif (mess.startswith('$over')  or mess.startswith('$muteall')) and  message.author.roles.count(chair) > 0:
            await com.muteall(message)
@bot.event
async def on_ready():
    print('Ok connected')
# @bot.event
# async def on_message(message):
#     print(message.content)
@bot.event
async def on_reaction_add(reaction, user):
    print('Found 1 reactaion add')
    try:
        roleList = reaction.message.guild.roles
    except:
        await reaction.message.channel.send('Something went wrong!')
        return
    dele = None

    for i in roleList:
        if i.name == '@delegate': dele = i
    #global isReplyTheRollCall
    name = reaction.message.channel.name.upper()
    if name in commiteeDict.keys():
        com = commiteeDict[name]
    else:
        return
    if  str(reaction.emoji) == '👍' and reaction.message == com.messageNeedToVote and user.roles.count(dele) > 0:
        com.voteYes += 1
        com.voting_Count += 1
    elif  str(reaction.emoji) == '👎'and reaction.message == com.messageNeedToVote and user.roles.count(dele) > 0:

        com.voteNo += 1
        com.voting_Count += 1
    elif str(reaction.emoji) == '😃' and reaction.message == com.messageNeedToVote and user.roles.count(dele) > 0:
        com.whiteVote += 1
        com.voting_Count += 1
    elif str(reaction.emoji) == '👍' and reaction.message == com.raiseMessage and user.roles.count(dele) > 0:
        print('Found 1 want to raise')
        com.raiseList.append(user)
    elif str(reaction.emoji) == '👍' and reaction.message == com.rollCallMessage and user == com.memberNeedtoReply:
        com.isReplyTheRollCall = True

@bot.event
async def on_reaction_remove(reaction,user):
    try:
        roleList = reaction.message.guild.roles
    except:
        await reaction.message.channel.send('Something went wrong!')
        return
    dele = None

    for i in roleList:
        if i.name == '@delegate': dele = i
    #global isReplyTheRollCall
    name = reaction.message.channel.name.upper()
    if name in commiteeDict.keys():
        com = commiteeDict[name]
    else:
        return
    if  str(reaction.emoji) == '👍' and reaction.message == com.messageNeedToVote and user.roles.count(dele) > 0:
        #print(1111)
        com.voteYes -= 1
        com.voting_Count -= 1
    elif  str(reaction.emoji) == '👎'and reaction.message == com.messageNeedToVote and user.roles.count(dele) > 0:
        #print(111)
        com.voteNo -= 1
        com.voting_Count -= 1
    elif str(reaction.emoji) == '😃' and reaction.message == com.messageNeedToVote and user.roles.count(dele) > 0:
        com.whiteVote -= 1
        com.voting_Count -= 1
    elif str(reaction.emoji) == '👍' and reaction.message == com.raiseMessage and user.roles.count(dele) > 0:
        com.raiseList.remove(user)
        ####################################


bot.run(token)
