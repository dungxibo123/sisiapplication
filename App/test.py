import discord
token = 'Njg4MzIyMDQxODM2NzMyNTY4.Xm3lxA.pDaNSl5ImMOtl-lyM_TpXI0r3Mw'

'''class MyClient inherit discord.Client create a connection to Bot and we
can easily use Python to send command through discord Server'''
bot = discord.Client()
HPC = 688332663098048532

COUNTRIES = ['VIETNAM', 'IRAQ']
voting_Count = 0
voteYes = 0
voteNo = 0
def validCountry(country):
    if COUNTRIES.count(country) > 0: return True
    return False

def setRegisterationResquest(message,country,role):
    pass
@bot.event
async def on_message(message):
    global voting_Count,voteNo,voteYes
    mess = message.content  
    roleList = message.guild.roles
    DEL = None
    CHAIR = None
    
    for i in roleList:
        if i.name == '@delegate': DEL = i
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
        elif mess.startswith('$raise'):
            #gửi cho chair private kêu rằng thằng ni muốn nói cái gì đó :V
            pass




        ######################################################################################
        elif mess.startswith('$startvote') and message.author.roles.count(CHAIR) > 0:
            voteYes = 0
            voteNo = 0
            voting_Count = 0
        elif mess.startswith('$agree') or mess.startswith('$disagree'):
            if mess.startswith('$agree'):
                voteYes += 1
                print('yes', voteYes,voting_Count)
                
            else:
                voteNo += 1
                print('no',voteNo, voting_Count)   
                
            if (voteYes + voteNo == del_Nums):
                await message.channel.send('Numbers of members Disagree: {}\nNumbers of members Agree: {}'.format(voteNo, voteYes))
    
        
            
            #đếm số lượng người biểu quyết
        ######################################################################################
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