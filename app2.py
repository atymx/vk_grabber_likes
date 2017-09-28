# -*- coding: utf-8 -*-

import vk_api
import config
import time
import json
import webbrowser
import os

if not os.path.exists('likes'):
    os.mkdir('likes')
if not os.path.exists('posts'):
    os.mkdir('posts')

# -- -- -- получение токена и авторизация -- -- --
print(u'Сейчас сейчас откроется браузер. Дайте приложению доступы, скопируйте токен и вернитесь в консоль')
time.sleep(1)
webbrowser.open('https://oauth.vk.com/authorize?client_id={}&scope=photos,audio,video,docs,notes,pages,status,offers,'
                'questions,wall,groups,messages,email,notifications,stats,ads,offline,docs,pages,stats,'
                'notifications&response_type=token'.format(config.vk_app_id))
print(u'Вставьте токен')
access_token = input()
session = vk_api.VkApi(token=access_token)
tools = vk_api.VkTools(session)
# -- -- -- получение токена и авторизация -- -- --

print(u'Укажите id сообщества')
group_id = -int(input())


print(u'Подождите, формируется файл с id-шниками постов и файлы с содержимым постов')

wall = tools.get_all('wall.get', 100, {'owner_id': group_id, 'filter': config.filter})
print(u'Всего постов в сообществе - {}'.format(wall['count']))
posts = open('post_ids.txt', 'a')
for i in range(wall['count']):
    posts.write('{}\n'.format(wall['items'][i]['id']))
    post_file = open('posts/{}.txt'.format(wall['items'][i]['id']), 'wb')
    post_file.write(json.dumps(wall['items'][i], ensure_ascii=False).encode())
    post_file.close()
posts.close()

print(u'Файл post_ids.txt сформирован')


print(u'Начинаем формировать файлы likes/post[id].txt с id-шниками пользователей.')

file_ids = open('post_ids.txt', 'r')
for i in range(wall['count']):
    while True:
        try:
            print(u'{} из {}'.format(i + 1, wall['count']))
            id = int(file_ids.readline())
            post = open('likes/post{}.txt'.format(id), 'w')
            likes = tools.get_all('likes.getList', 1000, {'type': 'post', 'owner_id': group_id, 'item_id': id})
            for j in range(likes['count']):
                post.write('{}\n'.format(likes['items'][j]))
            post.close()
            break
        except:
            print('Ошибка! Пробуем снова!')

print(u'Все файлы сформированы. Спасибо!')
