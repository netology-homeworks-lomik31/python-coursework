import requests
import json as JSON

class VK:
    def __init__(self, TOKEN) -> None:
        self.token = TOKEN
    def getPhotos(self, userId: int, count: int = 5, album: str = "profile"):
        print("Получаю список фотографий пользователя: ", end="")
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "owner_id": userId,
            "album_id": album,
            "extended": 1,
            "v": "5.131",
            "rev": 0,
            "count": count
        }
        resp = requests.get("https://api.vk.com/method/photos.get", headers=headers, params=params).json()
        if (resp.get("error") or not resp.get("response") or not resp["response"].get("items")):
            print(f"Ошибка. Подробности:\n{resp}")
            return {"success": False}
        print("Успешно.")
        res = []
        def getLink(links: list):
            lettersSize = ["w", "z", "y", "x", "m", "s"]
            link = []
            i = 0
            while (len(link) < 1):
                link = list(filter(lambda j: j["type"] == lettersSize[i], links))
                i += 1
            return [lettersSize[i], link[0]["url"]]

        print("Получаю ссылки на фото пользователя: ", end="")
        a = []
        for i in resp["response"]["items"]:
            link = getLink(i["sizes"])
            name = f"{i['likes']['count']}.{requests.get(link[1]).headers['content-type'][6:]}"
            res.append({"date": i["date"], "link": link[1], "name": name})
            a.append({"file_name": name, "size": link[0]})
        with open("./result.json") as f:
            f.write(JSON.dumps(a))

        print("Успешно.")
        return {"success": True, "data": res}