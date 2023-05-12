from vk import VK
from disk import Disk
import time, argparse

class Program:
    def createFilesDict(files: list):
        res = {}
        for i in files:
            res[f"{i['name']} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['date']))}" if i["name"] in res else i["name"]] = i["link"]
        return res
    
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("VKT", metavar="VKTokenFile", type=str, nargs=1, help="Путь к файлу с токеном VK")
        # parser.add_argument("VKID", type=str, nargs=1, help="ID пользователя VK для бэкапа")
        # parser.add_argument("YADT", metavar="YaDiskTokenFile", type=str, nargs=1, help="Путь к файлу с токеном ядиска")
        parser.add_argument("-c", "--count", metavar="count", type=int, nargs=1, required=False, default=[5], help="Количество фото для сохранения (default: 5)")
        # parser.add_argument("--google", metavar="googleTokenFile", type=str, nargs=1, required=False, help="Путь к файлу с токеном google drive")
        parser.add_argument("-a", "--album", metavar="albumID", type=str, nargs=1, required=False, default=["profile"], help="ID альбома, из которого будет производиться загрузка фото (доступные варианты: 'wall', 'profile', 'saved', albumId; default: profile)")
        args = parser.parse_args()

        yaKey = input("Введите токен Яндекс.Диска: ")
        vkId = input("Введите id пользователя VK для бэкапа: ")

        try:
            with open(args.VKT[0], "r") as f:
                vkKey = f.read()
        except:
            print(f"Файл {args.VKT[0]} не найден")
            return
        # if (args.google):
        #     try:
        #         with open(args.google[0], "r") as f:
        #             googleKey = f.read()
        #     except:
        #         print(f"Файл {args.google[0]} не найден")
        #         return
        res = VK(vkKey).getPhotos(vkId, args.count[0], args.album[0])
        if (not res.get("success")): return print("Произошла ошибка при выполнении запроса VK")
        disk = Disk(yaKey)
        disk.createFolder(f"vk-photos-{vkId}-{args.album[0]}")
        d = Program.createFilesDict(res.get("data"))
        for i in d:
            disk.upload(d[i], i)

if __name__ == "__main__": Program.main()