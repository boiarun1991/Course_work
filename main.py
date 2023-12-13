from pprint import pprint
from urllib.parse import urlencode
import requests
from datetime import datetime
from tqdm import tqdm
import json

VK_TOKEN = 'VK_TOKEN'
APP_VK_ID = 'VK_ID'
OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
API_YANDEX_URL = 'https://cloud-api.yandex.net'
YA_OAUTH_TOKEN = 'YA_TOKEN'


class VKAPICLIENT:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {'access_token': self.token,
                'v': '5.199'}

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': 1})
        response = requests.get(self._build_url('photos.get'), params=params)
        return response.json().get('response', {}).get('items', {})




class YA_DISK_UPLOAD:
    headers_dict = {'Authorization': YA_OAUTH_TOKEN}

    def __int__(self, token):
        self.token = token

    def download_files(self):
        for file in tqdm(photo_max_size.items()):
            response = requests.get(file[1])
            with open(f'Download_Photos/{file[0]}.jpg', 'wb') as f:
                f.write(response.content)
            with open(f'Download_Photos/{file[0]}.jpg', 'rb') as f:
                params = {'path': {file[0]}}
                headers_dict = {'Authorization': YA_OAUTH_TOKEN}
                response = requests.get(f'{API_YANDEX_URL}/v1/disk/resources/upload', params=params,
                                        headers=headers_dict)
                url_upload = response.json().get('href')
                upload_file = requests.put(url_upload, files={'file': f}, headers=headers_dict)
        upload_info = requests.get(f'{API_YANDEX_URL}/v1/disk/resources/last-uploaded?limit={len(photo_max_size)}',
                                   headers=headers_dict)
        upload = upload_info.json().get('items', {})
        information_json = []
        info_dict = {}
        for item in upload:
            info_dict.setdefault('file_name', item.get('name'))
            info_dict.setdefault('size', item.get('size'))
            information_json.append(info_dict)
            info_dict = {}
        with open('information.json', 'w') as f_json:
            json.dump(information_json, f_json)

        return print(f'Загрузка завершена, {len(photo_max_size)} файлов загружено на Яндекс диск')


if __name__ == '__main__':
    vk_client = VKAPICLIENT(VK_TOKEN, APP_VK_ID)
    photos_info = vk_client.get_profile_photos()

    photo_max_size = {}

    for photo in photos_info[:5]:
        name_photo = str(photo.get('likes', {}).get('count'))
        downloaded_photo = photo.get('sizes')[-1].get('url')

        if name_photo not in photo_max_size.keys():
            photo_max_size.setdefault(name_photo, downloaded_photo)
        else:
            date_photo = photo.get('date')
            date_photo = datetime.fromtimestamp(date_photo)
            photo_max_size.setdefault(f'{name_photo}_{str(date_photo)[:10]}', downloaded_photo)

    APP_VK_ID = input('Введите VK id: ')
    YA_OAUTH_TOKEN = 'OAuth ' + input('Введите Yandex TOKEN: ')
    YA_DISK_UPLOAD.download_files(YA_OAUTH_TOKEN)
