from typing import List
from funcy import  rcompose, raiser, ignore
import time
from .common import accepts, today, tap
from ..nodes import Node, User, Media




@accepts(Media)
def like(bot, nodes,  args):


    amount = float(args['amount']) if 'amount' in args else 1

    count = 0

    def increment():
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    process = rcompose(
        lambda node: node \
            if bot.suitable(node) \
            else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node))),
        lambda node: like_media(node, bot=bot) \
            if node else None,
        lambda x: tap(x, increment) if x else None,
        lambda x: stop() if x and count >= amount + 1 else x,
    )


    liked = map(process, nodes)
    liked = filter(lambda x: x, liked)

    return liked, bot.last


def like_media(media, bot):
        bot.api.like(media.id)
        if bot.last['status'] != 'ok':
            bot.logger.warn('request didn\'t return "ok" liking {}'.format(media.url))
            bot.sleep('error')
            return None
        else:
            with bot.cache as cache:
                cache['liked'].insert(
                    dict(identifier=media.id,
                        url=media.url,
                        time=today(),
                        type='media',
                        interaction='like')
                )
            bot.logger.debug('liked %s' % media.url)
            bot.sleep('like')
            return media
