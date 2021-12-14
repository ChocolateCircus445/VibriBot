# -- Init -- #

from random import randint, choice
from vibscore import render
import requests, time, sys, os, datetime

import discord
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

# Get tokens
tokens = open("tokens.txt", "r").read().split("\n")
reg_token = tokens[0]  # Regular token is on first line
dev_token = tokens[1]  # Developer token is on second line

# Set version number
version_num = "2.0"

# Set help text
help_text = """

Thank you for adding Vib-RiBot (Discord edition)
This is loosely based off of the Twitter bot (@VibRibot) by @zeriben12
Problems? Tell @_PLAY_NOW on Twitter

Press the "/" key for the slash command menu!

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
`!vib tpose` Vibri T-poses
`!vib hon` Vibri posts a random page of Vibrihon
`!vib cue <filename> <instruction>` - Creates a CUE file
    <filename> should be in quotes, e.g. "Song.wav"
    <instruction> can be one of two things:
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

# Get quotes
quotes = open("quotes.txt", "r").read().split("\n")

# Get ratings
ratings = open("ratings.txt", "r").read().split("\n")

# Get slurs
slurs = open("slurs.txt", "r").read().split("\n")

# Developer mode toggle
dev_mode = True

# Set token for given mode
if dev_mode:
    token = dev_token
else:
    token = reg_token

# Image urls
images = {
    "christmas": "https://cdn.discordapp.com/attachments/760576449387954229/791703944799059988/video.mp4",
    "nus": "https://cdn.discordapp.com/attachments/587087600360226817/763503886622654494/Screen_Shot_2020-10-07_at_4.48.10_PM.png",
    "stroke": "https://cdn.discordapp.com/attachments/587066858239295491/762884846196359189/unknown.png",
    "tpose": "https://cdn.discordapp.com/attachments/760576449387954229/833772562357420042/vibri_t-pose.png",
    "vib_check_pass": "https://cdn.discordapp.com/attachments/760576449387954229/782784397178699786/vib_check_pass.png",
    "vib_check_fail": "https://cdn.discordapp.com/attachments/760576449387954229/782784230521438238/vib_check_fail.png",

}

# Vibrihon image urls (loaded from file)
hon = {

}

# Load vibrihon urls
print("Loading vibrihon urls")
hf = open("hon.txt", "r")
h = hf.read().split("\n")
for i in h:
    l = i.split(";")
    hon[l[0]] = l[1]
hf.close()

print("Loaded!")

# Phrases
phrases = {
    "growl": "Grrrrrrrggh!!",
    "scream": "Aahhhhhhhhh!",
    "cry": "Waah! Waah!"
}


# -- Functions -- #

# Update vibrihon database
def update_hon():
    f = open("hon.txt", 'w')
    txt = ""
    for i in hon:
        txt += i + ";" + hon[i] + "\n"
    f.write(txt[:-1])
    print("Updated database")


# Send a quote
def quote():
    return choice(quotes) or "tfw you miss a block :pensive:"  # The last part is an error handler


# Get YouTube character sequence from link
def get_video_chars(l):
    return l.split("?v=")[1][:11]


# Test if string is a link
def get_link_type(l):
    ltype = "TEXT"
    if l.startswith("http://") or l.startswith("https://"):
        ltype = "LINK"
        image_links = ['.jpg', '.png', '.jpeg', '.gif']
        for i in image_links:
            if l.endswith(i):
                return "IMG"
        if "youtube" in l:
            return "YT"
    return ltype


# Hug Vibri
def hug_react():
    rct = [
        "Yay!",
        "Haha!",
        "Happy!",
        "pog"
    ]
    return choice(rct)


# Roulette
def roulette(g, b, c):
    chance = c or 5
    fvar = randint(1, chance)
    if fvar != 1:
        return g
    else:
        return b


# Rate
def rate():
    v = choice(ratings)
    r = choice(v.split("[")[1].split(","))  # rating text[0,1,2,3
    v = v.split("[")[0]
    return v + " " + r + "/10"


# Slap
def slap_react():
    rct = [
        "Ouch!",
        "Owie!",
        "Eeek!",
        "Aahhhhhhhhh!"
    ]
    return choice(rct)


# Execution
def execution_countdown():
    today = datetime.date.today()
    future = datetime.date(2021, 7, 2)
    diff = future - today
    if (diff.days == 0):
        return "Vibri will be publicly executed today."
    elif (diff.days < 0):
        return "Vibri was publicly executed " + str(abs(diff.days)) + " days ago."
    else:
        return "Vibri will be publicly executed in " + str(diff.days) + " days"


# !vib say function
def vib_say(m, usingSlash):
    for i in m.split(" "):
        if i.lower() in slurs and i != "":
            return "Grrrrrrrggh!!"

    if usingSlash:
        return m  # If using slash commands, no need to crop anything out
    return m[9:]  # Used to crop out "!vib say"


# !vib cue functions
# I can't port these to slash commands because I forgot how they work. Oops!

def cue(m):
    cue_inst = str(m).split(" ")[2:]
    ct = " ".join(cue_inst)
    file = ct.split("\"")[1]
    cue_inst = " ".join(cue_inst).split('"' + file + '"')
    ret = ""
    if cue_inst[1].startswith(" *"):
        count = int(cue_inst[1].split("*")[1]) or 1
        for i in range(1, count + 1):
            if toDouble(i) == "ERR":
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
            if "?" in i:
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
    if n > 99:
        return "ERR"
    elif n < 1:
        return "01"
    num = str(n)
    if len(num) == 1:
        num = "0" + num
    return num


# !vib rihon

def get_hon():
    pass

# -- Discord initialization -- #

# Enable slash commands through the client
client = discord.Client()
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print("Discord says that the bot is ready")
    game = discord.Game("!vib help (v" + version_num + ")")
    await client.change_presence(status=discord.Status.online, activity=game)


# -- Slash commands -- #


# /vib
@slash.slash(name="vib", description="A quote from Vib-Ribbon")
async def _send_quote(ctx):
    await ctx.send(quote())


# /hug
@slash.slash(name="hug", description="Hug Vibri")
async def _hug(ctx):
    await ctx.send(hug_react())


# /vibcheck
@slash.slash(name="vibcheck", description="Vibri does a vib check")
async def _vibcheck(ctx):
    await ctx.send(roulette(
        images["vib_check_pass"],
        images["vib_check_fail"],
        5
    ))


# /number
@slash.slash(name="number", description="Vib-Ribbon number", options=[
    create_option(name="number", description="Number", option_type=4, required=True)
])
async def _number(ctx, number: int):
    rnum = number
    if (rnum < 0):
        rnum = 0
    ts = str(datetime.datetime.now()).replace(":", "-")
    render.render(str(rnum), "render-" + ts)
    await ctx.send(file=discord.File("render-" + ts + ".jpg"))
    os.remove("render-" + ts + ".jpg")


# /rate
@slash.slash(name="rate", description="Send a phrase, or a link to a picture or a YouTube video.", options=[
    create_option(name="thing", description="A text, link to an image, or link to a video", option_type=3,
                  required=True)
])
async def _rate(ctx, thing):
    vib_rating = "Vibri says: " + rate()
    em = discord.Embed(title=vib_rating)
    em.description = thing
    thumbnail = ""
    lt = get_link_type(thing)  # Reduce redundancy
    if lt == "IMG":
        em.set_image(url=thing)
    if lt == "YT":  # Only using if statements in case the text type changes...
        try:  # Test if this is a valid YouTube link
            thumbnail = "https://i.ytimg.com/vi/" + get_video_chars(thing) + "/hqdefault.jpg"
            em.set_image(url=thumbnail)
            em.url = "https://youtube.com/watch?v=" + get_video_chars(thing)
            em.description = em.url
        except:
            lt = "LINK"  # ...like in here
    if lt == "LINK":
        em.url = thing
        em.description = thing
    if lt == "TEXT":
        em.description = thing
    print(thing)
    await ctx.send(embed=em)


# /slap
@slash.slash(name="slap", description="Slap Vibri")
async def _slap(ctx):
    await ctx.send(slap_react())


"""
# Commented out because the PS3 store is not shutting down for now
# /execution
@slash.slash(name="execution", description="Countdown to Vibri's public execution on the PS3 store")
async def _execution(ctx):
    await ctx.send(execution_countdown())
