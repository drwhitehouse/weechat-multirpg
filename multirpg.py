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
def get_creep(my_level):
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
    elif my_level > 70:
        my_creep = "monkey"
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
def get_monster(my_sum):
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
def gamble(WINNER, LOSER):
    weechat.prnt(SCRIPTBUFFER, "%sBetting ..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 100")
    weechat.command(BOTBUFFER, "bet %s %s 100" % (WINNER, LOSER))

# have a ruck
def fight(my_opponent):
    weechat.prnt(SCRIPTBUFFER, "%sFighting ..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "align priest")
    weechat.command(BOTBUFFER, "fight %s" % (my_opponent))

# upgrade my stuff
def upgradeitems(my_player, cash):
    if cash > 200 and int(my_player['hlevel']) == 9:
        if int(my_player['bets']) == 5:
            if cash > 1999:
                lvl = 10
                wd = 2000
                cash = cash - wd
            elif cash > 999:
                lvl = 5
                wd = 1000
                cash = cash - wd
            else:
                lvl = 1
                wd = 200
                cash = cash - wd
            weechat.prnt(SCRIPTBUFFER, "%sUpgrading items ..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "bank withdraw %s" % (wd))
            weechat.command(BOTBUFFER, "upgrade all %s" % (lvl))
    return cash

# refresh bar
def refreshbar():
    weechat.bar_item_update("MRPGCOUNTERS")
    return weechat.WEECHAT_RC_OK

# show counters for mrpgbar
def show_mrpgcounters(data, item, window):
    return my_content

# get rawplayers3 from url
def get_rawplayers3(data, timer):
    weechat.hook_process("url:http://multirpg.net/rawplayers3.php",60 * 1000, "rawplayers3_cb", "")
    return weechat.WEECHAT_RC_OK

# rawplayers3 callback
def rawplayers3_cb(data, command, rc, out, err):
    global raw_players, my_content
    if out != "":
        raw_players += out
        if int(rc) >= 0:
            my_player, all_players = get_stats(raw_players)
            if int(my_player['online']) == 1:
                check_alignment(my_player)
                cash = check_finances(my_player)
                cash = go_shopping(my_player, cash)
                cash = hire_sidekicks(my_player, cash)
                takeaction(my_player)
                if int(my_player['level']) > 29:
                    challenger, opponent, odds = bestbet(all_players)
                    weechat.prnt(SCRIPTBUFFER, "Best bet: %s vs %s odds: %s" % (challenger, opponent, odds))
                    weechat.prnt(SCRIPTBUFFER, "")
                    if int(my_player['bets']) < 5:
                        cash = betting(challenger, opponent, cash)
                cash = upgradeitems(my_player, cash)
                if int(my_player['level']) > 9 and int(my_player['level']) < 200:
                    my_opponent, odds = get_opponent(my_player, all_players)
                    weechat.prnt(SCRIPTBUFFER, "Best fight: %s Odds: %s" % (str(my_opponent), str(odds)))
                    weechat.prnt(SCRIPTBUFFER, "")
                    if odds > 1:
                        fighting(my_player, my_opponent)
            else:
                weechat.prnt(SCRIPTBUFFER, "%s WARNING: offline" % weechat.color("red, black"))
                weechat.prnt(SCRIPTBUFFER, "")
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
            mins = ttltime // 60
            my_content = "rank: %s, level: %s, sum: %s, gold: %s, bank: %s, attack: %s, challenge: %s, slay: %s, ttl: %s days, %s:%s" % (my_player['rank'],
                                                                                                                                         my_player['level'],
                                                                                                                                         my_player['sum'],
                                                                                                                                         my_player['gold'],
                                                                                                                                         my_player['bank'],
                                                                                                                                         a_time,
                                                                                                                                         c_time,
                                                                                                                                         s_time,
                                                                                                                                         int(day),
                                                                                                                                         str(int(hour)).zfill(2),
                                                                                                                                         str(int(mins)).zfill(2),
)
            refreshbar()
            raw_players = ""
    return weechat.WEECHAT_RC_OK

# get all_players
def get_stats(raw_players):
    player = ""
    all_players = {}
    myrawplayers = re.sub(r'\{[^{}]*\}', lambda x: x.group(0).replace(' ','_'), raw_players)
    for player in myrawplayers.splitlines():
        playerstats = dict([(x, y) for x, y in zip(player.split()[::2], player.split()[1::2])])
        all_players[playerstats['rank']] = playerstats
    for player in all_players:
        this_player = all_players[player]
        if this_player['char'] == MYNICK:
            my_player = this_player
    return my_player, all_players

# check my alignment
def check_alignment(my_player):
    global MYALIGNMENT
    cur_align = my_player['align']
    if int(my_player['level']) < 30 and cur_align != "g":
        weechat.command(BOTBUFFER, "align priest")
    else:
        if MYALIGNMENT == "priest":
            des_align = "g"
        elif MYALIGNMENT == "undead":
            des_align = "e"
        else:
            MYALIGNMENT = "human"
            des_align = "h"
        if cur_align != des_align:
            weechat.command(BOTBUFFER, "align %s" % (MYALIGNMENT))

# get bank & gold
def check_finances(my_player):
    gold = int(my_player['gold'])
    if gold > 40:
        depositgold(gold - 40)
    cash = int(my_player['bank'])
    return cash

# shopping
def go_shopping(my_player, cash):
    buy_lvl = 15
    itm_cost = int(my_player['level']) * 6
    itm_lvl = int(my_player['level']) * 2
    itm_diff = 19
    my_gear = {}
    if int(my_player['level']) > buy_lvl:
        amulet = int(re.sub("[^0-9]", "", my_player['amulet']))
        my_gear[amulet] = "amulet"
        boots = int(re.sub("[^0-9]", "", my_player['boots']))
        my_gear[boots] = "boots"
        charm = int(re.sub("[^0-9]", "", my_player['charm']))
        my_gear[charm] = "charm"
        gloves = int(re.sub("[^0-9]", "", my_player['gloves']))
        my_gear[gloves] = "gloves"
        helm = int(re.sub("[^0-9]", "", my_player['helm']))
        my_gear[helm] = "helm"
        leggings = int(re.sub("[^0-9]", "", my_player['leggings']))
        my_gear[leggings] = "leggings"
        ring = int(re.sub("[^0-9]", "", my_player['ring']))
        my_gear[ring] = "ring"
        shield = int(re.sub("[^0-9]", "", my_player['shield']))
        my_gear[shield] = "shield"
        tunic = int(re.sub("[^0-9]", "", my_player['tunic']))
        my_gear[tunic] = "tunic"
        weapon = int(re.sub("[^0-9]", "", my_player['weapon']))
        my_gear[weapon] = "weapon"
        for item in my_gear:
            if item < ( itm_lvl - itm_diff):
                if cash > itm_cost:
                    weechat.prnt(SCRIPTBUFFER, "%sBuying new %s..." % (weechat.color("red, black"), my_gear[item]))
                    weechat.prnt(SCRIPTBUFFER, "")
                    weechat.command(BOTBUFFER, "bank withdraw %s" % itm_cost)
                    weechat.command(BOTBUFFER, "buy %s %s" % (my_gear[item], itm_lvl))
                    cash = cash - itm_cost
    return cash

# sidekicks
def hire_sidekicks(my_player, cash):
    eng_hire_lvl = 24
    if int(my_player['level']) > eng_hire_lvl:
        if int(my_player['englevel']) < 9:
            if int(my_player['engineer']) == 0 and cash > 2000:
                hireengineer()
                cash = cash - 2000
            if int(my_player['engineer']) == 1 and cash > 200:
                upengineer()
                cash = cash - 200
        elif int(my_player['hlevel']) < 9 and int(my_player['sum']) > 1200:
            if int(my_player['hero']) == 0 and cash > 1000:
                summonhero()
                cash = cash - 1000
            if int(my_player['hero']) == 1 and cash > 200:
                uphero()
                cash = cash - 200
    return cash

# take action (attack / challenge / slay)
def takeaction(my_player):
    time_now = int(time.time())
    if int(my_player['level']) > 9:
        if time_now > int(my_player['regentm']):
            my_creep = get_creep(int(my_player["level"]))
            weechat.prnt(SCRIPTBUFFER, "%sAttacking..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "align priest")
            weechat.command(BOTBUFFER, "attack %s" % (my_creep))
    if int(my_player['level']) > 34:
        if time_now > int(my_player['challengetm']):
            weechat.prnt(SCRIPTBUFFER, "%sChallenging..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "align priest")
            weechat.command(BOTBUFFER, "challenge")
    if int(my_player['level']) > 39:
        if time_now > int(my_player['slaytm']):
            my_monster = get_monster(int(my_player["sum"]))
            weechat.prnt(SCRIPTBUFFER, "%sSlaying..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "align priest")
            weechat.command(BOTBUFFER, "slay %s" % (my_monster))

def bestbet(all_players):
    all_bets = {}
    for player in all_players:
        challenger = all_players[player]
        if int(challenger['level']) > 29 and int(challenger['online']) == 1:
            opponent, odds = get_opponent(challenger, all_players)
            this_bet = { "challenger": challenger['char'], "opponent": opponent, "odds": odds}
            all_bets[player] = this_bet
    sorted_keys = sorted(all_bets.keys(), key=lambda y: (all_bets[y]['odds']), reverse=True)
    best_bet = all_bets[sorted_keys[0]]
    return best_bet['challenger'], best_bet['opponent'], best_bet['odds']

def betting(WINNER, LOSER, cash):
    if cash > 100:
        gamble(WINNER, LOSER)
        cash = cash - 100
    return cash

def get_real_sum(player):
    bonus = int(0.1 * int(player['sum']))
    if player['hero'] == 1:
        hbonus = ((int(player['hlevel']) + 2) / 100)
    else:
        hbonus = 0
    if player['align'] == "g":
        effective_sum = int(player['sum']) + bonus
    elif player['align'] == "e":
        effective_sum = int(player['sum']) - bonus
    else:
        effective_sum = int(player['sum'])
    effective_sum += hbonus
    return effective_sum

def get_opponent(my_player, all_players):
    candidates = {}
    keylist = []
    my_effective_sum = int(my_player['sum'])
    no_opponent = "no opponent"

    # Get all players my level or above who aren't me or on my team and key by rank.

    for player in all_players:
        this_player = all_players[player]
        t_p_effective_sum = get_real_sum(this_player)
        if int(this_player['online']) == 1:
            if int(this_player['level']) >= int(my_player['level']):
                if this_player['char'] != my_player['char'] and this_player['team'] != my_player['team']:
                    candidates[t_p_effective_sum] = this_player

    # Go through that getting a list of the keys.

    if candidates != {}:
        for efsum in candidates:
            keylist.append(efsum)
            keylist.sort()
        my_dude = candidates[keylist[0]]
        my_opponent = my_dude['char']
        odds = float(my_effective_sum) / keylist[0]
        return my_opponent, odds
    else:
        return no_opponent, 0

def fighting(my_player, my_opponent):
    if int(my_player['fights']) < 5:
        fight(my_opponent)

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):

    # display lines about me
    if MYNICK in msg:
        weechat.prnt(SCRIPTBUFFER, msg)
        weechat.prnt(SCRIPTBUFFER, "")

    # return
    return weechat.WEECHAT_RC_OK

# initialise variables
SCRIPT_NAME = 'multirpg'
SCRIPT_AUTHOR = 'drwhitehouse and contributors'
SCRIPT_VERSION = '8.2.1'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'fully automatic multirpg playing script'
CONFIG_FILE_NAME = "multirpg"
MULTIRPG_CONFIG_FILE = ""
MULTIRPG_CONFIG_OPTION = {}
raw_players = ""
my_content = ""
cash = 0

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

# initialise hooks
PHOOK = weechat.hook_print("", "notify_private,nick_multirpg", "", 0, "msgparser", "")

# setup bar
MRPGCOUNTERS = weechat.bar_item_new("MRPGCOUNTERS", "show_mrpgcounters", "")
version = int(weechat.info_get("version_number", "") or 0)
three = 50331648
if version < three:
    CTRBAR = weechat.bar_new("mrpgbar", "off", "100", "window", "${buffer.full_name} == python.weechat-multirpg", "top", "horizontal", "vertical","0", "5", "default", "white", "blue", "off", "MRPGCOUNTERS")
else:
    CTRBAR = weechat.bar_new("mrpgbar", "off", "100", "window", "${buffer.full_name} == python.weechat-multirpg", "top", "horizontal", "vertical","0", "5", "default", "white", "blue", "darkgray", "off", "MRPGCOUNTERS")

# Issue command to kick us off with this new bullshit...
get_rawplayers3("", "")

# Set power potions to manual loading:

weechat.prnt(SCRIPTBUFFER, "Setting Power Potion loading to manual...")
weechat.prnt(SCRIPTBUFFER, "")
weechat.command(BOTBUFFER, "load power 0")

# Get data every 5 minutes...
DELAY = 300
weechat.hook_timer(DELAY * 1000, 0, 0, "get_rawplayers3", "")
