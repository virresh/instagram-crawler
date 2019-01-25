import os
import argparse
import json
import requests
from bs4 import BeautifulSoup

FILE_PATH = './'

def get_data_set(path):
    with open(path) as f:
        return json.loads(f.read())

def get_img_url_by_post_url(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return None 
    soup = BeautifulSoup(resp.text, 'html.parser')
    for meta in soup.find_all('meta'):
        if meta.get('property') == 'og:image':
            return meta.get('content')


def save_image(savepath, url):
    with open(savepath, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            return 'fail'

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

        return 'success'


def main(filepath, savedir):
    fail_posts = []
    images = get_data_set(filepath)

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    for idx, image in enumerate(images):
        filename = os.path.join(savedir, '%04d.jpg' % (idx))

        status = save_image(filename, image['img_url'])
        if status == 'fail':
            image_url = get_img_url_by_post_url(image['key'])

            if not img_url:
                fail_posts.append(image)
                continue

            status = save_image(filename, image['img_url'])
            if status == fail:
                fail_posts.append(image)

    if fail_posts:
        with open('fail_posts.json','w') as f:
            f.write(json.dumps(fail_posts))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath')
    parser.add_argument('-s', '--savedir')
    args = parser.parse_args()

    if args.filepath:
        filepath = args.filepath
    if args.savedir:
        savedir = args.savedir
    else:
        savedir = os.path.dirname(args.filepath)

    main(filepath, savedir)