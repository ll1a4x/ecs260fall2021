import requests
from bs4 import BeautifulSoup
import re


def get_files_changed_count(url):

    page = requests.get(url)
    # ----------------Head of Debugged Section4 by Lynden----------------
    # Important fix...
    # If page is None, then Python3 will print
    #       'NoneType' object has no attribute 'text'
    # when calling .text
    if page == None:
        return 0
    else:
        soup = BeautifulSoup(page.text, 'html.parser')
        try:
            soup_find1 = soup.find('button', {'class': 'btn-link js-details-target'})
            if soup_find1 == None:
                return 0
            else:
                value = soup_find1.text.replace(" changed files", "").\
                    replace(" changed file", "").strip()
                return int(value)
        except:
            soup_find2 = soup.find('div', {'class': 'toc-diff-stats'})
            if soup_find2 == None:
                return 0
            else:
                value_new = soup_find2.text.replace(" changed files", "").\
                    replace(" changed file", "").strip()

                value = re.findall(r"[0-9]+\,[0-9]+|[0-9]+", value_new)[0].replace(",", "")
                return int(value)
    # ----------------Tail of Debugged Section4 by Lynden----------------

#url = 'https://github.com/jatrost/accumulo/commit/6be40f2f3711aaa7d0b68b5b6852b79304af3cff'
# url = 'https://github.com/jatrost/accumulo/commit/d15b9ca4d24d84e62c7fca2ad87fd73b797af23f'
url = 'https://github.com/jatrost/accumulo/commit/e0880e263e4bf8662ba3848405200473a25dfc9f'
print(get_files_changed_count(url))
