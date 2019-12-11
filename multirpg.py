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

# get seconds
def getseconds(msg):
    seconds = 0
    digits = [int(s) for s in re.findall(r'\b\d+\b', msg)]
    seconds = seconds + digits[0] * 86400       # Days
    seconds = seconds + digits[1] * 3600        # Hours
    seconds = seconds + digits[2] * 60          # Minutes
    seconds = seconds + digits[3]               # Seconds
    return seconds

# countdown
def countdown(data,timer):
    global acount, ccount, scount 
    if data == "attack":
        acount = timer
    if data == "challenge":
        ccount = timer
    if data == "slay":
        scount = timer
    if int(timer) == 0:
        weechat.command(botbuffer, "stats")
    else:
        weechat.bar_item_update("mrpgbar")
    return weechat.WEECHAT_RC_OK

def show_mrpgbar(data, item, window):
    global acount, ccount, scount
    mycontent = "a:%s c:%s s:%s" % (acount, ccount, scount)
    return mycontent

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    global ahook, chook, shook

    creep = "skeleton"
    monster = "medusa"

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
        weechat.command(botbuffer, "stats")

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

    # display lines about me

    if "horseshoecrab" in msg:
        weechat.prnt(scriptbuffer, msg)
        weechat.prnt(scriptbuffer, "")

    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

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
chanbuffer = weechat.info_get("irc_buffer", "freenode, #multirpg")

# query bot
weechat.command(chanbuffer, "/query multirpg")
botbuffer = weechat.current_buffer()

# initialise hooks
ahook = "0"
chook = "0"
shook = "0"
phook = weechat.hook_print("", "notify_private,nick_multirpg", "", 0, "msgparser", "")

# initialise counters
acount = 0
ccount = 0
scount = 0

# setup bar
mrpgbar = weechat.bar_item_new("mrpgbar", "show_mrpgbar", "")
weechat.bar_item_update("mrpgbar")

# Issue stats command to kick us off...
weechat.prnt(scriptbuffer, "Running stats to get counters...")
weechat.prnt(scriptbuffer, "")
weechat.command(botbuffer, "stats")
