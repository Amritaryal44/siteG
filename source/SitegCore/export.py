from jinja2 import Environment, FileSystemLoader
import json
import os
import shutil
from datetime import datetime
from fuzzyset import FuzzySet

import os

currentDir = os.getcwd()
VARS = {
    "site-detail":os.path.normpath(currentDir+"/database/site-detail.json"),
    "gallery":os.path.normpath(currentDir+"/database/gallery/gallery-list.json"),
    "more-gallery":os.path.normpath(currentDir+"/database/gallery/more-gallery.json"),
    "service":os.path.normpath(currentDir+"/database/services/service-list.json"),
    "category":os.path.normpath(currentDir+"/database/posts/category-list.json"),
    "post":os.path.normpath(currentDir+"/database/posts/post-list.json"),
    "date":os.path.normpath(currentDir+"/database/posts/date.json"),
    "service-dir":os.path.normpath(currentDir+"/database/services"),
    "mdHTML-dir":os.path.normpath(currentDir+"/database/posts/html"),
    "saved-template":os.path.normpath(currentDir+"/baseHTML/saved/globals.html")
}

Files = {
    "index":os.path.normpath(currentDir+"/output/index.html"),
    "category":os.path.normpath(currentDir+"/output/category-post.html"),
    "search":os.path.normpath(currentDir+"/output/search.html"),
    "more":os.path.normpath(currentDir+"/output/more.html"),
    "thankyou":os.path.normpath(currentDir+"/output/thankyou.html"),
    "search-json":os.path.normpath(currentDir+"/output/posts/search.json"),
    "post-cards":os.path.normpath(currentDir+"/output/posts/post-cards.html"),
    "recent-posts":os.path.normpath(currentDir+"/output/posts/recent-posts.html"),
    "category-dir":os.path.normpath(currentDir+"/output/posts/categories"),
}

