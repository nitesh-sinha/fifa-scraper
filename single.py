# Single threaded implementation of FIFA website scraper
from fifascraper import go_scrape
from helper import *
from time import time
from tqdm import tqdm


def main():
    player_ids = []
    player_names = []
    player_img_links = []
    country_img_links = []
    club_img_links = []
    print("Starting to scrape!!!")
    sofifa_urls = ["https://sofifa.com/players?offset=" + str(offset) for offset in range(0, 500, 60)]
    for url in tqdm(sofifa_urls):
        #print("Processing page at " + url)
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
        df.to_csv("working-links-single-thread.csv")
        return df.shape[0]
    except Exception as e:
        print("Exception during dataframe creation: " + str(e))


if __name__ == "__main__":
    ts = time()
    num_rows = main()
    print("Took {} secs to scrape {} players".format(time() - ts, num_rows))
