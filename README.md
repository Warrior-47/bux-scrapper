# buX-Scrapper

A python desktop app that scraps BRAC University's buX website.
Given a registered user email and password and an enrolled course ID of that account, it scraps all the youtube video links of the course, makes valid youtube urls, and saves them in a .csv file. You can also make a youtube playlist after downloading the youtube links.

> Note: You will need to create a youtube channel using your GSuite account. Just select your GSuite account in Youtube, click on your display image at the top right corner and click **Create a Channel**

It needs to be GSuite account because its easier to give app access to accounts in the same organization.

It uses python's modules BeautifulSoup and requests to scrap the website.

## How it Works

Provide your GSuite email address given by BRACU and buX password. Enter which course's videos you would like to get the youtube links of, and click **Start Scrapping**. The app will log into your buX account and if you are enrolled in the course, it will download all the video links of the course.
> The Youtube links are stored in a csv file in a folder named Output.

![Sign In GUI](/icon/scrapper_login.JPG)
![Progress GUI When Starting](/icon/scrapper_progress_init.JPG)

After doing it's work, two button will appear. **Make Playlist** and **Scrap Again**.

![Progress GUI When Done](/icon/scrapper_progress_done.JPG)

**Make Playlist** will create a youtube playlist and add the course videos to it. You have to give consent using your GSuite account so that the app can create a playlist and add course videos to it. The playlist will be available in your gsuite youtube account.
> Keep in mind, Google enforces a quota limit and if that limit is exceeded, you'll need to wait a day to add more playlists.

**Scrap Again** will take you back to the login GUI.

## Where to Download

Go to https://warrior-47.github.io/bux-scrapper/buX%20Scrapper.zip
