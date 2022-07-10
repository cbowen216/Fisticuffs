from fistacuffs_pkg.character_class import Character
from fistacuffs_pkg.display import clear, win_battle, lose_battle, name_too_long, fight_display, develop_character, game_story
#from fistacuffs_pkg.test_fight import fight
import time
import random

"""
Chris Bowen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
abstract:
The player will go through 5 levels of battle with increasingly difficult opponents.
The player will have attributes like Strength, Defense, Speed, and Luck, that the 
player can level up and will effect the outcome of each attacking round of 
the fight.  The type of attack chosen will also effect the damage outcome of each
attacking round.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

this file is the overall flow control of the game
Charater and monster objects controlled by the Character class
display.py does most of the heavy lifting for how things are displayed on the screen

"""

### Functions ###


def stat_mod(choice: int) -> int:
    """
    calculate stat modification based on attack selection
    """
    str_mod = 0
    luck_mod = 0
    def_mod = 0
    spd_mod = 0

    if choice == 1:
        attack_type = "Attacks"

    if choice == 2:
        attack_type = "strikes precisely at"
        str_mod = attack_dict["Precise"]["Strength"]
        luck_mod += attack_dict["Precise"]["Luck"]
        def_mod += attack_dict["Precise"]["Defense"]
        spd_mod += attack_dict["Precise"]["Speed"]

    if choice == 3:
        attack_type = "deals a brutal blow to"
        str_mod = attack_dict["Brutal"]["Strength"]
        luck_mod += attack_dict["Brutal"]["Luck"]
        def_mod += attack_dict["Brutal"]["Defense"]
        spd_mod += attack_dict["Brutal"]["Speed"]

    if choice == 4:
        attack_type = "swings wildly at"
        str_mod = attack_dict["Wild"]["Strength"]
        luck_mod += attack_dict["Wild"]["Luck"]
        def_mod += attack_dict["Wild"]["Defense"]
        spd_mod += attack_dict["Wild"]["Speed"]

    return str_mod, luck_mod, def_mod, spd_mod, attack_type

### End of Functions ###

### Game set up ###


### Attack library ###
attack_dict = {"Precise": {"Strength": 1, "Luck": -1, "Defense": -1, "Speed": 1},
               "Brutal": {"Strength": 2, "Luck": -1, "Defense": 0, "Speed": 3},
               "Wild": {"Strength": -1, "Luck": 3, "Defense": 0, "Speed": 4}}
clear()
clear()
print(game_story("intro"))
print()

player = Character(input("Hello, you are not from here.  What is your name? ").title())

### begin game play ###
if len(player.name) >= 23:  # limit the player name to 23 characters for formatting purposes
    player.name = name_too_long(player.name)
    print()

