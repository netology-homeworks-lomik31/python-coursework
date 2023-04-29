import requests

class Disk:
    def __init__(self, TOKEN) -> None:
        self.token = TOKEN
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
    def upload(self, fileUrl, fileName):
        args = {"path": f"{self.folderName}/{fileName}"}
        res = requests.get("https://cloud-api.yandex.net/v1/disk/resources/upload", params=args, headers=self.headers)
        resj = res.json()
        link = resj.get("href")
        if (res.status_code != 200 or not link):
            return
        args = {"fromFile": fileUrl}
        res = requests.put(link, params=args)
        if (res.status_code != 201):
            return
    def createFolder(self, folderName):
        self.folderName = folderName
        args = {"path": folderName}
        res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", params=args, headers=self.headers)
        if (res.status_code != 201):
            print(res.json())
            from time import localtime, strftime, time
            args = {"path": strftime('%Y-%m-%d-%H\:%M\:%S', localtime(time())) + "-" + folderName}
            res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", params=args, headers=self.headers)
            if (res.status_code != 201):
                raise Exception(res.json())