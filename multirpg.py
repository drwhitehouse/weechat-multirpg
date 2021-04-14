#
# weechat play bot for multirpg (multirpg.net)
#

# import my shiz
import weechat
import re
import sys
import time

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
    MULTIRPG_CONFIG_OPTION["MYALIGNMENT"] = weechat.config_new_option(MULTIRPG_CONFIG_FILE, section_multirpg, "MYALIGNMENT", "string", "multirpg class", "", 0, 0, "", "", 0, "", "", "", "", "", "")
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
def getcreep(my_level):
    if my_level > 150:
        my_creep = "ogre"
    elif my_level > 140:
        my_creep = "wyvern"
    elif my_level > 130:
        my_creep = "beholder"
    elif my_level > 120:
        my_creep = "minotaur"
    elif my_level > 110:
        my_creep = "phoenix"
    elif my_level > 100:
        my_creep = "monkey"
    elif my_level > 90:
        my_creep = "mutant"
    elif my_level > 80:
        my_creep = "cyclops"
    elif my_level > 70:
        my_creep = "troll"
    elif my_level > 60:
        my_creep = "shadow"
    elif my_level > 50:
        my_creep = "ghost"
    elif my_level > 40:
        my_creep = "skeleton"
    elif my_level > 30:
        my_creep = "lich"
    elif my_level > 20:
        my_creep = "goblin"
    elif my_level > 15:
        my_creep = "spider"
    elif my_level > 10:
        my_creep = "locust"
    else:
        my_creep = "bush"
    return my_creep

# get monster for slay
def getmonster(my_sum):
    if my_sum > 10000:
        my_monster = "hippogriff"
    elif my_sum > 9000:
        my_monster = "sphinx"
    elif my_sum > 8000:
        my_monster = "dragon"
    elif my_sum > 7000:
        my_monster = "vampire"
    elif my_sum > 6000:
        my_monster = "mammoth"
    elif my_sum > 5000:
        my_monster = "centaur"
    else:
        my_monster = "medusa"
    return my_monster

