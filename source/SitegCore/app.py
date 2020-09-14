from flask import Flask, render_template, request, send_from_directory, abort, Response
from flask import redirect, url_for
from SitegCore.model import loadDates, loadJSON, saveDate, DATABASE, saveFavIcon
from SitegCore.model import SiteSetup, Services, Gallery, MoreGallery, Category, Posts, PostManager
from SitegCore.export import Renderer, Model
import os

def create_app():
    app = Flask('SitegCore')

    # define renderer
    renderer = Renderer(Model.formatSiteJson())

    @app.route('/')
    def home():
        # Load site-detail.json file and image-data
        formData = SiteSetup.loadSiteDetail()
        imageData = SiteSetup.loadImage()
        return redirect(url_for('siteDetail'))

    @app.route('/site-detail/', methods = ['GET', 'POST'])
    def siteDetail():
        if request.method == 'POST':
            SiteSetup.saveSiteDetail(request.form, request.files)

            # save favIcon if profile image is available
            saveFavIcon()

            # render all required files
            renderer.siteDetail = Model.formatSiteJson()
            renderer.homePage(Model.galleries(), Model.services())
            renderer.thanksPage()
            renderer.searchPage()
            renderer.categoryPage()
            renderer.postCard(Model.posts(), Model.postDate())
            renderer.recentPost(Model.posts(), Model.postDate())
            renderer.refreshBlogs()
            renderer.moreGalleryPage(Model.moreGalleries())
        
        # Load site-detail.json file and image-data
        formData = SiteSetup.loadSiteDetail()
        imageData = SiteSetup.loadImage()
        return render_template('site-detail.html', formData=formData, imageData=imageData)

    @app.route('/gallery-section/', methods = ['GET', 'POST'])
    def gallerySection():
        if request.method == 'POST':
            if request.form['submit'] == 'add':
                if request.files["image"].filename.endswith(".gif"):
                    abort(404, description=".gif not allowed")
                Gallery.add(request.files["image"])
            elif request.form['submit'] == 'delete':
                Gallery.delete(request.form["service"])
            else:
                Gallery.save(request.form)

            renderer.homePage(Model.galleries(), Model.services())

        imageData, galleryFiles = Gallery.galleryList()
        return render_template('gallery-section.html', galleryFiles=galleryFiles, imageData=imageData)

    @app.route('/service-section/', methods = ['GET', 'POST'])
    def serviceSection():
        if request.method == 'POST':
            if request.form['submit'] == "Add":
                Services.add()
            elif request.form['submit'] == "Delete":
                Services.delete(request.form["service"])
            else:
                Services.save(request.form, request.files)

            renderer.homePage(Model.galleries(), Model.services())

        serviceFiles = Services.servicesList()
        imageData = Services.loadImages()
        return render_template('service-section.html', serviceFiles=serviceFiles, imageData=imageData)

    @app.route('/gallery-section/more/', methods = ['GET', 'POST'])
    def moreGallery():
        if request.method == 'POST':
            if request.form['submit'] == 'add':
                if request.files["image"].filename.endswith(".gif"):
                    abort(404, description=".gif not allowed")
                MoreGallery.add(request.files["image"])
            elif request.form['submit'] == 'delete':
                MoreGallery.delete(request.form["service"])
            elif request.form['submit'] == 'Save':
                MoreGallery.save(request.form)
            elif request.form['submit'] == 'save-head':
                MoreGallery.saveHead(request.form['title'], request.form['description'])
            
            renderer.moreGalleryPage(Model.moreGalleries())

        imageData, galleryFiles = MoreGallery.galleryList()
        head = MoreGallery.loadHead()
        return render_template('more-gallery.html', galleryFiles=galleryFiles, imageData=imageData, head=head)
    
    @app.route('/post-section/', methods = ['GET', 'POST'])
    def categorySection():
        if request.method == 'POST':
            if request.form['submit'] == 'add':
                Category.add(request.form["name"])
                renderer.refreshBlogs()
            elif request.form['submit'] == 'delete':
                Category.delete(request.form["name"])
            elif request.form['submit'] == 'rename':
                Category.rename(request.form["old-name"], request.form["new-name"])
            
            renderer.refreshBlogs()
            renderer.postCard(Model.posts(), Model.postDate())
            renderer.recentPost(Model.posts(), Model.postDate())
            renderer.createSearchJson(Model.posts())

            
        categories = Category.prettifyCategories()
        return render_template('category-section.html', categories = categories)

    @app.route('/post-section/<category>/', methods = ['GET', 'POST'])
    def postSection(category):
        if request.method == 'POST':
            if request.form['submit'] == 'add':
                postId = Posts.add(request.form["title"], category)
                renderer.blog(Model.post(postId), Model.categoriesBlogPage(), Model.mdHTML(postId))
            elif request.form['submit'] == 'delete':
                renderer.deletePost(Model.post(request.form["id"]))
                Posts.delete(request.form["id"])
            elif request.form['submit'] == 'rename':
                Posts.rename(request.form["id"], request.form["title"])
                renderer.blog(Model.post(request.form["id"]), Model.categoriesBlogPage(), Model.mdHTML(request.form["id"]))
            
            renderer.postCard(Model.posts(), Model.postDate())
            renderer.recentPost(Model.posts(), Model.postDate())
            renderer.createSearchJson(Model.posts())

        categoryName = Posts.prettifyCategory(category)
        if category in Category.getCategories():
            posts = Posts.getPosts(category=category)
            return render_template('post-section.html', category=categoryName, posts=posts)
        else:
            return abort(404, description=category+" Not Found")

    @app.route('/post-section/<path:postPath>/', methods = ['GET', 'POST'])
    def postManager(postPath):
        category, postId = PostManager.splitPath(postPath)
        if request.method == 'POST':
            if request.form["submit"] == "Save":
                if request.files['image'].filename.endswith(".gif"):
                    abort(404, description=".gif not allowed")
                PostManager.savePageInfo(postId, request.form, request.files)
                renderer.blog(Model.post(postId), Model.categoriesBlogPage(), Model.mdHTML(postId))
                renderer.postCard(Model.posts(), Model.postDate())
                renderer.recentPost(Model.posts(), Model.postDate())
                renderer.createSearchJson(Model.posts())
                return {'postId':postId}
            elif request.form["submit"] == "save-md":
                PostManager.saveMD(postId, request.form)
            elif request.form["submit"] == "delete":
                PostManager.deleteImage(postId, request.form['id'], request.form['format'])
            elif request.form["submit"] == "upload":
                imgId, imgFormat = PostManager.uploadImage(postId, request.files['image'])
                renderer.blog(Model.post(postId), Model.categoriesBlogPage(), Model.mdHTML(postId))
                renderer.postCard(Model.posts(), Model.postDate())
                renderer.recentPost(Model.posts(), Model.postDate())
                renderer.createSearchJson(Model.posts())
                return {"category":category, "postId":postId, "imgId":imgId, "imgFormat":imgFormat}
            elif request.form["submit"] == "setup-md":
                PostManager.setupMD(postId, request.form)
            elif request.form["submit"] == 'date':
                saveDate(postId, request.form['date'])
            
            renderer.blog(Model.post(postId), Model.categoriesBlogPage(), Model.mdHTML(postId))
            renderer.postCard(Model.posts(), Model.postDate())
            renderer.recentPost(Model.posts(), Model.postDate())
            renderer.createSearchJson(Model.posts())
        
        postDetail, postImage = PostManager.loadPageInfo(postId)
        return render_template(
            'post.html', 
            post=postDetail, 
            category=category, 
            postImage=postImage, 
            images=PostManager.loadImages(postId), 
            mdConfig=PostManager.loadMDConfig(postId),
            mdData = PostManager.loadMD(postId),
            categories = Category.prettifyCategories(),
            date = loadDates()[postId]
        )

    # post images routing
    @app.route('/all-posts/')
    def allPosts():
        posts = Posts.getPosts()
        return render_template('post-section.html', posts=posts)

    # post images routing
    @app.route('/posts/images/<path:filepath>')
    def postImage(filepath):
        dirPath = os.path.normpath(os.path.join(os.getcwd(), 'output', DATABASE['posts'], 'images'))
        response = send_from_directory(dirPath, filepath)
        response.cache_control.max_age = 1  
        return response

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error=str(e))

    return app
