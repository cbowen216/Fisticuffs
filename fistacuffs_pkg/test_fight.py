""" Testing if I can call fight recurrsivly """

from fistacuffs_pkg.character_class import Character
from fistacuffs_pkg.display import clear, fight_display, win_battle, lose_battle
import random

attack_dict = {"Precise": {"Strength": 1, "Luck": -1, "Defense": -1, "Speed": 1},
               "Brutal": {"Strength": 2, "Luck": -1, "Defense": 0, "Speed": 3},
               "Wild": {"Strength": -1, "Luck": 3, "Defense": 0, "Speed": 4}}

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


def fight(player: Character, monster: Character) -> bool:
### fight setup ###

    player_turn = True
    message1 = ""
    message2 = ""
    attacker = Character("")  
    defender = Character("")

    if monster.speed > player.speed:
        ### fighter with greater speed goes first ###
        player_turn ^= True

    if player.hit_points <= 0 or monster.hit_points <= 0: #recurrsion break

        if player.hit_points > 0:  #player wins
            monster.hit_points = 0
            clear()
            fight_display(message1, message2, player, monster)
            player.level += 1
            player.stat_points += 2
            player.refresh_hp()
            player_turn = True
            win_battle()
            return True

        else: # player loses
            player.hit_points = 0
            clear()
            fight_display(message1, message2, player, monster)
            play_again = False
            lose_battle()
            return False

    else:

        #while player.hit_points > 0 and monster.hit_points > 0:  # breaks fight loop
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


