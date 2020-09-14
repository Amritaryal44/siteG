import json
import os
import shutil
from SitegCore.image import HandleImage
import base64
from PIL import Image
import re
from datetime import date
import time
import os

currentDir = os.getcwd()
DATABASE = {
    "location":os.path.normpath(currentDir+"/database"),
    "image-loc":os.path.normpath(currentDir+"/output/img"),
    "gallery-loc":"gallery",
    "service-loc":"services",
    "post-loc":"posts", 
    "category-loc":"categories",
    "posts":os.path.normpath(currentDir+"/output/posts"),
    "images":{
        "home-image":os.path.normpath("banners/home-banner.jpg"),
        "post-image":os.path.normpath("banners/post-banner.jpg"),
        "contact-image":os.path.normpath("banners/contact-banner.jpg"),
        "profile-image":os.path.normpath("about-profile.jpg"),
    }
}

def loadJSON(databaseLoc, database):
    with open(os.path.join(databaseLoc, database), 'r') as f:
        try:
            formData = json.load(f)
            return formData 
        except:
            return {}

def saveDate(postId, date):
    '''Date is in yyyy-mm-dd format
    when date=None -> deletes the date of post
    '''
    databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
    dateJson = loadJSON(databaseDir, 'date.json')
    
    if date == None:
        dateJson.pop(postId)
    else:
        dateJson[postId] = str(date)

    with open(os.path.join(databaseDir, 'date.json'), "w") as f:
        json.dump(dateJson, f)

def loadDates():
    databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
    dateJson = loadJSON(databaseDir, 'date.json')
    return dateJson

def saveFavIcon():
    rootDir = os.path.normpath(currentDir+"/output")
    profImage = os.path.normpath(currentDir+"/output/img/about-profile.jpg")
    if os.path.exists(profImage):
        HandleImage.faviconGenerator(profImage, rootDir)

        # create ieconfig.xml file
        with open(os.path.join(rootDir, "ieconfig.xml"), "w") as f:
            text = """<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square70x70logo src="/smalltile.png"/>
      <square150x150logo src="/mediumtile.png"/>
      <wide310x150logo src="/widetile.png"/>
      <square310x310logo src="/largetile.png"/>
      <TileColor>#009900</TileColor>
    </tile>
  </msapplication>
</browserconfig>"""
    f.write(text)

class SiteSetup:
    def loadImage():
        data = {}
        for name, value in DATABASE["images"].items():
            img_loc = os.path.join(DATABASE["image-loc"], value)
            if os.path.exists(img_loc):
                img = open(img_loc, "rb")
                encoded = base64.b64encode(img.read())
                encoded = encoded.decode()
                data[name] = 'data:image/jpg;base64,{}'.format(encoded)
                img.close()
            else:
                data[name] = ""
        return data

    def saveSiteDetail(formData, imageData):
        with open(os.path.join(DATABASE["location"], "site-detail.json"), 'w') as form:
            json.dump(formData, form)
        
        for image in imageData:
            if imageData[image]:
                img_obj = HandleImage.load(imageData[image])
                img_obj = HandleImage.reduce_size(img_obj)
                HandleImage.save(img_obj, os.path.join(DATABASE["image-loc"], DATABASE["images"][image]))

    def loadSiteDetail():
        return loadJSON(DATABASE["location"], "site-detail.json")

