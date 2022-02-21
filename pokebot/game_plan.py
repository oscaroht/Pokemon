
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

if __name__ == '__main__':
    print(Gameplan.player_name)


