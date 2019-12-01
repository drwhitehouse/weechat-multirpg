# import my shiz
import weechat
import re

# register the script
weechat.register("weechat-multirpg", "drwhitehouse", "1.0", "GPL3", "multirpg script", "", "")

# some variables
myserver="freenode"
mynick="horseshoecrab"

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
    return weechat.WEECHAT_RC_OK

# send query to bot
def querybot(msg):
    weechat.command(botbuffer, msg)
    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    displaybuffer(buffer, data)
#    displaybuffer(buffer, bufferp)
#    displaybuffer(buffer, tm)
#    displaybuffer(buffer, tags)
#   displaybuffer(buffer, display)      # Not strings
#   displaybuffer(buffer, is_hilight)   # Don't prnt
    displaybuffer(buffer, prefix)
    displaybuffer(buffer, msg)

    if msg.startswith("You can"):
        chunks = msg.split("You can")
        for chunk in chunks:
            displaybuffer(buffer, chunk)
            if "ATTACK in" in chunk:
                digits = [int(s) for s in re.findall(r'\b\d+\b', chunk)]
                for digit in digits:
                    displaybuffer(buffer, str(digit))
                attackcounter = 0
                attackcounter = attackcounter + digits[0] * 86400
                attackcounter = attackcounter + digits[1] * 3600
                attackcounter = attackcounter + digits[2] * 60
                attackcounter = attackcounter + digits[3]
                displaybuffer(buffer, str(attackcounter))
    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

# create script buffer
buffer = weechat.buffer_new("weechat-multirpg", "buffer_input_cb", "", "buffer_close_cb", "")

# set title
weechat.buffer_set(buffer, "title", "weechat-multirpg - multirpg bot for weechat.")

# disable logging, by setting local variable "no_log" to "1"
weechat.buffer_set(buffer, "localvar_set_no_log", "1")

# create channel buffer
chanbuffer = weechat.info_get("irc_buffer", 'myserver,#multirpg')

# start script
displaybuffer(buffer, "Starting weechat-multirpg")

# query bot
weechat.command(chanbuffer, "/query multirpg")

# create bot buffer
botbuffer = weechat.info_get("irc_buffer", 'myserver,multirpg')

# timer test
# weechat.hook_timer(60 * 1000, 60, 0, "querybot", "whoami")

# read test
weechat.hook_print("chanbuffer", "", 'mynick', 0, "msgparser", "")
weechat.hook_print("botbuffer", "notify_private", "", 1, "msgparser", "")

# getting stats
querybot("stats")
