import random

from src import api


def test_post_return_new():
    haha = str(random.random())
    assert (haha,) in api.post(hi=haha)['stuff']
