# import my shiz
import weechat
import re

# register the script
weechat.register("weechat-multirpg", "drwhitehouse", "1.0", "GPL3", "multirpg script", "unload_script_cb", "")

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
    global mynick, myclass, creep, monster, bank, ahook, chook, shook, lhook

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
                bank = bank + deposit

    if msg.startswith("Power Potions:"):
        has_eng = getdigits(msg)[5]
        eng_lvl = getdigits(msg)[6]
        has_her = getdigits(msg)[3]
        her_lvl = getdigits(msg)[4]
        if eng_lvl < 9:
            if has_eng == 0 and bank > 1500:
                weechat.prnt(scriptbuffer, "Hiring engineer...")
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 1000")
                bank = bank - 1000
                weechat.command(botbuffer, "hire engineer")
            if has_eng == 1 and bank > 200:
                weechat.prnt(scriptbuffer, "%sUpgrading engineer..." % weechat.color("red, black"))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 200")
                bank = bank - 200
                weechat.command(botbuffer, "engineer level")
        if her_lvl < 9:
            if has_her == 0 and bank > 1500:
                weechat.prnt(scriptbuffer, "Summoning hero...")
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 1000")
                bank = bank - 1000
                weechat.command(botbuffer, "summon hero")
            if has_her == 1 and bank > 200:
                weechat.prnt(scriptbuffer, "%sUpgrading hero..." % weechat.color("red, black"))
                weechat.prnt(scriptbuffer, "")
                weechat.command(botbuffer, "bank withdraw 200")
                bank = bank - 200
                weechat.command(botbuffer, "hero level")

    if bank >= 2000:
        weechat.prnt(scriptbuffer, "Upgrading items ...")
        weechat.prnt(scriptbuffer, "")
        weechat.command(botbuffer, "bank withdraw 2000")
        weechat.command(botbuffer, "upgrade boots 100")
        bank = bank - 2000

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
        callbot()

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

    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

# initialise variables
CONFIG_FILE_NAME = "multirpg"

# config file and options
multirpg_config_file = ""
multirpg_config_option = {}

# initialise foes
creep = "bush"
monster = "medusa"

# initialise bank account
bank = 0

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

# create channel buffer
chanbuffer = weechat.info_get("irc_buffer", "%s, #multirpg" %(ircserver))

# query bot
weechat.command(chanbuffer, "/query multirpg")
botbuffer = weechat.current_buffer()

# initialise hooks
ahook = ""
chook = ""
shook = ""
lhook = ""
phook = weechat.hook_print("", "notify_private,nick_multirpg", "", 0, "msgparser", "")

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
