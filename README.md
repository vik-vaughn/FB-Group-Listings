# FB Group Listing Scraper

A Facebook group scraper that collects information from formatted listings in any public Facebook group. Built with **Python** and **Scrapy**.

## Setup

We start off by installing the prerequisites, which can be found in the **_results.txt_** file. To do this, first enter the main folder in your command prompt: `cd C:\Users\yourusername\Downloads\fb-project-final\listings`.

Install the prerequisites with `pip install -r requirements.txt`.

The script exports the results to an **_Excel_** file as well as a local database by default. To configure the database, navigate to **_listings\listings\pipelines.py_** and edit the required fields (as shown in the example).

![Setting up the database](https://i.imgur.com/hTCayTI.png)

Finally, copy the links to your desired groups and paste them into the **_groups.txt_** file in the main folder (two are provided by default - add or remove them as needed)

The tool can scrape **listings**, but not generic posts. The proper format is shown below.

![Proper post format](https://i.imgur.com/GS4ZD0o.png)

## Running the script

To run the script, simply use `scrapy crawl groups` in your command prompt. A Google Chrome driver will be downloaded, and a browser will now open. Accept the cookies if a window pops up and you're done! By default, the command will perform **two** scrolls (can be adjusted by using `scrapy crawl groups -a scroll=Number` instead of the default command) in each of your chosen groups and collect the loaded listings.

After the script finishes, you can see the amount of scraped posts in the command prompt (as shown below).

![Amount of scraped posts](https://i.imgur.com/4jwShte.png)

To view the results, open the **_listings_** table in your Postgres GUI tool, or open the **_output-listings.xlsx_** file, which can be found in the **_results_** directory. Both options are shown below.

![Results in a local database](https://i.imgur.com/EwkA8vI.png)

![Results in an Excel sheet](https://i.imgur.com/FaC5vCc.png)

## Features

* The script scrapes the following information: the **_name_** of the author; the **_title_** of the listing; its **_price_** and **_description_**; the **_date_** that the post was made; the **_path_** to the **_HTML_** file and the **_URL_** of the listing itself.
* The whole **_HTML_** file is scraped along with the relevant information, you can find it in your **_results_** folder (the location is also specified in the database/excel sheet).
* Running the script again will populate the same database/excel sheet with new listings, this is done by storing the **_post ID_** in the **_listings_done.txt_** file and skipping listings that match any of the ID's already stored there.
* Specify the amount of scrolls to be done in each group by using `scrapy crawl groups -a scroll=Number` instead of the default command (more scrolls = more scraped listings).
* The script automatically formats the date of the listing (relevant if you're scraping older posts).

## Troubleshooting & known issues

### Troubleshooting:

* If you encounter issues while installing the requirements - first, remove the specific version requirements from the **_requirements.txt_** (leave just the names). If that doesn't work, try downgrading to an older **_Python_** version (Python 3.9 has been tested and confirmed as working, while 3.11 has issues).
* If you encounter issues while running the script - check to see if the post format is correct. The script will not scrape generic listings (listings with *just* text and photos).

### Known issues:

* Some of the fields in the results database/excel sheet can be blank after running the script, this is because Facebook changes the class names in an effort to prevent scraping. This can be avoided by using the whole **_XPATH_**, but it doesn't always work, since the listings can have varying structures/tag layouts (which also changes the location of the text/XPATH). You can fix this by updating the class names every few days/whenever you encounter an issue.
* After multiple days of usage, it's not uncommon to see a *please log in to view this page* popup. There's not much to be done here, since free proxies are automatically detected by Facebook, and using a VPN will lead to a login window. A login function *could* be implemented, but this would require you to post dummy posts/add friends/ etc. for up to a week, at which point your account can still get banned from extensive scraping. Easiest way to avoid this is to only scrape every few days, or relaunching the script until you don't get the popup.
* If the same person decides to post a listing to multiple groups, it will have different ID's, which will lead to it still being scraped (despite having the same information).
* The cached **_HTML_** file which is downloaded only lets you see the first photo.
