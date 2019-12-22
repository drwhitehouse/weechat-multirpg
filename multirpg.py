# import my shiz
import weechat
import re

# register the script
weechat.register("weechat-multirpg", "drwhitehouse", "1.0", "GPL3", "multirpg script", "", "")

# callback for data received in input
def buffer_input_cb(data, buffer, input_data):
    # ...
    return weechat.WEECHAT_RC_OK

# callback called when buffer is closed
def buffer_close_cb(data, buffer):
    # ...
    return weechat.WEECHAT_RC_OK

# call bot for whoami & stats
def callbot():
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

# get seconds
def getseconds(msg):
    seconds = 0
    digits = [int(s) for s in re.findall(r'\b\d+\b', msg)]
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
        weechat.bar_item_update("mrpgbar")
    return weechat.WEECHAT_RC_OK

def show_mrpgbar(data, item, window):
    global acount, ccount, scount, lcount
    mycontent = "a:%s c:%s s:%s l:%s" % (acount, ccount, scount, lcount)
    return mycontent

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    global mynick, myclass, creep, ahook, chook, shook, lhook

    monster = "medusa"

    # display lines about me

    if mynick in msg:
        weechat.prnt(scriptbuffer, msg)
        weechat.prnt(scriptbuffer, "")
        if myclass in msg:
            chunks = msg.split(". ")
            for chunk in chunks:
                if chunk.startswith("You are"):
                    mylevel = [int(s) for s in re.findall(r'\b\d+\b', chunk)]
                    creep = getcreep(mylevel[0])
                    weechat.prnt(scriptbuffer, "Attack target: %s" % (creep))
                    weechat.prnt(scriptbuffer, "")
                if chunk.startswith("Next level"):
                    weechat.prnt(scriptbuffer, "Resetting ttl counter...")
                    weechat.prnt(scriptbuffer, "")
                    weechat.unhook(lhook)
                    lhook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "level") # step in seconds

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
                weechat.prnt(scriptbuffer, "Resetting attack counter...")
                weechat.prnt(scriptbuffer, "")
                weechat.unhook(ahook)
                ahook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "attack") # step in seconds
	    if "CHALLENGE in" in chunk:
                weechat.prnt(scriptbuffer, "Resetting challenge counter...")
                weechat.prnt(scriptbuffer, "")
                weechat.unhook(chook)
                chook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "challenge") # step in seconds
	    if "SLAY in" in chunk:
                weechat.prnt(scriptbuffer, "Resetting slay counter...")
                weechat.prnt(scriptbuffer, "")
                weechat.unhook(shook)
                shook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "slay") # step in seconds

    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

# initialise variables
mynick = "horseshoecrab"
myclass = "weechat tester"
ircserver = "freenode"

# initialise foes
creep = ""

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
mrpgbar = weechat.bar_item_new("mrpgbar", "show_mrpgbar", "")
weechat.bar_item_update("mrpgbar")

# Issue stats command to kick us off...
weechat.prnt(scriptbuffer, "Getting counters...")
weechat.prnt(scriptbuffer, "")
callbot()
