#imports
import discord
from discord.ext import commands
import discordBotCode.databaseManagement as databaseManagement
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
import sys
import datetime
import re
from textblob import TextBlob
import time

#consts
reader = open("/home/bkowalski99/ohiobot/discordBotCode/SecretKeyURI.txt","r")
uri = reader.readline()
print(uri)
cryingEmoji = "/home/bkowalski99/ohiobot/discordBotCode/crying-emoji-dies.gif"
intents = discord.Intents.default()
intents.message_content = True
jaredHate = False
sentimentOn = False

bot = commands.Bot(command_prefix='$', intents=intents)

client = discord.Client(intents=intents)

def areTheyBeingMean(text):
    if sentimentOn:
        blob = TextBlob(text)

        sentiment_polarity = blob.sentiment.polarity


        return sentiment_polarity
    else:
        return 0.0        

def uwuize(text):
    msg = ''
    
    updtext = text.replace("ove", "uv")
    updtext = updtext.replace('r', 'w')
    updtext = updtext.replace('l', 'w')
    updtext = updtext.replace('R', 'W')
    updtext = updtext.replace('L', 'W')
    updtext = updtext.replace('ni', "nyi")
    updtext = updtext.replace('Ni', "Nyi")
    updtext = updtext.replace('na', "nya")
    updtext = updtext.replace('Na', "Nya")
    updtext = updtext.replace('no', "nyo")
    updtext = updtext.replace('No', "Nyo")
    updtext = updtext.replace('ne', "nye")
    updtext = updtext.replace('Ne', "Nye")
    updtext = updtext.replace('nu', "nyu")
    updtext = updtext.replace('Nu', "Nyu")
    updtext = updtext.replace('the ', "da ")
    updtext = updtext.replace('fuck', 'frig')
    updtext = updtext.replace('Fuck', 'Frig')
    updtext = updtext.replace('god', 'gawsh')
    updtext = updtext.replace('God', 'Gawsh')
    msg += updtext
    return msg

# Converts messages with EST to PST
def convert_to_pst(text):
    text = text.replace(":", "")
    match = re.search(r'\d+ est', text)
    number = match.group(0)[0:-4]
    if len(number) == 4:
        value = str(((9 + int(number[0:2]))%12))+":" + (number[2:4]) 
    elif len(number) == 3:
        value = str(((9 + int(number[0:1]))%12))+":" + (number[1:3])
    elif len(number) == 2:
        value = str((9 + int(number))%12)+ ":00"
    else:
        value = str((9 + int(number)))+ ":00" 
    return(value)

def get_messages_count():
        conn = databaseManagement.getCollection(uri,"messages")        
        table = databaseManagement.print_collection(conn)
        count = ''
        for row in table:
            count = count + str(row["name"]) + ' has sent '+ str(row["count"]) + ' messages' + '\n'
        return count

def get_pings_count():
        conn = databaseManagement.getCollection(uri,"pings")
        
        rows = databaseManagement.print_collection(conn)
        count = ''
        for row in rows:
            count = count + str(row["name"]) + ' has sent '+ str(row["count"]) + ' pings' + '\n'
        return count

# Sends message to alert Discord that there was an error
async def error_occurred():
    await discord.message.channel.send("Something went horribly wrong")

# commands require new invite to server to allow for commands to be listed as a part of the bot
@bot.command()
async def howManySends(ctx, content: get_pings_count):
    count = get_pings_count()
    await ctx.send(count)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



@client.event
async def on_message(message):
    
    global jaredHate
    global sentimentOn
    global bot
    global client
    if message.author == client.user:
        return

    text = message.content.lower()
    
    
    
    sentiment = areTheyBeingMean(message.content.lower())
    if (sentiment < -0.5 and message.author.name == "conchiliga2"):
        await message.channel.send("Hey "+ message.author.name +", consider slowing down, your words can hurt people... :(")
    elif (sentiment > 0.5 and message.author.name == "conchiliga2"):
        await message.channel.send("DICKKKKKK RIDAAAAAAA")

    # Update count of messages in DB
    conn = databaseManagement.getCollection(uri, "messages")
    user = message.author.name
    user = user.replace('\'', '')
    user = user.replace('\"', '')
    databaseManagement.insertOrUpdateUserCollection(conn,user)
        
    if (len(text) == 0):
        return

    # bot control methods
    if '$sentiment' in message.content.lower():
        sentimentOn = not sentimentOn
        await message.channel.send("Sentiment set to "+str(sentimentOn))

    if '$jaredhate' in message.content.lower():
        jaredHate = not jaredHate
        await message.channel.send("JaredHate set to "+str(jaredHate))

    if '$close' in text and message.author.name == "bearington.":
        await message.channel.send("Shutting down...")
        print("attempting shutdown")
        await client.close()
        sys.exit()
        return
    
    if '$help' in text:
        await message.channel.send('''**$count** will tell you how many times we've pinged csgamer\n **$messages** will tell you how many messages everyone has sent
        ''')

    if '$$member' in text:
        await message.channel.send((message.author.id))
        return

    if '$count' in text:        
            count = get_pings_count()
            await message.channel.send(count)


    if '$messages' in message.content.lower():        
            count = get_messages_count()
            await message.channel.send(count)


    # bot response methods
    if 'ohio' in text:
        await message.channel.send('I love Ohio! 🎉')
    
    if 'california' in text:
        await message.channel.send('Fuck California. 😠')


    if ' est' in message.content.lower():
        text = message.content.lower()
        # does not check if " est" occurs with non-numeric entries and will try to convert them
        value = convert_to_pst(text)
        await message.channel.send("That's " + str(value) + " PST")
        
    if jaredHate and message.author.name == "jwalk427":
        try:
            await message.channel.send(uwuize(message.content))
        except:
            error_occurred()

    if ' pst' in message.content.lower():
        with open(cryingEmoji, 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)

    if ' cst' in message.content.lower():
        
        await message.channel.send("Shuddup")

    if len(message.role_mentions) > 0:
        for role in message.role_mentions:
            if 'csgamer' in role.name.lower():                    

                conn = databaseManagement.getCollection(uri,"pings")
                user = message.author.name
                databaseManagement.insertOrUpdateUserCollection(conn,user)
                
    
    if '$help' in text:
        await message.channel.send('''**$count** will tell you how many times we've pinged csgamer\n **$messages** will tell you how many messages everyone has sent
        ''')



def start():
    key = ''
    reader = open("/home/bkowalski99/ohiobot/discordBotCode/SecretKey.txt","r")
    key = reader.readline()
    client.run(key)
