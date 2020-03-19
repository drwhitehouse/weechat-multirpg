# import my shiz
import weechat
import re

# callback for data received in input
def buffer_input_cb(data, buffer, input_data):
    # ...
    return weechat.WEECHAT_RC_OK

# callback called when buffer is closed
def buffer_close_cb(data, buffer):
    weechat.bar_remove(ctrbar)
    return weechat.WEECHAT_RC_OK

# callback called when script unloaded
def unload_script_cb():
    # ...
    return weechat.WEECHAT_RC_OK

# initialise configuration
def multirpg_config_init():
    global multirpg_config_file, multirpg_config_option
    multirpg_config_file = weechat.config_new(CONFIG_FILE_NAME,"","")
    if multirpg_config_file == "":
        return
    section_multirpg = weechat.config_new_section(multirpg_config_file, "multirpg", 0, 0, "", "", "", "", "", "", "", "", "", "")
    if section_multirpg == "":
        weechat.config_free(multirpg_config_file)
        return
    multirpg_config_option["mynick"] = weechat.config_new_option(multirpg_config_file, section_multirpg, "mynick", "string", "multirpg nickname", "", 0, 0, "", "", 0, "", "", "", "", "", "")
    multirpg_config_option["myclass"] = weechat.config_new_option(multirpg_config_file, section_multirpg, "myclass", "string", "multirpg class", "", 0, 0, "", "", 0, "", "", "", "", "", "")
    multirpg_config_option["ircserver"] = weechat.config_new_option(multirpg_config_file, section_multirpg, "ircserver", "string", "multirpg ircserver", "", 0, 0, "", "", 0, "", "", "", "", "", "")

# read config file
def multirpg_config_read():
    global multirpg_config_file
    return weechat.config_read(multirpg_config_file)

# call bot for whoami & stats
def callbot():
    weechat.command(botbuffer, "bank")
    weechat.command(botbuffer, "whoami")
    weechat.command(botbuffer, "stats")

# get creep for attack
def getcreep(mylevel):
    if mylevel >= 150:
        creep = "ogre"
    elif mylevel >= 140:
        creep = "wyvern"
    elif mylevel >= 130:
        creep = "beholder"
    elif mylevel >= 120:
        creep = "minotaur"
    elif mylevel >= 110:
        creep = "phoenix"
    elif mylevel >= 100:
        creep = "monkey"
    elif mylevel >= 90:
        creep = "mutant"
    elif mylevel >= 80:
        creep = "cyclops"
    elif mylevel >= 70:
        creep = "troll"
    elif mylevel >= 60:
        creep = "shadow"
    elif mylevel >= 50:
        creep = "ghost"
    elif mylevel >= 40:
        creep = "skeleton"
    elif mylevel >= 30:
        creep = "lich"
    elif mylevel >= 20:
        creep = "goblin"
    elif mylevel >= 15:
        creep = "spider"
    elif mylevel >= 10:
        creep = "locust"
    else:
        creep = "bush"
    return creep

# get monster for slay
def getmonster(mysum):
    if mysum >= 10000:
        monster = "hippogriff"
    elif mysum >= 9000:
        monster = "sphinx"
    elif mysum >= 8000:
        monster = "dragon"
    elif mysum >= 7000:
        monster = "vampire"
    elif mysum >= 6000:
        monster = "mammoth"
    elif mysum >= 5000:
        monster = "centaur"
    else:
        monster = "medusa"
    return monster

# get opponents for gambling
def getbets():
    weechat.command(mingbuffer, "!bestbet")

# get opponent for fighting
def getfights():
    global mynick
    weechat.command(mingbuffer, "!bestfight %s" % (mynick))

# get digits
def getdigits(msg):
    digits = [int(s) for s in re.findall(r'\b\d+\b', msg)]
    return digits

# get seconds
def getseconds(msg):
    seconds = 0
    digits = getdigits(msg)
    seconds = seconds + digits[0] * 86400       # Days
    seconds = seconds + digits[1] * 3600        # Hours
    seconds = seconds + digits[2] * 60          # Minutes
    seconds = seconds + digits[3]               # Seconds
    seconds = seconds + 30                      # This isn't very accurate...
    return seconds

# countdown
def countdown(data,timer):
    global acount, ccount, scount, lcount
    if data == "attack":
        acount = timer
    if data == "challenge":
        ccount = timer
    if data == "slay":
        scount = timer
    if data == "level":
        lcount = timer
    if int(timer) == 0:
        callbot()
    else:
        weechat.bar_item_update("mrpgcounters")
    return weechat.WEECHAT_RC_OK

