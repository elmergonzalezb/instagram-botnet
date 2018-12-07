
from typing import List
from ..nodes import User, Media


def user_feed(bot, nodes, amount, args) -> List[Media]:

    result = []

    for node in nodes:
        result += get_feed(bot, node, amount)


    return result, bot.last


def get_feed(bot, node, amount) -> List[Media]:
    return [User(id=item['pk']) for item in bot.api.get_user_feed(node.id)][:amount]
