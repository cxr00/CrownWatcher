import bs4
from datetime import datetime
import os
import requests

from typing import Optional

site = "https://dailymail.co.uk"
ignore = "https://shop.dailymail.co.uk"


class Jewel:
    """
    Gather and organize soup for your family
    """

    def __init__(self):
        self.sess = None
        # {"category": {"main": bs4_obj, "subcategory1": bs4_obj1, "subcategory2": bs4_obj2}}
        self._pages: dict[str, Optional[bs4.BeautifulSoup]] = {}

    def __getitem__(self, item):
        return self._pages[item]

    def __iter__(self):
        return iter(self._pages.keys())

    def __setitem__(self, key, value):
        self._pages[key] = value

    def keys(self):
        return self._pages.keys()

    def refresh(self, *categories):
        """
        Refresh bs4 objects for each category; takes a little while
        """
        self.sess = requests.Session()
        self["Home"] = {"main": bs4.BeautifulSoup(self.sess.get(site).text, "html.parser")}
        self.sess.close()
        for li in self["Home"]["main"].find(class_="nav-primary").find_all("li")[1:-1]:
            if (not categories or li.span.a.string in categories) and li.span.a.string != "Video":
                print(f"pulling from {li.span.a.string}...")
                self.sess = requests.Session()
                self[li.span.a.string] = {"main": bs4.BeautifulSoup(self.sess.get(site + li.span.a["href"]).text, "html.parser")}
                self.refresh_category(li.span.a.string)
                self.sess.close()
        # self.sess.close()
        self.sess = None

    def refresh_category(self, category):
        """
        Get HTML for selected category's subcategories
        """
        if category not in self:
            raise KeyError(f"Invalid category: {category}")
        for li in self[category]["main"].find(class_="nav-secondary").ul.find_all("li")[1:]:
            st = li.a.string.strip()
            if not ("Latest" in st or "More" in st or st in ("Video", "Games", "Puzzles", "Mail Travel")):
                print(f"pulling from {category}/{st}")
                self[category][st] = bs4.BeautifulSoup(self.sess.get(site + li.a["href"]).text, "html.parser")


class Colony:
    """
    Post-processing for Jewel
    """

    def __init__(self, jewel):
        self.jewel = jewel
        self._articles = {}
        self._condensation = set()

    def __getitem__(self, item):
        return self._articles[item]

    def __iter__(self):
        return iter(self._articles.keys())

    def archive(self):
        fn = datetime.now().strftime("%Y-%m-%d").split("-")
        y, m, d = fn[0], fn[1], fn[2]
        for a in self._articles:
            if not os.path.exists(f".\\archive\\{y}\\{m}\\{d}\\{a}"):
                os.makedirs(f"archive\\{y}\\{m}\\{d}\\{a}")
            for article in self._articles[a]:
                with open(f"archive\\{y}\\{m}\\{d}\\{a}\\{article}.txt", "w+", encoding="utf-8") as f:
                    for headline in self._articles[a][article]:
                        f.write(headline + "\n")

    def condense(self):
        for c in self:
            for sc in self[c]:
                self._condensation = self._condensation.union(self[c][sc])
        print(len(self._condensation))

    def defame_crown(self):
        for c in self.jewel:
            if c not in self._articles:
                self._articles[c] = {}
            for sc in self.jewel[c]:
                self._articles[c][sc] = self.process_articles(self.jewel[c][sc])

    def process_articles(self, ruby):

        headlines = [n.find("h2") for n in ruby.find_all(class_="article-tri-headline")]
        headlines = [n.a.string.strip() for n in headlines if n.a and n.a.string]

        larges = [n.find("h2") for n in ruby.find_all(class_="article-large")]
        larges = [n.a.string.strip() for n in larges if n.a and n.a.string]

        smalls = [n.find("h2") for n in ruby.find_all(class_="article-small")]
        smalls = [n.a.string.strip() for n in smalls if n.a and n.a.string]

        list_row_headlines = [n.string.strip() for n in ruby.find_all(class_="articleListRowHeadline") if n and n.string]

        linkros = [n.a.string.strip() for n in ruby.find_all(class_="linkro-darkred") if n.a and n.a.string]

        procured = set()
        for e in [headlines, larges, smalls, list_row_headlines, linkros]:
            procured = procured.union(set(e))
        return procured
