import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_with_selenium():
    url = "https://www.mintscan.io/dydx/address/dydx1qky3h294ewewk3ry7t2849lk47y380srxyawau"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    data = {}
    try:
        # Wallet
        wallet_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div:nth-of-type(3) div.title"))
        )
        data["Wallet"] = wallet_elem.text
        
        # Total Equity
        total_equity_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-mono][data-h='2']"))
        )
        data["Total Equity"] = total_equity_elem.text
        
        # Total Size
        total_size_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".svelte-1jj3k7x div:nth-of-type(3) div[data-mono]"))
        )
        data["Total Size"] = total_size_elem.text
        
        # Symbol
        symbol_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".svelte-3ohtpx div.text.svelte-10wjg4h"))
        )
        data["Symbol"] = symbol_elem.text
        
        # Size
        size_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-type='number-with-sub-text'] div[data-mono][data-h='6']"))
        )
        data["Size"] = size_elem.text
        
        # Entry Price
        entry_price_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".svelte-3ohtpx div.cell:nth-of-type(2) div[data-mono]"))
        )
        data["Entry Price"] = entry_price_elem.text

        # Realized PNL
        realized_pnl_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "#content-root > div:nth-child(3) > div > div > div.--contents.svelte-7sr7w9 > section > div > div:nth-child(3) > div > div > div > div.root.svelte-1j03fzy > div.root.svelte-7sr7w9 > div.--contents.svelte-7sr7w9 > div > div > div.props-fill.svelte-ugxps7 > div.items > div > div > div:nth-child(4) > div > div"
            ))
        )
        data["Realized PNL"] = realized_pnl_elem.text

        # Unrealized PNL
        unrealized_pnl_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".svelte-3ohtpx div:nth-of-type(5) .prop div[data-mono]"))
        )
        data["Unrealized PNL"] = unrealized_pnl_elem.text
        
        # Net Funding
        net_funding_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".svelte-3ohtpx div:nth-of-type(6) div[data-mono]"))
        )
        data["Net Funding"] = net_funding_elem.text
        
    except Exception as e:
        st.error(f"Error during Selenium scraping: {e}")
    finally:
        driver.quit()
    
    return data

st.title("Mintscan DYDX Address Scraper")

if st.button("Scrape Data"):
    with st.spinner("Scraping data..."):
        scraped_data = scrape_with_selenium()
        if scraped_data:
            st.success("Scraping complete!")
            st.write(scraped_data)
        else:
            st.error("No data scraped. Check the selectors or page structure.")
