# Multi-threaded implementation of FIFA website scraper

from fifascraper import go_scrape
from helper import *
import concurrent.futures
from time import time


def worker_scraper(url):
    print("Processing page at " + url)
    return go_scrape(url)


def main():
    # After running some experiments, this seems to be the best value for maximum efficiency
    NUMBER_THREADS = 20
    player_ids = []
    player_names = []
    player_img_links = []
    country_img_links = []
    club_img_links = []
    print("Starting to scrape!!!")
    sofifa_urls = ["https://sofifa.com/players?offset=" + str(offset) for offset in range(0, 20000, 60)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_THREADS) as executor:
        # submit() returns a Future instance, which encapsulates the asynchronous execution of a callable
        futures = [executor.submit(worker_scraper, url) for url in sofifa_urls]
        for future in futures:
            (ids, names, p_links, c_links, cl_links) = future.result() # blocks until a result is returned
            player_ids.extend(ids)
            player_names.extend(names)
            player_img_links.extend(p_links)
            country_img_links.extend(c_links)
            club_img_links.extend(cl_links)

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


if __name__ == '__main__':
    ts = time()
    main()
    print("Took {} secs to complete".format(time() - ts))