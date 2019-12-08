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

# send stats
def sendstats(data,timer):
    displaybuffer(scriptbuffer, "Sending stats:")
    weechat.command(botbuffer, "stats")
    return weechat.WEECHAT_RC_OK

# get seconds
def getseconds(msg):
    attackcounter = 0
    displaybuffer(scriptbuffer, msg)
    digits = [int(s) for s in re.findall(r'\b\d+\b', msg)]
    for digit in digits:
        attackcounter = attackcounter + digits[0] * 86400
        attackcounter = attackcounter + digits[1] * 3600
        attackcounter = attackcounter + digits[2] * 60
        attackcounter = attackcounter + digits[3]
    displaybuffer(scriptbuffer, str(attackcounter))

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    #displaybuffer(scriptbuffer, "---")
    #displaybuffer(scriptbuffer, data)              # Very boring
    #displaybuffer(scriptbuffer, bufferp)
    #displaybuffer(scriptbuffer, tm)
    #displaybuffer(scriptbuffer, tags)
    #displaybuffer(scriptbuffer, str(display))      # Not strings
    #displaybuffer(scriptbuffer, str(is_hilight))   # Don't prnt
    #displaybuffer(scriptbuffer, prefix)
    #displaybuffer(scriptbuffer, msg)
    #displaybuffer(scriptbuffer, "---")

    if "You can now ATTACK." in msg:
        displaybuffer(scriptbuffer, "Attacking:")
        weechat.command(botbuffer, "attack lich")

    if "You can now CHALLENGE." in msg:
        displaybuffer(scriptbuffer, "Challenging:")
        weechat.command(botbuffer, "challenge")

    if msg.startswith("You can ATTACK"):
        chunks = msg.split("You can")
        for chunk in chunks:
	    if "in" in chunk:
                getseconds(chunk)

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

# debug
displaybuffer(scriptbuffer, "Buffer pointers:")
displaybuffer(scriptbuffer, "")
displaybuffer(scriptbuffer, "---")
displaybuffer(scriptbuffer, "scriptbuffer:")
displaybuffer(scriptbuffer,str(scriptbuffer))
displaybuffer(scriptbuffer, "")
displaybuffer(scriptbuffer, "chanbuffer:")
displaybuffer(scriptbuffer,str(chanbuffer))
displaybuffer(scriptbuffer, "")
displaybuffer(scriptbuffer, "botbuffer:")
displaybuffer(scriptbuffer,str(botbuffer))
displaybuffer(scriptbuffer, "---")

# hooks
#weechat.hook_print(botbuffer, "", "", 0, "msgparser", "")
#weechat.hook_print(chanbuffer, "nick_multirpg", "", 0, "msgparser", "")
#weechat.hook_print("", "nick_multirpg", "", 0, "msgparser", "")
#weechat.hook_print("", "notify_private,nick_multirpg", "", 0, "msgparser", "")

# set timer
weechat.hook_timer(75 * 60 * 1000, 0, 0, "sendstats", "")

# set print hook
weechat.hook_print("", "notify_private", "", 0, "msgparser", "") # Private only
#weechat.hook_print("", "nick_multirpg", "", 0, "msgparser", "") # Multirpg

# initialising
displaybuffer(scriptbuffer, "Sending whoami & stats:")
displaybuffer(scriptbuffer, "")
weechat.command(botbuffer, "whoami")
weechat.command(botbuffer, "stats")
