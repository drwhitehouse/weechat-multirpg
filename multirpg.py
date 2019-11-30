import weechat

weechat.register("weechat-multirpg", "drwhitehouse", "1.0", "GPL3", "multirpg script", "", "")

# callback for data received in input
def buffer_input_cb(data, buffer, input_data):
    # ...
    return weechat.WEECHAT_RC_OK

# callback called when buffer is closed
def buffer_close_cb(data, buffer):
    # ...
    return weechat.WEECHAT_RC_OK

def displaybuffer(buffer, msg):
    weechat.prnt(buffer, msg)
    return weechat.WEECHAT_RC_OK

def querybot(msg, data):
    mrpgbotbuffer = weechat.info_get("irc_buffer", "freenode,multirpg")
    displaybuffer(buffer, data)
    weechat.command(mrpgbotbuffer, msg)
    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    displaybuffer(buffer, data)
    displaybuffer(buffer, bufferp)
    displaybuffer(buffer, tm)
    displaybuffer(buffer, tags)
#   displaybuffer(buffer, display)      # Not strings
#   displaybuffer(buffer, is_hilight)   # Don't prnt
    displaybuffer(buffer, prefix)
    displaybuffer(buffer, msg)
    return weechat.WEECHAT_RC_OK

#---------------------------------------------------------------------------#

#reate buffer
buffer = weechat.buffer_new("weechat-multirpg", "buffer_input_cb", "", "buffer_close_cb", "")

# set title
weechat.buffer_set(buffer, "weechat-multirpg", "This is title for my buffer.")

# disable logging, by setting local variable "no_log" to "1"
weechat.buffer_set(buffer, "localvar_set_no_log", "1")

# start script
displaybuffer(buffer, "Starting weechat-multirpg")

# create query buffer
mrpgchanbuffer = weechat.info_get("irc_buffer", "freenode,#multirpg")
weechat.command(mrpgchanbuffer, "/query multirpg")

# timer test
# weechat.hook_timer(60 * 1000, 60, 0, "querybot", "whoami")

# read test
weechat.hook_print("mrpgbuffer", "", "", 1, "msgparser", "") # catch prvmsg
