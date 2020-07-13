#
# weechat play bot for multirpg (multirpg.net)
#

# import my shiz
import weechat
import re
import sys

# callback for data received in input
def buffer_input_cb(data, buffer, input_data):
    # ...
    return weechat.WEECHAT_RC_OK

# callback called when buffer is closed
def buffer_close_cb(data, buffer):
    weechat.bar_remove(CTRBAR)
    return weechat.WEECHAT_RC_OK

# callback called when script unloaded
def unload_script_cb():
    # ...
    return weechat.WEECHAT_RC_OK

# initialise configuration
def multirpg_config_init():
    global MULTIRPG_CONFIG_FILE, MULTIRPG_CONFIG_OPTION
    MULTIRPG_CONFIG_FILE = weechat.config_new(CONFIG_FILE_NAME, "", "")
    if MULTIRPG_CONFIG_FILE == "":
        return
    section_multirpg = weechat.config_new_section(MULTIRPG_CONFIG_FILE, "multirpg", 0, 0, "", "", "", "", "", "", "", "", "", "")
    if section_multirpg == "":
        weechat.config_free(MULTIRPG_CONFIG_FILE)
        return
    MULTIRPG_CONFIG_OPTION["MYNICK"] = weechat.config_new_option(MULTIRPG_CONFIG_FILE, section_multirpg, "MYNICK", "string", "multirpg nickname", "", 0, 0, "", "", 0, "", "", "", "", "", "")
    MULTIRPG_CONFIG_OPTION["MYOPPONENT"] = weechat.config_new_option(MULTIRPG_CONFIG_FILE, section_multirpg, "MYOPPONENT", "string", "multirpg class", "", 0, 0, "", "", 0, "", "", "", "", "", "")
    MULTIRPG_CONFIG_OPTION["IRCSERVER"] = weechat.config_new_option(MULTIRPG_CONFIG_FILE, section_multirpg, "IRCSERVER", "string", "multirpg IRCSERVER", "", 0, 0, "", "", 0, "", "", "", "", "", "")

# read config file
def multirpg_config_read():
    global MULTIRPG_CONFIG_FILE
    return weechat.config_read(MULTIRPG_CONFIG_FILE)

# call bot for whoami & stats
def callbot():
    weechat.command(BOTBUFFER, "rawstats2")

# deposit gold
def depositgold(deposit):
    weechat.prnt(SCRIPTBUFFER, "Depositing: %s gold..." % (deposit))
    weechat.command(BOTBUFFER, "bank deposit %s" % (deposit))
    weechat.prnt(SCRIPTBUFFER, "")

# hire engineer
def hireengineer():
    weechat.prnt(SCRIPTBUFFER, "%sHiring engineer..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 1000")
    weechat.command(BOTBUFFER, "hire engineer")

# summon hero
def summonhero():
    weechat.prnt(SCRIPTBUFFER, "%sSummoning hero..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 1000")
    weechat.command(BOTBUFFER, "summon hero")

# upgrade engineer
def upengineer():
    weechat.prnt(SCRIPTBUFFER, "%sUpgrading engineer..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 200")
    weechat.command(BOTBUFFER, "engineer level")

# upgrade hero
def uphero():
    weechat.prnt(SCRIPTBUFFER, "%sUpgrading hero..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 200")
    weechat.command(BOTBUFFER, "hero level")

# get creep for attack
def getcreep(MYLEVEL):
    if MYLEVEL > 150:
        CREEP = "ogre"
    elif MYLEVEL > 140:
        CREEP = "wyvern"
    elif MYLEVEL > 130:
        CREEP = "beholder"
    elif MYLEVEL > 120:
        CREEP = "minotaur"
    elif MYLEVEL > 110:
        CREEP = "phoenix"
    elif MYLEVEL > 100:
        CREEP = "monkey"
    elif MYLEVEL > 90:
        CREEP = "mutant"
    elif MYLEVEL > 80:
        CREEP = "cyclops"
    elif MYLEVEL > 70:
        CREEP = "troll"
    elif MYLEVEL > 60:
        CREEP = "shadow"
    elif MYLEVEL > 50:
        CREEP = "ghost"
    elif MYLEVEL > 40:
        CREEP = "skeleton"
    elif MYLEVEL > 30:
        CREEP = "lich"
    elif MYLEVEL > 20:
        CREEP = "goblin"
    elif MYLEVEL > 15:
        CREEP = "spider"
    elif MYLEVEL > 10:
        CREEP = "locust"
    else:
        CREEP = "bush"
    return CREEP

