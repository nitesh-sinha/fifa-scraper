from fifascraper import go_scrape
import pandas as pd


def create_dataframe(ids, names, p_links, c_links, cl_links):
    try:
        dict = {'ID':ids, 'Name': names, 'Photo':p_links, 'Flag':c_links, 'Club Logo':cl_links}
        df = pd.DataFrame(dict)
        df.to_csv("working-links.csv")
        return df
    except Exception as e:
        print("Exception creating or storing the dataframe: " + str(e))


if __name__ == "__main__":
    player_ids = []
    player_names = []
    player_img_links = []
    country_img_links = []
    club_img_links = []
    print("Starting to scrape!!!")
    sofifa_urls = ["https://sofifa.com/players?offset=" + str(offset) for offset in range(420, 600, 60)]
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

    # for (p_id, p_name, p_link, ctry_link, clb_link) in zip(player_ids, player_names, player_img_links,
    #                                                        country_img_links, club_img_links):
    #     print(p_id, p_name, p_link, ctry_link, clb_link, sep="        ")
    print("Finally we have {} IDs, {} player name, {} links of player-images, {} links of countries and {} "
          "links of clubs".format(len(player_ids), len(player_names), len(player_img_links),
                                  len(country_img_links), len(club_img_links)))

    try:
        # All pages scraped successfully. Now create a dataframe with scraped data
        df = create_dataframe(player_ids, player_names, player_img_links,
                         country_img_links, club_img_links)
        print("Dataframe created successfully")
        print(df)
    except Exception as e:
        print("Exception during dataframe creation: " + str(e))
