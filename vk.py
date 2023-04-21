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
        if (resp.get("error") or not resp.get("response") or not resp["response"].get("items")): return {"success": False}

        res = []
        def getLink(links: list):
            lettersSize = ["w", "z", "y", "x", "m", "s"]
            link = []
            i = 0
            while (len(link) < 1):
                link = list(filter(lambda j: j["type"] == lettersSize[i], links))
                i += 1
            return link[0]["url"]

        for i in resp["response"]["items"]:
            res.append({"date": i["date"], "link": getLink(i["sizes"]), "likes": i["likes"]["count"]})
        return {"success": True, "data": res}