class Services:
    def add():
        serviceLoc = os.path.join(DATABASE["location"], DATABASE["service-loc"])
        services = Services.getServiceFiles()
        oldServiceID = ""
        if not len(services):
            oldServiceID = "0"
        else:
            oldServiceID = services[len(services) - 1].split(".")[0]
        newServiceID = str(int(oldServiceID)+1)
        newServiceFile = os.path.join(serviceLoc, newServiceID+".json")
        with open(newServiceFile, "w") as f:
            f.write('{"name":"Dummy '+ newServiceID +'" , "description":"Dummy Description"}')
        with open(os.path.normpath(serviceLoc+"/service-list.json"), "r") as fr:
            jsonData = json.load(fr)
            jsonData["services"].append(newServiceID+'.json')
            fw = open(os.path.normpath(serviceLoc+"/service-list.json"), "w")
            json.dump(jsonData, fw)
            fw.close()

    def delete(service):
        serviceID = service[7:]
        serviceFile = serviceID+'.json'
        loc = os.path.join(DATABASE["location"], DATABASE["service-loc"])
        serviceFileLoc = os.path.join(loc, serviceFile)
        os.remove(serviceFileLoc)
        if os.path.exists(os.path.join(DATABASE["image-loc"], DATABASE["service-loc"], serviceID+'.png')):
            os.remove(os.path.join(DATABASE["image-loc"], DATABASE["service-loc"], serviceID+'.png'))
        jsonData = loadJSON(loc, 'service-list.json')
        listData = []
        for data in jsonData["services"]:
            if data != serviceFile:
                listData.append(data)
        jsonData["services"] = listData

        fw = open(os.path.join(loc, "service-list.json"), "w")
        json.dump(jsonData, fw)
        fw.close()

    def save(formData, imageData):
        loc = os.path.join(DATABASE["location"], DATABASE["service-loc"])
        img_loc = os.path.join(DATABASE["image-loc"], DATABASE["service-loc"])
        serviceFiles = Services.getServiceFiles()
        for serviceFile in serviceFiles:
            nameKey = "name-"+serviceFile.split(".")[0]
            descriptionKey = "description-"+serviceFile.split(".")[0]
            imageKey = "image-"+serviceFile.split(".")[0]

            jsonData = loadJSON(loc, serviceFile)
            jsonData["name"]=formData[nameKey]
            jsonData["description"]=formData[descriptionKey]
            with open(os.path.join(loc, serviceFile), "w") as f:
                json.dump(jsonData, f)
            
            if imageData[imageKey]:
                img_obj = Image.open(imageData[imageKey])
                HandleImage.save(img_obj, os.path.join(img_loc, serviceFile.split(".")[0]+".png"))
    
    def getServiceFiles():
        loc = os.path.join(DATABASE["location"], DATABASE["service-loc"], "service-list.json")
        f = open(loc, 'r')
        jsonData = json.load(f)
        services = jsonData["services"]
        return services
    
    def servicesList():
        serviceFiles = Services.getServiceFiles()
        serviceData = []
        for serviceFile in serviceFiles:
            loc = os.path.join(DATABASE["location"], DATABASE["service-loc"])
            jsonData = loadJSON(loc, serviceFile)
            jsonData["id"] = serviceFile.split(".")[0]
            serviceData.append(jsonData)
        return serviceData
    
    def loadImages():
        data = {}
        for serviceFiles in Services.getServiceFiles():
            name = serviceFiles.split(".")[0]
            img_loc = os.path.join(DATABASE["image-loc"], DATABASE["service-loc"], name+".png")
            if os.path.exists(img_loc):
                img = open(img_loc, "rb")
                encoded = base64.b64encode(img.read())
                encoded = encoded.decode()
                data[name] = 'data:image/jpg;base64,{}'.format(encoded)
                img.close()
            else:
                data[name] = ""
        return data

class Gallery:
    def add(image):
        databaseLoc = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        imgLoc = os.path.join(DATABASE["image-loc"], DATABASE["gallery-loc"])
        img = HandleImage.load(image)
        img = HandleImage.reduce_size(img)
        jsonData = loadJSON(databaseLoc, "gallery-list.json")["galleries"]
        newId = 1
        if len(jsonData):
            newId = int(jsonData[len(jsonData)-1]["id"])+1
        newJson = {
            "id": str(newId),
            "caption":"dummy caption"
        }
        jsonData.append(newJson)
        with open(os.path.join(databaseLoc, "gallery-list.json"), "w") as f:
            json.dump({"galleries":jsonData}, f)
        
        HandleImage.save(img, os.path.join(imgLoc, str(newId)+".jpg"))  

    def delete(gallery):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        imgDir = os.path.join(DATABASE["image-loc"], DATABASE["gallery-loc"])
        id = gallery[7:]
        os.remove(os.path.join(imgDir, id+".jpg"))
        jsonData = loadJSON(databaseDir, "gallery-list.json")["galleries"]
        newJsonData = []
        for gallery in jsonData:
            if gallery["id"] != id:
                newJsonData.append(gallery)
        
        with open(os.path.join(databaseDir, "gallery-list.json"), "w") as f:
            json.dump({"galleries":newJsonData}, f)

    def save(formData):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        jsonData = loadJSON(databaseDir, "gallery-list.json")["galleries"]
        newJsonData = []
        for gallery in jsonData:
            newGallery = gallery
            captionKey = "caption-"+gallery["id"]
            newGallery["caption"] = formData[captionKey]
            newJsonData.append(newGallery)
        
        with open(os.path.join(databaseDir, "gallery-list.json"), "w") as f:
            json.dump({"galleries":newJsonData}, f)          

    def galleryList():
        databaseLoc = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        imgDir = os.path.join(DATABASE["image-loc"], DATABASE["gallery-loc"])
        images = {}
        jsonData = loadJSON(databaseLoc, "gallery-list.json")["galleries"]

        for gallery in jsonData:
            id = gallery["id"]
            img_loc = os.path.join(imgDir, id+".jpg")
            if os.path.exists(img_loc):
                img = open(img_loc, "rb")
                encoded = base64.b64encode(img.read())
                encoded = encoded.decode()
                images[id] = 'data:image/jpg;base64,{}'.format(encoded)
                img.close()
            else:
                images[id] = ""
        
        return (images, jsonData)

