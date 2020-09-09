import requests
from bs4 import BeautifulSoup as bs
import time
import numpy as np
# TODO: Add tqdm

def scrape_player_image(html, player_img_links):
    # Scrape player images
    player_image_boxes = html.findAll("td", {"class": "col-avatar"})
    # print("Number of player images on this page = {}".format(len(player_image_boxes)))
    for player_image in player_image_boxes:
        if player_image.figure is None:
            player_img_links.append(np.Nan)
        else:
            player_img_links.append(player_image.figure.img['data-src'])


def scrape_player_id(html, player_ids):
    # Scrape player ids
    player_id_boxes = html.findAll("a", {"class": "tooltip"})
    num_players_on_page = min(60, len(player_id_boxes))  # Eliminate 4 extra unwanted boxes towards end of page
    for idx in range(0, num_players_on_page):
        # href = /player/252886/kwame-osigwe/200056/
        # is in the form /player/ID/....
        # Extract the ID
        href = player_id_boxes[idx]['href']
        player_ids.append(href.split("/")[2])


def scrape_player_name_country_club(html, player_names, country_img_links, club_img_links):
    # Scrape player name along with his country and club images
    country_club_image_boxes = html.findAll("div", {"class": "bp3-text-overflow-ellipsis"})
    # print("Number of countries+club images on this page = {}".format(len(country_club_image_boxes)))
    for idx, img_box in enumerate(country_club_image_boxes):
        try:
            if img_box is None:
                print("found none empty country_club row")
                country_img_links.append(np.NaN)
                player_names.append(np.NaN)
                club_img_links.append(np.NaN)
            elif img_box.figure is not None:
                club_img_links.append(img_box.figure.img['data-src'])  # has both img_box.figure and img_box.img
            elif img_box.a is not None and img_box.figure is None:
                print("found one with no figure tag but only a tag")
                club_img_links.append(np.NaN)
                continue
            elif img_box.figure is None and img_box.img is not None:
                country_img_links.append(
                    img_box.img['data-src'])  # only img_box.img exists. img_box.fig does not exist.
                player_names.append(img_box.text)
        except Exception as e:
            print("Exception during parse of country/club: " + str(e))
            continue


def go_scrape():
    # Without user-agent header, this site return 403 Forbidden
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.37"
    scraping_started = False
    player_img_links = []
    player_ids = []
    player_names = []
    country_img_links = []
    club_img_links = []
    for offset in range(0, 120, 60):
        try:
            #time.sleep(1)
            print("Processing page at offset " + str(offset))
            sofifa_url = "https://sofifa.com/players?offset=" + str(offset) # preparing the URL
            player_list_page = requests.get(sofifa_url, headers={'User-Agent': user_agent}) # requesting the webpage from the internet
            player_list_html = bs(player_list_page.text, "html.parser") # parsing the webpage as HTML

            # Check if all players have been scraped already
            # Use "Previous" button as a deciding factor
            # Noticed that some intermediate pages sometimes miss "next" button
            # TODO: update logic since "Previous" might not always be second from last in button list
            # buttons = player_list_html.findAll("span", {"class": "bp3-button-text"})
            # # After starting to scrape, keep scraping only until Previous button is visible on current page
            # if scraping_started and buttons[-2].text != "Previous":
            #     break
            # scraping_started = True # This should be True until scraping continues

            scrape_player_image(player_list_html, player_img_links)
            scrape_player_id(player_list_html, player_ids)
            scrape_player_name_country_club(player_list_html, player_names, country_img_links, club_img_links)
            # print("Number of country images on this page = {}".format(len(country_img_links)))
            # print("Number of players successfully processed on this page = {}".format(len(player_img_links)))
        except Exception as e:
            print("Exception occured: " + str(e))
            continue

    for (p_id, p_name, p_link, ctry_link, clb_link) in zip(player_ids, player_names, player_img_links, country_img_links, club_img_links):
        print(p_id, p_name, p_link, ctry_link, clb_link, sep="        ")

    print("Finally we have {} links of players, {} links of countries and {} links of clubs".format(len(player_img_links), len(country_img_links), len(club_img_links)))
    return player_ids, player_names, player_img_links, country_img_links, club_img_links

