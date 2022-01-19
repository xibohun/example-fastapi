from typing import List
from app import schemas
import pytest





def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    def validate(post):
        return schemas.PostOut(**post)
    posts_map= map(validate, res.json())
    posts_list = list(posts_map)
    
    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_all_post_not_exists(client, test_posts):
    res = client.get('/posts/88888')
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize('title, content, published',[

    ('awesome new tilte', 'awesome new content', True),
    ('favourite pizza', 'l love pepperoni', False),
    ('tallest skyscraper', 'whawho', True),


])

def test_create_posts(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/',json={'title': title, 'content':content, 'published':published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_user_published_true(authorized_client, test_user, test_posts):

    res = authorized_client.post('/posts/',json={'title': 'title', 'content':'content'})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == 'title'
    assert created_post.content == 'content'
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_client_create_post(client, test_user, test_posts):
    res = client.post('/posts/',json={'title': 'title', 'content':'content'})
    #created_post = schemas.Post(**res.json())
    assert res.status_code == 401

def test_unauthorized_client_delete_user(client,test_user, test_posts):
    res = client.delete(f'/posts/test_posts[0].id')
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/test_posts[0].id')
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete(f'/posts/800000000')
    assert res.status_code == 404
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403


def test_updated_posts(authorized_client, test_user, test_posts):
    data = {
        'tilte' : 'updated title',
        'content' : 'updated content',
        'published' :True
    }
    res = authorized_client.update(f'/posts/{test_user[0].id}', json=data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title  == data['title']
    assert updated_post.content  == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title" : 'updated title',
        'cotent' : 'updated content',
        'owner_id' : 'test_posts[3].id'
    }

    res = authorized_client.update(f'/posts/{test_posts[3].id}', json=data)

    assert res.status_code == 403



def test_unauthorized_client_update_post(client,test_user, test_posts):
    res = client.update(f'/posts/test_posts[0].id')
    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_posts): 
    data = {
        "title" : 'updated title',
        'cotent' : 'updated content',
        'owner_id' : 'test_posts[3].id'
    }

    res = authorized_client.update(f'/posts/800000000', json=data)
    assert res.status_code == 404





