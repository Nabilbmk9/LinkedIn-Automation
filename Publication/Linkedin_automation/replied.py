from bs4 import BeautifulSoup
from Publication.models import Linkedin_Profile_Info


def reponse(browser):
    print("lancement du bot Replied")
    browser.get("https://www.linkedin.com/messaging/thread/2-NDNiMTVkNjEtOGU3MS00Yzc2LWI2ZDctMTZmNDE2MTk0MzQ1XzAxMg==/?filter=unread")

    soup = BeautifulSoup(browser.page_source, "html.parser")

    profiles_messages = soup.find_all('div', {'class': 'msg-conversation-card'})

    for personne in profiles_messages:
        name_div = personne.find('h3', {'class': 'msg-conversation-listitem__participant-names'})
        full_name = name_div.get_text().strip()
        first_name = full_name.split()[0]
        last_name = ' '.join(full_name.split()[1:])
        print(first_name)
        try:
            profil = Linkedin_Profile_Info.objects.get(first_name=first_name, last_name=last_name)
            if (profil.message_sent==True) and (profil.follow_up_1==True):
                profil.replied = True
                profil.save()
        except:
            pass
    return




