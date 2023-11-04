from bs4 import BeautifulSoup
import requests
import csv


headers: dict = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

def make_titles_csv() -> None:
    data: dict = {'title': 'title', 'text': 'text', 'author': 'author', 'since': 'since'}
    save(data)


def get_html(url:str) -> str:
    html: str = requests.get(url, headers=headers).text
    return html


def parsing(articles) -> list[dict]:
    data: list = []
    for article in articles:
        rewiev: dict = {}
        title: str = article.find('h2').text.strip()
        text: str = article.find('p').text.strip()
        author: str = article.find('p', class_='testimonial-author').text.strip()
        since: str = article.find('p', class_='traxer-since').text.strip().split(' ')[2]
        rewiev['title'] = title
        rewiev['text'] = text
        rewiev['author'] = author
        rewiev['since'] = since
        data.append(rewiev)
    return data


def save(data:dict) -> None:
    with open('review.csv', 'a') as file:
        fields: tuple = ('title', 'text','author', 'since')
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerow(data)


def get_data(html:str):
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find('div', class_='builder-posts-wrap clearfix loops-wrapper testimonial grid3').find_all('article')
    return articles
        


def main() -> None:
    make_titles_csv()
    page: int = 1
    while True:
        url: str = f'https://catertrax.com/traxers/page/{page}/?themify_builder_infinite_scroll=no'
        html: str = get_html(url=url)
        articles = get_data(html=html)
        if articles:
            data = parsing(articles=articles)
            for rewiev in data:
                save(data=rewiev)
            page += 1
        else:
            break


if __name__ == '__main__':
    main()
