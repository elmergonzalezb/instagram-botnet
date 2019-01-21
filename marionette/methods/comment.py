from typing import List
from funcy import  rcompose, raiser, ignore, mapcat, partial, tap as _tap
import time
from random import choice
from ..bot import Bot
from .common import accepts, today, tap, extract_urls
from ..nodes import Node, User, Media




@accepts(User)
def text(bot, nodes,  args):

    try:
        amount = float(args['amount']) if 'amount' in args else 1
        comments = args['comments']
    except:
        bot.logger.error('please add all necessary args, {} isn\'t enought'.format(args))
        return [], {}

    count = 0

    def increment():
        bot.total['comments'] += 1
        nonlocal count
        count += 1

    stop = raiser(StopIteration)

    def store_in_cache(node):
        with bot.cache as cache:
            cache['commented'].insert(
                dict(identifier=node.id,
                    specifier=str(comments),
                    time=today(),
                    type='media')
            )
        return node

    return_if_suitable = lambda node: node \
        if bot.suitable(node, table='commented', specifier=str(comments)) \
        else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node)))

    discard_if_reached_limit = lambda node: node \
        if not bot.reached_limit('texts') \
        else tap(None, bot.logger.error('reached texting daily limit'))

    do_comment_from_groups = lambda node: map(
            lambda cmnts: do_comment(bot, choice(cmnts), node),
            comments) \
         if node else [],



    process = rcompose(
        lambda x: stop() if x and count >= amount else x,
        return_if_suitable,
        discard_if_reached_limit,
        do_comment_from_groups,
        lambda arr: list(arr)[0] if arr else None,
        lambda node: store_in_cache(node) if node else None,
        lambda x: tap(x, increment) if x else None,
    )


    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, bot.last




def do_comment(bot: Bot, text, node, thread_id=None):

    media_id = node.id

    bot.api.comment(
        media_id=media_id,
        comment_text=text,
    )
    if bot.last['status'] == 'ok':
        bot.logger.debug('texted %s' % node)
        bot.sleep('comment')
        return node
    else:
        bot.logger.error("message to {} wasn't sent".format(node))
        bot.sleep('error')
        return None
