# Multi-threaded implementation of FIFA website scraper
from fifascraper import go_scrape
from helper import *
import concurrent.futures
from time import time
from tqdm import tqdm


def worker_scraper(url):
    """
    Function executed by every worker thread in the thread pool
    :param url: HTTP URL address currently being worked on by the worker thread
    :return: All the scraped data of FIFA players(on one single HTML page pointed to by url)
    """
    # print("Processing page at " + url)
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
    sofifa_urls = ["https://sofifa.com/players?offset=" + str(offset) for offset in range(0, 300, 60)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_THREADS) as executor:
        # submit() returns a Future instance, which encapsulates the asynchronous execution of a callable
        futures = [executor.submit(worker_scraper, url) for url in sofifa_urls]
        for future in tqdm(futures):
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
        df.to_csv("working-links-multi-thread.csv")
        return df.shape[0]
    except Exception as e:
        print("Exception during dataframe creation: " + str(e))


if __name__ == '__main__':
    ts = time()
    num_rows = main()
    print("Took {} secs to scrape {} players".format(time() - ts, num_rows))