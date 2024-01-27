import requests
from bs4 import BeautifulSoup
import datetime


"""
Steps:
    1. Get Data [Periodic]
    2. Store in SQlite DB
    3. If it hits threshold alert[Gmail]
"""
print("""⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠴⠏⠁⠀⢣⠀⠀⠀⠀⠀⠀
⠀⣴⣿⢹⣉⣙⢻⣖⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠰⠀⣾⡄⠀⠀⠀⠀⠀
⢸⣿⣿⠘⣷⢀⠈⠉⠛⢯⣗⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⠏⠀⠀⠀⠀⣽⡇⠀⠀⠀⠀⠀
⢸⣿⣿⠀⢽⠀⠀⠀⠀⠀⢹⣷⣝⣲⡤⣄⡀⣀⣠⣤⣖⣲⡶⠚⠛⠒⠋⠉⠲⣶⣿⣻⠋⠀⠀⠐⠀⠀⣹⡇⠀⠀⠀⠀⠀
⢸⣿⣿⡀⠈⠓⠳⢦⣄⠀⠈⢿⣟⢛⣷⣶⣾⣶⣾⣛⣻⣿⠷⠒⠂⠀⠀⠀⠀⠀⠉⠹⠖⠀⠀⠂⠀⢰⣿⠀⠀⠀⠀⠀⠀
⣘⣿⣿⣷⣀⠀⠀⠀⠹⡇⠀⠈⢿⡝⠻⡽⠛⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣗⠀⣤⣻⠀⠀⠀⠀⠀⠀
⠈⠸⣿⠙⢿⣆⠀⠀⠀⠃⠀⠀⠀⠁⠀⠀⢸⠋⠀⣀⣤⣶⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣗⠻⠻⡄⠀⠀⠀⠀⠀
⠀⠀⢈⡆⠘⠻⠿⣦⢄⠀⠀⠀⠀⠀⠀⠀⡎⠀⣾⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠈⠻⡿⠿⠟⠒⠀⢙⣦⡀⠀⠀⠀
⠀⠀⠈⢹⡀⠀⠀⠘⣾⠀⠀⠀⠀⠀⢀⣴⣟⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⠀⠀⣠⣤⣤⡤⣄⠀⠀⠀⠀⠀⠘⢿⣿⣦⠀⠀
⠀⠀⠀⠀⢣⢀⣀⣀⠘⠂⠀⠀⢰⣿⣿⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠻⣍⣹⠋⠀⢀⡀⢀⣀⣀⣈⠈⢻⣧⠀
⠀⠀⠀⠀⠸⡌⣿⣿⣷⣤⣶⣶⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠬⠭⠥⢤⣦⣾⠽⠗⠚⠋⠉⠉⠛⠶⠦⠴⠈⣻⡄
⠀⠀⠀⠀⠠⢧⢿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠶⠶⠴⠾⠛⠁⠀⠀⠀⢠⠂⣸⡇
⠀⠀⠀⠀⠀⠘⢶⣿⣿⣿⣿⣿⣿⣿⡇⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠿⡔
⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣷⣤⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⣰⠊⡰⠁
⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣾⡿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠏⢸⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⡟⣿⣿⣿⣿⡟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠏⢀⡏⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣷⡝⠻⠿⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠉⠀⡼⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡼⠽⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⢯⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠐⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⡇⠀⢳⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠘⡆⠘⡄⠀⠀
⠀⠀⠀⠀⠀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⡁⢰⡇⠀⠀
⠀⠀⠀⠀⢰⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠘⡇⠀⠀
⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢸⢷⠀⠀
⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠘⢹⠀⠀
⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⢸⠀⠀
⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢹⠀⠀
⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢸⠀⠀
⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀""")
print("AUTHOR: 'dottore")



def get_amazon_product_params(product_name, product_url):
    """
    This function:
    Takes in [Inp]: p1: 'product_name', p2: 'product_url'
    Returns [Op]: [product_price, current_date, string_shouter]
    """

    ## GOOGLE SCRAPER:

    # response = requests.get(product_url)
    # page_html = response.text
    #
    # soup = BeautifulSoup(page_html, "html.parser")
    # # print(soup)
    #
    # res = soup.select('span[class="r0bn4c rQMQod"] ')
    #
    # item_price = res[2].text
    # check_if_item_in_stock = res[4].text
    #
    # if check_if_item_in_stock == "In stock":
    #     print(f"\nGOOGLE SCRAPED: The price of '{product_name}' on {datetime.date.today()}: {item_price[1:]}")

    HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'),
        'Accept-Language': 'en-US, en;q=0.5'
    }

    response = requests.get(product_url, headers=HEADERS)
    page_html = response.text

    soup = BeautifulSoup(page_html, "html.parser")
    # print(soup.prettify())

    res = soup.select('div [class="a-section"] span[class="a-price-whole"]')

    price = res[0].text.replace(".", "")
    current_date = datetime.date.today()
    res_list = [price, current_date, f"DIRECT SCRAPED: The price of '{product_name}' "
                                                         f"on {current_date}: ₹{price}"]
    return res_list


if __name__ == "__main__":
    PRODUCT_1_NAME = "VINCENT CHASE EYEWEARVINCENT CHASE EYEWEAR"
    PRODUCT_1_URL = "https://www.amazon.in/ATHLEISURE-Sunglasses-Polarized-VC-S14525/dp/B09VTHQN1S"
    
    res = get_amazon_product_params(PRODUCT_1_NAME, PRODUCT_1_URL)

    print("\n"*3)
    print(res)
    print(res[2])