from datetime import datetime
from time import sleep
import requests
import traceback

# ПОЛУЧЕНИЕ ТОКЕНА
username = input('Login: ')
password = input('Password: ')

resp = requests.post(
    f'https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnABp8ncuU&username={username}&password={password}').json()
token = resp["access_token"]

# ПОЛУЧЕНИЕ СПИСКА ГРУПП
with open('group.txt', 'r') as g_file:
    group = g_file.read().splitlines()

# ПОЛУЧЕНИЕ СПИСКА ВИДЕО/ НАДО ПЕРЕДЕЛАТЬ НА ОПИСАНИЕ + ССЫЛКА НА КТВ + ТЕГИ
with open('video.txt', 'r') as v_file:
    video = v_file.read().splitlines()


def spam(group, video, token):
    count = 0
    kol = 0
    while True:
        try:
            for g in group:
                resp = requests.get('https://api.vk.com/method/wall.post'
                                    f'?owner_id={g}'  # ID group
                                    f'&attachments={video[count]}'  # video
                                    '&from_group=0'
                                    f'&access_token={token}&v=5.124').json()  # token
                if 'response' in resp:
                    print(resp)
                    print(datetime.today().strftime(f'%H:%M:%S | Пост отправлен!\n'
                                                    f'Группа: {g}\n'
                                                    f'Видео: {video[count]}'))
                    print(datetime.today().strftime(f'%H:%M:%S | Отправлено постов: {kol + 1}\n'
                                                    f'Пауза 1 час.'))
                    kol += 1
                    sleep(3600)

                if 'error' in resp:
                    if resp.get('error').get('error_code') == 214:
                        print(datetime.today().strftime(f'%H:%M:%S | Ошибка при отправке поста. Возможно ЧС.\n'
                                                        f'Группа: {g}'))

                    else:
                        print(datetime.today().strftime(f'%H:%M:%S | Произошла ошибка.'))
                        print(resp)
                        print('Пауза 1 час.')
                        sleep(3600)

            count += 1
            if count > len(video) - 1:  # если количество отправленных видео больше списка видео
                count = 0
                print(count)
        except Exception as err:
            print(datetime.today().strftime(f'%H:%M:%S | Произошла ошибка:\n', traceback.format_exc()))
            print(resp)


if __name__ == '__main__':
    spam(group, video, token)