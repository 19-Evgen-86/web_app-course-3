import json
import logging
import os
import re
from dataclasses import dataclass
from json import JSONDecodeError, load
from typing import List

logging.basicConfig(filename="log_list.log", level=logging.INFO, encoding='utf-8')

PATH_POSTS_JSON_TEST = os.path.join("..", 'data', "data.json")
PATH_POSTS_JSON = os.path.join('data', "data.json")
PATH_COMMENTS_JSON = os.path.join('data', "comments.json")
PATH_BOOKMARKS_JSON = os.path.join('data', "bookmarks.json")


@dataclass
class MyException(Exception):
    exc: str


class JsonFileManager:

    def __init__(self, file):
        self.file = file

    def open_json(self):
        """
        открывает файл JSON
        :return:
        """
        logging.info(f" начало работы {self.open_json.__name__}")
        if os.path.isfile(self.file):
            try:
                with open(self.file, encoding="utf-8") as file:
                    posts: List[dict] = load(file)
                    return posts
            except JSONDecodeError:
                logging.error("Нет доступа к файлу json!")
                raise MyException("")
        else:
            logging.error("Нет доступа к файлу json!")
            raise MyException("")

    def save_json(self, data):
        logging.info(f" начало работы {self.save_json.__name__}")
        with open(self.file, 'w', encoding='utf-8') as file:
            try:
                json.dump(data, file, ensure_ascii=False)
            except JSONDecodeError:
                logging.error("Ошибка при записи в json!")
                raise MyException("")


class Posts(JsonFileManager):

    def replace_hashtags(self, posts_data: List[dict]):
        """
        заменяет хэштеги на ссылки
        :param posts_data:
        :return:
        """
        logging.info(f" начало работы {self.replace_hashtags.__name__}")
        for post in posts_data:
            hashtags = re.findall(r'(#\w+)', post["content"])
            if hashtags:
                hashtags_links = [f"<a href = '/tag/{tag.replace('#', '')}'>{tag}</a>" for tag in hashtags]
                for i in range(len(hashtags_links)):
                    post["content"] = post["content"].replace(hashtags[i], hashtags_links[i], 1)
        logging.info(f" преобразование хэштегов на ссылки прошло успешно")
        return posts_data

    def get_posts_all(self):
        """
        возвращает посты
        :return:
        """
        logging.info(f" начало работы {self.get_posts_all.__name__}")
        return self.open_json()

    def get_posts_by_user(self, user_name: str):
        """
        возвращает посты определенного пользователя
        :param user_name:
        :return:
        """
        logging.info(f" начало работы {self.get_posts_by_user.__name__}")
        posts: List[dict] = self.open_json()
        find_posts: List[dict] = []
        for post in posts:
            if post["poster_name"] == user_name:
                find_posts.append(post)

        if find_posts:
            logging.info(f" успешно! ")
            return find_posts
        else:
            logging.info(f"Постов {user_name} не найдено! ")
            return find_posts

    def search_for_post(self, query: str):
        """
        возвращает список словарей по вхождению query
        :param query:
        :return:
        """
        logging.info(f" начало работы {self.search_for_post.__name__}")
        posts: List[dict] = self.open_json()
        find_posts: List[dict] = []
        for post in posts:
            if query.lower() in post['content'].lower():
                find_posts.append(post)

        if find_posts:
            logging.info(f" успешно! ")
            return find_posts
        else:
            logging.info(f"Постов по запросу \"{query}\" не найдено! ")
            return find_posts

    def get_post_by_pk(self, pk):
        """
        возвращает один пост по его идентификатору
        :param pk:
        :return:
        """
        logging.info(f" начало работы {self.get_post_by_pk.__name__}")
        posts: List[dict] = self.replace_hashtags(self.open_json())
        for post in posts:
            if post["pk"] == pk:
                logging.info(f" успешно! ")
                return post
        else:
            logging.info(" Пост не найден")
            return None

    def get_posts_by_tag(self, tagname: str):
        """
        возвращает список словарей по вхождению tagname
        :param tagname:
        :return:
        """
        logging.info(f" начало работы {self.get_posts_by_tag.__name__}")
        tag = "#" + tagname
        posts: List[dict] = self.open_json()
        find_posts: List[dict] = []
        for post in posts:
            if tag in post['content']:
                find_posts.append(post)
        logging.info(f" успешно! ")
        return find_posts

    def get_bookmarks_posts(self, bookmarks: list):
        """
        возвращает посты в закладках
        :param bookmarks:
        :return:
        """
        logging.info(f" начало работы {self.get_bookmarks_posts.__name__}")
        posts: List[dict] = self.open_json()
        find_posts: List[dict] = []
        for post in posts:
            if post["pk"] in bookmarks:
                find_posts.append(post)
        logging.info(f" успешно! ")
        return find_posts

    def add_view(self, post_id):
        logging.info(f" начало работы {self.add_view.__name__}")
        posts: List[dict] = self.open_json()
        for post in posts:
            if post["pk"] == post_id:
                post["views_count"] += 1

        self.save_json(posts)
        logging.info(f" успешно! ")

class Comments(JsonFileManager):

    def get_comments_by_post_id(self, post_id: int):
        """
        возвращает комментарии определенного поста
        :param post_id:
        :return:
        """
        logging.info(f" начало работы {self.get_comments_by_post_id.__name__}")
        comments = self.open_json()
        find_comments: List[dict] = []
        for comment in comments:
            if comment["post_id"] == post_id:
                find_comments.append(comment)
        logging.info(f" успешно! ")
        return find_comments


class Bookmarks(JsonFileManager):

    def add_bookmarks(self, post_id):
        """
        добавляет пост в закладки
        :param post_id:
        :return:
        """
        logging.info(f" начало работы {self.add_bookmarks.__name__}")
        bookmarks: List[dict] = self.open_json()
        bookmarks.append({'pk': post_id})
        self.save_json(bookmarks)
        logging.info(f" успешно! ")
    def get_bookmarks_activ(self):
        """
        возвращает ID постов в закладках
        :return:
        """
        logging.info(f" начало работы {self.get_bookmarks_activ.__name__}")
        bookmarks = self.open_json()
        logging.info(f" успешно! ")
        return [bookmark["pk"] for bookmark in bookmarks]

    def remove_bookmarks(self, post_id):
        """
        удаляет пост из закладок
        :param post_id:
        :return:
        """
        logging.info(f" начало работы {self.remove_bookmarks.__name__}")
        bookmarks: List[dict] = self.open_json()
        for bookmark in bookmarks:
            if bookmark['pk'] == post_id:
                bookmarks.pop(bookmarks.index(bookmark))
        self.save_json(bookmarks)
        logging.info(f" успешно! ")

posts = Posts(PATH_POSTS_JSON)
comments = Comments(PATH_COMMENTS_JSON)
bookmarks = Bookmarks(PATH_BOOKMARKS_JSON)
