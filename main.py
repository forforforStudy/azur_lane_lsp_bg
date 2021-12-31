import os
import os.path as path

from urllib.request import Request, urlopen, urlretrieve, build_opener, install_opener
from bs4 import BeautifulSoup

lsp_url_root = 'https://wiki.biligame.com/blhx/%E5%BD%B1%E7%94%BB%E7%9B%B8%E5%85%B3'

headers = {'Accept': 'text/html',
           'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

assets_folder = path.join(os.getcwd(), 'assets')


def get_target_url_response(url: str):
    request_inst = Request(url=url, headers=headers)
    response: str = urlopen(request_inst).read().decode('utf-8')

    return response


if __name__ == '__main__':
    if not path.exists(assets_folder):
        os.mkdir(assets_folder)

    root_response = get_target_url_response(lsp_url_root)
    print('插画页面拉取完成, 页面包含字符: {}'.format(len(root_response)))

    lsp_soup = BeautifulSoup(root_response, 'html.parser')
    all_lsp_images = lsp_soup.find_all('a', class_='image')

    print('找到老色批插画共: {} 张'.format(len(all_lsp_images)))

    print('开始拉图片')

    for index, a_wrapper in enumerate(all_lsp_images):
        img = next(a_wrapper.children)
        origin_img_src: str = img['src']

        if origin_img_src.find('/thumb') > -1:
            temp_src = img['src'].replace('/thumb', '')
            processed_src = temp_src[:temp_src.rfind('/')]
        else:
            processed_src = origin_img_src

        print('处理第{}张图片: {}'.format(index + 1, processed_src))

        image_name = processed_src[processed_src.rfind('/') + 1:]
        urlretrieve(processed_src, path.join(assets_folder, image_name))

    print('开炮!')
