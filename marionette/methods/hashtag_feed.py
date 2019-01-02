
from typing import List
from funcy import  rcompose, flatten, partial, print_calls
from itertools import islice
from time import time
from ..nodes import  Media, Hashtag
from .common import accepts

@accepts(Hashtag)
def hashtag_feed(bot, nodes, amount, args) -> List[Media]:


    get_items = rcompose(
        lambda tag: tag.name,
        lambda name: get_feed(name, bot=bot, amount=amount),
    )

    pack_media = rcompose(
        lambda data: data['pk'],
        lambda id: Media(id=id)
    )

    result = (pack_media(item) for user in nodes for item in get_items(user))
    result = (node for node in result if bot.suitable(node))
    result = islice(result, amount)

    return result, bot.last




def get_feed(hashtag, bot , amount) -> List[Media]:

    next_max_id = ''
    done = 0
    sleep_track = 0

    while True:
        try:
            bot.api.get_hashtag_feed(hashtag, next_max_id)
            items = bot.last["items"] if 'items' in bot.last else []

            if len(items) <= amount:
                yield from items
                done += len(items)
                return

            elif (done + len(items)) >= amount:
                yield from items[:amount - done]
                done += len(items)
                return

            else:
                yield from items
                done += len(items)

        except Exception:
            return

        if sleep_track > 10:
            bot.logger.debug('sleeping some time while getting hashtag feed')
            time.sleep(bot.delay['getter'])
            sleep_track = 0

        next_max_id = bot.last.get("next_max_id", "")
        sleep_track += 1