from os import system, name
from fistacuffs_pkg.character_class import Character

"""
File is for some of the larger text block to help keep main code readable
Also contains display control functions
"""


def clear():
    """
    clear the console screen function copied from
    https://www.geeksforgeeks.org/clear-screen-python/
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def hp_string_format(player: object):
    """
    HP formatting display helper
    """
    start = " Hit Points:"
    width = 10
    padding = ' '

    return (f'{start}{player.hit_points:{padding}>{width}} |')


def name_string_format(player):
    """
    Name formatting display helper
    """
    s = '|'  # end of string
    padding = ' '  # pad with spaces
    length = 23 - len(player.name)

    return player.name + format(s, padding + '>' + str(length))


def player_stat_display(message1: str, message2: str, player: Character):
    """
    Display a formatted version of the player stats
    """

    ### formatting ###
    format_length = 25
    disp_name = name_string_format(player)
    disp_hp = hp_string_format(player)

    ### display ###
    print("#" * format_length)
    print("| " + disp_name)
    print(f"| Level: {player.level}              |")
    print(f"| 1) Strength:        {player.strength} |" if player.strength <
          player.level + 1 else f"| 1) Strength:        {player.strength}*|")
    print(f"| 2) Defense:         {player.defense} |" if player.defense <
          player.level + 1 else f"| 2) Defense:         {player.defense}*|")
    print(f"| 3) Speed:           {player.speed} |" if player.speed <
          player.level + 1 else f"| 3) Speed:           {player.speed}*|")
    print(f"| 4) Luck:            {player.luck} |" if player.luck <
          player.level + 1 else f"| 4) Luck:            {player.luck}*|")
    print("#" * format_length)
    print("|" + disp_hp)
    print("#" * format_length)
    print(message1)
    print(message2)
    print("#" * format_length)


def fight_display(message1: str, message2: str, player: Character, monster: Character):
    """
    Display formatting for the fight rounds
    """

    # Name display line set up
    length_format = 25
    disp_player_name = name_string_format(player)
    disp_monster_name = name_string_format(monster)
    hp_player = hp_string_format(player)
    hp_monster = hp_string_format(monster)

    # below is the code I am keeping change the vars to the player and monster class attributes

    # show stats
    print("#" * ((length_format * 2) - 1))
    print(f"# {message1}")
    print(f"# {message2}")
    print("#" * ((length_format * 2) - 1))
    print("| " + disp_player_name + " " + disp_monster_name)
    print(
        f"| Level: {player.level}              | Level: {monster.level}              |")
    print(
        f"| Strength:           {player.strength} | Strength:           {monster.strength} |")
    print(
        f"| Defense:            {player.defense} | Defense:            {monster.defense} |")
    print(
        f"| Speed:              {player.speed} | Speed:              {monster.speed} |")
    print(
        f"| Luck:               {player.luck} | Luck:               {monster.luck} |")
    print("#" * ((length_format * 2) - 1))
    print("|" + hp_player + hp_monster)
    print("#" * ((length_format * 2) - 1))
    print("| 1) Attack  2) Precise Strike")
    print("| 3) Brutal Strike  4) Wild Swing")
    print("#" * ((length_format * 2) - 1))


def win_battle():
    """
    message to player when they win a battle
    """

    print("You are victorious.")
    print("You have ganined a level\n")


def lose_battle():
    """
    message to player when they lose a battle
    """

    print("You have lost that battle.\n")
    print("Your lack of glory will be the source of family shame for ages to come.")
    print("Really... this could not have gone worse.")
    print()
    print("I'm not sure I see the point, but I suppose could reserecut you.\n")


def name_too_long(new_name: str) -> str:
    """
    control name length for display formatting
    """
    print(f"Your name is seriously {new_name}? \n")

    if len(new_name) >= 20:

        if new_name.find(" ") != -1:
            new_name = new_name[0: new_name.find(" ")]

        else:
            x = slice(20)
            new_name = new_name[x]

    print(
        f"Well.. that IS a mouthfull... How about I just call you {new_name}?\n")
    x = input("Press enter to continue...")
    return new_name


def develop_character(player: Character):
    """
    Flow control and screen output for assigning stat
     points to attributes to level up character
    """

    # setup display messages
    message1 = ""
    message2 = ""
    clear()

    while player.stat_points > 0:  # attribute assignment loop

        player_stat_display(message1, message2, player)
        message1 = ""
        message2 = ""

        print(f"{player.name}, you can train {player.stat_points} skills today.")
        assign_to = input(
            "Select the number of the skill you want to imporve. ").lower()

        if assign_to == "1" and player.strength < player.level + 1:
            player.modify_strength()
            message1 = "Aren't you looking buff!? Strength +1"
            clear()

        elif assign_to == "2" and player.defense < player.level + 1:
            player.modify_defense()
            message1 = "The best offense is a good defense. Defense +1"
            clear()

        elif assign_to == "3" and player.speed < player.level + 1:
            player.modify_speed()
            message1 = "You somehow just seem faster. Speed +1"
            clear()

        elif assign_to == "4" and player.luck < player.level + 1:
            player.modify_luck()
            message1 = "Umm... I am not sure how you trained this skill... but okay. Luck +1"
            clear()

        else:
            clear()
            message1 = "Input not recognized or that stat is maxed (*)"
            message2 = "Stat can only be the character Level +1"

    clear()
    message2 = "Your training is done for now."
    player_stat_display(message1, message2, player)
    x = input("Press enter to begin battle...")


def game_story(level: str) -> str:
    """
    feed parts of the story based on input
    """

    if level == "intro":
        story = """You have been traveling all day and come up on a small town that looks a bit rough...
But there is an Inn and you are tired.  So you enter and approach the bar to get a meal and some rest.
The bar keep look you up and down and says."""

    elif level == "1":
        story = (f"""Hmm... ok well you have stumbled on the town Fistacuffs.  You can stay but I am going to
warn you that fighting is a way of life here.  So before I can even pour you a drink you must
prepair yourself.  You must fight in order to stay.  In fact you must fight in order to leave.\n""")

    elif level == "2":
        story = """Okay... that was not too bad but my grandmother can beat one of those in her sleep.
Get some rest we will train more in the morning.\n"""

    elif level == "3":
        story = """Really...? I was sure you were going to lose! In fact I placed a prety hefty wager
against you.  Here is some food... you fight again tomorrow.\n"""

    elif level == "4":
        story = "Lorem Ipsum - level 4 story text - Lorem Ipsum"

    elif level == "5":
        story = "Lorem Ipsum - level 5 story text - Lorem Ipsum"

    else:
        story = "fail"

    return story
