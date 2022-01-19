import pytest
from . import models


@pytest.fixture

def test_vote(test_user, session,test_posts):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()






def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/', json = {'vote_id' :'test_post[0].id', 'dir':1})

    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts,test_vote):
    res = authorized_client.post('/vote/', json={'post_id': 'test_post[3].id', 'dir':1})
    assert res.status_code == 409


def test_vote_twice_post(authorized_client, test_posts,test_vote):
    res = authorized_client.post(
        '/vote/', json={'post_id': 'test_post[3].id', 'dir':0})
    assert res.status_code == 201

def test_vote_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': 'test_post[3].id', 'dir':0})
    assert res.status_code == 404

def test_vote_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        '/vote/', json={'post_id': 9000, 'dir':1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        '/vote/', json={'post_id': 'test_posts[3].id', 'dir':1})
    assert res.status_code == 404



