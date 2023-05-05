from vk import VK
from disk import Disk
import sys, time, argparse

class Program:
    def createFilesDict(files: list):
        res = {}
        for i in files:
            res[f"{i['likes']} {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['date']))}" if i["likes"] in res else i["likes"]] = i["link"]
        return res
    
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("VKT", metavar="VKTokenFile", type=str, nargs=1, help="Путь к файлу с токеном VK")
        parser.add_argument("VKID", type=str, nargs=1, help="ID пользователя VK для бэкапа")
        parser.add_argument("YADT", metavar="YaDiskTokenFile", type=str, nargs=1, help="Путь к файлу с токеном ядиска")
        parser.add_argument("-c", "--count", metavar="count", type=int, nargs=1, required=False, default=5, help="Количество фото для сохранения (default: 5)")
        parser.add_argument("--google", metavar="googleTokenFile", type=str, nargs=1, required=False, help="Путь к файлу с токеном google drive")
        parser.add_argument("-a", "--album", metavar="albumID", type=str, nargs=1, required=False, default="profile", help="ID альбома, из которого будет производиться загрузка фото (default: profile)")
        args = parser.parse_args()

        with open("./key.txt", "r") as f:
            key = f.read()
        if (len(sys.argv) < 3): return print("Параметры переданы неверно либо не переданы")
        args = []
        if (len(sys.argv) > 3):
            try: args.append(int(sys.argv[3]))
            except: return print("Параметры переданы неверно либо не переданы")
        res = VK(key).getPhotos(sys.argv[1], *args)
        if (not res.get("success")): return print("Произошла ошибка при выполнении запроса VK")
        disk = Disk(sys.argv[2])
        disk.createFolder(f"vk-photos-{sys.argv[1]}")
        d = Program.createFilesDict(res.get("data"))
        for i in d:
            disk.upload(d[i], i)

if __name__ == "__main__": Program.main()