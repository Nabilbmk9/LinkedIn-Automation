import threading
from Publication.models import Linkedin_Account
from Publication.Linkedin_automation.lancer_bot import lancer_bot




def main():
    s = Linkedin_Account.objects.filter(campaign=True)
    for i in s:
        t= threading.Thread(target=lancer_bot, args=(i.pk,))
        t.start()


main()
