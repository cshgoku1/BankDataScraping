from bankDataWebscraping import BankingWebdataScrapper
from datetime import datetime
import os

# create data folder 
os.makedirs("data", exist_ok=True)

# get today's date
timestamp = datetime.now().strftime("%Y-%m-%d")

# perform webscraping
scraper = BankingWebdataScrapper()
scraper.savingsAccountRates()
scraper.cdRates()
scraper.checkingAccountRates()
scraper.moneyMarketRates()

# Save saving/cd/checking/moneymarket rate to csv files
scraper.savingRatedf.to_csv(f"data/savings_{timestamp}.csv", index=False)
scraper.cdRatedf.to_csv(f"data/cd_{timestamp}.csv", index=False)
scraper.checkingRatedf.to_csv(f"data/checking_{timestamp}.csv", index=False)
scraper.moneyMarketRatedf.to_csv(f"data/mm_{timestamp}.csv", index=False)

print(f"Banking data saved successfully on {timestamp}")
