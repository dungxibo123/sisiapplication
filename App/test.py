import discord
token = 'Njg4MzIyMDQxODM2NzMyNTY4.XmyqgQ.tkA-imK5DXuX9OAhsRw8nEqxuMY'

'''class MyClient inherit discord.Client create a connection to Bot and we
can easily use Python to send command through discord Server'''
bot = discord.Client()
HPC = 688332663098048532

COUNTRIES = ['VIETNAM', 'IRAG']

def validCountry(country):
    if COUNTRIES.count(country) > 0: return True
    return False


@bot.event
async def on_message(message):
    mess = message.content
    roleList = message.guild.roles
    DEL = None
#   CHAIR = None
    for i in roleList:
        if i.name == '@delegate': DEL = i
    if mess.startswith('$'):
        if mess.startswith('$regis'):
            country = mess.split(' ')[1].upper()
            if validCountry(country):
                #setNickname, role as delegate
                member = message.author
                await member.edit(nick = country,roles = [DEL], reason = None)

            else:
                pass
                #send message, invalid country
        elif mess.startswith('$raise'):
            #gửi cho chair private kêu rằng thằng ni muốn nói cái gì đó :V
            pass
        elif mess.startswith('disagree') or mess.startswith('agree'):
            pass
            #đếm số lượng người biểu quyết
        elif mess.startswith('$send'):
            #$send <message> to <country>
            #gửi private message cho thằng quỷ <country>
            pass
@bot.event 
async def on_member_join(member):
    if len(member.role) == 0:
        pass
        #sent through bot TextChannel that something went wrong
        
# @bot.event
# async def on_member_join(member):
#         print(member.name)

bot.run(token)