




class Enemy:
    type_of_enemy: str
    health_points: int = 10
    attack_damage: int = 1

    def __init__(self):
        pass

    def talk(self):
        print(f'I am a {self.type_of_enemy}. be prepare to fight.')

    def walk(self):
        print(f'{self.type_of_enemy} moves closer to you!')

    def attack(self):
        print(f'{self.type_of_enemy} attacks for {self.attack_damage} damage')
