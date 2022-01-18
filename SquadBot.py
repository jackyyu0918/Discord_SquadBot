from datetime import datetime

import discord
import os
import requests
import json
import random

client = discord.Client()
cs_queue = list()
timer: datetime = None


def get_token() -> str:
    f = open("token.txt", "r")
    token = (f.read())

    return token


def get_stock_api_key() -> str:
    f = open("stock_api_key.txt", "r")
    stock_api_key = (f.read())

    return stock_api_key


@client.event
async def on_message(message):
    print(message.author.name + ": " + message.content)

    if message.content == "!helloDerek":
        concat_str = "```Hello " + message.author.name + ".\nType !help to get info of " \
                                                         "the avalible command.``` "
        await message.channel.send(concat_str)

        # team function
    elif message.content == "!joinTeam":
        if len(cs_queue) >= 5:
            await message.channel.send("Sorry the team is already full")
        else:
            for member in cs_queue:
                if message.author.id in member:
                    await message.channel.send("**" + message.author.name + "** already in the team!")
                    return

            cs_queue.append([message.author.id, message.author.name])
            await message.channel.send("**" + message.author.name + "** has join the team!")
            await message.channel.send(list_Team_str(cs_queue))

            if len(cs_queue == 1):
                timer = datetime.now()

            if len(cs_queue) == 5:
                await message.channel.send(
                    'The team is full, no bullshit let\'s go  <:bighead:919980311960490014> <:bighead:919980311960490014>\n'
                    'It takes ')
                await message.channel.send(file=discord.File('chung.gif'))

    elif message.content == "!listTeam":
        if len(cs_queue) > 0:
            if len(cs_queue) == 5:
                await message.channel.send(
                    list_Team_str(
                        cs_queue) + '\n The team is full, no bullshit let\'s go  <:bighead:919980311960490014> <:bighead:919980311960490014>')
                await message.channel.send(file=discord.File('chung.gif'))
            else:
                await message.channel.send(list_Team_str(cs_queue))
        else:
            await message.channel.send("Nobody in the team now.\nTry !joinTeam to join the team")

    elif message.content == "!quitTeam":
        for member in cs_queue:
            if message.author.id in member:
                await message.channel.send("**" + member[1] + "** has quit the team!")
                cs_queue.remove(member)
                return

        await message.channel.send(message.author.name + " is not in the team.")

    elif message.content == "!dismissTeam":
        if message.author.id == cs_queue[0][0]:
            cs_queue.clear()
            await message.channel.send("Team dismissed by team leader...")
        else:
            await message.channel.send("You do not have right to dismiss the team.\n You are not the team leader.")

    elif message.content.startswith("!kickMember"):
        # get Symbol from user request
        if message.author.id == cs_queue[0][0]:
            member_number = int(message.content.strip('!kickMember').strip())
            if member_number in range(2, 5):
                await message.channel.send(cs_queue[member_number - 1][1] + "is kicked by team leader...")
                cs_queue.pop(member_number - 1)
        else:
            await message.channel.send("You do not have right to kick team member.\n You are not the team leader.")

    elif message.content == "!listAllUser":
        nameList = ""
        x = message.guild.members
        for i in range(len(x)):
            print(x[i].name)
            nameList = nameList + "\n" + x[i].name
        printString = "```All User in this server: \n" + nameList + "```"
        await message.channel.send(printString)

    elif message.content == "!listUser":
        nameList = ""
        x = message.guild.members
        for i in range(len(x)):
            if x[i].status != discord.Status.offline:
                print(x[i].name)
                nameList = nameList + "\n" + x[i].name
        printString = "```Online user in this server: \n" + nameList + "```"
        await message.channel.send(printString)

    elif message.content == "!RLX":
        # Yahoo API
        json_obj = call_yahoo_stock_api('RLX', api_key=get_stock_api_key())

        stock_name = json.dumps(json_obj['price']['longName'], indent=4)
        price = json.dumps(json_obj['price']['postMarketPrice']['fmt'], indent=4)

        stock_message = ':smoking: :smoking: :smoking: RLX :smoking: :smoking: :smoking: \n' + \
                        'Stock name: ' + stock_name + '\n Post Market Price: ' + price

        await message.channel.send(stock_message)

    elif message.content.startswith('!checkStock'):
        # get Symbol from user request
        symbol = message.content.strip('!checkStock').strip()

        # Yahoo API
        json_obj = call_yahoo_stock_api(symbol, api_key=get_stock_api_key())

        stock_name = json.dumps(json_obj['price']['longName'], indent=4)
        price = json.dumps(json_obj['price']['postMarketPrice']['fmt'], indent=4)

        stock_message = 'Stock name: ' + stock_name + '\n Post Market Price: ' + price

        await message.channel.send(stock_message)

    elif message.content == '!testAddMember':
        # get Symbol from user request
        for i in range(5):
            ran_int = random.randint(1, 10)
            cs_queue.append([str(ran_int), 'member'])

        await message.channel.send('Added')
        await message.channel.send(
            list_Team_str(
                cs_queue) + '\n The team is full, no bullshit let\'s go  <:bighead:919980311960490014> <:bighead:919980311960490014>')
        await message.channel.send(file=discord.File('chung.gif'))

    elif message.content.startswith("!checkNade"):
        map = message.content.replace('!checkNade ', '').lower()

        list_map = ['Mirage', 'Inferno', 'Dust2', 'Overpass', 'Nuke', 'Vertigo', 'Ancient', 'Cache', 'Train']

        if map == '':
            await message.channel.send("https://www.csgonades.com/")
        else:
            if map not in [x.lower() for x in list_map]:
                warning_message = 'Please provide correct map name:\n' + str(list_map)
                await message.channel.send(warning_message)
            else:
                map = 'CSGO nade tutorial for map ' + map + ':\n https://www.csgonades.com/maps/' + map
                await message.channel.send(map)

    elif message.content == "!help":
        await message.channel.send(
            "```User Manual:\n"
            "!help: Get help from me\n"
            "!helloDerek: Greeting\n"
            "!joinTeam: Join the team queue\n"
            "!listTeam: Show the current team list\n"
            "!quitTeam: Quit the current team you are joining\n"
            "!kickMember [2-5]: Kick team member by giving the member id [Team leader only]\n"
            "!dismissTeam: Dismiss the team [Team leader only]\n"
            "!checkStock <symbol>: Check the full name and post market price\n"
            "!RLX: See simple info for RLX (Supported by YAHOO Finance API)\n"
            "!checkNade <map>: Check CSGO Nade, e.g. !checkNade dust2```")


def call_yahoo_stock_api(symbol: str, api_key: str):
    url = "https://stock-market-data.p.rapidapi.com/yfinance/price"
    querystring = {"ticker_symbol": symbol}
    headers = {
        'x-rapidapi-host': "stock-market-data.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_obj = json.loads(response.text)
    return json_obj


def list_Team_str(team_queue: list) -> str:
    queueMessage = "```Team queue: \n==============\n"
    count = 0
    for member in team_queue:
        queueMessage = queueMessage + str(count + 1) + ": " + member[1]

        if count == 0:
            queueMessage = queueMessage + ' [Team Leader]\n'
        else:
            queueMessage = queueMessage + '\n'

        count += 1

    queueMessage = queueMessage + "```"
    return queueMessage


token = get_token()
client.run(token)
