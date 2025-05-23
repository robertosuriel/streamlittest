########################################################
# This WholeFoods scraper is created by Youssef Sultan
# This Data is utilized for noncommercial use via Whole Foods Market L.P. 
# @ www.wholefoodsmarket.com                  
########################################################
import argparse
import os, sys, time 
from selenium import webdriver
import pandas as pd
from datetime import date
import pickle
import pathlib
import platform
import warnings
from selenium.webdriver.chrome.options import Options
t1 = time.monotonic() # start timer to calculate elapsed time
#########################################################
cwd = os.getcwd() # Current Path
driver_dir = cwd + "\chromedriver.exe" # chrome driver for running script locally
try:
    path = pathlib.Path(__file__).parent / 'chromedriver.exe' # try to pull chrome driver from local
except Exception as e:
    print(e)
    path=driver_dir
#########################################################
warnings.filterwarnings("ignore", category=DeprecationWarning) # ignore selenium 4.x deprecation warnings
#########################################################
try:
    if platform.system()=='Windows':
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-level=3') # when running locally
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(path, options=options) # Chrome Driver Windows Path --if running on windows
    else:                    #if platform is 'Debian/linux'
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')  
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        browser = webdriver.Chrome(options=options) # Chrome Driver Linux Path --if running on linux (Streamlit Debian Deployment)
    browser.get('https://www.wholefoodsmarket.com/products/all-products?featured=on-sale') # Website Link
    print('Checking zipcode...')
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("zipcode")
        args = parser.parse_args()
        zipcode = str(args.zipcode)
        browser.find_element_by_xpath("//input[@id='pie-store-finder-modal-search-field']").send_keys(zipcode) # Zip code
    except:
        browser.find_element_by_xpath("//input[@id='pie-store-finder-modal-search-field']").send_keys(input()) # Zip code
    time.sleep(2.5) # lag for 3 seconds to allow elements to load
    location = ', '.join(browser.find_elements_by_class_name("wfm-search-bar--list_item")[0].text.split(', ')[-2:])
    print('Getting items from the WholeFoods in ' + str(location) + '.')
    browser.find_elements_by_class_name("wfm-search-bar--list_item")[0].click()
except Exception as e:
    print(e)
    print('invalid zipcode')
    sys.exit()
time.sleep(2)
#########################################################
print('Pulling all "on-sale" results from each category...')
#########################################################
browser.get('https://www.wholefoodsmarket.com/products/produce?featured=on-sale') # Website Link
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching produce") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
produce = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/dairy-eggs?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching dairy") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
dairy_eggs = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/meat?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching meat") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
meat = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/prepared-foods?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching prepared foods") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
prepared_foods = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/pantry-essentials?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching pantry essentials") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
pantry_essentials = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/breads-rolls-bakery?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching bread rolls & bakery") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
bread_rolls_bakery = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/desserts?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching desserts") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
desserts = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/body-care?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching body care") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
body_care = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/supplements?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching supplements") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
supplements = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/frozen-foods?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching frozen foods") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
frozen_foods = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/snacks-chips-salsas-dips?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching snacks and chips") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
snacks_chips_salsas_dips = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/seafood?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching seafood") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
seafood = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/beverages?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching beverages") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
Beverages = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/beauty?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching beauty") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
beauty = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/floral?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching floral") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
floral = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split

browser.get('https://www.wholefoodsmarket.com/products/lifestyle?featured=on-sale')
try:
    load = browser.find_element_by_xpath("//span[contains(text(),'Load more')]") 
    while True:
        load.click()
        time.sleep(2.5) # Must have a 2 sec time lag so the 'load more' button can reappear
except:
    print("Fetching lifestyle") # If all possible data is populated
