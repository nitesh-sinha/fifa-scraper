# doing necessary imports
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import numpy as np

player_img_links = []
player_names = []
country_img_links = []
club_img_links = []

def go_scrape():
    # Without user-agent header, this site return 403 Forbidden
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
    scraping_started = False
    for offset in range(19800, 25000, 60):
        try:
            #time.sleep(1)
            print("Processing page at offset " + str(offset))
            sofifa_url = "https://sofifa.com/players?offset=" + str(offset) # preparing the URL
            player_list_page = requests.get(sofifa_url, headers={'User-Agent': user_agent}) # requesting the webpage from the internet
            player_list_html = bs(player_list_page.text, "html.parser") # parsing the webpage as HTML
            # Check if all players have been scraped already
            # Use "Previous" button as a deciding factor
            buttons = player_list_html.findAll("span", {"class": "bp3-button-text"})
            # After starting to scrape, keep scraping only until Previous button is visible on current page
            if scraping_started and buttons[-2].text != "Previous":
                break
            scraping_started = True # This should be True until scraping continues
            player_image_boxes = player_list_html.findAll("td", {"class": "col-avatar"})
            #print("Number of player images on this page = {}".format(len(player_image_boxes)))
            for player_image in player_image_boxes:
                if player_image.figure is None:
                    player_img_links.append(np.Nan)
                else:
                    player_img_links.append(player_image.figure.img['data-src'])
            country_club_image_boxes = player_list_html.findAll("div", {"class": "bp3-text-overflow-ellipsis"})
            #print("Number of countries+club images on this page = {}".format(len(country_club_image_boxes)))
            for idx, img_box in enumerate(country_club_image_boxes):
                try:
                    if img_box is None:
                        print("found none empty country_club row")
                        country_img_links.append(np.NaN)
                        player_names.append(np.NaN)
                        club_img_links.append(np.NaN)
                    elif img_box.figure is not None:
                        club_img_links.append(img_box.figure.img['data-src']) # has both img_box.figure and img_box.img
                    elif img_box.a is not None and img_box.figure is None:
                        print("found one with no figure tag but only a tag")
                        club_img_links.append(np.NaN)
                        continue
                    elif img_box.figure is None and img_box.img is not None:
                        country_img_links.append(img_box.img['data-src'])  # only img_box.img exists. img_box.fig does not exist.
                        player_names.append(img_box.text)
                except Exception as e:
                    print("Exception during parse of country/club: " + str(e))
                    continue
            # print("Number of country images on this page = {}".format(len(country_img_links)))
            # print("Number of players successfully processed on this page = {}".format(len(player_img_links)))
        except Exception as e:
            print("Exception occured: " + str(e))
            continue

    for (p_name, p_link, ctry_link, clb_link) in zip(player_names, player_img_links, country_img_links, club_img_links):
        print(p_name, p_link, ctry_link, clb_link, sep="        ")

    print("Finally we have {} links of players, {} links of countries and {} links of clubs".format(len(player_img_links), len(country_img_links), len(club_img_links)))


def create_dataframe():
    try:
        dict = {'Name': player_names, 'Photo':player_img_links, 'Flag':country_img_links, 'Club Logo':club_img_links}
        df = pd.DataFrame(dict)
        df.to_csv("working-links-1.csv")
    except Exception as e:
        print("Exception creating or storing the dataframe: " + str(e))


if __name__ == "__main__":
    print("Starting to scrape!!!")
    go_scrape()
    create_dataframe()


