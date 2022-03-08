import json
import os
import re
from dataclasses import dataclass
from json import JSONDecodeError, load
from typing import List

PATH_POSTS_JSON_TEST = os.path.join("..", 'data', "data.json")
PATH_POSTS_JSON = os.path.join('data', "data.json")
PATH_COMMENTS_JSON = os.path.join('data', "comments.json")
PATH_BOOKMARKS_JSON = os.path.join('data', "bookmarks.json")


@dataclass
class MyException(Exception):
    exc: str


@dataclass
class Posts:
    path_posts_json: str

    def open_posts_json(self):
        """
        открывает файл JSON
        :return:
        """
        try:
            with open(self.path_posts_json, encoding="utf-8") as file:
                posts: List[dict] = load(file)
                return posts
        except JSONDecodeError:
            raise MyException("Ошибка чтения файла posts.json!")
        except FileNotFoundError:
            raise MyException("Нет доступа к файлу posts.json!")

    def save_posts_json(self, posts):
        with open(self.path_posts_json, 'w', encoding='utf-8') as file:
            try:
                json.dump(posts, file, ensure_ascii=False)
            except JSONDecodeError:
                raise MyException("Ошибка при записи в post.json!")

    def replace_hashtags(self, posts_data: List[dict]):
        """
        заменяет хэштеги на ссылки
        :param posts_data:
        :return:
        """
        for post in posts_data:
            hashtags = re.findall(r'(#\w+)', post["content"])
            if hashtags:
                hashtags_links = [f"<a href = '/tag/{tag.replace('#', '')}'>{tag}</a>" for tag in hashtags]
                for i in range(len(hashtags_links)):
                    post["content"] = post["content"].replace(hashtags[i], hashtags_links[i], 1)
        return posts_data

    def get_posts_all(self):
        """
        возвращает посты
        :return:
        """
        return self.open_posts_json()

    def get_posts_by_user(self, user_name: str):
        """
        возвращает посты определенного пользователя
        :param user_name:
        :return:
        """
        posts: List[dict] = self.open_posts_json()
        find_posts: List[dict] = []
        for post in posts:
            if post["poster_name"] == user_name:
                find_posts.append(post)

        if find_posts:
            return find_posts
        else:
            raise MyException(f"Постов {user_name} не найдено! ")

    def search_for_post(self, query: str):
        """
        возвращает список словарей по вхождению query
        :param query:
        :return:
        """
        posts: List[dict] = self.open_posts_json()
        find_posts: List[dict] = []
        for post in posts:
            if query.lower() in post['content'].lower():
                find_posts.append(post)

        if find_posts:
            return find_posts
        else:
            raise MyException(f"по запросу {query} постов не найдено :(")

    def get_post_by_pk(self, pk):
        """
        возвращает один пост по его идентификатору
        :param pk:
        :return:
        """
        posts: List[dict] = self.replace_hashtags(self.open_posts_json())
        for post in posts:
            if post["pk"] == pk:
                return post
        else:
            raise MyException(f" Пост не найден! ")

    def get_posts_by_tag(self, tagname: str):
        """
        возвращает список словарей по вхождению tagname
        :param tagname:
        :return:
        """
        tag = "#" + tagname
        posts: List[dict] = self.open_posts_json()
        find_posts: List[dict] = []
        for post in posts:
            if tag in post['content']:
                find_posts.append(post)
        return find_posts

    def get_bookmarks_posts(self, bookmarks: list):
        """
        возвращает посты в закладках
        :param bookmarks:
        :return:
        """
        posts: List[dict] = self.open_posts_json()
        find_posts: List[dict] = []
        for post in posts:
            if post["pk"] in bookmarks:
                find_posts.append(post)
        return find_posts

    def add_view(self, post_id):
        posts: List[dict] = self.open_posts_json()
        for post in posts:
            if post["pk"] == post_id:
                post["views_count"] += 1

        self.save_posts_json(posts)


@dataclass
class Comments:
    path_comments_json: str

    def open_comments_json(self):
        """
        открывает файл JSON
        :return:
        """
        try:
            with open(self.path_comments_json, encoding="utf-8") as file:
                comments: List[dict] = load(file)
                return comments
        except JSONDecodeError:
            raise MyException("Ошибка чтения файла comments.json!")
        except FileNotFoundError:
            raise MyException("Нет доступа к файлу comments.json!")

    def get_comments_by_post_id(self, post_id: int):
        """
        возвращает комментарии определенного поста
        :param post_id:
        :return:
        """
        comments = self.open_comments_json()
        find_comments: List[dict] = []
        for comment in comments:
            if comment["post_id"] == post_id:
                find_comments.append(comment)
        return find_comments

    def save_comments_json(self, comments):
        with open(self.path_comments_json, 'w', encoding='utf-8') as file:
            try:
                json.dump(comments, file,ensure_ascii=False)
            except JSONDecodeError:
                raise MyException("Ошибка при записи в comments.json")


@dataclass
class Bookmarks:
    path_bookmarks_json: str

    def open_bookmarks_json(self):
        with open(self.path_bookmarks_json, encoding='utf-8') as file:
            try:
                bookmarks: List[dict] = load(file)
                return bookmarks
            except JSONDecodeError:
                raise MyException("Ошибка при открытии в Bookmarks.json")

    def save_bookmarks_json(self, bookmarks):
        with open(self.path_bookmarks_json, 'w', encoding='utf-8') as file:
            try:
                json.dump(bookmarks, file,ensure_ascii=False)
            except JSONDecodeError:
                raise MyException("Ошибка при записи в Bookmarks.json")

    def add_bookmarks(self, post_id):

        bookmarks: List[dict] = self.open_bookmarks_json()
        bookmarks.append({'pk': post_id})
        self.save_bookmarks_json(bookmarks)

    def get_bookmarks_activ(self):
        bookmarks = self.open_bookmarks_json()
        return [bookmark["pk"] for bookmark in bookmarks]

    def remove_bookmarks(self, post_id):
        bookmarks: List[dict] = self.open_bookmarks_json()
        for bookmark in bookmarks:
            if bookmark['pk'] == post_id:
                bookmarks.pop(bookmarks.index(bookmark))
        self.save_bookmarks_json(bookmarks)


posts = Posts(PATH_POSTS_JSON)
comments = Comments(PATH_COMMENTS_JSON)
bookmarks = Bookmarks(PATH_BOOKMARKS_JSON)
