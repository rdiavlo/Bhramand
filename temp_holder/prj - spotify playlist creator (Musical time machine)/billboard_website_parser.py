import requests
from bs4 import BeautifulSoup


"""
Steps:
    1. User date [Right format]
    2. Extract top 10 from url on that date
    3. print
"""


def get_top_10_songs_for_date(usr_input):

    url = f"https://www.billboard.com/charts/hot-100/{usr_input}/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)

    res_2 = soup.select(
        'h3[class="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"]')

    res_3 = soup.findAll('span', attrs={
        'class': 'c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only'})
    lst = []
    for i in range(len(res_2)):

        if i > 9:
            break

        song_title = res_2[i].text.strip()
        artist = res_3[i].text.strip()
        res_string = str(i + 1) + ". " + song_title + " " + artist

        lst.append([artist, song_title, res_string])

    return lst


if __name__ == "__main__":

    usr_input_str = "2000-10-12"

    res = get_top_10_songs_for_date(usr_input_str)

    for i in res:
        print(i[2])
