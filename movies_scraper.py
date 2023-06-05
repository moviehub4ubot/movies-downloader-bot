import requests
from bs4 import BeautifulSoup


url_list = {}
api_key ="6dadfdffd0cec854aa06cbae97da7c0678a0eccf"
websites = [
    {'name': 'Website 1', 'url': 'https://84.46.254.230/'},
    {'name': 'Website 2', 'url': 'https://example2.com/movies?search='}
]


def search_movies(query):
    movies_list = []
    movies_details = {}
    for website in websites:
        website_name = website['name']
        website_url = website['url']
        search_url = f"{website_url}{query.replace(' ', '+')}"
        website_content = BeautifulSoup(requests.get(search_url).text, "html.parser")
        movies = website_content.find_all("a", {'class': 'ml-mask jt'})
        for movie in movies:
            if movie:
                movies_details["id"] = f"{website_name}-link{movies.index(movie)}"
                movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
                url_list[movies_details["id"]] = movie['href']
            movies_list.append(movies_details)
            movies_details = {}
    return movies_list


def get_movie(query):
    movie_details = {}
    movie_link = url_list.get(query)
    if movie_link:
        movie_page_content = BeautifulSoup(requests.get(movie_link).text, "html.parser")
        if movie_page_content:
            title = movie_page_content.find("div", {'class': 'mvic-desc'}).h3.text
            movie_details["title"] = title
            img = movie_page_content.find("div", {'class': 'mvic-thumb'})['data-bg']
            movie_details["img"] = img
            links = movie_page_content.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
            final_links = {}
            for link in links:
                final_links[link.text] = link['href']
            movie_details["links"] = final_links
    return movie_details