# gamble
def gamble(WINNER, LOSER, BETS):
    weechat.prnt(SCRIPTBUFFER, "%sBetting ..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    for _ in range(5 - BETS):
        weechat.command(BOTBUFFER, "bank withdraw 100")
        weechat.command(BOTBUFFER, "bet %s %s 100" % (WINNER, LOSER))

# have a ruck
def fight(OPPONENT, FIGHTS):
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

# refresh bar
def refreshbar():
    weechat.bar_item_update("MRPGCOUNTERS")
    return weechat.WEECHAT_RC_OK

# show counters for mrpgbar
def show_mrpgcounters(data, item, window):
    time_now = int(time.time())
    if int(my_player['level']) > 9:
        a_time = time.strftime("%H:%M", time.gmtime(int(my_player['regentm']) - time_now))
    else:
        a_time = 'level 10'
    if int(my_player['level']) > 34:
        c_time = time.strftime("%H:%M", time.gmtime(int(my_player['challengetm']) - time_now))
    else:
        c_time = 'level 35'
    if int(my_player['level']) > 39:
        s_time = time.strftime("%H:%M", time.gmtime(int(my_player['slaytm']) - time_now))
    else:
        s_time = 'level 40'
    ttltime = float(my_player['ttl'])
    day = ttltime // (24 * 3600)
    ttltime = ttltime % (24 * 3600)
    hour = ttltime // 3600
    ttltime %= 3600
    minutes = ttltime // 60
    my_content = "rank: %s, level: %s, sum: %s, gold: %s, bank: %s, attack: %s, challenge: %s, slay: %s, ttl: %s days, %s:%s." % (my_player['rank'],
                                                                                                                     my_player['level'],
                                                                                                                     my_player['sum'],
                                                                                                                     my_player['gold'],
                                                                                                                     my_player['bank'],
                                                                                                                     a_time,
                                                                                                                     c_time,
                                                                                                                     s_time,
                                                                                                                     int(day),
                                                                                                                     str(int(hour)).zfill(2),
														     str(int(minutes)).zfill(2))
    return my_content

# get rawplayers3 from url
def get_rawplayers3(data, timer):
    weechat.hook_process("url:http://multirpg.net/rawplayers3.php",60 * 1000, "rawplayers3_cb", "")
    return weechat.WEECHAT_RC_OK

# rawplayers3 callback
def rawplayers3_cb(data, command, rc, out, err):
    global raw_players
    if out != "":
	raw_players += out
        if int(rc) >= 0:
            get_allplayers()
            get_stats()
            check_alignment()
            check_finances()
            takeaction()
            betting()
            getopponent()
            fighting()
            refreshbar()
    return weechat.WEECHAT_RC_OK

# get all_players
def get_allplayers():
    global raw_players, all_players
    player = ""
    all_players = {}
    myrawplayers = re.sub(r'\{[^{}]*\}', lambda x: x.group(0).replace(' ','_'), raw_players)
    for player in myrawplayers.splitlines():
        playerstats = dict([(x, y) for x, y in zip(player.split()[::2], player.split()[1::2])])
        all_players[playerstats['rank']] = playerstats
    raw_players = ""

# get my_player
def get_stats():
    global my_player
    for player in all_players:
        this_player = all_players[player]
        if this_player['char'] == MYNICK:
            my_player = this_player

# check my alignment
def check_alignment():
    global MYALIGNMENT
    if MYALIGNMENT == "priest":
        my_alignment = "g"
    elif MYALIGNMENT == "undead":
        my_alignment = "e"
    else:
        MYALIGNMENT = "human"
        my_alignment = "n"
    if int(my_player['level']) < 10:
        if my_player['align'] != "g":
            weechat.command(BOTBUFFER, "align priest")
    else:
        if my_alignment != my_player['align']:
            weechat.command(BOTBUFFER, "align %s" % (MYALIGNMENT))

# get bank & gold
def check_finances():
    bank = int(my_player['bank'])
    gold = int(my_player['gold'])
    if gold > 40:
        my_deposit = gold - 40
        depositgold(my_deposit)
    elif int(my_player['level']) > 14:
        if int(my_player['englevel']) < 9:
            if int(my_player['engineer']) == 0 and bank > 1000:
                hireengineer()
            if int(my_player['engineer']) == 1 and bank > 200:
                upengineer()
        elif int(my_player['hlevel']) < 9:
            if int(my_player['hero']) == 0 and bank > 1000:
                summonhero()
            if int(my_player['hero']) == 1 and bank > 200:
                uphero()
        elif bank >= 2000:
            upgradeitems()

# take action (attack / challenge / slay)
def takeaction():
    time_now = int(time.time())
    if int(my_player['level']) > 9:
	if time_now > int(my_player['regentm']):
            my_creep = getcreep(int(my_player["level"]))
            weechat.prnt(SCRIPTBUFFER, "%sAttacking..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "attack %s" % (my_creep))
    if int(my_player['level']) > 34:
	if time_now > int(my_player['challengetm']):
            weechat.prnt(SCRIPTBUFFER, "%sChallenging..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "challenge")
    if int(my_player['level']) > 39:
	if time_now > int(my_player['slaytm']):
            my_monster = getmonster(int(my_player["sum"]))
            weechat.prnt(SCRIPTBUFFER, "%sSlaying..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "slay %s" % (my_monster))

def betting():
    if int(my_player["bets"]) < 5 and int(my_player["level"]) > 29:
        if WINNER == "" and LOSER == "":
            weechat.command(MINGBUFFER, "!bestbet")
        else:
            weechat.command(MINGBUFFER, "!bestbet")
            gamble(WINNER, LOSER, int(my_player["bets"]))

def getopponent():
    global OPPONENT
    candidates = {}
    final_selection = {}
    keylist = []

    # Get all players my level or above who aren't me or on my team and key by rank.

    for player in all_players:
        this_player = all_players[player]
        if int(this_player['online']) == 1:
            if int(this_player['level']) >= int(my_player['level']):
                if this_player['char'] != MYNICK and this_player['team'] != my_player['team']:
                    candidates[this_player['rank']] = this_player

    # Go through the candidates calculating and keying by effective sum.

    for candidate in candidates:
        this_candidate = candidates[candidate]
        bonus = int(0.1 * int(this_candidate['sum']))
        if this_candidate['align'] == "g":
            effective_sum = int(this_candidate['sum']) + bonus
        elif this_candidate['align'] == "e":
            effective_sum = int(this_candidate['sum']) - bonus
        else:
            effective_sum = int(this_candidate['sum'])
        final_selection[str(effective_sum)] = this_candidate

    # Go through that getting a list of the keys.

    for finalist in final_selection:
        keylist.append(int(finalist))
        keylist.sort()
    my_guy = keylist[0]
    my_dude = final_selection[str(my_guy)]
    OPPONENT = my_dude['char']
    mybonus = int(0.1 * int(my_player['sum']))
    if my_player['align'] == "g":
        my_effective_sum = int(my_player['sum']) + mybonus
    elif my_player['align'] == "e":
        my_effective_sum = int(my_player['sum']) - mybonus
    else:
        my_effective_sum = int(my_player['sum'])
    if my_effective_sum < int(my_guy):
        OPPONENT = ""

def fighting():
    if int(my_player['level']) > 9 and int(my_player['level']) < 200:
        if int(my_player['fights']) < 5:
            if OPPONENT == "":
                weechat.prnt(SCRIPTBUFFER, "No suitable opponent...")
                weechat.prnt(SCRIPTBUFFER, "")
            else:
                fight(OPPONENT, int(my_player["fights"]))

#---------------------------------------------------------------------------#

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    global WINNER, LOSER, OPPONENT

    # Get gambling odds
    if msg.startswith("bestbet"):
        chunks = msg.split(" ")
        WINNER = chunks[1]
        LOSER = chunks[2]

    # display lines about me
    if MYNICK in msg:
        weechat.prnt(SCRIPTBUFFER, msg)
        weechat.prnt(SCRIPTBUFFER, "")

    # return
    return weechat.WEECHAT_RC_OK
#---------------------------------------------------------------------------#

# initialise variables
SCRIPT_NAME = 'multirpg'
SCRIPT_AUTHOR = 'drwhitehouse'
SCRIPT_VERSION = '5.1.0'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'fully automatic multirpg playing script'
CONFIG_FILE_NAME = "multirpg"

raw_players = ""
all_players = {}
my_player = {}

# config file and options
MULTIRPG_CONFIG_FILE = ""
MULTIRPG_CONFIG_OPTION = {}

# initialise winner / loser
WINNER = ""
LOSER = ""

# initialise opponent
OPPONENT = ""

# register the script
weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

# read configuration
multirpg_config_init()
multirpg_config_read()
MYNICK = weechat.config_string(MULTIRPG_CONFIG_OPTION['MYNICK'])
MYALIGNMENT = weechat.config_string(MULTIRPG_CONFIG_OPTION['MYALIGNMENT'])
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
PHOOK = weechat.hook_print("", "notify_private,nick_multirpg,nick_Mingbeast", "", 0, "msgparser", "")

# setup bar
MRPGCOUNTERS = weechat.bar_item_new("MRPGCOUNTERS", "show_mrpgcounters", "")
CTRBAR = weechat.bar_new("mrpgbar", "off", "100", "window", "${buffer.full_name} == python.weechat-multirpg", "top", "horizontal", "vertical",
                         "0", "5", "default", "white", "blue", "off", "MRPGCOUNTERS")

#############################################################################

# Issue command to kick us off with this new bullshit...
get_rawplayers3("", "")

# Get data every 5 minutes...
DELAY = 300
weechat.hook_timer(DELAY * 1000, 0, 0, "get_rawplayers3", "")

#############################################################################
