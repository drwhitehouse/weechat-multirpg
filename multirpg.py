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

# print to buffer
def displaybuffer(buffer, msg):
    weechat.prnt(buffer, msg)

# get seconds
def getseconds(msg):
    attackcounter = 0
    displaybuffer(scriptbuffer, msg)
    digits = [int(s) for s in re.findall(r'\b\d+\b', msg)]
    attackcounter = attackcounter + digits[0] * 86400       # Days
    attackcounter = attackcounter + digits[1] * 3600        # Hours
    attackcounter = attackcounter + digits[2] * 60          # Minutes
    attackcounter = attackcounter + digits[3]               # Seconds
    attackcounter = attackcounter + 10                      # And 10 more for luck
    displaybuffer(scriptbuffer, str(attackcounter))
    return attackcounter

# hook init
def hookinit(data,timer):
    if int(timer) == 0:
        displaybuffer(scriptbuffer, "Hook initialised...")
    else:
        displaybuffer(scriptbuffer, timer)
    return weechat.WEECHAT_RC_OK

# countdown
def countdown(data,timer):
    if int(timer) == 0:
        weechat.command(botbuffer, "stats")
    else:
        displaybuffer(scriptbuffer, timer)
    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    global ahook, chook, shook, phook

    # take action

    if "You can now" in msg:
        if "You can now ATTACK." in msg:
            displaybuffer(scriptbuffer, "Attacking:")
            weechat.command(botbuffer, "attack lich")
        if "You can now CHALLENGE." in msg:
            displaybuffer(scriptbuffer, "Challenging:")
            weechat.command(botbuffer, "challenge")
        if "You can now CHALLENGE." in msg:
            displaybuffer(scriptbuffer, "Slaying:")
            weechat.command(botbuffer, "slay madusa")
        weechat.command(botbuffer, "stats")

    # set hooks

    if "You can" in msg:
        chunks = msg.split(". ")
        for chunk in chunks:
	    if "ATTACK in" in chunk:
                weechat.unhook(ahook)
                ahook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "") # step in seconds
	    if "CHALLENGE in" in chunk:
                weechat.unhook(chook)
                chook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "") # step in seconds
	    if "SLAY in" in chunk:
                weechat.unhook(shook)
                shook = weechat.hook_timer(1 * 1000, 60, getseconds(chunk), "countdown", "") # step in seconds

    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

# create script buffer
scriptbuffer = weechat.buffer_new("weechat-multirpg", "buffer_input_cb", "", "buffer_close_cb", "")

# set title
weechat.buffer_set(scriptbuffer, "title", "weechat-multirpg - multirpg bot for weechat.")

# disable logging, by setting local variable "no_log" to "1"
weechat.buffer_set(scriptbuffer, "localvar_set_no_log", "1")

# start script
displaybuffer(scriptbuffer, "Starting weechat-multirpg")
displaybuffer(scriptbuffer, "")

# create channel buffer
chanbuffer = weechat.info_get("irc_buffer", "freenode, #multirpg")

# query bot
weechat.command(chanbuffer, "/query multirpg")
botbuffer = weechat.current_buffer()

# initialise hooks
ahook = weechat.hook_timer(1 * 1000, 60, 60, "hookinit", "")
chook = weechat.hook_timer(1 * 1000, 60, 120, "hookinit", "")
shook = weechat.hook_timer(1 * 1000, 60, 240, "hookinit", "")
phook = weechat.hook_print("", "notify_private", "", 0, "msgparser", "")
