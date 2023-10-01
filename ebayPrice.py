from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

LINK = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=galaxy+fold+4&_sacat=0&LH_TitleDesc=0&_odkw=airpods+1st+generation&_osacat=0"


def get_prices_by_link(link):
    # get source
    r = requests.get(link)
    # parse source
    page_parse = BeautifulSoup(r.text, 'html.parser')
    #print(page_parse)

    # find all list items from search results
    search_results = page_parse.find("ul",{"class":"srp-results"}).find_all("li",{"class":"s-item"})
    print(search_results[0:12])
    item_prices = []

    for result in search_results:
        price_as_text = result.find("span",{"class":"s-item__price"}).text 
        if "to" in price_as_text:
            continue
        # taking out commas from numbers over 1000 and starting at index 1 to avoid $
        price = float(price_as_text[1:].replace(",",""))
        item_prices.append(price)
    return item_prices

def get_average(prices):
    return np.mean(prices)

def remove_outliers(prices, m=2):
    data = np.array(prices)
    print(data[abs(data - np.mean(data)) < m * np.std(data)])
    return data[abs(data - np.mean(data)) < m * np.std(data)]

def save_to_file(prices, item):
    realPrices = remove_outliers(prices)
    avgPrice = get_average(realPrices)
    fullInfo = [datetime.today().strftime("%B-%D-%Y"), item, realPrices, "Average Price: " + str(avgPrice)]
    with open('ebayPrice.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fullInfo)
    return prices

priceList = get_prices_by_link(LINK)
priceAvg = get_average(priceList)
print(priceList)
print("Average: ", priceAvg)
print("removing outliers: ", remove_outliers(priceList))
save_to_file(priceList, "galaxy fold 4")
print("CSV file updated.")