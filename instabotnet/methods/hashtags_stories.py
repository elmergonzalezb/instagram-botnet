from typing import List
from funcy import  rcompose, mapcat
from ..nodes import  Media, Hashtag
from .common import decorate, cycled_api_call



@decorate(accepts=Hashtag, returns=Media)
def hashtag_stories(bot, nodes,  args) -> List[Media]:
    amount = args.get('amount')

    pack_story = lambda data: Story(id=data['pk'], data=data)

    process = rcompose(
        lambda tag: tag.name,
        # lambda x: tap(x, lambda: print(bot.last)),
        lambda id: cycled_api_call(amount, bot, bot.api.tag_feed, id, ['story', 'items']),
        lambda items: map(pack_story, items),
    )

    result = mapcat(process, nodes)

    return result, {}
