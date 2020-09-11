import pandas as pd


def display_scraped_data(ids, names, p_links, c_links, cl_links):
    """
    Helper function to display the list of data scraped from the FIFA website
    :param ids: IDs of players from all scraped pages
    :param names: Names of players from all scraped pages
    :param p_links: Links of players images from all scraped pages
    :param c_links: Links of players country flags from all scraped pages
    :param cl_links: Links of players club logos from all scraped pages
    :return: None
    """
    # for (p_id, p_name, p_link, ctry_link, clb_link) in zip(ids, names, p_links,
    #                                                        c_links, cl_links):
    #     print(p_id, p_name, p_link, ctry_link, clb_link, sep="        ")
    print("Finally we have {} IDs, {} player name, {} links of player-images, {} links of countries and {} "
          "links of clubs".format(len(ids), len(names), len(p_links),
                                  len(c_links), len(cl_links)))


def create_dataframe(ids, names, p_links, c_links, cl_links):
    """
    Creates a Pandas dataframe from the scraped data
    :param ids: IDs of players from all scraped pages
    :param names: Names of players from all scraped pages
    :param p_links: Links of players images from all scraped pages
    :param c_links: Links of players country flags from all scraped pages
    :param cl_links: Links of players club logos from all scraped pages
    :return: None
    """
    try:
        dict = {'ID':ids, 'Name': names, 'Photo':p_links, 'Flag':c_links, 'Club Logo':cl_links}
        df = pd.DataFrame(dict)
        return df
    except Exception as e:
        print("Exception creating or storing the dataframe: " + str(e))