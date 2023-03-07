from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

driver = webdriver.Chrome('usr/local/bin/chromedriver')
driver.implicitly_wait(15)
driver.maximize_window()

# Prepare the system
url_ee = "https://www.finnomena.com/stock/EE"
driver.get(url_ee)
print(driver.title)

# Wait for input on terminal to start scraping
input('Press Enter to start scraping')

# Functions to scrape data from website
def get_index_table_1(Quarter):
    try:
        INDEX_TABLE_1_XPATH = '//*[@id="stock-financial-ratio"]/div/div/div/div/div[2]/div[2]/div/div[1]/div[@class="year"]'
        index_table_1_elements = driver.find_elements(By.XPATH, INDEX_TABLE_1_XPATH)
        # Convert the elements into list of text
        index_table_1_list = [element.text for element in index_table_1_elements]
        quater_index = index_table_1_list.index(Quarter)
        return quater_index
    except:
        return -1

def get_index_table_2(Quarter):
    try:
        INDEX_TABLE_2_XPATH = '//*[@id="stock-statistics"]/div/div/div/div/div[2]/div[2]/div/div[1]/div[@class="year"]'
        index_table_2_elements = driver.find_elements(By.XPATH, INDEX_TABLE_2_XPATH)
        # Convert the elements into list of text
        index_table_2_list = [element.text for element in index_table_2_elements]
        quater_index = index_table_2_list.index(Quarter)
        return quater_index
    except:
        return -1

def is_40Quarter():
    try:
        Q_XPATH = '//*[@id="stock-financial-ratio"]/div/div/div/div/div[2]/div[2]/div/div[1]/div[@class="year"]'
        q_elements = driver.find_elements(By.XPATH, Q_XPATH)
        # Convert the elements into list of text
        q_list = [element.text for element in q_elements]
        # Check if Q3 is in the list
        if len(q_list) == 41:
            return True
        else:
            return False
    except:
        return False

def get_roa(Q_index):
    try:
        ROA_XPATH = '//*[@id="stock-financial-ratio"]/div/div/div/div/div[2]/div[2]/div/div[2]/div[@class="data-each"]'
        roa_elements = driver.find_elements(By.XPATH, ROA_XPATH)
        # Convert the elements into list of text
        roa_list = [element.text for element in roa_elements]
        roa_value = roa_list[Q_index]
        return roa_value
    except:
        return ""

def get_roe(Q_index):
    try:
        ROE_XPATH = '//*[@id="stock-financial-ratio"]/div/div/div/div/div[2]/div[2]/div/div[3]/div[@class="data-each"]'
        roe_elements = driver.find_elements(By.XPATH, ROE_XPATH)
        # Convert the elements into list of text
        roe_list = [element.text for element in roe_elements]
        roe_value = roe_list[Q_index]
        return roe_value
    except:
        return ""

def get_profit_ratio(Q_index):
    try:
        PROFIT_RATIO_XPATH = '//*[@id="stock-financial-ratio"]/div/div/div/div/div[2]/div[2]/div/div[6]/div[@class="data-each"]'
        profit_ratio_elements = driver.find_elements(By.XPATH, PROFIT_RATIO_XPATH)
        # Convert the elements into list of text
        profit_ratio_list = [element.text for element in profit_ratio_elements]
        profit_ratio_value = profit_ratio_list[Q_index]
        return profit_ratio_value
    except:
        return ""

def get_pe(Q_index):
    try:
        PE_XPATH = '//*[@id="stock-statistics"]/div/div/div/div/div[2]/div[2]/div/div[4]/div[@class="data-each"]'
        pe_elements = driver.find_elements(By.XPATH, PE_XPATH)
        # Convert the elements into list of text
        pe_list = [element.text for element in pe_elements]
        pe_value = pe_list[Q_index]
        return pe_value
    except:
        return ""

def get_pbv(Q_index):
    try:
        PBV_XPATH = '//*[@id="stock-statistics"]/div/div/div/div/div[2]/div[2]/div/div[5]/div[@class="data-each"]'
        pbv_elements = driver.find_elements(By.XPATH, PBV_XPATH)
        # Convert the elements into list of text
        pbv_list = [element.text for element in pbv_elements]
        pbv_value = pbv_list[Q_index]
        return pbv_value
    except:
        return ""