play_again = True  # set to true to start the inital play again loop
while play_again:  # if player loses ask if they would like to play again

    while player.level < 6 and play_again:

        ### character and story development ###
        print()
        print(game_story(str(player.level)))
        print()
        x = input("Press enter to continue...")
        print("\nIt is time to prepair for the next battle.\n")
        x = input("Press enter to continue...")

        if player.stat_points > 0:
            develop_character(player)

        ### fight setup ###
        player_turn = True

        ### load new monster ###
        monster = Character("")
        monster.new_monster(player.level)

        if monster.speed > player.speed:
            ### fighter with greater speed goes first ###
            player_turn ^= True

        ### message and temp character holders set up for in fight display ###
        message1 = ""
        message2 = ""
        attacker = Character("")  
        defender = Character("")

        while player.hit_points > 0 and monster.hit_points > 0:  # breaks fight loop
            ### fight round setup ###
            damage = 0

            if player_turn:  # define attacker and defender each round
                attacker.name = player.name
                attacker.strength = player.strength
                attacker.defense = player.defense
                attacker.luck = player.luck
                attacker.speed = player.speed

                defender.name = monster.name
                defender.strength = monster.strength
                defender.defense = monster.defense
                defender.luck = monster.luck
                defender.speed = monster.speed

            else:
                defender.name = player.name
                defender.strength = player.strength
                defender.defense = player.defense
                defender.luck = player.luck
                defender.speed = player.speed

                attacker.name = monster.name
                attacker.strength = monster.strength
                attacker.defense = monster.defense
                attacker.luck = monster.luck
                attacker.speed = monster.speed

            clear()
            fight_display(message1, message2, player, monster)

            #set to base line for each round
            message1 = ""
            message2 = ""
            attack_type = ""

            # manipulate input string
            message_in = f"{player.name} choose your attack.  " if player_turn else f"{monster.name} attacks.  Press enter to continue..."


            if not player_turn:
                #monster makes a rnadon attack choice
                choice = random.randint(1, 4)
                str_mod, luck_mod, def_mod, spd_mod, attack_type = stat_mod(
                    choice)
                input(message_in)

            else:
                while True:
                    try:
                        choice = int(input(message_in))

                        if choice == 1 or choice == 2 or choice == 3 or choice == 4:
                            str_mod, luck_mod, def_mod, spd_mod, attack_type = stat_mod(choice)
                            break

                        else:
                            print("Input the number of your choice.")

                    except KeyboardInterrupt:
                        exit()

                    except:
                        print("Input not valid")

            # mod stats based on attack choice
            # if stat + ( a negative mod) < 0 then cap it at 0 
            attacker.strength += str_mod if attacker.strength + str_mod >= 0 else 0
            attacker.luck += luck_mod if attacker.luck + luck_mod >= 0 else 0
            defender.defense += def_mod if defender.defense + def_mod >= 0 else 0
            defender.speed += spd_mod if defender.speed + spd_mod >= 0 else 0

            crit_hit = attacker.crit_hit()

            if not crit_hit:
                dodge_sucess = defender.dodge()

                if dodge_sucess:
                    message1 = f"{defender.name} has doged the attack and takes no damage."
                    player_turn ^= True # switch players
                    continue

            # get round attack and defend numbers
            attack = attacker.attack(crit_hit)
            defense = defender.defend()

            #keep defense capped at less than the attack calc. if defense is > defender still takes HP 1 damage
            # keeps the game moving even if stats are stacked unevenly 
            defense = defense if attack > defense else attack - 1

            #damage done calculation
            damage = attack - defense

            #crit string manipulation
            crit = "for a critical hit!" if crit_hit else "!"

            #build messages for the next fight display call
            message1 = f"{attacker.name} {attack_type} {defender.name} {crit}"
            message2 = f"{defender.name} takes {damage} damage."

            #apply damage done to hitpoints lost
            if player_turn:
                monster.hit_points -= damage

            else:
                player.hit_points -= damage

            player_turn ^= True # switch players

        if player.hit_points > 0:  #player wins
            monster.hit_points = 0
            clear()
            fight_display(message1, message2, player, monster)
            player.level += 1
            player.stat_points += 2
            player.refresh_hp()
            player_turn = True
            win_battle()
            continue

        else: # player loses
            player.hit_points = 0
            clear()
            fight_display(message1, message2, player, monster)
            play_again = False
            lose_battle()
            continue

    while True: #play again loop
        choice = input("Would you like to try again? (Enter Y or N)  ").lower()

        if choice == "y":
            clear()
            play_again = True

            # start over at level 1
    
            player = Character(player.name)  # overwrite original player with new player

            print("Very well. You will be starting at level 1 and must work your way up again.")
            print("Good Luck!")
            x = input("Press enter to continue")
            break

        elif choice == "n":
            clear()
            print("Then I shall let you rest for eternity." if player.hit_points <=
                  0 else "Thank you for playing.")
            print("Good Bye")
            break

        else:
            print("Enter Y or N... It's not that difficult.\n")
            time.sleep(0.55)
            print("Seriously.... \n")
