import random
import math

class Character:
    def __init__(self, name):
        """
        character constructer
        """
        self.name = name
        self.level = 1
        self.strength = 1
        self.luck = 1
        self.defense = 1
        self.speed = 1
        self.hit_points = 0
        self.stat_points = 2
        self.refresh_hp()

    def refresh_hp(self):
        """
        reset HP
        """
        self.hit_points = 100 * self.level

    def modify_strength(self):
        """
        player leveling
        """
        self.strength += 1
        self.stat_points -= 1

    def modify_defense(self):
        """
        player leveling
        """
        self.defense += 1
        self.stat_points -= 1

    def modify_luck(self):
        """
        player leveling
        """
        self.luck += 1
        self.stat_points -= 1

    def modify_speed(self):
        """
        player leveling
        """
        self.speed += 1
        self.stat_points -= 1

    def new_monster(self, level):
        """
        new random monster from monster library 
        """

        ### load monster library ###
        import json
        with open("fistacuffs_pkg/monster_definition.json") as f:
            monster_library = json.load(f)

        ### make list of monster from dictionary keys
        monster_list = []
        
        lvl = "lvl" + str(level)

        for mon in monster_library:
            monster_list.append(mon)

        mon_name = random.choice(monster_list)  # choose rand monster from list

        ### set monster stats ###
        self.name = mon_name
        self.level = level
        self.strength = monster_library[mon_name][lvl]["Str"]
        self.luck = monster_library[mon_name][lvl]["Luck"]
        self.defense = monster_library[mon_name][lvl]["Def"]
        self.speed = monster_library[mon_name][lvl]["Speed"]
        #self.hit_points = self.refresh_hp()
        self.refresh_hp()

    def crit_hit(self) -> bool:
        """
        calculate if attacker gets a critical hit
        """
        rand_roll = random.randint(0, 100)

        return True if rand_roll >= (100 - self.luck) else False

    def dodge(self) -> bool:
        """
        calulate if defender dodges
        """
        rand_roll = random.randint(0, 100)

        return True if rand_roll >= (100 - self.speed) else False

    def attack(self, crit: bool) -> int:
        """
        calcualte damage done by attacker
        """
        if crit:
            rand_roll = 110
        
        else:
            rand_roll = random.randint(70, 100)

        return math.floor((10*(self.strength + self.level) + self.strength)*(rand_roll/100))

    def defend(self) -> int:
        """
        Calculate damage mitigated by defender
        """
        rand_roll = random.randint(20, 40)

        return math.floor(10*(self.defense + self.level)*(rand_roll/100))
