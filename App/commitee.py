import discord
import asyncio
import data

class Commitee:
    voting_Count = 0; voteNo = 0; voteYes = 0; whiteVote = 0
    messageNeedToVote = None

    raiseList = []
    raiseMessage = None


    rollCallMessage = None
    memberNeedtoReply = None
    isReplyTheRollCall = False
    nations = []
    embed = discord.Embed(colour = discord.Colour.gold())
    guild = None
    def __init__(self, name, guild):
        self.nations = data.nations
        self.name = name
        self.guild = guild


    def validCountry(self, nation):
        if self.nations.count(nation) > 0:
            return True
        else: return False

    def getRoleList(self):
        dele, chair, admin = None,None,None
        temp = self.guild.roles
        for i in temp:
            if i.name == '@delegate': dele = i
            if i.name == '@chair': chair = i
            if i.name == '@admin': admin = i
        return dele,chair, admin

    async def hello(self, message):
        dele, chair, admin = self.getRoleList()
        if admin in message.author.roles:
            self.embed.title = 'Hello, I\'m SiSi, your admin in this Conference'
            await message.channel.send(content = None,embed = self.embed)
    async def register(self, message):
        dele, chair, admin = self.getRoleList()
        mess = message.content
        try:
            country = mess.split(' -> ')[1].upper()
            if self.validCountry(country):
                member = message.author
                if member.roles.count(dele) > 0:

                    await message.channel.send('UNVALID ACTIVITY\n{} have already registered as {}'.format(member.name,member.nick))
                elif member.roles.count(chair) > 0 and member.roles.count(dele) == 0:
                    await member.edit(nick = country,roles = [dele], reason = None)
                    await message.channel.send('Succesfully registered as {}'.format(country))
                    self.nations.remove(country)
            else: await message.channel.send('Invalid nation')

        except Exception as e:
            await message.channel.send('Invalid guild\'s input')
            raise e
    async def rollcall(self, message):
        dele, chair, admin = self.getRoleList()

        if chair in message.author.roles:
            self.rollCallMessage = None
            absentList = []
            onlineList = []
        delList = dele.members
        for i in delList:
            self.memberNeedtoReply = i
            await message.channel.send('$call {}. You have 10 seconds to react 👍 on this message'.format(i.mention))
            await asyncio.sleep(10)
            if self.isReplyTheRollCall:
                onlineList.append(i)
            else:
                absentList.append(i)
            self.isReplyTheRollCall = False
            #print(self.rollCallMessage.content)
        roll = 'Absent delegate(s):'
        for i in absentList: roll += '\n{}'.format(i.mention)
        roll+='\nOnline delegate(s):'
        for i in onlineList: roll += '\n{}'.format(i.mention)
        print(roll)
        await message.channel.send(roll)
    async def startvote(self, message):
        dele, chair, admin = self.getRoleList()
        if chair in message.author.roles and not dele in message.author.roles:
            print('Update message to raising hand')
#            global raiseList
            self.raiseList = []
            time = 30
            try:
                time = float(mess.split(' ')[1])
                await message.channel.send('You got {} seconds to raise your hand by reacting 👍 to $startraise message', time)
            except Exception as e:
                await message.channel.send('Error with time, automatic time is 15 seconds to raise your hand by reacting 👍 to $startraise message')
                time = 15
#            global raiseMessage
            self.raiseMessage = message
            await asyncio.sleep(time)
            notification = 'Numbers of Delegates want to raise hand: {}'.format(len(raiseList))
            for i in self.raiseList:
                notification += '\n{}'.format(i.mention)
            await message.channel.send(notification)
    async def startraise(self,message):
        dele, chair, admin = self.getRoleList()
        if chair in message.author.roles and not dele in message.author.roles:
            self.voteYes = 0
            self.voteNo = 0
            self.whiteVote = 0
            self.voting_Count = 0
            self.messageNeedToVote = message
            print('Update new message that need to vote')
            try:
                time = float(mess.split(' ')[1])
            except Exception as e:
                await message.channel.send('Error with time, automatic time is 20 seconds for voting stuff')
                time = 20
            await asyncio.sleep(time)
            await message.channel.send('Numbers of agree: {}\nNumbes of disagree: {}\nNumbers of white-vote: {}\nUnvoted: {}'.format(self.voteYes,self.voteNo,self.whiteVote,len(dele.members) - self.voteYes - self.voteNo - self.whiteVote))
    async def invite(self, message):
        dele, chair, admin = self.getRoleList()
        if chair in message.author.roles and not dele in message.author.roles:
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
    async def muteall(self, message):
        dele, chair, admin = self.getRoleList()
        if chair in message.author.roles and not dele in message.author.roles:
            try:
                await message.mentions[0].edit(mute = True, reason = None)
                await message.channel.send('Over speech of {}'.format(message.mentions[0].nick))
            except:
                print('Mute all confirmed')
                await message.channel.send('Mute all')
                for member in message.guild.members:
                    if member.roles.count(CHAIR) == 0:
                        await member.edit(mute = True, reason = None)