def get_div_yield(Q_index):
    try:
        DIV_YIELD_XPATH = '//*[@id="stock-statistics"]/div/div/div/div/div[2]/div[2]/div/div[7]/div[@class="data-each"]'
        div_yield_elements = driver.find_elements(By.XPATH, DIV_YIELD_XPATH)
        # Convert the elements into list of text
        div_yield_list = [element.text for element in div_yield_elements]
        div_yield_value = div_yield_list[Q_index]
        return div_yield_value
    except:
        return ""

old_stock_path = "/Users/sarmkunatham/Desktop/GithubCodes/WebScraping/finnomena - 2555-2565.csv"
old_stock_df = pd.read_csv(old_stock_path, header=1)
new_stock_df = old_stock_df[["รายชื่อหุ้น", "Line"]]

print(new_stock_df.head())

missing_value_df = pd.DataFrame(columns=["รายชื่อหุ้น", "Line"])
quarter = "4Q2565"
start_row = int(input("Start Row: "))
end_row = int(input("End Row: "))

for index, row in tqdm(new_stock_df[start_row: end_row].iterrows(), total=new_stock_df[start_row: end_row].shape[0]):
    stock_url = row["Line"]
    # Navigate to the stock page
    driver.get(stock_url)
    
    # Get the index of the quarter from two tables
    table1_index = get_index_table_1(quarter)
    table2_index = get_index_table_2(quarter)

    # Check if Quarter 3 2565 exist
    if not (table1_index == -1 or table2_index == -1):
        roa_value = get_roa(table1_index)
        roe_value = get_roe(table1_index)
        profit_ratio_value = get_profit_ratio(table1_index)
        pe_value = get_pe(table2_index)
        pbv_value = get_pbv(table2_index)
        div_yield_value = get_div_yield(table2_index)

    else:
        
        missing_value_df.loc[index, "รายชื่อหุ้น"] = row["รายชื่อหุ้น"]
        missing_value_df.loc[index, "Line"] = row["Line"]
        missing_value_df.loc[index, quarter] = f"No {quarter}"
        roa_value = ""
        roe_value = ""
        profit_ratio_value = ""
        pe_value = ""
        pbv_value = ""
        div_yield_value = ""
        
    new_stock_df.loc[index, "ROA%"] = roa_value
    new_stock_df.loc[index, "ROE%"] = roe_value
    new_stock_df.loc[index, "อัตรากำไรสุทธิ%"] = profit_ratio_value
    new_stock_df.loc[index, "P/E"] = pe_value
    new_stock_df.loc[index, "P/BV"] = pbv_value
    new_stock_df.loc[index, "อัตราปันผล%"] = div_yield_value


new_stock_df.to_csv(f'Finnomena_Stock_{quarter}_{start_row}-{end_row}.csv', index=False)
missing_value_df.to_csv(f'MissValue_Finnomena_{quarter}_{start_row}-{end_row}.csv', index=True)
print('Finish Scraping !!!')
print('Missing Value: ', missing_value_df.shape[0])


try:
    missing_value_df_1 = pd.read_csv(f"/Users/sarmkunatham/Desktop/GithubCodes/WebScraping/MissValue_Finnomena_{quarter}_0-200.csv", index_col=0)
    missing_value_df_2 = pd.read_csv(f"/Users/sarmkunatham/Desktop/GithubCodes/WebScraping/MissValue_Finnomena_{quarter}_200-400.csv", index_col=0)
    missing_value_df_3 = pd.read_csv(f"/Users/sarmkunatham/Desktop/GithubCodes/WebScraping/MissValue_Finnomena_{quarter}_400-854.csv", index_col=0)

    # Concatenate the three dataframes
    merge_missing_value_df = pd.concat([missing_value_df_1, missing_value_df_2, missing_value_df_3])
    print(merge_missing_value_df.head())

    merge_missing_value_df.to_csv(f"Extra_MissValue_Finnomena_{quarter}.csv", index=True)

except:
    print("The file is not ready")

print("Finish")

# Close the driver
driver.close()
    
