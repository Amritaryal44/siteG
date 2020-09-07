import click
import shutil
import os
from SitegCore import create_app, copier, readSite
from flask.cli import FlaskGroup
import http.server
import socketserver
import os


def isSite():
    if not "output" in os.listdir() and not "database" in os.listdir():
        return False
    setFound = set()
    for root, dirs, files in os.walk("./", topdown=False):
        for name in files:
            setFound.add(os.path.join(root, name).replace("./",""))
        for name in dirs:
            setFound.add(os.path.join(root, name).replace("./",""))
    for root, dirs, files in os.walk("./database", topdown=False):
        for name in files:
            setFound.add(os.path.join(root, name).replace("./",""))
        for name in dirs:
            setFound.add(os.path.join(root, name).replace("./",""))
    subset = readSite()
    if subset.issubset(setFound):
        return True
    else:
        return False

@click.group(cls=FlaskGroup, create_app=create_app)
def siteg():
    ''' Build your site instantly

    SiteG is a static site generator with automatic management techniques.
    A user is able to manage galleries, posts and services with siteG site.
    It also have 'search site' feature. 
    
    siteG allows user to use markdown for writing posts with its own markdown 
    editor (powered by ace editor) with useful snippets. It also have drag image 
    feature for using the image in the post. 

    siteG supports 'google form' for the contact form. User have to manage the 
    form with their google account and follow instructions as per siteG says.
    User have to configure the site providing information and the site is ready 
    to be pushed to the server.
    '''
    pass

@click.group()
def setup():
    ''' Build your site instantly

    SiteG is a static site generator with automatic management techniques.
    A user is able to manage galleries, posts and services with siteg site.
    It also have 'search site' feature. 
    
    siteG allows user to use markdown for writing posts with its own markdown 
    editor (powered by ace editor) with useful snippets. It also have drag image 
    feature for using the image in the post. 

    siteG supports 'google form' for the contact form. User have to manage the 
    form with their google account and follow instructions as per siteG says.
    User have to configure the site providing information and the site is ready 
    to be pushed to the server.
    '''
    pass

@setup.command(name='create')
@click.argument('sitename', default='my site')
def create(sitename):
    ''' Create a site. 
    If no name is porvided, it uses "my site" as default.

    Syntax: siteg create <site-name> 

    Example: siteg create "my site"
    '''
    click.echo(f"Creating site ...")
    if copier(sitename):
        click.echo(f"{sitename} created successfully")
    else:
        click.echo(f"Error while creation")
        
@siteg.command(name='test')
def test():
    ''' Test the site. 

    Be sure to be inside the site folder created with siteg

    Syntax: siteg test 
    '''
    os.chdir('output')

    PORT = 8000

    class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def send_response_only(self, code, message=None):
            super().send_response_only(code, message)
            self.send_header('Cache-Control', 'no-store, must-revalidate')
            self.send_header('Expires', '0')

    with socketserver.TCPServer(('0.0.0.0', PORT), NoCacheHTTPRequestHandler) as httpd:
        print("Server started at http://127.0.0.1:" + str(PORT))
        httpd.serve_forever()

if __name__ == '__main__':
    if isSite():
        siteg()
    else:
        setup()