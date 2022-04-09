import datetime
from Publication.models import Linkedin_Account,Linkedin_Profile_Info
from Publication.Linkedin_automation.api import connection_compte, connexion_proxy, voir_relations
from Publication.Linkedin_automation.replied import reponse
from Publication.Linkedin_automation.follow_up3 import follow_up_3
from Publication.Linkedin_automation.follow_up2 import follow_up_2
from Publication.Linkedin_automation.follow_up1 import follow_up_1
from Publication.Linkedin_automation.auto_message import message1


def lancer_bot(pk):
    aujourdhui = datetime.date.today()
    compte = Linkedin_Account.objects.get(pk=pk)
    s = len(Linkedin_Profile_Info.objects.filter(associated_account=compte, last_message=aujourdhui))

    if s >=30:
        return print(f"Dejja envoyé {s}")

    if compte.proxy_use == True:
        browser = connexion_proxy(compte=compte)
    else :  
        browser = connection_compte(compte=compte)
        
    reponse(browser=browser)

    if (compte.active_follow_up_3 == True) or (compte.active_follow_up_2 == True) or (compte.active_follow_up_1 == True):
        relations = voir_relations(browser=browser)

    if compte.active_follow_up_3 == True:
        follow_up_3(browser=browser, compte=compte, total_li=relations)

    if compte.active_follow_up_2 == True:
        follow_up_2(browser=browser, compte=compte, total_li=relations)

    if compte.active_follow_up_1 == True:
        follow_up_1(browser=browser, compte=compte, total_li=relations)

    message1(browser=browser, compte=compte)



