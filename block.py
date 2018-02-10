import json
import os
import hashlib

# Находим папку blockchain относительно нашей текущей папки
blockchain_dir = os.curdir + '/blockchain/'

# Считаем hexdigest файла переданного в filename
def get_hash(filename):
#    blockchain_dir = os.curdir + '/blockchain/'
# 'rb' - открываем в двоичном виде
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()

def get_files():
   files = os.listdir(blockchain_dir)
# переводим имена файлов в int и сортируем по порядку (от 1 по возрастанию)
   return sorted([int(i) for i in files])

def check_integrity():
#    blockchain_dir = os.curdir + '/blockchain/'
# Получаем список файлов из папки blockchain
#    files = os.listdir(blockchain_dir)
# переводим имена файлов в int и сортируем по порядку (от 1 по возрастанию)
#    files = sorted([int(i) for i in files])
    files = get_files()

    results = []

# По очереди для всех файлов, кроме первого (он генезис блок и не имеет Hash предыдущего блока)
    for file in files[1:]:
# Открываем файл
        f = open(blockchain_dir + str(file))
# загружаем из файла в json формате значение соответсвующее 'hash'
        h = json.load(f)['hash']
# имя предыдущего файла
        prev_file = str(file - 1)
# расчет hexdigest
        actual_hash = get_hash(prev_file)

# Проверка посчитанного и записаного

        if h == actual_hash:
            res = 'OK'
        else:
            res = 'Corrupted'

# Вывод результата. Функция format расставляет свои аргументы (prev_file, res) в {}
#        print('block {} is: {}'.format(prev_file, res))

        results.append({'block': prev_file, 'result': res})

    return results


def write_block(name, amount, to_whom, prev_hash=''):
#    blockchain_dir = os.curdir + '/blockchain/'

#    files = sorted(os.listdir(blockchain_dir))
#    files = sorted([int(i) for i in files])
    files = get_files()

# Нашли последний файл
    prev_file = files[-1]
# Определяем новое имя файла и преводим его в строку
    filename = str(prev_file + 1)
# Получаем hash предыдущего файла
    prev_hash = get_hash(str(prev_file))

    #    print(filename)

    data = {'name': name,
            'amount': amount,
            'to_whom': to_whom,
            'hash': prev_hash}
# открываем для записи новый файл (filename), 'w' - запись
    with open(blockchain_dir + filename, 'w') as file:
# запись в формате json, indent=4 - делаем 4 отступа, чтобы все в одну строку не было
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
#Создание и запись блоков
    #    write_block(name='ivan', amount=2, to_whom='katja')

# проверка блоков
    print(check_integrity())


if __name__ == '__main__':
    main()
