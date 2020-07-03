from bs4 import BeautifulSoup
from requests import get
from time import sleep


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


def is_reputable(link):
    product_page = BeautifulSoup(get(link).text, "html.parser")
    thermometer = str(
        product_page.find(
            class_="card-section seller-thermometer"))
    sleep(0.25)

    if any(badrep in thermometer for badrep in ("newbie", "red", "orange")):
        return False

    return True

def get__search_pages():
    pass
if __name__ == "__main__":
    search_term = "128gb"
    price_min = 1200
    price_max = 1550
    if price_min > price_max:
        price_min, price_max = price_max, price_min
    category = "celulares"
    # TODO : CATEGORY SELECTION
    # """

    index = 1
    pages = []
    while True:
        page = get(
            f"https://{category}.mercadolivre.com.br/novo/{search_term}_Desde_{index}_OrderId_PRICE_PriceRange_{price_min}-{price_max}")
        index += 50
        if page.status_code == 404:
            print(f"Error 404 - Not found. Last page: {((index-1) // 50 )-1}")
            break
        else:
            pages.append(page.text)
        sleep(0.25)
        print(f"Page {(index-1) // 50} sucess. Status: {page.status_code}.")

    pages = get_all_products(pages)

    results = [
        {
            "link": get_link(product),
            "title": get_title(product),
            "price": get_price(product),
            "no-interest": is_no_interest(product),
            "reputable": is_reputable(
                get_link(product))} for page in pages for product in page]

    for product in sorted(results, key=lambda p: p["price"]):
        if product["reputable"]:
            for k, v in product.items():
                print(f"{k}: {v}")
            print()
