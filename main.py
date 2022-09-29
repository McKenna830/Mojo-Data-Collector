from Mojo import MojoData

CHROME_DRIVER_PATH = ""  # insert Chromedriver location
TOTAL_ENTRIES = 0  # insert total number of entries in data set as integer

pages_to_scrape = int(TOTAL_ENTRIES / 100)
bot = MojoData(CHROME_DRIVER_PATH)
bot.login()
bot.find_scrape_list()

for pages in range(0, pages_to_scrape):
    bot.find_names()
    bot.find_addresses()
    bot.find_numbers()
    bot.find_emails()
    bot.next_page()

bot.compile_mojo_data()
