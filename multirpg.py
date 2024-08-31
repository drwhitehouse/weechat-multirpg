""" weechat play bot for multirpg (multirpg.net) """

# import my shiz
import re
import sys
import time
import collections
import random
import weechat

def buffer_input_cb(data, buffer, input_data):
    """ callback for data received in input """
    # ...
    return weechat.WEECHAT_RC_OK

def buffer_close_cb(data, buffer):
    """ callback called when buffer is closed """
    weechat.bar_remove(CTRBAR)
    return weechat.WEECHAT_RC_OK

def unload_script_cb():
    """ callback called when script unloaded """
    # ...
    return weechat.WEECHAT_RC_OK

def multirpg_config_init():
    """ initialise configuration """
    MULTIRPG_CONFIG_FILE = weechat.config_new(CONFIG_FILE_NAME, "", "")
    if MULTIRPG_CONFIG_FILE == "":
        return

    section_multirpg = weechat.config_new_section(MULTIRPG_CONFIG_FILE,
                                                  "multirpg", 0, 0, "",
                                                  "", "", "", "", "", "", "", "", "")
    if section_multirpg == "":
        weechat.config_free(MULTIRPG_CONFIG_FILE)
        return

    MULTIRPG_CONFIG_OPTION["MYNICK"] = weechat.config_new_option(MULTIRPG_CONFIG_FILE,
                                                                 section_multirpg,
                                                                 "MYNICK", "string",
                                                                 "multirpg nickname",
                                                                 "", 0, 0, "", "", 0,
                                                                 "", "", "", "", "", "")

    MULTIRPG_CONFIG_OPTION["IRCSERVER"] = weechat.config_new_option(MULTIRPG_CONFIG_FILE,
                                                                    section_multirpg,
                                                                    "IRCSERVER", "string",
                                                                    "multirpg IRCSERVER",
                                                                    "", 0, 0, "", "", 0,
                                                                    "", "", "", "", "", "")
    weechat.config_read(MULTIRPG_CONFIG_FILE)
    return

def depositgold(deposit):
    """ deposit gold """
    weechat.prnt(SCRIPTBUFFER, "%sDepositing: %s%s gold..." % (weechat.color("yellow, black"), 
                                                               weechat.color("white, black"),
                                                               deposit))
    weechat.command(BOTBUFFER, "bank deposit %s" % (deposit))
    weechat.prnt(SCRIPTBUFFER, "")

