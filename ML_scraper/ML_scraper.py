from bs4 import BeautifulSoup
from requests import get
from time import sleep
from pickle import load


def get_link(product):
    link = product.find(class_="item__info-title").get("href").strip()
    jm_loc = link.find('-_JM')
    if jm_loc == -1:
        return link
    return link[:jm_loc + 4]


def get_title(product):
    return product.find(class_="main-title").contents[0].strip()


def get_price(product):
    return float(
        product.find(
            class_="price__fraction").contents[0].strip()) * 1000


def is_no_interest(product):
    return True if product.find(class_="stack_column_item installments highlighted").contents[0].get(
        "class") == "item-installments free-interest" else False


def get_all_products(pages):
    return [
        BeautifulSoup(
            page,
            "html.parser").find_all(
            class_="item__info item--hide-right-col") for page in pages]


def is_reputable(link, min_rep=3):
    product_page = BeautifulSoup(get(link).text, "html.parser")
    thermometer = str(
        product_page.find(
            class_="card-section seller-thermometer"))
    sleep(0.25)
    THERM_LEVELS = ("newbie", "red", "orange",
                    "yellow", "light_green", "green")
    if any(badrep in thermometer for badrep in (THERM_LEVELS[i] for i in range(min_rep))):
        return False

    return True


with open("categories.pickle", "rb") as cat:
    CATS = load(cat)


def print_cats():
    for father_cat in CATS:
        print(f"{father_cat[0][0]} ---> {father_cat[0][1]}:")
        print()
        for cat in father_cat[1]:
            print(f"{father_cat[0][0]}.{cat['number']} -> {cat['name']}")
        print()


def get_cat(catid):
    father_num, child_num = map(int, catid.split('.'))
    for father in CATS:
        if father_cat[0][0] == father_num:
            for child in father_cat[1]:
                if child['number'] == child_num:
                    subdomain = child['subdomain']
                    suffix = child['suffix']
                    break
    return subdomain, suffix


def get_search_pages(term, cat='0.0', price_min=0, price_max=2147483647, condition=0):
    CONDITIONS = ["", "_ITEM*CONDITION_2230284", "_ITEM*CONDITION_2230581"]
    CATS.insert(0, [[0, 'Todas as categorias'], [
                {'subdomain': 'lista', 'suffix': '', 'number': '0', 'name': 'Todas'}]])
    subdomain, suffix = get_cat(cat)
    index = 1
    pages = []
    while True:
        page = get(
            f"https://{subdomain}.mercadolivre.com.br/{suffix}{term}_Desde_{index}_PriceRange_{price_min}-{price_max}{CONDITIONS[condition]}")
        index += 50
        if page.status_code == 404:
            break
        else:
            pages.append(page.text)
        sleep(0.25)
    return pages


if __name__ == "__main__":
    # TODO: input encapsulation
    search_term = input("Digite os termos da pesquisa: ")  # "128gb"
    price_min = int(input(
        "Digite como um número inteiro, sem outros símbolos, o preço mínimo para os resultados da pesquisa (Ex: '150' sem aspas para R$ 150,00): "))
    price_max = int(input(
        "Digite como um número inteiro, sem outros símbolos, o preço máximo para os resultados da pesquisa (Ex: '1500' sem aspas para R$ 1500,00): "))
    if price_min > price_max:
        price_min, price_max = price_max, price_min
    condition = int(input(
        "Insira a condição do produto para os resultados da busca.\n(0 - misto | 1 - novo | 2 - usado): "))
    order = int(input(
        "Insira a ordenação desejada dos resultados.\n(0 - relevância | 1 - preço mínimo | 2 - preço máximo): "))
    print_cats()
    category = input(
        "Insira a categoria de acordo com os código identificadores exibidos (Ex: Caso queira a categoria \"Adultos\", digite '31.1' sem aspas): ")
    min_rep = input(
        "Insira, de 0 a 6, qual é o nível mínimo de reputação desejada para os vendedores: ")
    # TODO: option - aggressiveness (speed)

    pages = get_search_pages(search_term, category, price_min, price_max)

    products = get_all_products(pages)

    results = [
        {
            "link": get_link(product),
            "title": get_title(product),
            "price": get_price(product),
            "no-interest": is_no_interest(product),
            "reputable": is_reputable(
                get_link(product), min_rep)} for page in pages for product in page]
    if order:
        if order == 1:
            results = sorted(results, key=lambda p: p["price"])
        else:
            results = sorted(results, key=lambda p: -p["price"])

    for product in results:
        if product["reputable"]:
            for k, v in product.items():
                print(f"{k}: {v}")
            print()
