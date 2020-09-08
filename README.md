<p align="center">
  <a href="https://github.com/Amritaryal44/siteG">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">SiteG - A static site generator</h3>

  <p align="center">
    Create and manage your site easily!
    <br />
    <a href="./learn-more.html"><strong>Explore More »</strong></a>
    <br />
    <br />
    <a href="https://www.amritaryal.com.np">View Demo</a>
    ·
    <a href="https://github.com/Amritaryal44/siteG/issues">Report Bug</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
    * [Using Windows](#using-windows)
    * [Using Linux](#using-linux)
* [Usage](#usage)
    * [Creating Website](#creating-website)
    * [Testing the site](#testing-the-site)
    * [Setup Site](#setup-site)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

<!-- ABOUT THE PROJECT -->
## About The Project

[![ScreenShot][product-screenshot]](https://amritaryal.com.np)

SiteG is a static site generator with automatic management techniques. It is specially designed for portfolio websites. A user is able to manage galleries, posts and services easily. It also have 'search site' feature. SiteG allows user to use markdown for writing posts with its own markdown 
editor (powered by ace editor) with useful snippets. It also have drag image 
feature for using the image in the post. 

SiteG supports ```google form``` for the contact form. User have to manage the 
form with their google account and follow instructions as per siteG says.
User have to configure the site providing information and the site is ready 
to be pushed to the server.

Special Features:
* Automatic related posts and recent post generation.
* Automatic pagination of posts page.
* Site Search with provided keywords.
* Automatic listing of related sites.
* It has its own post editor with useful snippets and common features to other editors.
* Automatic image compression and resizing.

SiteG works on a template with limited feature. I use the template as most commonly used features in portfolio.

### Built With
* [Python](https://python.org)
* [Flask](https://flask.palletsprojects.com)
* [Jquery](https://jquery.com)
* [Bootstrap](https://getbootstrap.com)
* [Jinja2](https://jinja.palletsprojects.com)


<!-- GETTING STARTED -->
## Getting Started

### Installation

#### **Using Windows**
1. Download the setup file from [here](https://www.amritaryal.com.np/siteG/)
2. Run the setup file
3. Copy the program folder where ```siteg.exe``` lies.<br> By default it is  ```C:\Program Files (x86)\```
The Next steps are not mandatory but to access **siteG** from anywhere, I would recommend to follow them too.
4. Open **Run** by pressing ```Win + R``` from keyboard and type ```sysdm.cpl```
5. Now, System Properties dialog should appear. Go to ```Advanced``` Tab and click ```Environment Variables```.
![ScreenShot][system-properties]
6. Below ```System variables```, You will find ```Path``` in ```Variable``` column.  Select it and Click ```Edit...``` button.
![ScreenShot][env-variables]
7. You will see paths separated with ```;```<br>
Example: ```C:\Program Files;C:\Winnt;C:\Winnt\System32```
Now, paste the copied path here following ```;```. <br>
Now it should look like: <br>
```C:\Program Files;C:\Winnt;C:\Winnt\System32;C:\Program Files (x86)\SiteG```

Hurray! Now you are done with installation part.

#### **Using Linux**
1. Download the tar file from [here](https://www.amritaryal.com.np/siteG/)
2. Extract the tar file to /home. <br>The Next steps are not mandatory but to access **siteG** from anywhere, I would recommend to follow them too.
3. Run the terminal (Ubuntu: Ctrl+Alt+T) and type :
    ```bash
    $ nano ~/.bashrc
    ``` 
4. Navigate to the bottom of the file and add this :
    ```bash
    export PATH="$PATH:/home/siteg"
    ```

Hurray! Now you are done with installation part.

<!-- USAGE EXAMPLES -->
## Usage

Now, Let's use the siteg to create website.
###  Creating Website
1. Navigate to the location where you want to create your website and run terminal(linux) or cmd/powershell (windows). <br>
    * Linux users : Simply right click on the folder and click open in terminal.
    * Windows users : ```Shift+ Right Click``` and click "open command window here"/"open power shell here".<br> OR<br>You can also type cmd into the Windows File Explorer address bar (use ```Ctrl+L``` | ```Alt+D``` to focus the address bar) and press Enter to open the shell.
2. To create site, Type ```siteg create <site-name>``` and navigate to ```<site-name>```
    ```bash
    $ siteg create "my site"
    $ cd "my site"
    ```
    Or, siteg will automatically create "my site" folder.
    ```bash
    $ siteg create
    $ cd "my site"
    ```
### Testing the site
Type ```siteg test``` after navigating to site folder.
```bash
/my site$ siteg test

Server started at http://127.0.0.1:8000
```
Now Copy the link ```http://127.0.0.1:8000``` and run it with your favourite browser. If you are a linux user, simply ```Ctrl+Click``` on the link will work. To quit, press ```Ctrl+C```.

Since we have not setup the site yet, It will display this.
![ScreenShot][no-setup-screenshot]

### Setup Site
Type ```siteg run``` to run the site setup 
```bash
/my site$ siteg run

 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to  quit)
```

![ScreenShot][site-setup-screenshot]

Fill all the inputs and click the ```save``` button. Add some galleries, services and posts.

> Note: if you want to run the server in your smartphone, just replace 127.0.0.1:PORT to [your local ip]:PORT and paste it in your smartphone browser.

You might be confused in the contact section for form. Please visit [here](./learn-more.html) to learn more.

_For more examples, please refer to the [this page](./learn-more.html)_


<!-- LICENSE -->

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/Amritaryal44/siteG/blob/master/LICENSE) for more information.

<!-- CONTACT -->

## Contact

Amrit Aryal - [@amritaryal44](https://twitter.com/AmritAryal44) - amritaryal44@gmail.com

Project Link: [https://github.com/amritaryal44/siteG](https://github.com/amritaryal44/siteG)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Ace Editor](https://ace.c9.io/)
* [Animate.css](https://daneden.github.io/animate.css)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Font Awesome](https://fontawesome.com)
* [FuzzysetJs](https://glench.github.io/fuzzyset.js/)
* [Markdown-it](https://github.com/markdown-it/markdown-it)





<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: images/main-screenshot.png
[system-properties]: images/system-properties.png
[env-variables]: images/envirvariables.jpg
[no-setup-screenshot]: images/no-setup-screenshot.png
[site-setup-screenshot]: images/site-setup-screenshot.png

