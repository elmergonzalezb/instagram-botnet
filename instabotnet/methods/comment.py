from funcy import ignore, raiser, rcompose
from random import choice
from ..bot import Bot
from .common import decorate, substitute_vars, tap
from ..nodes import Comment, Media




@decorate(accepts=Media, returns=Comment)
def comment(bot, nodes,  args):

    try:
        max = float(args['max']) if 'max' in args else float('inf')
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



    return_if_suitable = lambda node: node \
        if bot.suitable(node, table='commented', specifier=str(comments)) \
        else tap(None,lambda: bot.logger.warn('{} not suitable'.format(node)))

    discard_if_reached_limit = lambda node: node \
        if not bot.reached_limit('comments') \
        else tap(None, bot.logger.error('reached commenting daily limit'))

    do_comment_from_groups = lambda node: map(
            lambda cmnts: do_comment(bot, choice(cmnts), node),
            comments) \
         if node else []



    process = rcompose(
        lambda x: stop() if x and count >= max else x,
        return_if_suitable,
        discard_if_reached_limit,
        do_comment_from_groups,
        lambda arr: list(arr)[0] if arr else None,
        lambda x: tap(x, increment) if x else None,
    )


    result = map(process, nodes)
    result = filter(lambda x: x, result)

    return result, {}




def do_comment(bot: Bot, text, node, thread_id=None):

    media_id = node.id
    evaluated_text = substitute_vars(text,
        author=ignore(AttributeError, '')(
            lambda: node.get_author(bot).username
        )(),
        caption=node.get_caption(bot),
        geotag=ignore(AttributeError, '')(
            lambda: node.get_geotag(bot).name or ''
        )(),
        usertags=ignore(AttributeError, '')(
            lambda: list(map(lambda x: x.get_username(bot), node.get_usertags(bot))) or []
        )()
    )

    bot.api.post_comment(
        media_id=media_id,
        comment_text=evaluated_text,
    )

    bot.logger.info('commented %s' % node)
    bot.toal['comments'] += 1
    bot.sleep('comment')
    return node
