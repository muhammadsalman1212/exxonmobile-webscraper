import os
import pandas as pd
from playwright.async_api import async_playwright
import asyncio



user_data_dir = "userDir"

# Create the directory if it does not exist
if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)



async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(headless=False, user_data_dir=user_data_dir)
        page = await browser.new_page()

        await page.goto("https://corporate.exxonmobil.com/news", timeout=0)

        await page.click('//button[@aria-label="Load More"]', timeout=0)
        await page.wait_for_timeout(8000)

        link_and_text_elements = await page.query_selector_all(
            '//div[@class="contentCollection--content"]//a[@class="link-black lite"]')
        date_elements = await page.query_selector_all('//div[@class="article--info__bottom"]//span[@class="date"]')

        # Collect data
        data = []
        for all_text_and_link, all_dates in zip(link_and_text_elements, date_elements):
            href = await all_text_and_link.get_attribute('href')
            text = await all_text_and_link.inner_text()
            href = f"https://corporate.exxonmobil.com{href}"
            date = await all_dates.inner_text()

            data.append({
                'Date': date,
                'Header': text,
                'Link': href
            })

            print(f"Date: {date}, Header: {text}, Link: {href}")

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Save to CSV (overwriting the file each time)
        df.to_csv('exxonmobile.csv', index=False)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())



