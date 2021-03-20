dev_mode = False

version = "1.6.1"

from random import randint, choice
from vibscore import render
import requests, time, sys, os, datetime

help_text = """

Thank you for adding Vib-RiBot (Discord edition)
This is loosely based off of the Twitter bot (@VibRibot) by @zeriben12
Discord bot created by Twitter user @_PLAY_NOW

Commands:
---
`!vib` - Vib-Ribbon quote
`!vib scream` - Vibri screams
`!vib cry` - Vibri cries
`!vib growl` - Vibri growls
`!vib slap` - Slap Vibri
`!vib hug` - Hug Vibri
`!vib check` - Vibri does a vib check
`!vib nus` - nus!
`!vib stroke` - Vibri has a stroke reading the above text and fudging dies
`!vib say` - Vibri says what you want her to say!
`!vib rate` - Vibri rates your meme, poem, art piece, or any attachment!
`!vib number <n>` Vibri translates a base 10 number (<n>) into Vib-Ribbon shapes!
`!vib cue <filename> <instruction>` - Creates a CUE file
    <filename> should be in quotes, e.g. "Song.wav"
    <instruction can be one of two things:
    *<n> or %<timestamps>
        *<n> repeats the song <n> times, for example,
            `!vib cue "Song.wav" *10`
        will give a cue file that has Song.wav listed 10 times

        %<timestamps> works like this:
            `!vib cue "test song.wav" %00:00:00|01:00:00|01:59:00?02:00:00`
        Each track's timestamp is split by a | and the end of the previous track comes before a ?
        The end of the second track is 1 minute, 59 seconds, 0 frames.
---

"""


def quote():
    q = open("res.txt", "r").read().split("\n")
    return choice(q) or "tfw you miss a block :pensive:"


def slapReact():
    rct = [
        "Ouch!",
        "Owie!",
        "Eeek!",
        "Aahhhhhhhhh!"
    ]
    return choice(rct)


def hugReact():
    rct = [
        "Yay!",
        "Haha!",
        "Happy!",
        "pog"
    ]
    return choice(rct)


def rate():
    c = open("ratings.txt", "r").read().split("\n")
    v = choice(c)
    r = choice(v.split("[")[1].split(","))
    v = v.split("[")[0]
    return v + " " + r + "/10"


def roulette(g, b, c):
    chance = c or 5
    fvar = randint(1, chance)
    if fvar != 1:
        return g
    else:
        return b


def cue(m):
    cue_inst = str(m).split(" ")[2:]
    ct = " ".join(cue_inst)
    file = ct.split("\"")[1]
    cue_inst = " ".join(cue_inst).split('"' + file + '"')
    ret = ""

    if cue_inst[1].startswith(" *"):

        count = int(cue_inst[1].split("*")[1]) or 1

        for i in range(1, count + 1):
            if toDouble(i) == "ERR": # track no > 99
                return "Game over! Too many tracks."
            ret += "FILE \"" + file + "\" BINARY\n"
            ret += "\tTRACK " + toDouble(i) + " AUDIO\n"
            ret += "\t\tINDEX 01 00:00:00\n"

        prod = "```\n" + ret + "\n```"
        if len(prod) > 1999:
            return "Game over! The CUE file is too long!"
        return prod

    elif cue_inst[1].startswith(" %"):

        timestamps = cue_inst[1][2:].split("|")
        ret += "FILE \"" + file + "\" BINARY\n"
        ctr = 0

        for i in timestamps:
            ctr += 1
            ret += "  TRACK " + toDouble(ctr) + " AUDIO\n"
            if ("?" in i):
                l = i.split("?")
                ret += "    INDEX 00 " + l[0] + "\n"
                ret += "    INDEX 01 " + l[1] + "\n"
            else:
                ret += "    INDEX 01 " + i + "\n"
        prod = "```\n" + ret + "\n```"

        if len(prod) > 1999:
            return "Game over! The CUE file is too long."
        return prod

    else:
        return "Game over! Invalid argument '" + cue_inst[1][0] + "'"


