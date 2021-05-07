import unittest
import requests


class TestFlaskApiNews(unittest.TestCase):

    def test_news_not_int(self):
        """
        тест запроса не ID
        :return:
        """
        response = requests.get('http://localhost:5000/api/v2/news/q')
        self.assertEqual(response.json(), {'error': 'Not found'})

    def test_news_not(self):
        """
        тест запроса не существующего ID
        :return:
        """
        response = requests.get('http://localhost:5000/api/v2/news/99999')
        self.assertEqual(response.json(), {'message': 'News 99999 not found'})

    def test_news_create(self):
        """
        Тест добавления новости
        :return:
        """
        response = requests.post('http://localhost:5000/api/v2/news',
                                 json={'title': 'title',
                                       'content': 'content',
                                       'is_published': 1,
                                       'user_id': 1,
                                       'category_id': 1,
                                       'id': 9999,
                                       })
        self.assertEqual(response.json(), {'success': 'OK'})
        response = requests.delete('http://localhost:5000/api/v2/news/9999')
        self.assertEqual(response.json(), {'success': 'OK'})

    def test_news_get_valid(self):
        """
        Тест проверки добавленной новости
        :return:
        """
        response = requests.post('http://localhost:5000/api/v2/news',
                                 json={'title': 'title',
                                       'content': 'content',
                                       'is_published': 1,
                                       'user_id': 1,
                                       'category_id': 1,
                                       'id': 10002,
                                       })
        self.assertEqual(response.json(), {'success': 'OK'})
        response = requests.get('http://localhost:5000/api/v2/news/10002')
        self.assertEqual(response.json()['news']['content'], 'content')
        response = requests.delete('http://localhost:5000/api/v2/news/10002')
        self.assertEqual(response.json(), {'success': 'OK'})

    def test_news_all_get(self):
        """
        Тест запроса множества новостей
        :return:
        """
        response = requests.get('http://localhost:5000/api/v2/news')
        self.assertTrue(len(response.json()['news']) > 0)

    def test_news_delete(self):
        """
        Тест удаления добавленной новости
        :return:
        """
        response = requests.post('http://localhost:5000/api/v2/news',
                                 json={'title': 'title',
                                       'content': 'content',
                                       'is_published': 1,
                                       'user_id': 1,
                                       'category_id': 1,
                                       'id': 10000,
                                       })
        self.assertEqual(response.json(), {'success': 'OK'})
        response = requests.delete('http://localhost:5000/api/v2/news/10000')
        self.assertEqual(response.json(), {'success': 'OK'})

    def test_news_delete_no_id(self):
        """
        Тест удаления несуществующей новости
        :return:
        """
        response = requests.delete('http://localhost:5000/api/v2/news/10001')
        self.assertEqual(response.json(), {'message': 'News 10001 not found'})


class TestFlaskApiUsers(unittest.TestCase):

    def test_users_not_int(self):
        """
        тест запроса не ID пользователя
        :return:
        """
        response = requests.get('http://localhost:5000/api/v2/users/q')
        self.assertEqual(response.json(), {'error': 'Not found'})

    def test_users_not(self):
        """
        тест запроса не существующего ID пользователя
        :return:
        """
        response = requests.get('http://localhost:5000/api/v2/users/99999')
        self.assertEqual(response.json(), {'message': 'User 99999 not found'})

    def test_users_create(self):
        """
        Тест добавления пользователя
        :return:
        """
        response = requests.post('http://localhost:5000/api/v2/users',
                                 json={'name': 'name',
                                       'login': 'login9999',
                                       'email': 'email9999@q.q',
                                       'user_type_id': 2,
                                       'id': 9999,
                                       })
        self.assertEqual(response.json(), {'success': 'OK'})
        response = requests.delete('http://localhost:5000/api/v2/users/9999')
        self.assertEqual(response.json(), {'success': 'OK'})

    def test_users_get_valid(self):
        """
        Тест проверки добавленного пользователя
        :return:
        """
        response = requests.post('http://localhost:5000/api/v2/users',
                                 json={'name': 'name',
                                       'login': 'login10002',
                                       'email': 'email10002@q.q',
                                       'user_type_id': 2,
                                       'id': 10002,
                                       })
        self.assertEqual(response.json(), {'success': 'OK'})
        response = requests.get('http://localhost:5000/api/v2/users/10002')
        self.assertEqual(response.json()['users']['login'], 'login10002')
        response = requests.delete('http://localhost:5000/api/v2/users/10002')
        self.assertEqual(response.json(), {'success': 'OK'})

    def test_users_all_get(self):
        """
        Тест запроса множества пользователей
        :return:
        """
        response = requests.get('http://localhost:5000/api/v2/users')
        self.assertTrue(len(response.json()['users']) > 0)

    def test_users_delete(self):
        """
        Тест удаления добавленной пользователя
        :return:
        """
        response = requests.post('http://localhost:5000/api/v2/users',
                                 json={'name': 'name',
                                       'login': 'login10000',
                                       'email': 'email10000@q.q',
                                       'user_type_id': 2,
                                       'id': 10000,
                                       })
        self.assertEqual(response.json(), {'success': 'OK'})
        response = requests.delete('http://localhost:5000/api/v2/users/10000')
        self.assertEqual(response.json(), {'success': 'OK'})

    def test_users_delete_no_id(self):
        """
        Тест удаления несуществующего пользователя
        :return:
        """
        response = requests.delete('http://localhost:5000/api/v2/users/10001')
        self.assertEqual(response.json(), {'message': 'User 10001 not found'})



if __name__ == "__main__":
    unittest.main()