def hireengineer():
    """ hire engineer """
    weechat.prnt(SCRIPTBUFFER, "%sHiring engineer..." % weechat.color("cyan, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 1000")
    weechat.command(BOTBUFFER, "hire engineer")

def summonhero():
    """ summon hero """
    weechat.prnt(SCRIPTBUFFER, "%sSummoning hero..." % weechat.color("cyan, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 1000")
    weechat.command(BOTBUFFER, "summon hero")

def upengineer():
    """ upgrade engineer """
    weechat.prnt(SCRIPTBUFFER, "%sUpgrading engineer..." % weechat.color("cyan, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 200")
    weechat.command(BOTBUFFER, "engineer level")

def uphero():
    """ upgrade hero """
    weechat.prnt(SCRIPTBUFFER, "%sUpgrading hero..." % weechat.color("cyan, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 200")
    weechat.command(BOTBUFFER, "hero level")

def get_creep(my_level):
    """ get creep for attack """
    these_creeps = creeps
    for key in these_creeps:
        if my_level <= key:
            my_creep = these_creeps.get(key)
            break
    return my_creep

def get_monster(my_sum):
    """ get monster for attack """
    these_monsters = monsters
    for key in these_monsters:
        if my_sum >= key:
            my_monster = these_monsters.get(key)
    return my_monster

def gamble(winner, loser):
    """ gamble """
    weechat.prnt(SCRIPTBUFFER, "%sBetting..." % weechat.color("cyan, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    weechat.command(BOTBUFFER, "bank withdraw 100")
    weechat.command(BOTBUFFER, "bet %s %s 100" % (winner, loser))

def fight(my_player, my_opponent):
    """ have a ruck """
    if int(my_player['level']) > 89 and int(my_player['powerpots']) > 1:
        weechat.prnt(SCRIPTBUFFER, "%sLoading potion..." % weechat.color("cyan, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "load power 1")
    weechat.prnt(SCRIPTBUFFER, "%sFighting..." % weechat.color("red, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    take_vows(my_player)
    weechat.command(BOTBUFFER, "fight %s" % (my_opponent))

def upgradeitems(my_player, cash):
    """ upgrade my stuff """
    my_pots = int(my_player['powerpots'])
    if int(my_player['hlevel']) < 9:
        return cash
    if int(my_player['bets']) < 5:
        return cash
    if int(my_player['gold']) > 40:
        return cash
    if int(my_player['level']) > 69 and my_pots < 5:
        budget = 400
    else:
        budget = 200
    if cash < budget:
        return cash
    if budget == 400 and int(my_player['level']) < 99:
        weechat.prnt(SCRIPTBUFFER, "%sBuying potion..." % weechat.color("cyan, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "bank withdraw 400")
        weechat.command(BOTBUFFER, "buy power")
        cash = cash - 400
    else:
        lvl = int(cash / 200)
        withdraw = lvl * 200
        weechat.prnt(SCRIPTBUFFER, "%sUpgrading items..." % weechat.color("cyan, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "bank withdraw %s" % (withdraw))
        weechat.command(BOTBUFFER, "upgrade all %s" % (lvl))
        cash = cash - withdraw
    return cash

def check_bet(all_players, my_player, cash):
    """ wrapper for betting() """
    if int(my_player['level']) > 29:
        challenger, opponent, odds = bestbet(all_players)
        weechat.prnt(SCRIPTBUFFER, "%sBest bet: %s%s vs %s, odds: %s" % (weechat.color("yellow, black"),
                                                                         weechat.color("white, black"),
                                                                         challenger,
                                                                         opponent,
                                                                         odds))
        weechat.prnt(SCRIPTBUFFER, "")
        if int(my_player['bets']) < 5:
            cash = betting(challenger, opponent, cash)
    return cash

def check_fight(all_players, my_player):
    """ wrapper for fighting() """
    if int(my_player['level']) > 9 and int(my_player['level']) < 200:
        my_opponent, odds = get_opponent(my_player, all_players, bet=False)
        weechat.prnt(SCRIPTBUFFER, "%sBest fight: %s%s, odds: %s" % (weechat.color("red, black"),
                                                                     weechat.color("white, black"),
                                                                     str(my_opponent),
                                                                     str(odds)))
        weechat.prnt(SCRIPTBUFFER, "")
        if int(my_player['rank']) > 1:
            if int(my_player['level']) < 30:
                if odds > ODDS:
                    fighting(my_player, my_opponent)
            else:
                if odds > ODDS and int(my_player['bets']) > 4:
                    fighting(my_player, my_opponent)

def refreshbar():
    """ refresh bar """
    weechat.bar_item_update("MRPGCOUNTERS")
    return weechat.WEECHAT_RC_OK

def show_mrpgcounters(data, item, window):
    """ show counters for mrpgbar """
    return "".join(MY_CONTENT)

def display_activity(data, timer):
    """ flash the hat """
    weechat.hook_process("url:http://10.15.0.11:5000/flash",60 * 1000, "display_cb", "")
    return weechat.WEECHAT_RC_OK

def display_cb(data, command, rtncd, out, err):
    """ display callback """
    if out != "":
        weechat.prnt(SCRIPTBUFFER, "%sDisplay..." % weechat.color("red, black"))
        weechat.prnt(SCRIPTBUFFER, "")
    return weechat.WEECHAT_RC_OK

def get_rawplayers3(data, timer):
    """ get rawplayers3 from url """
    weechat.hook_process("url:http://multirpg.net/rawplayers3.php",60 * 1000, "rawplayers3_cb", "")
    return weechat.WEECHAT_RC_OK

def rawplayers3_cb(data, command, rtncd, out, err):
    """ rawplayers3 callback """
    if out != "":
        RAW_PLAYERS.append(out)
        if int(rtncd) >= 0:
            my_player, all_players = get_stats("".join(RAW_PLAYERS))
            if int(my_player['online']) == 1:
                cash = check_finances(my_player)
                cash = go_shopping(my_player, cash)
                cash = hire_sidekicks(my_player, cash)
                cash = check_bet(all_players, my_player, cash)
                cash = upgradeitems(my_player, cash)
                takeaction(my_player)
                check_fight(all_players, my_player)
                check_alignment(my_player)
            else:
                weechat.prnt(SCRIPTBUFFER, "%s WARNING: offline" % weechat.color("red, black"))
                weechat.prnt(SCRIPTBUFFER, "")
            time_now = int(time.time())
            if int(my_player['level']) > 9:
                a_time = time.strftime("%H:%M", time.gmtime(int(my_player['regentm']) - time_now))
            else:
                a_time = 'level 10'
            if int(my_player['level']) > 34:
                c_time = time.strftime("%H:%M",
                                       time.gmtime(int(my_player['challengetm']) - time_now))
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
            del MY_CONTENT[:]
            MY_CONTENT.append("rank: %s, "
                          "level: %s, "
                          "sum: %s, "
                          "gold: %s, "
                          "bank: %s, "
                          "attack: %s, "
                          "challenge: %s, "
                          "slay: %s, "
                          "ttl: %s days, %s:%s" % (my_player['rank'],
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
                          )
            refreshbar()
            del RAW_PLAYERS[:]
    return weechat.WEECHAT_RC_OK

def get_stats(RAW_PLAYERS):
    """ get all_players """
    player = ""
    all_players = {}
    myrawplayers = re.sub(r'\{[^{}]*\}', lambda x: x.group(0).replace(' ','_'), RAW_PLAYERS)
    for player in myrawplayers.splitlines():
        playerstats = dict(zip(player.split()[::2], player.split()[1::2]))
        if int(playerstats['online']) == 1:
            all_players[playerstats['rank']] = playerstats
    for player in all_players:
        this_player = all_players[player]
        if this_player['char'] == MYNICK:
            my_player = this_player
    return my_player, all_players

def check_alignment(my_player):
    """ check my alignment """
    my_align = my_player['align']
    my_ttl = int(my_player['ttl'])
    if int(my_player['level']) < 30:
        take_vows(my_player)
    elif int(my_player['level']) > 99 and my_align != "e":
        weechat.prnt(SCRIPTBUFFER, "%sThe undead shall rise..." % weechat.color("cyan, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "align undead")
    else:
        if my_ttl < 600:
            take_vows(my_player)
        else:
            if my_align != "n":
                only_human(my_player)

def check_finances(my_player):
    """ get bank & gold """
    weechat.prnt(SCRIPTBUFFER, "%sFiddling with loose change..." % weechat.color("yellow, black"))
    weechat.prnt(SCRIPTBUFFER, "")
    gold = int(my_player['gold'])
    cash = int(my_player['bank'])
    if gold > 40:
        depositgold(gold - 40)
    if gold < 40 and cash > 40 - gold:
        withdrawl = 40 - gold
        weechat.prnt(SCRIPTBUFFER, "%sWithdrawing: %s%s gold..." % (weechat.color("yellow, black"),
                                                                    weechat.color("white, black"),
                                                                    withdrawl))
        weechat.command(BOTBUFFER, "bank withdraw %s" % (withdrawl))
        weechat.prnt(SCRIPTBUFFER, "")
        cash = cash - withdrawl
    if random.randint(0, 1):
        if random.randint(0, 1):
            weechat.command(BOTBUFFER, "bank withdraw 1")
            cash = cash - 1
        else:
            weechat.command(BOTBUFFER, "bank deposit 1")
            cash = cash + 1
    return cash

def go_shopping(my_player, cash):
    """ shopping """
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
                    weechat.prnt(SCRIPTBUFFER, "%sBuying new %s from the shop..." % (weechat.color("cyan, black"), my_gear[item]))
                    weechat.prnt(SCRIPTBUFFER, "")
                    weechat.command(BOTBUFFER, "bank withdraw %s" % itm_cost)
                    weechat.command(BOTBUFFER, "buy %s %s" % (my_gear[item], itm_lvl))
                    cash = cash - itm_cost
    return cash

def hire_sidekicks(my_player, cash):
    """ sidekicks """
    eng_hire_lvl = 24
    if int(my_player['level']) > eng_hire_lvl:
        if int(my_player['englevel']) < 9:
            if int(my_player['engineer']) == 0 and cash > 2000:
                hireengineer()
                cash = cash - 2000
            if int(my_player['engineer']) == 1 and cash > 200:
                upengineer()
                cash = cash - 200
        elif int(my_player['hlevel']) < 9:
            if int(my_player['hero']) == 0 and cash > 1000:
                summonhero()
                cash = cash - 1000
            if int(my_player['hero']) == 1 and cash > 200:
                uphero()
                cash = cash - 200
    return cash

def take_vows(my_player):
    """ become priest if necessary """
    my_align = my_player['align']
    my_level = my_player['level']
    if int(my_level) < 100 and my_align != "g":
        weechat.prnt(SCRIPTBUFFER, "%sTaking the vows of a priest..." % weechat.color("cyan, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "align priest")

def only_human(my_player):
    """ become human """
    my_align = my_player['align']
    my_level = my_player['level']
    if int(my_level) < 100 and my_align != "n":
        weechat.prnt(SCRIPTBUFFER, "%sTo err is human..." % weechat.color("cyan, black"))
        weechat.prnt(SCRIPTBUFFER, "")
        weechat.command(BOTBUFFER, "align human")

def takeaction(my_player):
    """ take action (attack / challenge / slay) """
    Att_Now = False
    Chg_Now = False
    Sly_Now = False
    Action = False
    time_now = int(time.time())
    if int(my_player['level']) > 9 and time_now > int(my_player['regentm']):
        Att_Now = True
        Action = True
    if int(my_player['level']) > 34 and time_now > int(my_player['challengetm']):
        Chg_Now = True
        Action = True
    if int(my_player['level']) > 39 and time_now > int(my_player['slaytm']):
        Sly_Now = True
        Action = True
    if Action:
        take_vows(my_player)
        if Att_Now:
            my_creep = get_creep(int(my_player["level"]))
            weechat.prnt(SCRIPTBUFFER, "%sAttacking..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "attack %s" % (my_creep))
        if Chg_Now:
            weechat.prnt(SCRIPTBUFFER, "%sChallenging..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "challenge")
        if Sly_Now:
            my_monster = get_monster(int(my_player["sum"]))
            weechat.prnt(SCRIPTBUFFER, "%sSlaying..." % weechat.color("red, black"))
            weechat.prnt(SCRIPTBUFFER, "")
            weechat.command(BOTBUFFER, "slay %s" % (my_monster))

def bestbet(all_players):
    """ get bet """
    all_bets = {}
    for player in all_players:
        challenger = all_players[player]
        if int(challenger['level']) > 29:
            opponent, odds = get_opponent(challenger, all_players, bet=True)
            this_bet = { "challenger": challenger['char'], "opponent": opponent, "odds": odds}
            all_bets[player] = this_bet
    sorted_keys = sorted(all_bets.keys(), key=lambda y: (all_bets[y]['odds']), reverse=True)
    best_bet = all_bets[sorted_keys[0]]
    return best_bet['challenger'], best_bet['opponent'], best_bet['odds']

def betting(winner, loser, cash):
    """ betting """
    if cash > 100:
        gamble(winner, loser)
        cash = cash - 100
    return cash

def get_real_sum(player):
    """ get real sum """
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

def get_opponent(my_player, all_players, bet=False):
    """ get opponent """
    candidates = {}
    keylist = []
    my_effective_sum = int(my_player['sum'])
    # Get all players my level or above who aren't me or on my team and key by rank.
    for player in all_players:
        this_player = all_players[player]
        if bet:
            t_p_effective_sum = int(this_player['sum'])
        else:
            t_p_effective_sum = get_real_sum(this_player)
        if int(this_player['level']) >= int(my_player['level']):
            if this_player['char'] != my_player['char'] and \
                    this_player['team'] != my_player['team']:
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
    return "no opponent", 0

def fighting(my_player, my_opponent):
    """ fighting """
    if int(my_player['fights']) < 5:
        fight(my_player, my_opponent)

def msgparser(data, bufferp, tm, tags, display, is_hilight, prefix, msg):
    """ parse messages """
    # display lines about me
    if msg.startswith(MYNICK):
        weechat.prnt(SCRIPTBUFFER, msg)
        weechat.prnt(SCRIPTBUFFER, "")
        if ZEROWDISPLAY:
            display_activity("","")
    # return
    return weechat.WEECHAT_RC_OK

# initialise variables
SCRIPT_NAME = 'multirpg'
SCRIPT_AUTHOR = 'drwhitehouse and contributors'
SCRIPT_VERSION = '8.5.7'
SCRIPT_LICENSE = 'GPL3'
SCRIPT_DESC = 'fully automatic multirpg playing script'
CONFIG_FILE_NAME = "multirpg"
MULTIRPG_CONFIG_OPTION = {}
RAW_PLAYERS = []
MY_CONTENT = []
ODDS = 0.9
ZEROWDISPLAY = False

# The creeps and monsters lists show the level at which the script picks different opponents.
# It's not clear what the optimal level to challenge at is, but looking at players who are
# definitely not cheating, but frequently successful, it may be worth skipping some of them.

creeps = {
        10: "bush",
        15: "locust",
        20: "spider",
        30: "goblin",
        40: "lich",
#       50: "skeleton",
#       60: "ghost",
        70: "shadow",
#       80: "troll",
#       90: "cylcops",
#       100: "mutant",
        110: "monkey",
        120: "phoenix",
        130: "minotaur",
        140: "beholder",
        150: "wyvern",
        160: "ogre",
}

monsters = {
        1000: "medusa",
        3000: "centaur",
        4000: "mammoth",
#           : "vampire",
#           : "dragon",
#           : "sphinx",
        4750: "hippogriff",
}

# register the script
weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", "")

# read configuration
multirpg_config_init()
MYNICK = weechat.config_string(MULTIRPG_CONFIG_OPTION['MYNICK'])
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
CTRBAR = weechat.bar_new("mrpgbar", "off", "100", "window",
                         "${buffer.full_name} == python.weechat-multirpg",
                         "top", "horizontal", "vertical","0", "5", "default",
                         "white", "blue", "darkgray", "off", "MRPGCOUNTERS")

# Issue command to kick us off with this new bullshit...
get_rawplayers3("", "")

# Set power potions to manual loading:

weechat.prnt(SCRIPTBUFFER, "%sSetting Power Potion loading to manual..." % weechat.color("cyan, black"))
weechat.prnt(SCRIPTBUFFER, "")
weechat.command(BOTBUFFER, "load power 0")

# Get data every 5 minutes...
DELAY = 300
weechat.hook_timer(DELAY * 1000, 0, 0, "get_rawplayers3", "")
