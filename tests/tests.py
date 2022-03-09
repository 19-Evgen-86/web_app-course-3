from unittest.mock import patch, Mock

import pytest

import utils
from app import app
from utils import Posts, MyException, PATH_POSTS_JSON_TEST


class TestPosts:

    def test_open_json(self, from_open_json):
        posts = Posts(PATH_POSTS_JSON_TEST)
        assert posts.open_posts_json()[0] == from_open_json

    def test_open_json_error(self):
        with pytest.raises(MyException):
            posts = Posts("data.json")
            json = posts.open_posts_json()

    @patch("utils.Posts")
    def test_get_post_by_user(self, moskPosts, from_search_data):
        posts = moskPosts()
        posts.get_posts_by_user.return_value = from_search_data

        assert posts.get_posts_by_user("leo") == from_search_data

    def test_get_post_by_user_error(self, from_open_json):
        with pytest.raises(MyException):
            posts = Posts(PATH_POSTS_JSON_TEST)
            assert posts.get_posts_by_user("mark") == from_open_json

    def test_search_for_post(self, from_search_data):
        posts = Posts(PATH_POSTS_JSON_TEST)
        assert posts.search_for_post("еда") == from_search_data

    def test_search_for_post_error(self, from_search_data):
        with pytest.raises(MyException):
            posts = Posts(PATH_POSTS_JSON_TEST)
            assert posts.search_for_post("python") == from_search_data

    def test_get_post_by_pk(self, from_open_json):
        posts = Posts(PATH_POSTS_JSON_TEST)
        assert posts.get_post_by_pk(1) == from_open_json

    def test_get_post_by_pk_error(self):
        with pytest.raises(MyException):
            posts = Posts(PATH_POSTS_JSON_TEST)
            assert posts.get_post_by_pk(-1)


class TestApi:

    def setup(self):
        # создаем тестовый клиент для тестирования
        app.testing = True
        self.client = app.test_client()

    def test_api_posts(self):
        response = self.client.get("/api/posts/")
        assert response.status_code == 200
        resp_json = response.json
        assert isinstance(resp_json, list)
        for elem in resp_json:
            assert elem['poster_name']
            assert elem['poster_avatar']
            assert elem['pic']
            assert elem['content']
            assert elem['views_count']
            assert elem['likes_count']
            assert elem['pk']

    def test_api_posts_by_pk(self):
        response = self.client.get("/api/posts/1")
        assert response.status_code == 200
        resp_json = response.json
        assert isinstance(resp_json, dict)
        assert resp_json['poster_name']
        assert resp_json['poster_avatar']
        assert resp_json['pic']
        assert resp_json['content']
        assert resp_json['views_count']
        assert resp_json['likes_count']
        assert resp_json['pk']

    # выполняется после теста
    def teardown(self):
        app.testing = False
