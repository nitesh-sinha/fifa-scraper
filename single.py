from fifascraper import go_scrape
import pandas as pd


def create_dataframe(ids, names, p_links, c_links, cl_links):
    try:
        dict = {'ID':ids, 'Name': names, 'Photo':p_links, 'Flag':c_links, 'Club Logo':cl_links}
        df = pd.DataFrame(dict)
        df.to_csv("working-links.csv")
    except Exception as e:
        print("Exception creating or storing the dataframe: " + str(e))


if __name__ == "__main__":
    print("Starting to scrape!!!")
    (ids, names, p_links, c_links, cl_links) = go_scrape()
    create_dataframe(ids, names, p_links, c_links, cl_links)







