import firebase_admin
import platform
import requests

from firebase_admin import credentials
from firebase_admin import firestore


class Firestore:
    def __init__(self, game):
        cred = credentials.Certificate("pygame-89e86-firebase-adminsdk-fbsvc-25d3a65e98.json")
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def save_score(self, name: str, score: int, play_time, level: int):
        doc_ref = self.db.collection("scores").document()
        doc_ref.set({"name": name, "score": score, "play_time": play_time, "level": level, "country": self.get_country(), "created_at": firestore.SERVER_TIMESTAMP})

    def create_session(self, name: str):
        doc_ref = self.db.collection("sessions").document()
        doc_ref.set({"name": name, "created_at": firestore.SERVER_TIMESTAMP, "machine": platform.machine(), "system": platform.system(), "country": self.get_country()})

    def get_scores(self):
        scores = self.db.collection("scores").order_by("score", direction=firestore.Query.DESCENDING).limit(5).stream()
        return [score.to_dict() for score in scores]
    

    def get_country(self):
        try:
            res = requests.get("https://ipinfo.io/json")
            data = res.json()
            return data.get("country")
        
        except Exception as e:
            return {"error": str(e)}