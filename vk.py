import requests

class VK:
    def __init__(self, TOKEN) -> None:
        self.token = TOKEN
    def getPhotos(self, userId: int, count: int = 5):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "owner_id": userId,
            "album_id": "profile",
            "extended": 1,
            "v": "5.131",
            "rev": 0,
            "count": count
        }
        resp = requests.get("https://api.vk.com/method/photos.get", headers=headers, params=params).json()
        if (resp.get("error") or not resp.get("response")): return {"success": False}