# show counters for mrpgbar
def show_mrpgcounters(data, item, window):
    global acount, ccount, scount, lcount, bank
    mycontent = "attack: %s challenge: %s slay: %s level: %s gold: %s" % (acount, ccount, scount, lcount, bank)
    return mycontent

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    global mynick, myclass, mylevel, creep, monster, bank, ahook, chook, shook, lhook

    # Reset bot calling flag

    needtocall = 0

    # Wait, what, did we just log in?

    if msg.startswith(mynick) and "has logged in" in msg:
        needtocall = 1

    # finance

    if msg.startswith("You have"):
        if "gold in the bank" in msg:
            bank = getdigits(msg)[0]
            carry = getdigits(msg)[1]
            if carry > 40:
                deposit = carry - 40
                weechat.prnt(scriptbuffer, "Depositing: %s gold..." % (deposit))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank deposit %s" % (deposit))
                needtocall = 1

    if msg.startswith("Power Potions:"):
        has_eng = getdigits(msg)[5]
        eng_lvl = getdigits(msg)[6]
        has_her = getdigits(msg)[3]
        her_lvl = getdigits(msg)[4]
        bets = getdigits(msg)[7]
        fights = getdigits(msg)[2]
        if eng_lvl < 9:
            if has_eng == 0 and bank > 1500:
                weechat.prnt(scriptbuffer, "%sHiring engineer..." % weechat.color("red, black"))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 1000")
                weechat.command(botbuffer, "hire engineer")
                needtocall = 1
            if has_eng == 1 and bank > 200:
                weechat.prnt(scriptbuffer, "%sUpgrading engineer..." % weechat.color("red, black"))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 200")
                weechat.command(botbuffer, "engineer level")
                needtocall = 1
        if her_lvl < 9:
            if has_her == 0 and bank > 1500:
                weechat.prnt(scriptbuffer, "%sSummoning hero..." % weechat.color("red, black"))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 1000")
                weechat.command(botbuffer, "summon hero")
                needtocall = 1
            if has_her == 1 and bank > 200:
                weechat.prnt(scriptbuffer, "%sUpgrading hero..." % weechat.color("red, black"))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 200")
                weechat.command(botbuffer, "hero level")
                needtocall = 1
        if bets < 5 and mylevel[0] >= 30:
                getbets()
        if fights < 5 and mylevel[0] >= 10:
                getfights()

    # Gamble

    if msg.startswith("bestbet") and bank > 500:
        weechat.prnt(scriptbuffer, "%sBetting ..." % weechat.color("red, black"))
        weechat.prnt(scriptbuffer, "")
        chunks = msg.split(" ")
        win = chunks[1]
        lose = chunks[2]
        weechat.command(botbuffer, "bank withdraw 500")
        for _ in range(5):
            weechat.command(botbuffer, "bet %s %s 100" % (win, lose))
        needtocall = 1

    # Fight

    if msg.startswith("bestfight"):
        weechat.prnt(scriptbuffer, "%sFighting ..." % weechat.color("red, black"))
        weechat.prnt(scriptbuffer, "")
        chunks = msg.split(" ")
        opponent = chunks[1]
        if opponent == mynick:
            weechat.prnt(scriptbuffer, "Mingbeast can't get its act together - you need to find someone to fight!")
            weechat.prnt(scriptbuffer, "")
        else:
            for _ in range(5):
                weechat.command(botbuffer, "fight %s" % (opponent))
            needtocall = 1

    # Upgrade

    if bank >= 2000:
        weechat.prnt(scriptbuffer, "%sUpgrading items ..." % weechat.color("red, black"))
        weechat.prnt(scriptbuffer, "")
        weechat.command(botbuffer, "bank withdraw 2000")
        weechat.command(botbuffer, "upgrade all 10")
        needtocall = 1

    # display lines about me

    if mynick in msg:
        weechat.prnt(scriptbuffer, msg)
        weechat.prnt(scriptbuffer, "")
        if myclass in msg:
            chunks = msg.split(". ")
            for chunk in chunks:
                if chunk.startswith("You are"):
                    mylevel = getdigits(chunk)
                    creep = getcreep(mylevel[0])
                    weechat.prnt(scriptbuffer, "Attack target: %s" % (creep))
                    weechat.prnt(scriptbuffer, "")
                if chunk.startswith("Next level"):
                    weechat.unhook(lhook)
                    lhook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "level") # step in seconds

    # get monster

    if msg.startswith("Items:"):
        chunks = msg.split(". ")
        for chunk in chunks:
            if chunk.startswith("Items:"):
                bits = msg.split(", ")
                for bit in bits:
                    if bit.startswith("Total sum:"):
                        mysum = getdigits(bit)
                        monster = getmonster(mysum[0])
                        weechat.prnt(scriptbuffer, "Slay target: %s" % (monster))
                        weechat.prnt(scriptbuffer, "")

    # take action

    if "You can now" in msg:
        if "You can now ATTACK." in msg:
            weechat.prnt(scriptbuffer, "%sAttacking..." % weechat.color("red, black"))
            weechat.prnt(scriptbuffer, "")
            weechat.command(botbuffer, "attack %s" % (creep))
        if "You can now CHALLENGE." in msg:
            weechat.prnt(scriptbuffer, "%sChallenging..." % weechat.color("red, black"))
            weechat.prnt(scriptbuffer, "")
            weechat.command(botbuffer, "challenge")
        if "You can now SLAY." in msg:
            weechat.prnt(scriptbuffer, "%sSlaying..." % weechat.color("red, black"))
            weechat.prnt(scriptbuffer, "")
            weechat.command(botbuffer, "slay %s" % (monster))
        needtocall = 1

    # set hooks

    if "You can" in msg:
        chunks = msg.split(". ")
        for chunk in chunks:
            if "ATTACK in" in chunk:
                weechat.unhook(ahook)
                ahook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "attack") # step in seconds
            if "CHALLENGE in" in chunk:
                weechat.unhook(chook)
                chook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "challenge") # step in seconds
            if "SLAY in" in chunk:
                weechat.unhook(shook)
                shook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "slay") # step in seconds

    # if we need to, call the bot

    if needtocall == 1:
        callbot()

    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

