import datetime
import os, random, sys, time
from django.conf import settings
import win32clipboard
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Publication.models import Linkedin_Account, Linkedin_Profile_Info

delay = 30
aujourdhui = datetime.date.today()

############################################################################################################################
#API Connection

#Se connecter au compte Linkedin
def connection_compte(compte):
    #La fenetre ne se ferme pas quand c'est finis + mettre la fenetre en grand
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")

    #Récupère le chemin du driver et le compte sur lequel se connecter
    browser = webdriver.Chrome(r"C:\Users\boulm\Python_file\linkedin_publication\src\linkedin_api\Linkedin_automation\chromedriver99.exe", chrome_options=chrome_options) # type: ignore
    browser.get("https://www.linkedin.com/uas/login")
    browser.find_element_by_id('username')

    username = compte.linkedin_account
    password = compte.linkedin_password
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

    return browser

def get_chromedriver(compte, use_proxy=False, user_agent=None):
    PROXY_HOST = compte.proxy_host  # rotating proxy or host
    PROXY_PORT = compte.proxy_port # port
    PROXY_USER = compte.proxy_user # username
    PROXY_PASS = compte.proxy_pass # password


    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--start-maximized")
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(r'C:\Users\boulm\Python_file\linkedin_publication\src\linkedin_api\Linkedin_automation\chromedriver99.exe',
        chrome_options=chrome_options)
    return driver

def connexion_proxy(compte):
    driver = get_chromedriver(compte, use_proxy=True)
    driver.get("https://www.linkedin.com/uas/login")
    driver.find_element_by_id('username')

    username = compte.linkedin_account
    password = compte.linkedin_password
    elementID = driver.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = driver.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()

    return driver


############################################################################################################################
#API POUR MESSAGE AUTO

#Trouver et cliquer sur le bouton 'Envoyer une note'
def click_ajouter_note(browser):
    soup2 = BeautifulSoup(browser.page_source, "html.parser")
    action_bar = soup2.find('div', {'class': 'artdeco-modal__actionbar'})
    all_button = action_bar.find_all('button') # type: ignore
    for note_button in all_button:
        note_button2 = note_button.find('span').text.strip()
        if note_button2 == "Ajouter une note":
            id_button_note = note_button['id']
            browser.find_element_by_id(id_button_note).click()
            return

#Ecrire le message
def ecrire_message(browser, message):
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'custom-message')))
    custom_message = browser.find_element_by_id("custom-message")
    custom_message.send_keys(message)
    time.sleep(2)
    return

#Envoi du message
def envoi_message(browser):
    soup3 = BeautifulSoup(browser.page_source, "html.parser")
    action_bar = soup3.find('div', {'class': 'artdeco-modal__actionbar'})
    all_button = action_bar.find_all('button') # type: ignore
    for envoyer_button in all_button:
        envoyer_button2 = envoyer_button.find('span').text.strip()

        if envoyer_button2 == "Envoyer":
            id_envoyer = envoyer_button['id']
            browser.find_element_by_id(id_envoyer).click()
            return

#Sauvegarde BDD erreur
def error_bdd(profil):
    profil.error = True
    profil.save()
    return

#Sauvegarde BDD success
def sauvegarde_BDD(profil, associated_account):
    profil.last_message = aujourdhui
    profil.message_sent = True
    profil.error = False
    profil.associated_account = associated_account
    profil.save()

#Cliquer sur le "Plus" (ou les 3 petits points)
def click_plus(browser):
    # Récupère l'ID du "plus" pour cliquer dessus
    soup = BeautifulSoup(browser.page_source, "html.parser")
    zone = soup.find('div', {'class': 'ph5'})
    zone.find_all('div', {'class': 'artdeco-dropdown'}) # type: ignore
    id_a_cliquer = zone.select_one("div[class*=artdeco-dropdown]")['id'] # type: ignore
    browser.find_element_by_id(id_a_cliquer).click()
    time.sleep(1)
    return

