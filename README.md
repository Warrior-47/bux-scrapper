# bux-scrapper

A python desktop app that scraps BRAC University's buX website.
Given a registered user email and password and an enrolled course ID of that account, it scraps all the youtube ID of the course, makes valid youtube urls, and saves them in a .csv file. The file is saved in a folder called Output.

It uses pythons modules BeautifulSoup and request to scrap the website.