class MoreGallery:
    def add(image):
        databaseLoc = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        imgLoc = os.path.join(DATABASE["image-loc"], DATABASE["gallery-loc"], "more")
        img = HandleImage.load(image)
        img = HandleImage.reduce_size(img)
        jsonData = loadJSON(databaseLoc, "more-gallery.json")
        galleries = jsonData["galleries"]
        newId = 1
        if len(jsonData["galleries"]):
            newId = int(galleries[len(galleries)-1]["id"])+1
        newJson = {
            "id": str(newId),
            "caption":"dummy caption"
        }
        galleries.append(newJson)
        jsonData["galleries"] = galleries
        with open(os.path.join(databaseLoc, "more-gallery.json"), "w") as f:
            json.dump(jsonData, f)
        
        HandleImage.save(img, os.path.join(imgLoc, str(newId)+".jpg"))  

    def delete(gallery):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        imgDir = os.path.join(DATABASE["image-loc"], DATABASE["gallery-loc"], "more")
        id = gallery[7:]
        print(os.path.join(imgDir, id+".jpg"))
        os.remove(os.path.join(imgDir, id+".jpg"))
        jsonData = loadJSON(databaseDir, "more-gallery.json")
        galleries = jsonData["galleries"]
        newJsonData = []
        for gallery in galleries:
            if gallery["id"] != id:
                newJsonData.append(gallery)
        jsonData["galleries"] = newJsonData
        with open(os.path.join(databaseDir, "more-gallery.json"), "w") as f:
            json.dump(jsonData, f)

    def save(formData):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        jsonData = loadJSON(databaseDir, "more-gallery.json")
        newJsonData = []
        for gallery in jsonData["galleries"]:
            newGallery = gallery
            captionKey = "caption-"+gallery["id"]
            newGallery["caption"] = formData[captionKey]
            newJsonData.append(newGallery)
        jsonData["galleries"] = newJsonData
        with open(os.path.join(databaseDir, "more-gallery.json"), "w") as f:
            json.dump(jsonData, f)          

    # gallery list alon with base64 gallery images
    def galleryList():
        databaseLoc = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        imgDir = os.path.join(DATABASE["image-loc"], DATABASE["gallery-loc"], "more")
        images = {}
        jsonData = loadJSON(databaseLoc, "more-gallery.json")["galleries"]

        for gallery in jsonData:
            id = gallery["id"]
            img_loc = os.path.join(imgDir, id+".jpg")
            if os.path.exists(img_loc):
                img = open(img_loc, "rb")
                encoded = base64.b64encode(img.read())
                encoded = encoded.decode()
                images[id] = 'data:image/jpg;base64,{}'.format(encoded)
                img.close()
            else:
                images[id] = ""
        
        return (images, jsonData)

    def saveHead(title, description):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        jsonData = loadJSON(databaseDir, "more-gallery.json")
        jsonData["head"] = {'title':title, 'description':description}
        with open(os.path.join(databaseDir, "more-gallery.json"), "w") as f:
            json.dump(jsonData, f) 

    def loadHead():
        databaseDir = os.path.join(DATABASE["location"], DATABASE["gallery-loc"])
        head = loadJSON(databaseDir, "more-gallery.json")["head"]
        return head

