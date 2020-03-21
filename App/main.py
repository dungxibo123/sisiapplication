import discord,asyncio, data
from commitee import Commitee as commitee
from discord.ext import commands
token = data.token
bot = commands.Bot(command_prefix = '$')

commiteeDict = {}

@bot.command(pass_context = True)
async def hello(ctx):
    if ctx.message.channel.name.upper() in commiteeDict.keys():
        print('ok')
        await commiteeDict[ctx.message.channel.name.upper()].hello(ctx.message)
    else:
        newCommitee = commitee(ctx.message.channel.name.upper(), ctx.message.guild)
        commiteeDict.update({ctx.message.channel.name.upper(): newCommitee})
        print('ok')
        await commiteeDict[ctx.message.channel.name.upper()].hello(ctx.message)
@bot.command(pass_context = True)
async def regis(ctx):
    if ctx.message.channel.name.upper() in commiteeDict.keys():
        await commiteeDict[ctx.message.channel.name.upper()].register(ctx.message)

@bot.command(pass_context = True)
async def rollcall(ctx):
    if ctx.message.channel.name.upper() in commiteeDict.keys():
        await commiteeDict[ctx.message.channel.name.upper()].rollcall(ctx.message)

@bot.command(pass_context = True)
async def startvote(ctx):
    if ctx.message.channel.name.upper() in commiteeDict.keys():
        await commiteeDict[ctx.message.channel.name.upper()].startvote(ctx.message)
@bot.command(pass_context = True)
async def startraise(ctx):
    if ctx.message.channel.name.upper() in commiteeDict.keys():
        await commiteeDict[ctx.message.channel.name.upper()].startraise(ctx.message)

@bot.command(pass_context = True)
async def call(ctx):
    print(ctx.message.content)
    #if ctx.message.channel.name.upper() in commiteeDict.keys():
    #    commiteeDict[ctx.message.channel.name.upper()].rollCallMessage = ctx.message
@bot.event
async def on_ready():
    print('Ok connected')

@bot.event
async def on_reaction_add(reaction, user):
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
