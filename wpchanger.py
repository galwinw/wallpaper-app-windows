#!/usr/bin/env python

import time 
import io
import ctypes
import praw
import requests
import os
import random


def main():
    path = os.path.dirname(os.path.abspath(__file__)) + "/wp-images/" 
    ddmmyy = time.ctime()[0:11] + time.ctime()[-1:-5:-1][::-1] # This is to get the date in dd/mm/yy format, ex: 01/01/16
    listOfDates = getDatesDownloaded(path) # This is a list of dates that have already been downloaded
    if(not((ddmmyy + "\n") in listOfDates)): 
        pictureUrl = __getImage()    
        downloadImage(pictureUrl, path, ddmmyy)
        set_wallpaper(path + "wallpaperOfTheDay " + ddmmyy + ".jpg")
    else:
        return
    

def __getImage(): # This function returns the link to the top wallpaper of the day
    redditObject = praw.Reddit(
        client_id = "T46sr4defGPqYMYBntnRUA", 
        client_secret = "H8Snte7389b2Jee8mtJZi_usK52X4g",  
        user_agent = 'Daily Wallpaper Retriver for a new Windows Wallpaper',
        check_for_updates=False,
        comment_kind="t1",
        message_kind="t4",
        redditor_kind="t2",
        submission_kind="t3",
        subreddit_kind="t5",
        trophy_kind="t6",
        oauth_url="https://oauth.reddit.com",
        reddit_url="https://www.reddit.com",
        short_url="https://redd.it",
        ratelimit_seconds=5,
        timeout=16,
    )
    

    # Get the subreddit
    subreddit = redditObject.get('r/wallpaper')
    for post in subreddit:
        url = str(post.url)

        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            return url
            
def __getImageRandom(): # This function returns the link to a random wallpaper
    redditObject = praw.Reddit(
        client_id = "T46sr4defGPqYMYBntnRUA", 
        client_secret = "H8Snte7389b2Jee8mtJZi_usK52X4g",  
        user_agent = 'Daily Wallpaper Retriver for a new Windows Wallpaper',
        check_for_updates=False,
        comment_kind="t1",
        message_kind="t4",
        redditor_kind="t2",
        submission_kind="t3",
        subreddit_kind="t5",
        trophy_kind="t6",
        oauth_url="https://oauth.reddit.com",
        reddit_url="https://www.reddit.com",
        short_url="https://redd.it",
        ratelimit_seconds=5,
        timeout=16,
    )

    # Get the subreddit
    subreddit = redditObject.get('r/wallpaper')
    posts = []
    for post in subreddit:
        posts.append(post)
    random_post_number = random.randint(0, 10)
    random_post = posts[random_post_number]
    
    url = random_post.url
    if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
        print(url)
        return url
    else:
        return __getImageRandom()
    
def getRandomWallpapers(arr): # This function returns a list of random wallpapers
    redditObject = praw.Reddit(
        client_id = "T46sr4defGPqYMYBntnRUA", 
        client_secret = "H8Snte7389b2Jee8mtJZi_usK52X4g",  
        user_agent = 'Daily Wallpaper Retriver for a new Windows Wallpaper',
        check_for_updates=False,
        comment_kind="t1",
        message_kind="t4",
        redditor_kind="t2",
        submission_kind="t3",
        subreddit_kind="t5",
        trophy_kind="t6",
        oauth_url="https://oauth.reddit.com",
        reddit_url="https://www.reddit.com",
        short_url="https://redd.it",
        ratelimit_seconds=5,
        timeout=16,
    )

    # Get the subreddit
    subreddit = redditObject.get('r/wallpaper')
    for post in subreddit:
        url = str(post.url)
        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            arr.append(url)
    print (len(subreddit))
    print (len(arr))
    return arr


def getDatesDownloaded(path): # This function returns a list of dates that have already been downloaded
    logList = []
    logFile = open(path + "wallpaperLog.txt" , 'r')
    for line in logFile.readlines():
        logList.append(line)
    return logList


def downloadImage(url, path, date = '', update = True, random = False, image_name = ''): # This function downloads the image from the url and saves it in the path
    response = requests.get(url)

    if not random:
        dataWriter = io.FileIO(path + 'wallpaperOfTheDay ' + date + '.jpg', 'w') # This is the file that the image data will be written to
        print("Downloaded and added to list")
    else:
        dataWriter = io.FileIO(path + "\\" + image_name, 'w') # This is the file that the image data will be written to
        print("Downloaded random wallpaper")
    dataWriter.write(response.content)
    dataWriter.close()
    if(update):
        __updateDateFile(date, path)

    
def __updateDateFile(date, path): # This function updates the log file with the date of the downloaded image
    logFile = open(path + 'wallpaperLog.txt','a')
    logFile.write(date + "\n")
    logFile.close()
    
def set_wallpaper(image_path):
    # Constants for the SPI_SETDESKWALLPAPER action and the FILE_ATTRIBUTE_NORMAL flag
    SPI_SETDESKWALLPAPER = 20
    FILE_ATTRIBUTE_NORMAL = 0x80

    # Set the wallpaper
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, FILE_ATTRIBUTE_NORMAL
    )

    # Check if the wallpaper was set successfully
    if result:
        print("Wallpaper set successfully!")
    else:
        print("Failed to set wallpaper.")

class WallpaperChanger():
    def start(self):
        main()

    def set_wallpaper(self, image_path):
        set_wallpaper(image_path)

    def get_random_wallpapers(self, arr):
        return getRandomWallpapers(arr)
    
    def download_image(self, url, path, date='', update=True, random=False, image_name=''):
        downloadImage(url, path, date, update, random, image_name)

if __name__ == "__main__":
    wc = WallpaperChanger()
    wc.start()


