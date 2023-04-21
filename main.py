from vk import VK
import sys

class Program:
    def main():
        with open("./key.txt", "r") as f:
            key = f.read()
        if (len(sys.argv) < 3): return print("Параметры переданы неверно либо не переданы")
        res = VK(key).getPhotos(sys.argv[1])
        if (not res.get("success")): return print("Произошла ошибка при выполнении запроса VK")

if __name__ == "__main__": Program.main()