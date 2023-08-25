from flask import Flask
from flask_restful import Api, Resource, reqparse
import json

app = Flask(__name__)
api = Api(app)

try:
    with open('data.json', 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {"animeList": []}

class Anime(Resource):
    def get(self, id=None):
        if id is None:
            return data, 200
        for anime in data["animeList"]:
            if(id == anime["id"]):
                return anime, 200
        return "Anime not found", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True)
        parser.add_argument("tittle", required=True)  # es una buena práctica agregar required=True para campos esenciales
        parser.add_argument("categories", required=True, action='append')
        parser.add_argument("rating", type=float, required=True)
        parser.add_argument("reviews", type=int, required=True)
        parser.add_argument("seasons", type=int, required=True)
        parser.add_argument("type", required=True)
        parser.add_argument("poster", required=True)

        args = parser.parse_args()

        for anime in data["animeList"]:
            if args["tittle"] == anime["tittle"]:
                return "Anime with tittle already exists", 400


        anime = {
            "id": args["id"],
            "tittle": args["tittle"],
            "categories": args["categories"],
            "rating": args["rating"],
            "reviews": args["reviews"],
            "seasons": args["seasons"],
            "type": args["type"],
            "poster": args["poster"]
        }

        data["animeList"].append(anime)
        try:
            with open('data.json', 'w') as f:
                json.dump(data, f)
        except IOError:
            return "Error writing to data file", 500
        
        return anime, 200


    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True)
        parser.add_argument("tittle", required=True)
        parser.add_argument("categories", required=True, action='append')
        parser.add_argument("rating", type=float, required=True)  # Ensure type is float
        parser.add_argument("reviews", type=int, required=True)   # Ensure type is int
        parser.add_argument("seasons", type=int, required=True)   # Ensure type is int
        parser.add_argument("type", required=True)
        parser.add_argument("poster", required=True)
        args = parser.parse_args()

        for anime in data["animeList"]:
            if(id == anime["id"]):
                anime["id"] = args["id"]
                anime["tittle"] = args["tittle"]
                anime["categories"] = args["categories"]
                anime["rating"] = args["rating"]
                anime["reviews"] = args["reviews"]
                anime["seasons"] = args["seasons"]
                anime["type"] = args["type"]
                anime["poster"] = args["poster"]

                try:
                    with open('data.json', 'w') as f:
                        json.dump(data, f)
                except IOError:
                    return "Error writing to data file", 500
                return anime, 201
            else:
                return "Anime not found", 404

    def delete(self, id):
        data["animeList"] = [anime for anime in data["animeList"] if anime["id"] != id]
        try:
            with open('data.json', 'w') as f:
                json.dump(data, f)
        except IOError:
            return "Error writing to data file", 500
        return "{} is deleted.".format(id), 200

    def patch(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("categories", action='append')
        fields = ["tittle", "rating", "reviews", "seasons", "type", "poster"]
        for field in fields:
            parser.add_argument(field)

        args = parser.parse_args()

        for anime in data["animeList"]: 
            if(id == anime["id"]):
                for field in fields:
                    if args[field] is not None:
                        anime[field] = args[field]
                if args["categories"] is not None:
                    anime["categories"] = args["categories"]
                try:
                    with open('data.json', 'w') as f:
                        json.dump(data, f)
                except IOError:
                    return "Error writing to data file", 500
                return anime, 200
            else:
                return "Anime not found", 404

api.add_resource(Anime, "/anime", "/anime/", "/anime/<int:id>")

if __name__ == "__main__":
    app.run(debug=True, port=5000)