#Clique sur le "Se connecter" du "Plus"
def click_connect_on_plus(browser):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    div_plus = soup.find('div', {'class': 'ph5'})
    div_dropdown = div_plus.find('div', {'class': 'artdeco-dropdown__content-inner'}) # type: ignore
    toutli = div_dropdown.find_all('li') # type: ignore
    #Trouver l'id "Se connecter" et cliquer dessus
    for li_textes in toutli:
        try:
            li_texte = li_textes.find('span')
            if li_texte.text.strip() == "Se connecter":
                id_seconnecter = li_textes.find('div')['id']
                try:
                    browser.find_element_by_id(id_seconnecter).click() # type: ignore
                    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-modal__actionbar')))
                    return
                except:
                    click_plus(browser=browser)
                    browser.find_element_by_id(id_seconnecter).click() # type: ignore
                    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'artdeco-modal__actionbar')))
                    return
                
        except:
            continue

#Clique sur le "Se connecter" de l'action bar
def click_connect_on_actionbar(browser):
    soup2 = BeautifulSoup(browser.page_source, "html.parser")
    action_bar = soup2.find('div', {'class': 'artdeco-modal__actionbar'})
    all_button = action_bar.find_all('button') # type: ignore
    for connect_button in all_button:
        connect_button2 = connect_button.find('span').text.strip()
        if connect_button2 == "Se connecter":
            id_button_connect = connect_button['id']
            browser.find_element_by_id(id_button_connect).click()
            return

#Clique sur Connect et ajoute une note
def click_connect_on_page(browser):
    source = BeautifulSoup(browser.page_source, "html.parser")
    divprofile = source.find('div', {'class': 'ph5'})
    id_a_cliquer = divprofile.select_one("button[class*=artdeco-button]")['id'] # type: ignore
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, id_a_cliquer)))
    connect = browser.find_element_by_id(id_a_cliquer)
    connect.click()
    return


############################################################################################################################
#API POUR FOLLOW UP

#Scrape le nombre de relation

def nbr_relations(browser):
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'mn-connections__header')))
    soup = BeautifulSoup(browser.page_source, "html.parser")
    relations = soup.find('h1', {'class' : 't-18'})
    relations = relations.get_text().strip()  # type: ignore
    relations = relations.split()
    nombre_relations = int(relations[0])
    return nombre_relations

#Scroll jusqu'a qu'il trouve autant de profil que de nombre de relation
def scroller_en_bas(browser, nombre_relations):
    soup = BeautifulSoup(browser.page_source,"html.parser")
    nbr_li = len(soup.find_all('li', {'class': 'mn-connection-card'}))
    previous_li = nbr_li
    tour = 0
    #Scroller jusqu'a qu'il y est toutes le relations chargé
    while (nbr_li != nombre_relations): 

        #Cliquer sur le boutton "Afficher plus de resultat"
        try:
            all_btn = soup.find_all('div', {'class': 'display-flex'})
            for x in all_btn:
                try:
                    btn = x.select_one("button[class*=artdeco-button]")['id']
                    break
                except:
                    continue
            browser.find_element_by_id(btn).click() # type: ignore
        except:
            pass
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        nbr_li = len(soup.find_all('li', {'class': 'mn-connection-card'}))
        #Evite les boucle infini. S'il y a 10 fois le meme nombre, on arrete
        if nbr_li == previous_li:
            tour +=1
            if tour == 10:
                break
        else:
            tour = 0
        previous_li = nbr_li

#Sauvegarde dans la BDD pour followup1
def sauvegarde_followup1(profile, compte):
    profile.follow_up_1 = True
    profile.last_message = aujourdhui
    profile.error = False
    profile.associated_account = compte
    profile.save()
    time.sleep(random.uniform(12, 30))

#Sauvegarde dans la BDD pour followup2
def sauvegarde_followup2(profile, compte):
    profile.follow_up_2 = True
    profile.last_message = aujourdhui
    profile.error = False
    profile.associated_account = compte
    profile.save()
    time.sleep(random.uniform(12, 30))

#Sauvegarde dans la BDD pour followup3
def sauvegarde_followup3(profile, compte):
    profile.follow_up_3 = True
    profile.last_message = aujourdhui
    profile.error = False
    profile.associated_account = compte
    profile.save()
    time.sleep(random.uniform(12, 30))

#Voir toutes les relations
def voir_relations(browser):
    browser.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

    relations = nbr_relations(browser=browser)

    scroller_en_bas(browser=browser, nombre_relations=relations)

    src = BeautifulSoup(browser.page_source)
    totaldiv = src.find('div', {'class': 'scaffold-finite-scroll'})
    total_li = totaldiv.find_all('div', {'class': 'mn-connection-card__details'}) # type: ignore

    return total_li