import requests

class Disk:
    def __init__(self, TOKEN) -> None:
        self.token = TOKEN
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
    def upload(self, fileUrl, fileName):
        print(f"Загружаю файл {fileUrl} с названием {fileName}: ", end="")
        args = {"path": f"{self.folderName}/{fileName}"}
        res = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", params=args, headers=self.headers)
        resj = res.json()
        link = resj.get("href")
        if (res.status_code != 200 or not link):
            print(f"Ошибка. Подробности:\n{resj}.")
            return
        args = {"fromFile": fileUrl}
        res = requests.put(link, params=args)
        if (res.status_code != 201):
            print(f"Ошибка.\nПодробности:\n{res.json()}")
            return
        print("Успешно.")
    def createFolder(self, folderName):
        print(f"Создаю папку {folderName}: ", end="")
        args = {"path": f"/{folderName}"}
        res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", params=args, headers=self.headers)
        if (res.status_code != 201):
            print(f"Неудача.\n{res.json()}.\nПопытка 2: ",end="")
            from time import localtime, strftime, time
            folderName = f"{folderName}-{strftime('%Y-%m-%d-%H.%M.%S', localtime(time()))}"
            args = {"path": folderName}
            res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", params=args, headers=self.headers)
            if (res.status_code != 201):
                print("Ошибка.")
                raise Exception(res.json())
        self.folderName = folderName
        print("Успешно.")