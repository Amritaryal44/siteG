<p align="center">
  <a href="https://github.com/Amritaryal44/siteG">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">SiteG - A static site generator</h3>

  <p align="center">
    Create and manage your site easily!
    <br />
    <a href="https://www.amritaryal.com.np/siteG/"><strong>Home</strong></a>
    <br />
    <br />
    <a href="https://www.amritaryal.com.np">View Demo</a>
    ·
    <a href="https://github.com/amritaryal44/siteG/issues">Report Bug</a>
  </p>
</p>

___

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [1. Home Banner](#1-home-banner)
  * [Home Banner Subtitle](#home-banner-subtitle)
* [2. About Me](#2-about-me)
  * [Your introduction](#your-introduction)
* [3. Contact Form](#3-contact-form)
* [4. Posts](#4-posts)
* [5. For modification](#5-for-modification)
* [License](#license)
* [Contact](#contact)

Note: Go through this page: [click me](/) before moving forward because you will only learn some important rules and procedures available in **SiteG**.\
Some Rules:
* Siteg supports images listed here. 
    * BMP
    * EPS
    * GIF (Only for ```Images for post```)
    * ICO
    * JPEG
    * JPEG 2000
    * PNG
    * TIFF
* SiteG does not show upload progress information so better upload small size images.
* Keep your website files safe because siteG cannot recover your site if anything goes wrong by human mistake or in case of lost.

## 1. Home Banner
### Home Banner Subtitle
Hiting ```Enter``` will result in break of line.<br> Example:
![Screenshot][banner-subtitle2]
Result:<br>
![Screenshot][banner-subtitle1]

## 2. About Me
### Your introduction
Hiting ```Enter``` will result change in paragraph.<br> Example:
![Screenshot][intro-1]
Result:<br>
![Screenshot][intro-2]

## 3. Contact Form
SiteG supports google form. So to include google form, you will need to follow some steps. Let's see how.
1. Open this link. [Google Forms](https://docs.google.com/forms)
2. Click ```Blank``` to get a new form.
![Screenshot][form-img1]
3. First input should be like this.
![Screenshot][form-img2]
4. The whole form should look like this.
![Screenshot][form-img3]
5. Now get the link of the form. Click the ```send``` button.<br>
![Screenshot][form-img4]
6. Copy the link from here.
![Screenshot][form-img5]<br>
Replace ```/viewform``` to ```/formResponse```. It should look like ```https://docs.google.com/forms/d/e/<form-id>/formResponse```.
Paste it in the action input of ```contact section```
![Screenshot][form-img6]
7. For rest of inputs, paste it in new tab of browser and Hit ```Ctrl+Shift+I``` to open inspector and Focus on ```search HTML``` as shown in red box.<br>
![Screenshot][form-img7]
Now, search for "```entry.```" and you will see like this.
![Screenshot][form-img8]
> First one is for ```name```<br>
> Second one is for ```email```<br>
> Third one is for ```message```

Hurray! Form can now be submitted from your site.

## 4. Posts
![Screenshot][post-img1]

Click ```Go to Posts``` to post or edit articles. After clicking it, you will go to ```Category``` section. Category is here just to tell people what kind of posts you are writing.

![Screenshot][post-img2]

Add a category and click it to go to ```post``` section.

![Screenshot][post-img3]

If you want to ```delete``` or ```rename``` it, just right-click the category folder.

![Screenshot][post-img4]
See!! Its that simple.
Now, Let's add new post.

![Screenshot][post-img5]

Click it and you will see a window like below:
![Screenshot][post-img6]

In ```Post Setup```, you can write short descriptions and keywords about the post.

Next is ```Image for the post```. Here, you have to add the images you want to add in the post article.

Third is Markdown Editor. You can write post in markdown format. Also enabling ```Allow HTML``` will allow you to write in html format. You can learn to write markdown from [Common Mark](https://commonmark.org/help/). As it supports syntax from Common Mark, I would recommend learning from there. It's so easy and interesting than writing normal documents. :happy:

A demo file is already loaded in the editor to help you.

Things you need to know while writing markdown:
1. **Heading**: Do not use Heading 1. Start from Heading 2 and so on.
2. **Image**: For uploading image from your PC, First upload the image in ```Image for the post```. Then, copy the link generated below the added image and paste the link with image syntax in markdown. I will show a demo.

    * Upload the image<br>
    ![Screenshot][post-img7]
    * Get File Path<br>
    ![Screenshot][post-img8]
    * Go to Markdown Editor below and hit ```Ctrl+SPACE``` to get image snippet.<br>
    ![Screenshot][post-img9]
    * Now hitting ```Enter``` will produce a img code like this.<br>
    ![Screenshot][post-img10]
    * Replace ```alttext``` with image description and press ```TAB```. and give post id and image id. In this example, post-id is 1 and image-id is 1. Now it should look like this.
        ```bash
        ![Chair made on blender](/posts/images/1/1-1.jpg "Chair 3D model")
        ```

## 5. For modification
If you want to edit the site layout, go to the ```siteg``` location and navigate to: 
* ```SitegCore/baseHTML``` for changing html layout
* ```SitegCore/site_files/output``` for changing ```css,js``` files.
* ```SitegCore/templates``` for changing html layout of ```site manager```
* ```SitegCore/static``` for changing css,js files of ```site manager```

<!-- LICENSE -->
## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/Amritaryal44/siteG/blob/master/LICENSE) for more information.



<!-- CONTACT -->
## Contact

Amrit Aryal - [@amritaryal44](https://twitter.com/AmritAryal44) - amritaryal44@gmail.com

Project Link: [https://github.com/amritaryal44/siteG](https://github.com/amritaryal44/siteG)


[banner-subtitle1]: images/banner-subtitle1.png
[banner-subtitle2]: images/banner-subtitle2.png
[intro-1]: images/intro1.png
[intro-2]: images/intro2.png
[post-img1]: images/post-img1.png
[post-img2]: images/post-img2.png
[post-img3]: images/post-img3.png
[post-img4]: images/post-img4.png
[post-img5]: images/post-img5.png
[post-img6]: images/post-img6.png
[post-img7]: images/post-img7.png
[post-img8]: images/post-img8.png
[post-img9]: images/post-img9.png
[post-img10]: images/post-img10.png
[form-img1]: images/form-img1.png
[form-img2]: images/form-img2.png
[form-img3]: images/form-img3.png
[form-img4]: images/form-img4.png
[form-img5]: images/form-img5.png
[form-img6]: images/form-img6.png
[form-img7]: images/form-img7.png
[form-img8]: images/form-img8.png
