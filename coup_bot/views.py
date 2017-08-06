from django.http import HttpResponse, Http404
from coup_bot.bot_player import RandomBot
import json


bot_player = RandomBot()


def __decode_data(request):
    if request.method == 'POST':
        return json.loads(request.body)
    else:
        raise Http404


def __encode_data(response):
    return json.dumps(response)

'''
    cards: list
    coins: integer,
    players: list
'''


def start(request):
    data = __decode_data(request)
    cards = data['cards']
    coins = data['coins']
    you = data['you']
    players = data['players']
    bot_player.start(you, cards, coins, players)
    return HttpResponse()

'''
    must_coup: bool
'''


def play(request):
    must_coup = request.META['HTTP_MUST_COUP'] == 'true'
    response = bot_player.play(must_coup)
    print(response)
    return HttpResponse(__encode_data(response))

'''
    action: int
    player: string
'''


def tries_to_block(request):
    action = request.META['HTTP_ACTION']
    player = request.META['HTTP_PLAYER']
    response = bot_player.tries_to_block(action, player)
    print(response)
    return HttpResponse(__encode_data(response))

'''
    action: int
    player: string
    card: string
'''


def challenge(request):
    action = request.META['HTTP_ACTION']
    player = request.META['HTTP_PLAYER']
    card = request.META['HTTP_CARD']
    response = bot_player.challenge(action, player, card)
    print(response)
    return HttpResponse(__encode_data(response))

'''
'''


def lose_influence(request):
    response = bot_player.lose_influence()
    print(response)
    return HttpResponse(__encode_data(response))

'''
    player: string
    card: string
'''


def inquisitor(request, action):
    if action == 'give_card_to_inquisitor':
        player = request.META['HTTP_PLAYER']
        response = bot_player.give_card_to_inquisitor(player)
    elif action == 'show_card_to_inquisitor':
        player = request.META['HTTP_PLAYER']
        card = request.META['HTTP_CARD']
        response = bot_player.show_card_to_inquisitor(player, card)
    elif action == 'choose_card_to_return':
        card = request.META['HTTP_CARD']
        response = bot_player.choose_card_to_return(card)
    elif action == 'card_returned_from_investigation':
        data = __decode_data(request)
        player = data['player']
        same_card = data['same_card']
        card = data['card']
        response = bot_player.card_returned_from_investigation(player, same_card, card)
    else:
        raise Http404
    print(response)
    return HttpResponse(__encode_data(response))

'''
    players: list
    player_acting: string,
    action": int
    player_blocking: string,
    challenger: int,
    challenged: int,
    card: string
'''


def status(request, action):
    data = __decode_data(request)
    if action == 'status':
        players = data['players']
        bot_player.signal_status(players)
    elif action == 'new_turn':
        player = data['opponent']
        bot_player.signal_new_turn(player)
    elif action == 'blocking':
        player_acting = data['player_acting']
        action = data['action']
        player = data['opponent']
        card = data['card']
        bot_player.signal_blocking(player_acting, action, player, card)
    elif action == 'lost_influence':
        player = data['player']
        card = data['card']
        bot_player.signal_lost_influence(player, card)
    elif action == 'challenge':
        challenger = data['challenger']
        challenged = data['challenged']
        card = data['card']
        bot_player.signal_challenge(challenger, challenged, card)
    elif action == 'action':
        player = data['opponent']
        action = data['action']
        player_targetted = data['player_targetted']
        bot_player.signal_action(player, action, player_targetted)
    else:
        raise Http404
    return HttpResponse()
