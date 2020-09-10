# Single threaded implementation of FIFA website scraper
from fifascraper import go_scrape
from helper import *
from time import time


def main():
    player_ids = []
    player_names = []
    player_img_links = []
    country_img_links = []
    club_img_links = []
    print("Starting to scrape!!!")
    sofifa_urls = ["https://sofifa.com/players?offset=" + str(offset) for offset in range(0, 20000, 60)]
    for url in sofifa_urls:
        print("Processing page at " + url)
        try:
            (ids, names, p_links, c_links, cl_links) = go_scrape(url)
            player_ids.extend(ids)
            player_names.extend(names)
            player_img_links.extend(p_links)
            country_img_links.extend(c_links)
            club_img_links.extend(cl_links)
        except Exception as e:
            print("Exception during scrape: " + str(e))
            continue

    display_scraped_data(player_ids, player_names, player_img_links, country_img_links, club_img_links)

    try:
        # All pages scraped successfully. Now create a dataframe with scraped data
        df = create_dataframe(player_ids, player_names, player_img_links,
                              country_img_links, club_img_links)
        print("Dataframe created successfully")
        print(df)
        df.to_csv("working-links.csv")
    except Exception as e:
        print("Exception during dataframe creation: " + str(e))


if __name__ == "__main__":
    ts = time()
    main()
    print("Took {} secs to complete".format(time() - ts))
