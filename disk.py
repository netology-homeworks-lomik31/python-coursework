import requests

class Disk:
    def __init__(self, TOKEN) -> None:
        self.token = TOKEN
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"OAuth {self.token}"
        }
    def upload(self, fileLink, fileName):
        pass
    def createFolder(self, folderName):
        args = {
            "path": folderName
        }
        res = requests.put("https://cloud-api.yandex.net/v1/disk/resources", params=args, headers=self.headers)
        if (res.status_code != 201):
            print(res.json())
            from time import localtime, strftime, time
            self.createFolder(strftime('%Y-%m-%d-%H\:%M\:%S', localtime(time())) + "-" + folderName)