all_items = browser.find_elements_by_xpath("//div[@data-testid='product-tile']") # Pull all product elements by xpath
lifestyle = [items.text.splitlines() for items in all_items] # Create a list comprehension of all product elements with text shown and lines split
#############################################################################
print('There are ' + str(len(lifestyle) + len(produce) + len(dairy_eggs) + len(meat) + len(prepared_foods) + len(pantry_essentials) + len(bread_rolls_bakery) + len(desserts) + len(body_care) + len(supplements) + len(frozen_foods) + len(snacks_chips_salsas_dips) + len(seafood) + len(Beverages) + len(beauty) + len(floral)) + ' products on sale in ' + str(location) + '.')
#############################################################################
list_of_categories = ['lifestyle', 'produce', 'dairy_eggs', 'meat', 'prepared_foods', 'pantry_essentials', 'bread_rolls_bakery', 'desserts', 'body_care', 'supplements', 'frozen_foods', 'snacks_chips_salsas_dips', 'seafood', 'Beverages', 'beauty', 'floral']
d = {"company":[], "product":[], "regular":[], "sale":[], "prime":[], "category":[]} # Create a Dict
#############################################################################
for category in list_of_categories:                                         #
    for i in range(len(globals()[category])):                               # At the range of the length of all items (will loop i times)
            if 'Add to list' in globals()[category][i][-1]:
                d["company"].append(globals()[category][i][-6])                 # Append respective indexed data in list_of_items[i] for each column
                d["product"].append(globals()[category][i][-5])                 # 
                d["regular"].append(globals()[category][i][-4][8:])             #  
                d["sale"].append(globals()[category][i][-3][10:])               # 
                d["prime"].append(globals()[category][i][-2][18:])              #
                d["category"].append(str(category))  
            else:
                d["company"].append(globals()[category][i][-5])                 # Append respective indexed data in list_of_items[i] for each column
                d["product"].append(globals()[category][i][-4])                 # 
                d["regular"].append(globals()[category][i][-3][8:])             #  
                d["sale"].append(globals()[category][i][-2][10:])               # 
                d["prime"].append(globals()[category][i][-1][18:])              #
                d["category"].append(str(category))                             # 
#############################################################################
#############################################################################
if len(d['company']) == len(d['product']) == len(d['regular']) == len(d['sale']) == len(d['category']):  # Verify that the length of each column is == to each other, otherwise the dataframe wont be populated   
    print("All column lengths are equal, there are " + str(len(d['company'])) + " products on sale today.")
else:                                                                       #         
    print("Error, column lengths are not equal.")                           # 