class Category:
    def add(name):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        validName = name.replace(" ", "-").strip().lower()
        categoryDir = os.path.join(DATABASE["posts"], DATABASE["category-loc"], validName)
        jsonData = loadJSON(databaseDir, "category-list.json")["categories"]
        if validName in jsonData:
            return False
        
        jsonData.append(validName)
        with open(os.path.join(databaseDir, "category-list.json"), "w") as f:
            json.dump({"categories":jsonData}, f)
        os.mkdir(categoryDir)    
        return True

    def delete(name):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        validName = name.replace(" ", "-").lower()
        categoryDir = os.path.join(DATABASE["posts"], DATABASE["category-loc"], validName)
        jsonData = loadJSON(databaseDir, "category-list.json")["categories"]

        newJson = []
        for category in jsonData:
            if category != validName:
                newJson.append(category)

        with open(os.path.join(databaseDir, "category-list.json"), "w") as f:
            json.dump({"categories":newJson}, f)
        shutil.rmtree(categoryDir)

        # deleting the posts for that category
        posts = Posts.getPosts()
        for post in posts:
            if post['category']==validName:
                Posts.delete(post['id'])

    def rename(oldName, newName):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        validOldName = oldName.replace(" ", "-").strip().lower()
        validNewName = newName.replace(" ", "-").strip().lower()
        oldCategoryDir = os.path.join(DATABASE["posts"], DATABASE["category-loc"], validOldName)
        newCategoryDir = os.path.join(DATABASE["posts"], DATABASE["category-loc"], validNewName)

        # changing name in category-list.json and post-list.json
        listData = {"category":"categories", "post":"posts"}
        for key, value in listData.items():     
            jsonData = loadJSON(databaseDir, key+"-list.json")[value]
            newJson = []
            for data in jsonData:
                if key=="category" and data==validOldName:
                    newJson.append(validNewName)
                elif key=="post" and data['category']==validOldName:
                    data['category'] = validNewName
                    newJson.append(data)
                else:
                    newJson.append(data)

            with open(os.path.join(databaseDir, key+"-list.json"), "w") as f:
                json.dump({value:newJson}, f)

        os.rename(oldCategoryDir, newCategoryDir)

    def getCategories():
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        return loadJSON(databaseDir, "category-list.json")["categories"]
    
    def prettifyCategories():
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        jsonData = loadJSON(databaseDir, "category-list.json")["categories"]

        newJson = []
        for category in jsonData:
            newNames = []
            prettyName = ""
            for pretty in category.strip().split("-"):
                prettyName = prettyName+" "+pretty.capitalize()
            newJson.append(prettyName.strip())
        
        return newJson

class Posts:
    def prettifyCategory(name):
        prettyNames = name.split("-")
        newNames = []
        for name in prettyNames:
            newNames.append(name.capitalize())
        
        newCategory = str(newNames).replace("[","").replace("]","").replace(",", "").replace("'", "")
        return newCategory
    
    def getPosts(category=""):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        posts = loadJSON(databaseDir, "post-list.json")["posts"]
        if category=="":
            return posts
        newPosts = []
        for post in posts:
            if post["category"]==category:
                newPosts.append(post)
        return newPosts
 
    def add(name, category):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        imageDir = os.path.join(DATABASE["posts"], "images")
        posts = Posts.getPosts()

        Id = 1
        if len(posts):
            Id = int(posts[len(posts)-1]["id"])+1
        
        saveDate(Id, date.today()) # save the date of creation

        posts.append({"id":str(Id), "title":name, "category":category, "keywords":[""], "description": ""})
        with open(os.path.join(databaseDir, "post-list.json"), "w") as f:
            json.dump({"posts":posts}, f)
        
        os.mkdir(os.path.join(imageDir, str(Id)))
        return str(Id)
    
    def delete(postId):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        imageDir = os.path.join(DATABASE["posts"], "images")
        posts = Posts.getPosts()
        newPosts = []
        for post in posts:
            if post['id'] != postId:
                newPosts.append(post)
        
        # delete date
        saveDate(postId, None)

        # post config is in separate file which needs to be deleted
        postConfig = loadJSON(databaseDir, 'post-config.json')
        if postId in postConfig:
            postConfig.pop(postId)
            with open(os.path.join(databaseDir, 'post-config.json'), 'w') as f:
                json.dump(postConfig, f)

        with open(os.path.join(databaseDir, "post-list.json"), "w") as f:
            json.dump({"posts":newPosts}, f)
        shutil.rmtree(os.path.join(imageDir, postId))
        if os.path.exists(os.path.join(databaseDir, "markdown", postId+".md")):
            os.remove(os.path.join(databaseDir, "markdown", postId+".md"))

    def rename(postId, name):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        posts = Posts.getPosts()

        newPosts = []
        for post in posts:
            if post['id'] == postId:
                post["title"] = name
            newPosts.append(post)

        with open(os.path.join(databaseDir, "post-list.json"), "w") as f:
            json.dump({"posts":newPosts}, f)
 
