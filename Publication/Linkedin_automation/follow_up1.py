import datetime, sys
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Publication.Linkedin_automation.api import connection_compte, nbr_relations, sauvegarde_followup1, scroller_en_bas
from Publication.models import Linkedin_Account, Linkedin_Profile_Info

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random


def follow_up_1(browser, compte, total_li):
    print(f"lancement du fichier Follow up 1 pour le compte {compte.linkedin_account}")
    aujourdhui = datetime.date.today()
    delay = 10

    for x in total_li:

        #Arreter a 30 message
        message_envoye = len(Linkedin_Profile_Info.objects.filter(last_message=aujourdhui, associated_account=compte))
        if message_envoye > 30:
            print(f"FIN DU PROGRAMME !!! Tu as déjà envoyé {message_envoye} aujourd'hui")
            return
            
        try : 
            liens = x.select_one("a[class*=ember-view]")['href']
            full_link = "https://www.linkedin.com" + liens
            profile = Linkedin_Profile_Info.objects.get(linkedin_link=full_link)

            if (profile.message_sent==True) and (profile.follow_up_1==False):
                jours = (aujourdhui - profile.last_message).days
                if jours > 3 :
                    print(f"Message evoyé ajd : {message_envoye} pour le compte {compte.linkedin_account}")
                    #récupère le message et change la variable
                    Message = compte.follow_up_1
                    if '{first_name}' in Message:
                        Message = Message.replace('{first_name}', profile.first_name)

                    browser.get(full_link)
                    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'entry-point')))

                    #Récupère et se connecte au liens de la messageria
                    src = BeautifulSoup(browser.page_source)
                    message_div = src.find('div', {'class': 'entry-point'})
                    message_link = message_div.select_one("a[class*=message-anywhere-button]")['href'] # type: ignore
                    full_link = "https://www.linkedin.com" + message_link  # type: ignore
                    browser.get(full_link)
                
                    #Ecrire le texte
                    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'msg-s-message-list-container')))
                    browser.find_element_by_class_name('msg-form__contenteditable').send_keys(Message)
                    time.sleep(3)
                    browser.find_element_by_class_name('msg-form__contenteditable').submit()

                    #Sauvegarde dans la BDD
                    sauvegarde_followup1(profile=profile, compte=compte)
        except:
            pass

