from requests import get
from bs4 import BeautifulSoup
import re
import pickle

match_subdomain = re.compile(r"(https://|^)(\w*)\.")
match_suffix = re.compile(r".com.br/(.*)$")


def get_subdomain(link):

    return match_subdomain.search(link).group(2)


def get_suffix(link):

    return match_suffix.search(link).group(1)


cat_page = BeautifulSoup(
    get("https://www.mercadolivre.com.br/categorias").text,
    "html.parser")

master_categories = cat_page.findAll(class_="categories__container")

categories = []
for cat_container in master_categories:
    categories.append(
        [
            cat_container.find(
                'a', class_="categories__title").text, [
                {
                    "number": n + 1, "name": x.text, "suffix": get_suffix(
                        x["href"]), "subdomain": get_subdomain(
                        x["href"])} for n, x in enumerate(cat_container.find(
                            class_="categories__list").find_all(
                            class_="categories__subtitle"))]])

with open("categories.pickle", "wb") as savefile:
    pickle.dump(categories, savefile)
