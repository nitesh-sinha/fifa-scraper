import requests
from bs4 import BeautifulSoup as bs
import numpy as np


def scrape_player_images(html, player_img_links):
    """
    Scrapes player images(about 60 of them) on one HTML page
    :param html: Parsed HTML page with all tags intact
    :param player_img_links: list to store links of player's images while scraping
    :return: None(player_img_links will contain the scraped output)
    """
    # Scrape player images
    player_image_boxes = html.findAll("td", {"class": "col-avatar"})
    # print("Number of player images on this page = {}".format(len(player_image_boxes)))
    for player_image in player_image_boxes:
        if player_image.figure is None:
            player_img_links.append(np.Nan)
        else:
            player_img_links.append(player_image.figure.img['data-src'])


def scrape_player_ids(html, player_ids):
    """
    Scrapes player ids(about 60 of them) on one HTML page
    :param html: Parsed HTML page with all tags intact
    :param player_ids: list to store player's IDs while scraping
    :return: None(player_ids will contain the scraped output)
    """
    # Scrape player ids
    player_id_boxes = html.findAll("a", {"class": "tooltip"})
    for player_id_box in player_id_boxes[:-4]:   # Eliminate 4 extra unwanted boxes towards end of page
        # href = /player/252886/kwame-osigwe/200056/
        # is in the form /player/ID/....
        # Extract the ID
        href = player_id_box['href']
        player_ids.append(href.split("/")[2])


def scrape_player_name_country_clubs(html, player_names, country_img_links, club_img_links):
    """
    Scrapes player names, country and club logo links(almost 60) on one HTML page
    :param html: Parsed HTML page with all tags intact
    :param player_names: list to store player's names while scraping
    :param country_img_links: list to store links of country's flag of players while scraping
    :param club_img_links: list to store links of club logos of players while scraping
    :return: None(player_names,country_img_links,club_img_links will contain the scraped output)
    """
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
                #print("found one with no figure tag but only a tag")
                club_img_links.append(np.NaN)
                continue
            elif img_box.figure is None and img_box.img is not None:
                country_img_links.append(
                    img_box.img['data-src'])  # only img_box.img exists. img_box.fig does not exist.
                player_names.append(img_box.text)
        except Exception as e:
            print("Exception during parse of country/club: " + str(e))
            continue


def go_scrape(url):
    """
    Scrapes the page at the given url(with 60 players on it)
    :param url: HTTP address URL of one single HTML page to scrape data from
    :return: list with ids, names and links of player's(images, country flags, club logos) on a single HTML page
    """
    # Without user-agent header, this site return 403 Forbidden
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/79.0.3945.88 Safari/537.37"
    scraping_started = False
    player_img_links = []
    player_ids = []
    player_names = []
    country_img_links = []
    club_img_links = []
    try:
        player_list_page = requests.get(url, headers={'User-Agent': user_agent}) # requesting webpage from the internet
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

        scrape_player_images(player_list_html, player_img_links)
        scrape_player_ids(player_list_html, player_ids)
        scrape_player_name_country_clubs(player_list_html, player_names, country_img_links, club_img_links)
        # print("Number of country images on this page = {}".format(len(country_img_links)))
        # print("Number of players successfully processed on this page = {}".format(len(player_img_links)))
    except Exception as e:
        print("Exception occured: " + str(e))

    return player_ids, player_names, player_img_links, country_img_links, club_img_links
