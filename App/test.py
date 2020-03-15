import discord
token = 'Njg4MzIyMDQxODM2NzMyNTY4.Xm3lxA.pDaNSl5ImMOtl-lyM_TpXI0r3Mw'

'''class MyClient inherit discord.Client create a connection to Bot and we
can easily use Python to send command through discord Server'''
bot = discord.Client()
HPC = 688332663098048532

COUNTRIES = ['VIETNAM', 'IRAQ']

def validCountry(country):
    if COUNTRIES.count(country) > 0: return True
    return False

def setRegisterationResquest(message,country,role):
    pass
@bot.event
async def on_message(message):

    mess = message.content  
    if mess.startswith('$'):
        if mess.startswith('$regis'):
            try:
                roleList = message.guild.roles
                DEL = None
                CHAIR = None
                for i in roleList:
                    if i.name == '@delegate': DEL = i
                country = mess.split(' ')[1].upper()
                if validCountry(country):
                    member = message.author
                    if member.roles.count(DEL) > 0:
                        await message.channel.send('UNVALID ACTIVITY\n{} have already register as {}'.format(member.name,member.nick))
                    else:
                        await member.edit(nick = country,roles = [DEL], reason = None)
                        await message.channel.send('Succesfully registered as {}'.format(country))
                        

            except Exception as e:
                await message.channel.send('Invalid Country or Invalid Guild\'s Input')
                raise e
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