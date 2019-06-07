from bs4 import BeautifulSoup
import json
import requests

from config import settings

list_url = "https://9b199e13.prtimes.tech/list/{page_number}"
detail_url = "https://9b199e13.prtimes.tech/detail/{company_id}/{release_id}"
category_url = "https://9b199e13.prtimes.tech/category_release/{category_id}/{page_number}"

CATEGORY_DATA = [
    ('21', 'アート'),
    ('20', 'アニメ'),
    ('14', '映像'),
    ('15', '音楽'),
    ('37', 'メンズ'),
    ('68', '遊園地'),
    ('43', '外食'),
    ('42', '飲み物'),
    ('45', '美容'),
    ('23', 'スマホゲー'),
    ('25', 'おもちゃ'),
    ('41', '食べ物'),
    ('36', 'レディー'),
    ('13', '本'),
    ('67', '観光'),
]


class Release:
    def __init__(self, title, src, company_id, release_id):
        self.title = title
        if len(title) > 36:
            self.title = self.title[:36] + '...'
        self.src = src
        self.company_id = company_id
        self.release_id = release_id


class Entry:
    def __init__(self, title, subtitle, desc, body, main_image, images,
                 animation_images, company_id, release_id):
        self.title = title
        self.subtitle = subtitle
        self.desc = desc
        self.body = body
        self.main_image = main_image
        self.images = images
        self.company_id = company_id
        self.release_id = release_id


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_detail(company_id, release_id):
    url = detail_url.format(
        company_id=company_id,
        release_id=release_id
    )
    r = requests.get(url)
    data = json.loads(r.text)

    return data


def get_main_image(data):
    if data['animation_image1']:
        src = data['animation_image1']
    elif data['image1']:
        src = data['image1']
    else:
        src = data['main_image']

    return src


def get_release_list():
    release_list = []
    for i in range(1, 3):
        url = list_url.format(page_number=i)
        r = requests.get(url)
        data = json.loads(r.text)
        data = data['data']

        for release in data:
            data = get_detail(release['company_id'], release['release_id'])

            company_id = data['company_id']
            release_id = data['release_id']
            data = data['data']
            title = data['title']
            src = get_main_image(data)
            release_list.append(Release(title, src, company_id, release_id))

    return release_list


def get_category_release_list(category_id):
    release_list = []
    for i in range(1, 3):
        url = category_url.format(
            category_id=category_id,
            page_number=i
        )
        r = requests.get(url)
        data = json.loads(r.text)
        data = data['data']

        for release in data:
            data = get_detail(release['company_id'], release['release_id'])

            company_id = data['company_id']
            release_id = data['release_id']
            data = data['data']
            title = data['title']
            src = get_main_image(data)
            release_list.append(Release(title, src, company_id, release_id))

    return release_list


def get_entry(company_id, release_id):
    data = get_detail(company_id, release_id)
    data = data['data']

    title = data['title']
    subtitle = data['subtitle']
    desc = data['head']
    body = data['body']
    desc = BeautifulSoup(desc).text
    body = BeautifulSoup(body).text
    main_image = get_main_image(data)

    images = []
    for i in range(1, 21):
        if data['image' + str(i)] and data['image' + str(i)] is not main_image:
            images.append(data['image' + str(i)])

    animation_images = []
    for i in range(1, 11):
        if data['animation_image' + str(i)]:
            animation_images.append(data['animation_image' + str(i)])

    entry = Entry(title, subtitle, desc, body, main_image, images,
                  animation_images, company_id, release_id)

    return entry


def get_category_list():
    category_list = []

    for item in CATEGORY_DATA:
        category_list.append(Category(item[0], item[1]))

    return category_list


def get_current_category(id):
    for item in CATEGORY_DATA:
        if item[0] == str(id):
            return item[1]
