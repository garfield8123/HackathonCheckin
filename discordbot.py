import discord

with open("botCommands.json") as secretinformation:
    data = json.load(secretinformation)

TOKEN = data.get("token")
client = discord.Client()


@client.event

async def on_message(message):
    # we do not want the bot to reply to itself
    if "bot" not in message.channel.name: return
    if message.author == client.user:
        return
    elif message.content.startswith('!commands'):
        msg = 'All available commands are: !about, !help, !commands, !social, !website'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('!about'):
        msg = "Hi there! I am the Tri-Valley Crypto Hacks Bot and I'm a Discord bot made specifically for the Tri-Valley Crypto Hacks Discord. I'm pleased to meet you! To view my commands, do !commands.".format(message)
        await message.channel.send(msg)
    elif message.content.startswith('!help'):
        msg = "- If you want a list of commands, type !commands \n - Some frequently asked questions can be found on our !website".format(message)
        await message.channel.send(msg)
    elif message.content.startswith('!social'):
        msg = "Facebook: https://www.facebook.com/trivalleyhacks  \n Twitter: https://twitter.com/CryptoTri".format(message)
        await message.channel.send(msg)
    elif message.content.startswith('!website'):
        msg = 'Visit our site at https://cryptohacks.tech. If you want to donate to our hacakthon you can go to https://bank.hackclub.com/donations/start/tri-valley-crypto-hacks'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('commands'):
        msg = 'All available commands are: !about, !help, !commands, !social, !website'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('about'):
        msg = "Hi there! I am the Tri-Valley Crypto Hacks Bot and I'm a Discord bot made specifically for the Tri-Valley Crypto Hacks Discord. I'm pleased to meet you! To view my commands, do !commands.".format(message)
        await message.channel.send(msg)
    elif message.content.startswith('help'):
        msg = "- If you want a list of commands, type !commands \n - Some frequently asked questions can be found on our !website".format(message)
        await message.channel.send(msg)
    elif message.content.startswith('social'):
        msg = "Facebook: https://www.facebook.com/trivalleyhacks  \n Twitter: https://twitter.com/CryptoTri".format(message)
        await message.channel.send(msg)
    elif message.content.startswith('website'):
        msg = 'Visit our site at https://cryptohacks.tech. If you want to donate to our hacakthon you can go to https://bank.hackclub.com/donations/start/tri-valley-crypto-hacks'.format(message)
        await message.channel.send(msg)
    else:
        print('not a command')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)