class PostManager:
    def splitPath(path):
        return path.split("/")
    
    def getImageIds(postId):
        imageDir = os.path.join(DATABASE["posts"], "images", postId)
        ls = os.listdir(imageDir)
        r = re.compile(postId+"-\d+\.(jpg|gif)")
        return list(map(lambda x: int(x.split("-")[1].split(".")[0]),  list(filter(r.match, ls))))
    
    def uploadImage(postId, image):
        imageDir = os.path.join(DATABASE["posts"], "images", postId)
        imgIds = PostManager.getImageIds(postId)
        newId = "1"
        if imgIds:
            newId = max(imgIds) + 1 # last_id + 1
        img = HandleImage.load(image)
        img = HandleImage.reduce_size(img)
        # check if the image is in gif format
        imgFormat = ""
        if img.format != 'GIF':
            imageLoc = os.path.join(imageDir, postId+"-"+str(newId)+".jpg")
            imgFormat = "jpg"
        else:
            imageLoc = os.path.join(imageDir, postId+"-"+str(newId)+".gif")
            imgFormat = "gif"
        HandleImage.save(img, imageLoc)

        return str(newId), imgFormat

    def deleteImage(postId, imgId, imgFormat):
        imageDir = os.path.join(DATABASE["posts"], "images", postId)
        imgIds = PostManager.getImageIds(postId)
        if int(imgId) in imgIds:
            os.remove(os.path.join(imageDir, postId+"-"+str(imgId)+"."+imgFormat))
    
    def loadImages(postId):
        imageDir = os.path.join(DATABASE["posts"], "images", postId)
        imgIds = PostManager.getImageIds(postId)
        imgIds.sort()
        images = []
        for imgId in imgIds:
            imageLoc = os.path.join(imageDir, postId+"-"+str(imgId)+".jpg")
            if os.path.exists(imageLoc):
                image = '/posts/images/'+postId+'/'+postId+"-"+str(imgId)+".jpg"
                imgFormat = "jpg"
            else:
                image = '/posts/images/'+postId+'/'+postId+"-"+str(imgId)+".gif"
                imgFormat = "gif"
            images.append({'id':imgId, 'image': image, 'format':imgFormat})
        return images

    def saveMD(postId, formData):
        mdFile = os.path.join(DATABASE["location"], DATABASE["post-loc"], "markdown", postId+".md")
        htmlFile = os.path.join(DATABASE["location"], DATABASE["post-loc"], "html", postId+".html")
        with open(mdFile, 'w') as f:
            f.write(formData['mdData'])
        with open(htmlFile, 'w') as f:
            f.write(formData['htmlData'])
    
    def setupMD(postId, formData):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        jsonData = loadJSON(databaseDir, 'post-config.json')
        jsonData[postId] = {}
        for status, value in formData.items():
            if status != "submit":
                jsonData[postId][status] = value
        
        with open(os.path.join(databaseDir, 'post-config.json'), 'w') as f:
            json.dump(jsonData, f)

    def savePageInfo(postId, formData, imageData):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        imageLoc = os.path.join(DATABASE["posts"], "images", postId, postId+".jpg")
        posts = Posts.getPosts()

        newPosts = []
        for post in posts:
            if post['id'] == postId:
                post["title"] = formData["title"]
                post["description"] = formData["description"]
                post["category"] = formData["category"]
                post["keywords"] = formData["keywords"].strip().split(",")
            newPosts.append(post)

        with open(os.path.join(databaseDir, "post-list.json"), "w") as f:
            json.dump({"posts":newPosts}, f)
        
        if imageData["image"]:
            img = HandleImage.load(imageData["image"])
            img = HandleImage.reduce_size(img)
            HandleImage.save(img, imageLoc)

    def loadPageInfo(postId):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        imageLoc = os.path.join(DATABASE["posts"], "images", postId, postId+".jpg")
        posts = Posts.getPosts()
        detail = {}
        for post in posts:
            if post["id"]==postId:
                detail = post
                break
        
        image = ""
        if os.path.exists(imageLoc):
            img = open(imageLoc, "rb")
            encoded = base64.b64encode(img.read())
            encoded = encoded.decode()
            image = 'data:image/jpg;base64,{}'.format(encoded)
            img.close()

        return detail, image

    def loadMDConfig(postId):
        databaseDir = os.path.join(DATABASE["location"], DATABASE["post-loc"])
        jsonData =  loadJSON(databaseDir, 'post-config.json') 
        if postId in jsonData:
            return jsonData[postId]
        else:
            return {}          

    def loadMD(postId):
        mdFile = os.path.join(DATABASE["location"], DATABASE["post-loc"], "markdown", postId+".md")
        mdData = ""
        if os.path.exists(mdFile):
            with open(mdFile, 'r') as f:
                mdData = f.read()
        else:
            with open(os.path.join(DATABASE["location"], DATABASE["post-loc"], "markdown", "sample.md"), 'r') as f:
                mdData = f.read()
        return mdData
