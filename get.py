import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By



def get_item(input_dizi_adi):
    def check_class_exists(item, class_name):
        try:
            item.find_element(By.CLASS_NAME, class_name)
            return True
        except NoSuchElementException:
            return False


    website_search_link = f"https://www.imdb.com/find/?q={input_dizi_adi}&ref_=nv_sr_sm"
    driver = webdriver.Chrome()
    wait_seconds = 5

    driver.get(website_search_link)
    driver.implicitly_wait(wait_seconds)

    elements = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item__t')

    class_exists = check_class_exists(driver, 'ipc-metadata-list-summary-item__t')
    if not class_exists:
        print(f"/nDizi yok kardeşim/n")
        driver.quit()
        exit()

    text_list_search = [element.get_attribute('href') for element in elements]

    link = text_list_search[0]
    link = link.replace("https://www.imdb.com/title/", "").replace("/?ref_=fn_al_tt_1", "")
    website_link = f"https://www.imdb.com/title/{link}/episodes/?"

    driver.get(website_link)
    driver.implicitly_wait(wait_seconds)

    # Dizi adını sayfadan al
    dizi_adi_element = driver.find_element(By.XPATH,'//*[@id="__next"]/main/div/section/section/div[3]/section/section/div[2]/hgroup/h2')

    dizi_adi = dizi_adi_element.text

    print(f"Dizi Adı: {dizi_adi}")

    def get_results(page_count):
        items = driver.find_elements(By.CLASS_NAME, 'episode-item-wrapper')

        season_data = []
    
        for item in items:
            rating_texts = []

            
            class_exists = check_class_exists(item, 'ipc-rating-star--rating')

            if not class_exists:
                print(f"\n{page_count}. Sezon bölümleri puanlanmamış\n")
                return season_data

            rating = item.find_elements(By.CLASS_NAME, 'ipc-rating-star--rating')


            for title_ in rating:
              rating_texts.append(title_.text)
            
            season_data += rating_texts
            
        
    
        return season_data

    elements = driver.find_elements(By.CSS_SELECTOR, '.ipc-tab.ipc-tab-link.ipc-tab--on-base')
    text_list = [element.text for element in elements]
    total_results_count = int(text_list[-1])

    all_season_data = []

    for i in range(1, total_results_count + 1):
        driver.get(f"{website_link}season={i}")
        driver.implicitly_wait(wait_seconds)
        season_data = get_results(i)
        if len(season_data) > 0:
            all_season_data.append(season_data)
        
      

    driver.get(f"https://www.imdb.com/title/{link}")
    driver.implicitly_wait(wait_seconds)

    img_element = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div[1]/div/div[1]/img')
    dizi_puan_element = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]')
    dizi_puan = dizi_puan_element.text
    imdb_puani = " ⭐ " + dizi_puan + "/10"
    img_link = img_element.get_attribute('src')
    #print(f"Dizi Data: {all_season_data}")
    #print(f"Resim Linki: {img_link}")
    driver.quit()
    all_all_season_data = [all_season_data, img_link,dizi_adi,imdb_puani]
    print(all_all_season_data)
    return all_all_season_data


