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

# create buffer
buffer = weechat.buffer_new("weechat-multirpg", "buffer_input_cb", "", "buffer_close_cb", "")

# set title
weechat.buffer_set(buffer, "Weechat Multirpg", "This is title for my buffer.")

# disable logging, by setting local variable "no_log" to "1"
weechat.buffer_set(buffer, "localvar_set_no_log", "1")

weechat.prnt(buffer, "Hello, from python script!")