# get monster for slay
def getmonster(mysum):
    if mysum > 10000:
        MONSTER = "hippogriff"
    elif mysum > 9000:
        MONSTER = "sphinx"
    elif mysum > 8000:
        MONSTER = "dragon"
    elif mysum > 7000:
        MONSTER = "vampire"
    elif mysum > 6000:
        MONSTER = "mammoth"
    elif mysum > 5000:
        MONSTER = "centaur"
    else:
        MONSTER = "medusa"
    return MONSTER

# gamble
def gamble(WINNER, LOSER, BETS):
    weechat.prnt(SCRIPTBUFFER, "%sBetting ..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    for _ in range(5 - BETS):
        weechat.command(BOTBUFFER, "bank withdraw 100")
        weechat.command(BOTBUFFER, "bet %s %s 100" % (WINNER, LOSER))

# have a ruck
def fight(OPPONENT, FIGHTS):
    if OPPONENT == "":
        weechat.prnt(SCRIPTBUFFER, "Mingbeast can't get its act together - set MYOPPONENT in config file.")
        weechat.prnt(SCRIPTBUFFER, "")
    else:
        weechat.prnt(SCRIPTBUFFER, "%sFighting ..." % weechat.color("red, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        for _ in range(5 - FIGHTS):
            weechat.command(BOTBUFFER, "fight %s" % (OPPONENT))

# upgrade my stuff
def upgradeitems():
    weechat.prnt(SCRIPTBUFFER, "%sUpgrading items ..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 2000")
    weechat.command(BOTBUFFER, "upgrade all 10")

# take action (attack / challenge / slay)
def takeaction(attackttl, challengettl, slayttl, CREEP, MONSTER, level):
    refresh = 0
    if attackttl < 1 and level > 9:
        refresh = 1
        weechat.prnt(SCRIPTBUFFER, "%sAttacking..." % weechat.color("red, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "attack %s" % (CREEP))
    if challengettl < 1 and level > 34:
        refresh = 1
        weechat.prnt(SCRIPTBUFFER, "%sChallenging..." % weechat.color("red, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "challenge")
    if slayttl < 1 and level > 39:
        refresh = 1
        weechat.prnt(SCRIPTBUFFER, "%sSlaying..." % weechat.color("red, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "slay %s" % (MONSTER))
    if refresh == 1:
        callbot()

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
def countdown(data, timer):
    global ACOUNT, CCOUNT, SCOUNT, LCOUNT
    if data == "attack":
        ACOUNT = timer
    if data == "challenge":
        CCOUNT = timer
    if data == "slay":
        SCOUNT = timer
    if data == "level":
        LCOUNT = timer
    if int(timer) == 0:
        callbot()
    else:
        weechat.bar_item_update("MRPGCOUNTERS")
    return weechat.WEECHAT_RC_OK

# show counters for mrpgbar
def show_mrpgcounters(data, item, window):
    global ACOUNT, CCOUNT, SCOUNT, LCOUNT, BANK, LINES
    mycontent = "attack: %s, challenge: %s, slay: %s, level: %s, bank: %s, lines parsed: %s." % (ACOUNT, CCOUNT, SCOUNT, LCOUNT, BANK, LINES)
    return mycontent

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    global MYNICK, MYOPPONENT, MYLEVEL, CREEP, MONSTER, BANK, AHOOK, CHOOK, SHOOK, LHOOK, WINNER, LOSER, OPPONENT, LINES

    # increment line count
    LINES = LINES + 1

    # Get gambling odds
    if msg.startswith("bestbet"):
        chunks = msg.split(" ")
        WINNER = chunks[1]
        LOSER = chunks[2]

    # Get fight opponent
    if msg.startswith("bestfight"):
        chunks = msg.split(" ")
        OPPONENT = chunks[1]
        if MYOPPONENT != "":
            OPPONENT = MYOPPONENT
        else:
            if OPPONENT == MYNICK:
                OPPONENT = ""

    # refresh data
    if msg.startswith("level "):
        out = msg.split()
        mystats = dict([(x, y) for x, y in zip(out[::2], out[1::2])])

        # get bank & gold
        BANK = int(mystats["bank"])
        gold = int(mystats["gold"])
        if gold > 40:
            deposit = gold - 40
            depositgold(deposit)
        if BANK >= 2000 and int(mystats["level"]) > 14:
            upgradeitems()

        # get creep & monster
        CREEP = getcreep(int(mystats["level"]))
        MONSTER = getmonster(int(mystats["sum"]))
        weechat.prnt(SCRIPTBUFFER, "Attack target: %s" % (CREEP))
        weechat.prnt(SCRIPTBUFFER, "Slay target: %s" % (MONSTER))
        weechat.prnt(SCRIPTBUFFER, "")

        # check & set engineer & hero
        if int(mystats["level"]) > 14:
            if int(mystats["englevel"]) < 9:
                if int(mystats["engineer"]) == 0 and BANK > 1000:
                    hireengineer()
                if int(mystats["engineer"]) == 1 and BANK > 200:
                    upengineer()
            if int(mystats["hlevel"]) < 9:
                if int(mystats["hero"]) == 0 and BANK > 1000:
                    summonhero()
                if int(mystats["hero"]) == 1 and BANK > 200:
                    uphero()

        # set hooks
        ATTL = int(mystats["attackttl"])
        CTTL = int(mystats["challengettl"])
        STTL = int(mystats["slayttl"])
        LTTL = int(mystats["ttl"]) + 300

        if int(mystats["level"]) > 9:
            ATTL = ATTL + 300
        if int(mystats["level"]) > 34:
            CTTL = CTTL + 300
        if int(mystats["level"]) > 39:
            STTL = STTL + 300

        weechat.unhook(AHOOK)
        AHOOK = weechat.hook_timer(1 * 1000, 60, ATTL, "countdown", "attack") # step in seconds
        weechat.unhook(CHOOK)
        CHOOK = weechat.hook_timer(1 * 1000, 60, CTTL, "countdown", "challenge") # step in seconds
        weechat.unhook(SHOOK)
        SHOOK = weechat.hook_timer(1 * 1000, 60, STTL, "countdown", "slay") # step in seconds
        weechat.unhook(LHOOK)
        LHOOK = weechat.hook_timer(1 * 1000, 60, LTTL, "countdown", "level") # step in seconds

        # take action
        takeaction(int(mystats["attackttl"]), int(mystats["challengettl"]), int(mystats["slayttl"]), CREEP, MONSTER, int(mystats["level"]))

        # fightin' and bettin'
        if int(mystats["fights"]) < 5 and int(mystats["level"]) > 9:
            if OPPONENT == "":
                weechat.command(MINGBUFFER, "!bestfight %s" % (MYNICK))
            else:
                weechat.command(MINGBUFFER, "!bestfight %s" % (MYNICK))
                fight(OPPONENT, int(mystats["fights"]))
                callbot()

        if int(mystats["bets"]) < 5 and int(mystats["level"]) > 29:
            if WINNER == "" and LOSER == "":
                weechat.command(MINGBUFFER, "!bestbet")
            else:
                weechat.command(MINGBUFFER, "!bestbet")
                gamble(WINNER, LOSER, int(mystats["bets"]))
                callbot()

    # display lines about me
    if MYNICK in msg:
        weechat.prnt(SCRIPTBUFFER, msg)
        weechat.prnt(SCRIPTBUFFER, "")
        if "has logged in" in msg:
            callbot()

    # return
    return weechat.WEECHAT_RC_OK
#---------------------------------------------------------------------------#

# initialise variables
SCRIPT_NAME = 'multirpg'
SCRIPT_AUTHOR = 'drwhitehouse'
SCRIPT_VERSION = '3.0.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'fully automatic multirpg playing script'
CONFIG_FILE_NAME = "multirpg"

# config file and options
MULTIRPG_CONFIG_FILE = ""
MULTIRPG_CONFIG_OPTION = {}

# initialise MYLEVEL
MYLEVEL = 0

# initialise foes
CREEP = "bush"
MONSTER = "medusa"

# initialise bank account
BANK = 0

# initialise winner / loser
WINNER = ""
LOSER = ""

# initialise opponent
OPPONENT = ""

# initialise line count
LINES = 0

# register the script
weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

# read configuration
multirpg_config_init()
multirpg_config_read()
MYNICK = weechat.config_string(MULTIRPG_CONFIG_OPTION['MYNICK'])
MYOPPONENT = weechat.config_string(MULTIRPG_CONFIG_OPTION['MYOPPONENT'])
IRCSERVER = weechat.config_string(MULTIRPG_CONFIG_OPTION['IRCSERVER'])

# create script buffer
SCRIPTBUFFER = weechat.buffer_new("weechat-multirpg", "buffer_input_cb", "", "buffer_close_cb", "")

# set title
weechat.buffer_set(SCRIPTBUFFER, "title", "weechat-multirpg - multirpg bot for weechat.")

# disable logging, by setting local variable "no_log" to "1"
weechat.buffer_set(SCRIPTBUFFER, "localvar_set_no_log", "1")

# start script
weechat.prnt(SCRIPTBUFFER, "%sStarting weechat-multirpg..." % weechat.color("green,black"))
weechat.prnt(SCRIPTBUFFER, "")
PYMAJOR = sys.version_info[0]
PYMINOR = sys.version_info[1]
PYMICRO = sys.version_info[2]
weechat.prnt(SCRIPTBUFFER, "Weechat Version - %s" % weechat.info_get("version", ""))
weechat.prnt(SCRIPTBUFFER, "")
weechat.prnt(SCRIPTBUFFER, "Python Version - %s.%s.%s" % (PYMAJOR, PYMINOR, PYMICRO))
weechat.prnt(SCRIPTBUFFER, "")
weechat.prnt(SCRIPTBUFFER, "Script Version - %s" % SCRIPT_VERSION)
weechat.prnt(SCRIPTBUFFER, "")

# create channel buffer
CHANBUFFER = weechat.info_get("irc_buffer", "%s, #multirpg" %(IRCSERVER))

# query bot
weechat.command(CHANBUFFER, "/query multirpg")
BOTBUFFER = weechat.current_buffer()

# query other bot
weechat.command(CHANBUFFER, "/query Mingbeast")
MINGBUFFER = weechat.current_buffer()

# initialise hooks
AHOOK = ""
CHOOK = ""
SHOOK = ""
LHOOK = ""
PHOOK = weechat.hook_print("", "notify_private,nick_multirpg,nick_Mingbeast", "", 0, "msgparser", "")

# initialise counters
ACOUNT = 0
CCOUNT = 0
SCOUNT = 0
LCOUNT = 0

# setup bar
MRPGCOUNTERS = weechat.bar_item_new("MRPGCOUNTERS", "show_mrpgcounters", "")
CTRBAR = weechat.bar_new("mrpgbar", "off", "100", "window", "${buffer.full_name} == python.weechat-multirpg", "top", "horizontal", "vertical",
                         "0", "5", "default", "white", "blue", "off", "MRPGCOUNTERS")

# Issue command to kick us off...
callbot()
