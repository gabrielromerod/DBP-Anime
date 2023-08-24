import unittest
import json
from app import app

class TestAnime(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        with open('data.json', 'r') as f:
            self.data = json.load(f)
        
        self.anime = {
            "id": 1,
            "tittle": "Naruto",
            "categories": ["Action", "Adventure", "Comedy", "Super Power", "Martial Arts", "Shounen"],
            "rating": 8.19,
            "reviews": 120,
            "seasons": 9,
            "type": "TV",
            "poster": "https://cdn.myanimelist.net/images/anime/13/17405.jpg"
        }

    def test_get_all_anime(self):
        response = self.app.get('/anime')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.data)

    def test_get_anime(self):
        for anime in self.data["animeList"]:
            response = self.app.get('/anime/' + str(anime["id"]))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, anime)

    def test_get_anime_not_found(self):
        response = self.app.get('/anime/100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, "Anime not found")

    def test_delete_anime(self):
        response = self.app.delete('/anime/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, "1 is deleted.")

    def test_post_anime(self):
        response = self.app.post('/anime', json=self.anime)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, self.anime)

    def test_post_anime_error(self):
        response = self.app.post('/anime', json={
            "id": 2,
            "tittle": "Naruto",
            "categories": ["Action", "Adventure", "Comedy", "Super Power", "Martial Arts", "Shounen"],
            "rating": 8.19,
            "reviews": 120,
            "seasons": 9,
            "type": "TV",
            "poster": "https://cdn.myanimelist.net/images/anime/13/17405.jpg"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, "Anime with tittle already exists")

    def test_put_anime(self):
        response = self.app.put('/anime/1', json={
            "id": 3,
            "tittle": "Naruto Shippuden",
            "categories": ["Action", "Adventure", "Comedy", "Super Power", "Martial Arts", "Shounen"],
            "rating": 8.19,
            "reviews": 120,
            "seasons": 9,
            "type": "TV",
            "poster": "https://cdn.myanimelist.net/images/anime/13/17405.jpg"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "id": 3,
            "tittle": "Naruto Shippuden",
            "categories": ["Action", "Adventure", "Comedy", "Super Power", "Martial Arts", "Shounen"],
            "rating": 8.19,
            "reviews": 120,
            "seasons": 9,
            "type": "TV",
            "poster": "https://cdn.myanimelist.net/images/anime/13/17405.jpg"
        })

    def test_put_anime_not_found(self):
        response = self.app.put('/anime/100', json={
            "id": 3,
            "tittle": "Naruto Shippuden",
            "categories": ["Action", "Adventure", "Comedy", "Super Power", "Martial Arts", "Shounen"],
            "rating": 8.19,
            "reviews": 120,
            "seasons": 9,
            "type": "TV",
            "poster": "https://cdn.myanimelist.net/images/anime/13/17405.jpg"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, "Anime not found")

if __name__ == '__main__':
    unittest.main()
