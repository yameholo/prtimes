import json
import requests

from config import settings

list_url = "https://9b199e13.prtimes.tech/list/{page_number}"
detail_url = "https://9b199e13.prtimes.tech/detail/{company_id}/{release_id}"
category_url = "https://9b199e13.prtimes.tech/category_release/{category_id}/{page_number}"


class Release:
    def __init__(self, title, src, company_id, release_id):
        self.title = title
        if len(title) > 36:
            self.title = self.title[:36] + '...'
        self.src = src
        self.company_id = company_id
        self.release_id = release_id


class Entry:
    def __init__(self, title, subtitle, desc, main_image, images,
                 animation_images, company_id, release_id):
        self.title = title
        self.subtitle = subtitle
        self.desc = desc
        self.main_image = main_image
        self.images = images
        self.company_id = company_id
        self.release_id = release_id


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
    main_image = get_main_image(data)

    images = []
    for i in range(1, 21):
        if data['image' + str(i)] and data['image' + str(i)] is not main_image:
            images.append(data['image' + str(i)])

    animation_images = []
    for i in range(1, 11):
        if data['animation_image' + str(i)]:
            animation_images.append(data['animation_image' + str(i)])

    entry = Entry(title, subtitle, desc, main_image, images,
                  animation_images, company_id, release_id)

    return entry


def get_category():
    category = set()
    for i in range(1, 51):
        url = list_url.format(page_number=i)
        r = requests.get(url)
        data = json.loads(r.text)
        data = data['data']

        for record in data:
            url = detail_url.format(
                company_id=record['company_id'],
                release_id=record['release_id']
            )
            r = requests.get(url)
            data = json.loads(r.text)
            data = data['data']
            category.add((data['main_category_id'],
                          data['main_category_name']))

    return category