class Renderer:
    def __init__(self, siteDetail):
        self.siteDetail = siteDetail

    def homePage(self, galleries, services):
        text = self.renderTemplate("index.html",
            site = self.siteDetail, 
            galleries = galleries,
            services = services,
        )
        self.save(text, Files['index'])

    def searchPage(self):
        text = self.renderTemplate("search.html", site = self.siteDetail)
        self.save(text, Files["search"])

    def categoryPage(self):
        text = self.renderTemplate("category-post.html", site = self.siteDetail)
        self.save(text, Files["category"])

    def notFoundPage(self):
        pass

    def thanksPage(self):
        text = self.renderTemplate("thankyou.html", site = self.siteDetail)
        self.save(text, Files["thankyou"])

    def moreGalleryPage(self, galleries):
        text = self.renderTemplate("more-gallery.html", 
            site = self.siteDetail,
            galleries = galleries
        )
        self.save(text, Files["more"])

    def blog(self, post, categoriesBlogPage, mdHTML):
        text = self.renderTemplate("blog.html", 
            site = self.siteDetail,
            categories = categoriesBlogPage,
            post = post,
            mdHTML = mdHTML,
            date = Model.postDate()
        )
        postFile = os.path.join(Files["category-dir"], post["category"], post["id"]+".html")
        self.save(text, postFile)

    def createSearchJson(self, posts):
        self.save({"posts":posts}, Files["search-json"])

    def postCard(self, posts, postDate):
        text = self.renderTemplate("post-card.html", 
            posts = posts,
            postDate = postDate,
        )
        self.save(text, Files["post-cards"])

    def recentPost(self, posts, postDate):
        newPosts = sorted(posts, key=lambda k: k['id'] , reverse=True)[:4]
        text = self.renderTemplate("recent-posts.html", 
            posts = newPosts,
            postDate = postDate,
        )
        self.save(text, Files["recent-posts"])

    def refreshBlogs(self):
        for post in Model.posts():
            self.blog(post, Model.categoriesBlogPage(), Model.mdHTML(post["id"]))

    def renderTemplate(self, templateName, **kwargs):
        import sys
        try:
            base_path = sys._MEIPASS
        except:
            base_path = os.path.abspath(".")

        templates_path = os.path.join(base_path, "SitegCore", "baseHTML")
        fileLoader = FileSystemLoader(templates_path)
        env = Environment(loader=fileLoader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(templateName)
        return template.render(kwargs)

    def save(self, text, file):
        with open(file, 'w') as f:
            if file != Files["search-json"]:
                f.write(text)
            else:
                json.dump(text, f)

    def deletePost(self, post):
        print(post)
        postFile = os.path.join(Files["category-dir"], post["category"], post["id"]+".html")
        try:
            os.remove(postFile)
        except OSError:
            pass

class Model:
    def loadDB(file):
        with open(file, "r") as f:
            try:
                formData = json.load(f)
                return formData 
            except:
                return {}

    def formatSiteJson():
        siteJson = Model.loadDB(VARS['site-detail'])
        if "banner-subtitle" in siteJson:
            siteJson["banner-subtitle"] = siteJson["banner-subtitle"].replace("\r\n", "<br>")
        if "about-intro" in siteJson:
            siteJson["about-intro"] = siteJson["about-intro"].split("\r\n")
        return siteJson

    def postDate():
        dates = {}
        for postId, postDate in Model.loadDB(VARS['date']).items():
            dateTimeObj = datetime.strptime(postDate, "%Y-%m-%d")
            dates[postId] = dateTimeObj.strftime("%b %d, %Y")
        return dates

    def services():
        serviceFiles = Model.loadDB(VARS['service'])
        if "services" in serviceFiles:
            serviceFiles = serviceFiles["services"]
            services = []
            for serviceFile in serviceFiles:
                service = Model.loadDB(os.path.join(VARS["service-dir"], serviceFile))
                service["id"] = serviceFile.split(".")[0]
                services.append(service)
            return services
        else:
            return []

    def galleries():
        galleries =  Model.loadDB(VARS['gallery'])
        if "galleries" in galleries:
            return galleries["galleries"]
        return galleries

    def moreGalleries():
        return Model.loadDB(VARS['more-gallery'])

    def categoriesBlogPage():
        try:
            posts = Model.loadDB(VARS['post'])['posts']
            categories = Model.loadDB(VARS['category'])['categories']
            jsonList = []
            for category in categories:
                length = 0
                for post in posts:
                    if post["category"] == category:
                        length = length + 1
                prettyName = ""
                for pretty in category.strip().split("-"):
                    prettyName = prettyName+" "+pretty.capitalize()
                jsonList.append({
                    "name":category,
                    "pretty":prettyName.strip(),
                    "post-length":length
                })
            return jsonList
        except:
            return []

    def posts():
        posts =  Model.loadDB(VARS['post'])
        if "posts" in posts:
            return posts['posts']
        return posts

    def mdHTML(postId):
        htmlFile = os.path.join(VARS['mdHTML-dir'], postId+".html")
        if os.path.exists(htmlFile):
            with open(htmlFile, "r") as f:
                htmlText = f.read()
                return htmlText
        else:
            return "This post is not written yet"

    def post(postId):
        posts =  Model.loadDB(VARS['post'])
        p = {}
        if "posts" in posts:
            posts = posts['posts']
            for post in posts:
                if post["id"] == postId:
                    p = post
        return p

    def getKeywords():
        posts = Model.posts()
        keywords = []
        for post in posts:
            if "keywords" in post:
                keyword = list(filter(lambda x: x!="", post["keywords"]))+[post['title']]  
            else:
                keyword = [post['title']]
            keywords.append({
                    "id":post["id"],
                    "keywords":keyword
                })
        return keywords

    def matchedIds(postId, threshold):
        keywords = Model.getKeywords()
        postKeywords = list(filter(lambda x: x["id"]==postId, keywords))[0]["keywords"]
        matches = []
        for keyword in keywords:
            fs = FuzzySet(keyword['keywords'])
            for pk in postKeywords:
                if postId != keyword["id"]:
                    m = fs.get(pk)
                    if m:
                        for score, val in fs.get(pk):
                            if score>threshold:
                                matches.append((keyword["id"], score, val))
        return matches

