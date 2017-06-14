"""Define the routes."""


from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from turingtweets.models import mymodel
from turingtweets.models.mymodel import Tweet, FakeTweet
from pyramid.httpexceptions import HTTPNotFound
import random
from turingtweets.views.nlp import gen_tweet




@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home_view(request):
    """View for home route."""
    session = request.dbsession
    tweet_ct = session.query(Tweet).count()
    rand_tweet = random.randint(1, tweet_ct)
    real_tweet = session.query(Tweet).get(rand_tweet)
    fake_tweet = gen_tweet()
    if request.method == "POST" and request.POST:
        import pdb; pdb.set_trace()
        new_entry = FakeTweet(
            faketweet=request.POST['fakeTweet'],
            tweeted=False,
            shown=1,
            chosen=1
        )
        request.dbsession.add(new_entry)
        return {}
    return {
        'page': 'Home',
        'real': real_tweet.tweet,
        'fake': fake_tweet
    }
