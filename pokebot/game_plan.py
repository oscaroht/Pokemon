
# from main import go_to, train, buy, talk

class Gameplan:

    continue_or_new_game = 'continue'

    # game setup
    # player_name = 'automation'
    # foe_name = 'manual'

    player_name = 'blue'
    rival_name = 'red'

    starter_pokemon = 'charmander' # choose charmander/squirtle/bulbasor of zoiets
    catch_pokemon = ['pidgey', 'pikachu', 'geodude','nidoran_f']

    sku = {'item_name': 'Poke Ball', 'amount': 10}

    @classmethod
    def set_new_game(cls):
        cls.continue_or_new_game = 'new_game'

    @classmethod
    def set_continue_game(cls):
        cls.continue_or_new_game = 'continue'

    @classmethod
    def set_player_name(cls, name):
        # do some validation
        cls.player_name = name
        return True

    @classmethod
    def set_rival_name(cls, name):
        # do some validation
        cls.rival_name = name
        return True

if __name__ == '__main__':
    print(Gameplan.player_name)