def ctry(m):
    try:
        return cue(m)
    except:
        return "Game over! Something's wrong with your command."


def toDouble(n):
    # this was a stupid function name. basically makes a single digit number
    # into a double digit number by adding 0 before it.

    if n > 99:
        return "ERR"
    elif n < 1:
        return "01"
    num = str(n)
    if len(num) == 1:
        num = "0" + num
    return num


def vib_say(msg):
    m = msg.content
    slurs = open("slurs.txt", "r").read().split("\n")
    for i in m.split(" "):
        if i.lower() in slurs and i != "":
            return "Grrrrrrrggh!!"

    return m[9:]


import discord

tokens = open("tokens.txt", "r").split("\n")

if dev_mode:
    token = tokens[1]
else:
    token = tokens[0]

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "!vib":
        await message.channel.send(quote())
    elif message.content.lower() == "!vib scream":
        await message.channel.send("Aahhhhhhhhh!")
    elif message.content.lower() == "!vib check":
        await message.channel.send(roulette(
            "https://cdn.discordapp.com/attachments/760576449387954229/782784397178699786/vib_check_pass.png",
            "https://cdn.discordapp.com/attachments/760576449387954229/782784230521438238/vib_check_fail.png",
            5
        ))
    elif message.content.lower() == "!vib help":
        await message.channel.send(help_text)
    elif message.content.lower().startswith("!vib cue"):
        await message.channel.send(ctry(message.content))
    elif message.content.lower() == "!vib growl":
        await message.channel.send("Grrrrrrrggh!!")
    elif message.content.lower() == "!vib slap":
        await message.channel.send(slapReact())
    elif message.content.lower() == "!vib cry":
        await message.channel.send("Waah! Waah!")
    elif message.content.lower() == "!vib stroke":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/587066858239295491/762884846196359189/unknown.png")
    elif message.content.lower() == "!vib nus":
        await message.channel.send(
            "https://cdn.discordapp.com/attachments/587087600360226817/763503886622654494/Screen_Shot_2020-10-07_at_4.48.10_PM.png")
    elif message.content.lower() == "!vib hug":
        await message.channel.send(hugReact())
    elif message.content.lower().startswith("!vib say"):
        await message.channel.send(vib_say(message)) # this uses vib_say to check for slurs.
    elif message.content.lower().startswith("!vib rate"):
        await message.channel.send(rate())
    elif message.content.lower().startswith('!vib number'):
        try:
            l = int(message.content.split(" ")[2])
        except ValueError:
            await message.channel.send("Error: not a number")
            return
        rnum = message.content.split(" ")[2]
        if int(rnum) < 0:
            rnum = 0
        # rendering file name
        ts = str(message.created_at.hour) + "-" + str(message.created_at.minute) + "-" + str(
            message.created_at.second) + "-" + str(message.created_at.microsecond)
        render.render(str(rnum), "render-" + ts)
        await message.channel.send(file=discord.File("render-" + ts + ".jpg"))
        # delete file once sent to sace space
        os.remove("render-" + ts + ".jpg")
    elif message.content == "!vib stop":
        if dev_mode:
            await message.channel.send("Stopping...")
            await sys.exit()
    elif message.content == "!vib christmas":
        t = datetime.datetime.today()
        if t.month == 12 and t.day < 26:
            await message.channel.send("https://cdn.discordapp.com/attachments/760576449387954229/791703944799059988/video.mp4")
        else:
            await message.channel.send("This command is not available right now.")



@client.event
async def on_ready():
    game = discord.Game("!vib help (v" + version + ")")
    await client.change_presence(status=discord.Status.online, activity=game)


cres = 0

while cres != 200:
    try:
        cres = requests.get("http://www.google.com").status_code
    except requests.exceptions.ConnectionError:
        print("Connection failed. Trying again in 10 seconds.")
        time.sleep(10)

print("Vibri has started!")
client.run(token)
