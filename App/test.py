import discord
token = 'Njg4MzIyMDQxODM2NzMyNTY4.XmyqgQ.tkA-imK5DXuX9OAhsRw8nEqxuMY'
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(token)