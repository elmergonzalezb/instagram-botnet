from functools import partial
from .like import like
from .follow import follow
from .authors import authors
from .followers import followers
from .following import following
from .user_feed import user_feed
from .hashtag_feed import hashtag_feed
from .likers import likers



methods = dict(
               authors= authors,
               follow= follow,
               followers= followers,
               likers= likers,
               following= following,
               user_feed= user_feed,
               hashtag_feed= hashtag_feed,
               like= like,
               )


def make_methods(bot):
    return {key: partial(value, bot) for (key, value) in methods.items()}