# initialise variables

SCRIPT_NAME = 'weechat-multirpg'
SCRIPT_AUTHOR = 'drwhitehouse'
SCRIPT_VERSION = '1.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'fully automatic multirpg playing script'
CONFIG_FILE_NAME = "multirpg"

# config file and options
multirpg_config_file = ""
multirpg_config_option = {}

# initialise mylevel
mylevel = 0

# initialise foes
creep = "bush"
monster = "medusa"

# initialise bank account
bank = 0

# register the script
weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

# read configuration
multirpg_config_init()
multirpg_config_read()
mynick = weechat.config_string(multirpg_config_option['mynick'])
myclass = weechat.config_string(multirpg_config_option['myclass'])
ircserver = weechat.config_string(multirpg_config_option['ircserver'])

# create script buffer
scriptbuffer = weechat.buffer_new("weechat-multirpg", "buffer_input_cb", "", "buffer_close_cb", "")

# set title
weechat.buffer_set(scriptbuffer, "title", "weechat-multirpg - multirpg bot for weechat.")

# disable logging, by setting local variable "no_log" to "1"
weechat.buffer_set(scriptbuffer, "localvar_set_no_log", "1")

# start script
weechat.prnt(scriptbuffer, "%sStarting weechat-multirpg..." % weechat.color("green,black"))
weechat.prnt(scriptbuffer, "")
weechat.prnt(scriptbuffer, "Version - %s" % SCRIPT_VERSION)
weechat.prnt(scriptbuffer, "")

# create channel buffer
chanbuffer = weechat.info_get("irc_buffer", "%s, #multirpg" %(ircserver))

# query bot
weechat.command(chanbuffer, "/query multirpg")
botbuffer = weechat.current_buffer()

# query other bot
weechat.command(chanbuffer, "/query Mingbeast")
mingbuffer = weechat.current_buffer()

# initialise hooks
ahook = ""
chook = ""
shook = ""
lhook = ""
phook = weechat.hook_print("", "notify_private,nick_multirpg,nick_Mingbeast", "", 0, "msgparser", "")

# initialise counters
acount = 0
ccount = 0
scount = 0
lcount = 0

# setup bar
mrpgcounters = weechat.bar_item_new("mrpgcounters", "show_mrpgcounters", "")
ctrbar = weechat.bar_new("mrpgbar", "off", "100", "window", "${buffer.full_name} == python.weechat-multirpg", "top", "horizontal", "vertical",
            "0", "5", "default", "white", "blue", "off", "mrpgcounters")

# Issue callbot command to kick us off...
callbot()
