import os
import sys
import transaction
import json
# from turingtweets.scripts.tweet_scheduler import job

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models.mymodel import Tweet
from ..models.mymodel import FakeTweet
from turingtweets.scripts.builddict import fourgrams
from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL')

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    tweet_list = []
    models = []
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        HERE = os.path.dirname(__file__)

        with open(os.path.join(HERE, '../models/nhuntwalker_short.json'), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        for tweet_item in json_data:
            new_tweet = Tweet(
                tweet=tweet_item['text']
            )
            models.append(new_tweet)
            tweet_list.append(tweet_item['text'])

        a_fake_tweet = FakeTweet(
            faketweet="from now on my lectures will be semi-intelligible complete nonsense",
            tweeted=False,
            shown=0,
            chosen=0
        )
        fourgrams(tweet_list)
        dbsession.add(a_fake_tweet)
        dbsession.add_all(models)