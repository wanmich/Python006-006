import requests
import re
from time import sleep
from lxml import etree
from fake_useragent import UserAgent
import os
import django
import sys
from lxml import etree
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HomeWork.settings')
django.setup()
from Douban.models import ShortComments


def get_short_comment():
    ua = UserAgent(verify_ssl=False)
    header = {
        'user-agent': ua.random,
        'Refere': 'https://movie.douban.com/subject/24733428/'
    }
    urls = (f'https://movie.douban.com/subject/24733428/comments?start={i}&limit=20&status=P&sort=new_score' for i in range(0, 200, 20))
    count = 0
    for url in urls:
        try:
            response = requests.get(url, headers=header)
        except ConnectionError:
            response = requests.get(url, headers=header)
        html_text = response.text
        selector = etree.HTML(html_text)
        comments = selector.xpath("//div[@class='comment-item ']//p[@class=' comment-content']/span/text()")
        star_class = selector.xpath("//div[@class='comment-item ']//span[@class='comment-info']/span[2]/@class")
        comment_date = selector.xpath("//span[@class='comment-time ']/text()")

        stars = []
        for star in star_class:
            try:
                stars.append(int(int(re.findall(r'\d{2}', star)[0]) / 10))
            except IndexError:
                stars.append(0)

        comments = [comment.strip() for comment in comments]
        comment_dates = [comment_date.strip() for comment_date in comment_dates]

        try:
            data = zip(stars, comments, comment_dates)
            for cmt in data:
                try:
                    ShortComments.objects.create(stars=cmt[0], comment=cmt[1], comment_date=cmt[2])
                except Exception as e:
                    raise e
            print('20 comments inserted.')
        except Exception as e:
            print(e)
        finally:
            header['Refere'] = url
            print('wait for 5 sec.')
            sleep(5)
        count += 20
    print(f"About {count} comments inserted.")


if __name__ == "__main__":
    get_short_comment()