"""


# /say
@slash.slash(name="say", description="Vibri says anything you want her to!", options=[
    create_option(name="phrase", description="Thing that you want Vibri to say",
                  option_type=3, required=True)
])
async def _say(ctx, phrase):
    await ctx.send(vib_say(phrase, True))


# /scream
@slash.slash(name="scream", description="Make Vibri scream")
async def _scream(ctx):
    await ctx.send(phrases["scream"])


# /cry
@slash.slash(name="cry", description="Make Vibri cry")
async def _cry(ctx):
    await ctx.send(phrases["cry"])


# /stroke
@slash.slash(name="stroke", description="Vibri has a stroke and fudging dies")
async def _stroke(ctx):
    await ctx.send(images["stroke"])


# /nus
@slash.slash(name="nus", description="nus!")
async def _nus(ctx):
    await ctx.send(images["nus"])


# /growl
@slash.slash(name="growl", description="Make Vibri growl.")
async def _growl(ctx):
    await ctx.send(phrases["growl"])


# /tpose
@slash.slash(name="tpose", description="Vibri T-Poses")
async def _tpose(ctx):
    await ctx.send(images["tpose"])

# /hon
@slash.slash(name="hon", description="A random page from Vibrihon")
async def _hon(ctx):
    pg = str(randint(4, 86))
    if not pg in hon:
        await ctx.send("Vibrihon page " + pg, file=discord.File("hon/vibrihonpg" + str(pg) + ".png"))
    else:
        await ctx.send(hon[pg])

# -- Legacy commands -- #

# on_message blocks slash commands

@client.event
async def on_message(message):
    global hon

    if message.author == client.user:
        # Update vibrihon page database
        if message.content.startswith("Vibrihon page"):
            pg = message.content.split("page ")[1]
            hon[pg] = message.attachments[0].url
            update_hon()
        # Don't do a command if it comes from the bot itself
        return

    msg = message.content.lower()  # Redundancy

    if msg == "!vib":
        await message.channel.send(quote())

    elif msg == "!vib scream":
        await message.channel.send(phrases["scream"])

    elif msg == "!vib check":
        await message.channel.send(roulette(images["vib_check_pass"], images["vib_check_fail"], 5))

    elif msg == "!vib help":
        await message.channel.send(help_text)

    elif msg.startswith("!vib cue"):
        await message.channel.send(ctry(message.content))

    elif msg == "!vib growl":
        await message.channel.send(phrases["growl"])

    elif msg == "!vib slap":
        await message.channel.send(slap_react())

    elif msg == "!vib cry":
        await message.channel.send(phrases["cry"])

    elif msg == "!vib stroke":
        await message.channel.send(images["stroke"])

    elif msg == "!vib nus":
        await message.channel.send(images["nus"])

    elif msg == "!vib hug":
        await message.channel.send(hug_react())

    elif msg.startswith("!vib say"):
        await message.channel.send(vib_say(msg, False))

    elif msg.startswith("!vib rate"):
        await message.channel.send(rate())

    elif msg.startswith("!vib number"):
        try:
            l = int(msg.split(" ")[2])  # ['!vib', 'number', '(number)']
        except ValueError:
            await message.channel.send("Error: not a number")
            return
        rnum = message.content.split(" ")[2]
        if int(rnum) < 0:  # Don't allow negatives
            rnum = 0
        ts = str(datetime.datetime.now()).replace(":", "-")
        render.render(str(rnum), "render-" + ts)
        await message.channel.send(file=discord.File("render-" + ts + ".jpg"))
        os.remove("render-" + ts + ".jpg")

    elif msg == "!vib stop":
        if dev_mode:
            sys.exit()

    elif msg == "!vib christmas":
        t = datetime.datetime.today()
        if t.month == 12 and t.day < 26:
            await message.channel.send(images["christmas"])
        else:
            await message.channel.send("This command is not available right now.")

    elif msg == "!vib tpose":
        await message.channel.send(images["tpose"])

    elif msg == "!vib hon" or msg == "!vib rihon":
        pg = str(randint(4, 86))
        print(pg)
        if not pg in hon:
            await message.channel.send("Vibrihon page " + pg, file=discord.File("hon/vibrihonpg" + str(pg) + ".png"))
        else:
            await message.channel.send(hon[pg])

    # At one point sending files wasn't working, so I added this command to troubleshoot errors.
    # I simply upgraded discord.py!
    elif msg == "!vib file":
        if dev_mode:
            await message.channel.send(file=discord.File("hon/vibrihonpg4.png"))


# -- Startup assistance -- #

cres = 0

while cres != 200:
    try:
        # Google's a safe bet since it's always on.
        cres = requests.get("http://www.google.com").status_code
    except requests.exceptions.ConnectionError:
        print("Connection failed. Trying again in 10 seconds.")
        time.sleep(10)

print("Vibri has started!")

client.run(token)