#############################################################################
df = pd.DataFrame.from_dict(d)                                              # Turn our Dict to a Pandas DataFrame  
#############################################################################
browser.close()
#############################################################################
#           Data Cleaning for Products with missing company names           #
#############################################################################
if df['product'].str.contains('Original Vegan Bagels, 15.87 oz').any():                         
    ix = df[df['product'].str.contains('Original Vegan Bagels, 15.87 oz')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains('Original Sandwich Bread, 22.2 oz').any():                         
    ix = df[df['product'].str.contains('Original Sandwich Bread, 22.2 oz')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains('Arctic Char Fillet').any():                         
    ix = df[df['product'].str.contains('Arctic Char Fillet')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Whole Foods Market"

# Data cleaning/shifting for products by Brita
if df['company'].str.contains('/').any() and df['product'].str.contains('Brita').any():
    print('data error check company name containing "/" and "Brita"')

# Data cleaning/shifting for products
if df['product'].str.contains("Easy Peel White Shrimp 8-12 Count").any():
    ix = df[df['product'].str.contains("Easy Peel White Shrimp 8-12 Count")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Whole Foods Market"

if df['product'].str.contains("Organic Freeze Dried Chives, 0.14 oz").any():
    ix = df[df['product'].str.contains("Organic Freeze Dried Chives, 0.14 oz")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Green Garden"

if df['product'].str.contains("Organic Freeze Dried Thyme, 0.26 oz").any():
    ix = df[df['product'].str.contains("Organic Freeze Dried Thyme, 0.26 oz")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Green Garden"

if df['product'].str.contains("Organic Mild Plant Taco Meatless Crumbles").any():
    ix = df[df['product'].str.contains("Organic Mild Plant Taco Meatless Crumbles")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "PLANT BOSS"

if df['product'].str.contains("Organic Multicolor Kale").any():
    ix = df[df['product'].str.contains("Organic Multicolor Kale")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Whole Foods Market"        

# Data cleaning/shifting for products by Soozy's
if df['product'].str.contains("Soozy's Birthday Cake Cookies").any():
    ix = df[df['product'].str.contains("Soozy's Birthday Cake Cookies")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains("Soozys Chocolate Chip Cookies").any():
    ix = df[df['product'].str.contains("Soozys Chocolate Chip Cookies")].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

# Data cleaning/shifting for products by Whole Foods Market
if df['product'].str.contains('Whole Foods Market').any():
    print('data error checking product name containing "whole foods market"')

#---------------Any of these are definitely under the lifestyle category//all waterbottles------#

# Data cleaning/shifting for products by CAMELBAK
if df['product'].str.contains('CAMELBAK').any():
    print('data error, checking product name "CAMELBAK"')

# Data cleaning/shifting for products by NEW WAVE
if df['product'].str.contains('NEW WAVE').any():
    print('data error, checking product name containing "NEW WAVE"')

# Data cleaning/shifting for products by Enviro
if df['product'].str.contains('Enviro').any():
    print('data error, checking product name containing "Enviro"')

# Data cleaning/shifting for products by HYDRO FLASK
if df['product'].str.contains('HYDRO FLASK').any():
    print('data error, checking product name "HYDRO FLASK"')

# Data cleaning/shifting for products by SUNDESA
if df['product'].str.contains('SUNDESA').any():
    print('data error, checking product name "SUNDESA"')

if df['regular'].str.contains('9¢').any():
    ix = df[df['regular'].str.contains('9¢')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'regular'] = '9' + df.loc[ix[i], 'regular']

if df['company'].str.contains('365').any():
    ix = df[df['company'].str.contains('365')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'company'] = 'Whole Foods Market'

if df['product'].str.contains('Chicken Breast Cutlets').any():
    ix = df[df['product'].str.contains('Chicken Breast Cutlets')].index
    for i in range(len(ix)):
        df.loc[ix[i], 'company'] = 'Whole Foods Market'

if df['product'].str.contains('Soozy').any():
    ix = df[df['product'].str.contains('Soozy')].index
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"

if df['product'].str.contains('Superseed Vegan Bread, 22.2 oz').any():
    ix = df[df['product'].str.contains('Superseed Vegan Bread, 22.2 oz')].index 
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Soozy's"     

if df['company'].str.contains('CAVA MEZZE').any():
    ix = df[df['company'].str.contains('CAVA MEZZE')].index 
    for i in range(len(ix)):
        df.loc[ix[i],'company'] = "Cava"

if df['product'].str.contains('Distillery').any():
    ix = df[df['product'].str.contains('Distillery')].index  
    print('Dropped ' + str(len(ix)) + ' Distillery results.')
    df = df.drop(ix)
#############################################################################   
#---------------------------------------------------------------------------#
#                             Data Wrangling                                #
#---------------------------------------------------------------------------# 
#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#@@@#
if df['product'].str.contains('Whole Foods Market').any():                  #----------------------------------------------------------------------------|
    ix = df[df['product'].str.contains('Whole Foods Market')].index         # If the product column contains 'Whole Foods Market' then the item doesn't have a sale price, which shifts the 
    for i in range(len(ix)):                                                # appended information to the left once. Because of this the company category will be shifted as a different text value
        df.loc[ix[i], 'company'] = df.loc[ix[i], 'product']                 # Solution: Apply the text in the 'product' column to the 'company' column |
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@# ------------------------------------------------------------------------|
# Try fix column positioning using solution 1 if the product title exists in position [-3] of the list of the dictionary of each item in each category 
try:                                                                            # ------------------------------------------------------------------------|
    if df['regular'].str.contains('[a-zA-Z]', regex=True).any():               # Furthermore, this means that the other columns containing pricing have shifted values of information
        ix = df[df['regular'].str.contains('[a-zA-Z]', regex=True)].index      # To apply proper values to each column we iterate where 'Prime member deal' exists at position [n][0]
        for i in range(len(ix)):                                                # globals() is used to iterate through our list of categories which points to the actual objects containing the scraped data
            ct = globals()[df.loc[ix[i], 'category']]                           # -----------------------------------------------------------------------|
            df.loc[ix[i], 'company'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'regular'] in ct[n][-3]][0][-4]
            df.loc[ix[i], 'product'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'regular'] in ct[n][-3]][0][-3]
            df.loc[ix[i], 'regular'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'product'] in ct[n][-3]][0][-2].split('$')[1].replace(r'/lb','')
            df.loc[ix[i], 'sale'] = 0                                           # If 'Prime Member Deal' exists in position [n][0] of each category object, that means there is no sale price as it is for prime members only
            df.loc[ix[i], 'prime'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'product'] in ct[n][-3]][0][-1].split('$')[1].replace(r'/lb','')
            print('Some products are only on sale for prime members, wrangling data accordingly...')
except Exception as e:
# if error fix column positioning using solution 2 if the product title exists in position [-4] of the list of the dictionary of each item in each category 
    print(str(e) + " due to online element structure change, wrangling using solution #2")
    try:
        for i in range(len(ix)):                                                # globals() is used to iterate through our list of categories which points to the actual objects containing the scraped data
            ct = globals()[df.loc[ix[i], 'category']]                           # -----------------------------------------------------------------------|
            df.loc[ix[i], 'company'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'regular'] in ct[n][-4]][0][-5]
            df.loc[ix[i], 'product'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'regular'] in ct[n][-4]][0][-4]
            df.loc[ix[i], 'regular'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'product'] in ct[n][-4]][0][-3].split('$')[1].replace(r'/lb','')
            df.loc[ix[i], 'sale'] = 0                                           # If 'Prime Member Deal' exists in position [n][0] of each category object, that means there is no sale price as it is for prime members only
            df.loc[ix[i], 'prime'] = [ct[n] for n in range(len(ct)) if 'Prime Member Deal' in ct[n][0] if df.loc[ix[i], 'product'] in ct[n][-4]][0][-2].split('$')[1].replace(r'/lb','')
    except Exception as e:
        print(e)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#---------------------------------------------------------------------------# 
df['sale'] = df['sale'].str.replace(r'$', '', regex=True)                   # # # # # # # # # # # # # # # 
df['prime'] = df['prime'].str.replace(r'$', '', regex=True)                 # Remove "$" from results   #
df['regular'] = df['regular'].str.replace(r'$', '', regex=True)             # # # # # # # # # # # # # # # 
#---------------------------------------------------------------------------#                           #
df = df.fillna(0)                                                           #      Fill NaN with 0      # 
#---------------------------------------------------------------------------#                           #
if df['regular'].str.contains('/lb').any():                                 # # # # # # # # # # # # # # #  
    ix = df[df['regular'].str.contains('/lb')].index                        # Remove "/lb" from results #
    for i in range(len(ix)):                                                # # # # # # # # # # # # # # # 
        df.loc[ix[i], 'regular'] = df.loc[ix[i], 'regular'].replace(r'/lb','')
if df['sale'].str.contains('/lb').any():                                    #
    ix = df[df['sale'].str.contains('/lb', na=False)].index                 #
    for i in range(len(ix)):                                                #
        df.loc[ix[i], 'sale'] = df.loc[ix[i], 'sale'].replace(r'/lb','')    #
if df['prime'].str.contains('/lb').any():                                   #
    ix = df[df['prime'].str.contains('/lb')].index                          #
    for i in range(len(ix)):                                                #
        df.loc[ix[i], 'prime'] = df.loc[ix[i], 'prime'].replace(r'/lb','')  #
#---------------------------------------------------------------------------#
if df['regular'].str.contains('/ounce').any():                              # # # # # # # # # #
    ix = df[df['regular'].str.contains('/ounce')].index                     # Remove "/ounce" #
    for i in range(len(ix)):                                                # # # # # # # # # # 
        df.loc[ix[i], 'regular'] = df.loc[ix[i], 'regular'].replace(r'/ounce','')
if df['regular'].str.contains('/fluid ounce').any():                        # # # # # # # # # # # # # 
    ix = df[df['regular'].str.contains('/fluid ounce')].index               # Remove "/fluid ounce" #     
    for i in range(len(ix)):                                                # # # # # # # # # # # # #   
        df.loc[ix[i], 'regular'] = df.loc[ix[i], 'regular'].replace(r'/fluid ounce','')
if df['sale'].str.contains('/ounce').any():                                 #    
    ix = df[df['sale'].str.contains('/ounce')].index                        #
    for i in range(len(ix)):                                                #
        df.loc[ix[i], 'sale'] = df.loc[ix[i], 'sale'].replace(r'/ounce','') #
if df['sale'].str.contains('/fluid ounce').any():                           #
    ix = df[df['sale'].str.contains('/fluid ounce')].index                  #
    for i in range(len(ix)):                                                #
        df.loc[ix[i], 'sale'] = df.loc[ix[i], 'sale'].replace(r'/fluid ounce','')
if df['prime'].str.contains('/ounce').any():                                #
    ix = df[df['prime'].str.contains('/ounce')].index                       #
    for i in range(len(ix)):                                                #
        df.loc[ix[i], 'prime'] = df.loc[ix[i], 'prime'].replace(r'/ounce','')
if df['prime'].str.contains('/fluid ounce').any():                          #
    ix = df[df['prime'].str.contains('/fluid ounce')].index                 #
    for i in range(len(ix)):                                                #
        df.loc[ix[i], 'prime'] = df.loc[ix[i], 'prime'].replace(r'/fluid ounce','')
#---------------------------------------------------------------------------#
for i in range(len(df[df['sale'].str.contains('¢', na=False)].index)):      # # # # # # # # # # # # # # #
    ix = df[df['sale'].str.contains('¢', na=False)].index                   # Add '.' to items with '¢' #
    df.loc[ix[i]][3] = '.' + df.loc[ix[i]][3]                               # # # # # # # # # # # # # # #
                                                                            #
for i in range(len(df[df['prime'].str.contains('¢', na=False)].index)):     #
    ix = df[df['prime'].str.contains('¢', na=False)].index                  #
    df.loc[ix[i]][4] = '.' + df.loc[ix[i]][4]                               #
                                                                            #
try:                                                                        #
    for i in range(len(df[df['regular'].str.contains('¢', na=False)].index)):
        ix = df[df['regular'].str.contains('¢', na=False)].index            #
        df.loc[ix[i]][2] = '.' + df.loc[ix[i]][2]                           #
except:                                                                     #
    pass                                                                    #
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
ix = df[df['prime'].str.contains('¢', na=False)].index                      # # # # # # # # # # # # # # #
for i in range(len(ix)):                                                    # Del items with '¢'        #
    df.loc[ix[i]][4] = df.loc[ix[i]][4].replace('¢', '')                    # # # # # # # # # # # # # # #
                                                                            #
ix = df[df['regular'].str.contains('¢', na=False)].index                    #
for i in range(len(ix)):                                                    #
    df.loc[ix[i]][2] = df.loc[ix[i]][2].replace('¢', '')                    #
                                                                            #
ix = df[df['sale'].str.contains('¢', na=False)].index                       #
for i in range(len(ix)):                                                    #
    df.loc[ix[i]][3] = df.loc[ix[i]][3].replace('¢', '')                    #
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------# # # # # # # # # # # # # # #
d = df.to_dict('list')                                                      #     Dataframe ---> Dict   #
#---------------------------------------------------------------------------# # # # # # # # # # # # # # # 
try:                                                                                              #
    for i in range(len(d['sale'])):                                                               # 
        if isinstance(d['sale'][i], str) and 'for' in d['sale'][i].split():                       # 
            d['sale'][i] = float(d['sale'][i].split()[2]) / float(d['sale'][i].split()[0])        # # # # # # # # # # # # # # # # #
                                                                                                  # str '2 for 5' ---> int '2.50' #
    for i in range(len(d['prime'])):                                                              # # # # # # # # # # # # # # # # # 
            if isinstance(d['prime'][i], str) and 'for' in d['prime'][i].split():                 #
                d['prime'][i] = float(d['prime'][i].split()[2]) / float(d['prime'][i].split()[0]) # 
except Exception as e:                                                                            #
    print(e)                                                                                      #
#---------------------------------------------------------------------------------------------# # # # # # # # # # # # # # # 
df = pd.DataFrame.from_dict(d)                                                                #     Dict ---> Dataframe   #
#---------------------------------------------------------------------------------------------# # # # # # # # # # # # # # #    
#-------------------------------------------------------------------------------------------------# # # # # # # # # # # # # # # # # #     
if df['regular'].str.contains('[a-zA-Z]', regex=True).any():                                     # Drop columns that fail to parse #
    ix = df[df['regular'].str.contains('[a-zA-Z]', regex=True)].index                            # # # # # # # # # # # # # # # # # #
    df.drop(ix, inplace=True)                                                                     #              
    print('Dropping ' + str(len(ix)) + ' rows that failed to parse')                              #
#-------------------------------------------------------------------------------------------------#  
df = df.sort_index()                                                                          #
df["regular"] = pd.to_numeric(df["regular"]).round(2)                                         # # # # # # # # # # # # # # # # # # #
df["sale"] = pd.to_numeric(df["sale"]).round(2)                                               # Str ---> float, Feature Creation  #
df["prime"] = pd.to_numeric(df["prime"]).round(2)                                             # # # # # # # # # # # # # # # # # # #
df['sale_discount'] = (1-df['sale']/df['regular']).round(3)                                   # 
df['prime_discount'] = (1-df['prime']/df['regular']).round(3)                                 #
df['prime_sale_difference'] = (df['prime_discount'] - df['sale_discount']).round(3)           # # # # # # # # # # # # # # # # # # # # |------------------------------------|
df['discount_bins'] = pd.cut(df.prime_discount, [0,.10,.20,.30, .40, .50, .9], labels=['0% to 10%','10% to 20%','20% to 30%','30% to 40%','40% to 50%','50% or more'])    #|Discount Bins I.E. 0% Off to 10% off|
df = df.sort_values(by='prime_discount', ascending=False)                                     # # # # # # # # # # # # # # # # # # # # |------------------------------------|
df['prime_sale_difference'] = df['prime_sale_difference'].clip(lower=0)                       # sets prime_sale_difference as 0 if lower than 0 to fix distribution 
#---------------------------------------------------------------------------------------------# This occurs if items are on sale for prime members only

# Paths to dump location of Wholefoods and Cleaned DataFrame as .pkl files
# pkl files are dumped with protocol 4 for deployment purposes as streamlit is not compatible with the highest protocol (5) of serialization

#--------------------------------------------#
try:                                         #
  MY_DIR = pathlib.Path(__file__).parent     #
except NameError:                            #
  MY_DIR = pathlib.Path(os.getcwd()) # if not running as .py the directory is hardcoded locally
#--------------------------------------------# 
filename = "WF_Sales_" + str(date.today().strftime("%b_%d_%Y")) + '_' + str('_'.join(location.split()).replace(',','')) + ".pkl"
path = MY_DIR / 'scraped products dump' / filename
locpath = MY_DIR / 'scraped products dump' / 'location' / filename
#--------------DUMPS-------------------------#
with open(path, 'wb') as handle:             #                           
    pickle.dump(df, handle, protocol=4)      # Both .pkl files are saved as the same name however the location info of the store is under the location folder
with open(locpath, 'wb') as handle:          # The Dataframe file is in the 'scraped products dump' folder
    pickle.dump(location, handle, protocol=4)#
    print("Products saved as WF_Sales_" + str(date.today().strftime("%b_%d_%Y")) + '_' + str('_'.join(location.split()).replace(',','')) + ".pkl")
#--------------------------------------------#
t2 = time.monotonic() # end time
elapsed = t2 - t1
print('Elapsed time is %f seconds.' % elapsed)
