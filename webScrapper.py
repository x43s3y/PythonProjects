from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import Counter
import time
import os

#BeautifulSoup stuff
DRIVER_PATH = "D:\\TRASHTHINGS\\chromedriver_win32\\chromedriver"
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

nicknameInput = input("Profile name: ")
print("You can type:'pass' if you don`t wanna give pass but you will get the completed animes too :c")
passwordInput = input("Password: ")
ratingInput = float(input("Enter rating (0-10): "))

BASE_URL = "https://myanimelist.net/"
PROFILE_URL = "https://myanimelist.net/animelist/" + nicknameInput + "?status=7"
LOGIN_URL = "https://myanimelist.net/login.php?from=%2Ftopanime.php%3F_location%3Dmal_h_m"
mydir = 'C:\\Users\\sstef\\source\\repos\\PP\\WebScrapping'
myfile = 'Anime.txt'
fixedPath = os.path.join(mydir, myfile)
genresBio = []
valueList = []
filteredBioGenresList = []
rawGenresList = []
i = 0
#LOGIN TO ACC
def loginProfile():
    try:
        driver.get(LOGIN_URL)
        driver.find_element_by_xpath('//*[@id="loginUserName"]').send_keys(nicknameInput)
        driver.find_element_by_xpath('//*[@id="login-password"]').send_keys(passwordInput)
        driver.find_element_by_class_name("inputButton").click()
    except:
        driver.find_element_by_class_name("css-flk0bs").click()
        return loginProfile()
def is_file_empty_3(file_name):
    """ Check if file is empty by reading first character in it"""
    # open file in read mode
    with open(file_name, 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
           return True
    return False
def writingToNotepad(file, every):
    if os.path.isfile(file):
        with open(file, "r+", encoding='utf-8') as f:
        #for every in mainList:
            if type(every) != str:
                every = every.text
            if is_file_empty_3(file):
                    f.write("...")
            else:
                for line in f:
                    pass
                if line == every:
                    pass
                else:
                    f.write("\n" + every)
    else:
        with open(file, "x") as f:
            if type(every) != str:
                every = every.text
            if is_file_empty_3(file):
                    f.write("...")
            else:
                for line in f:
                    pass
                if line == every:
                    pass
                else:
                    f.write("\n" + every)
def stepThroughPages(pageLink, anime):
    driver.get(BASE_URL + "topanime.php" + pageLink)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nextPage = soup.find('a', class_='link-blue-box next')
    if nextPage is None:return anime
    for i in soup.find_all("tr", class_="ranking-list"):
        td_status = i.find("td", class_="status")
        td_score = i.find("td", class_="score ac fs14")
        div_score = td_score.find("div", class_="js-top-ranking-score-col di-ib al")
        statusCompleted = td_status.find("a", class_="Lightbox_AddEdit btn-addEdit-large btn-anime-watch-status js-anime-watch-status completed")
        statusOnHold = td_status.find("a", class_="Lightbox_AddEdit btn-addEdit-large btn-anime-watch-status js-anime-watch-status on-hold")
        statusWatching = td_status.find("a", class_="Lightbox_AddEdit btn-addEdit-large btn-anime-watch-status js-anime-watch-status watching")
        statusDropped = td_status.find("a", class_="Lightbox_AddEdit btn-addEdit-large btn-anime-watch-status js-anime-watch-status dropped")
        statusPlanToWatch = td_status.find("a", class_="Lightbox_AddEdit btn-addEdit-large btn-anime-watch-status js-anime-watch-status plantowatch")
        score = div_score.find("span")
        statusText = td_status.find("a", class_="Lightbox_AddEdit btn-addEdit-large btn-anime-watch-status js-anime-watch-status notinmylist")

        if float(score.text) >= ratingInput:
            if statusText == None:
                pass
            elif statusText.text == "Add to list":
                anime.append(i)
            else:
                continue
            if statusCompleted != None:
                if statusCompleted.text == "Completed":
                    continue
            elif statusWatching != None:
                if statusWatching.text == "Watching":
                    continue
            elif statusOnHold != None:
                if statusOnHold.text == "On-Hold":
                    continue
            elif statusDropped != None:
                if statusDropped.text == "Dropped":
                    continue
            elif statusPlanToWatch != None:
                if statusPlanToWatch.text == "Plan to Watch":
                    continue
        else:
            return anime
        # finally:
        #     return anime
    return stepThroughPages(nextPage['href'], anime)

#GETTING OWN GENRES
driver.get(PROFILE_URL)
soup = BeautifulSoup(driver.page_source, 'html.parser')
profileAnimeLinks = soup.find_all('a', class_="link sort")
for eachAnimeLink in profileAnimeLinks:
    hrefPart = eachAnimeLink['href']
    driver.get(BASE_URL + "/" + hrefPart)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rawGenresList.extend(soup.find_all('span', itemprop="genre"))
for genre in rawGenresList:
    genresBio.append(genre.text)
for allValues in Counter(genresBio).items():
    genre, value = allValues
    valueList.append(value)
    if value >= sum(valueList)/len(valueList):
        filteredBioGenresList.append(genre)

loginProfile()
scoreLinks = stepThroughPages("?limit=0", [])
#WRITING TO MAIN FILE
for scoreLink in scoreLinks:
    name = scoreLink.find("a", class_="hoverinfo_trigger")
    driver.get(name['href'])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    genresAnime = soup.find_all('span', itemprop='genre')
    for genres in genresAnime:
        if genres.text in filteredBioGenresList:
            i+=1
        if i >=len(filteredBioGenresList)/2:
            nameAnime = soup.find("h1", class_="title-name")
            writingToNotepad(fixedPath, nameAnime)
        else:
            continue