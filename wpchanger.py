
import time 
import io
import ctypes
import http.client
import praw
import requests
import urllib



def main():
    path = "C:/Users/galwi/redditWallpapers/"
    dateToday = time.localtime()
    ddmmyy = time.ctime()[0:11] + time.ctime()[-1:-5:-1][::-1] # This is to get the date in dd/mm/yy format, ex: 01/01/16
    listOfDates = getDatesDownloaded(path) # This is a list of dates that have already been downloaded
    if(not((ddmmyy + "\n") in listOfDates)): 
        pictureUrl = getImgurLink()    
        downloadImage(pictureUrl , ddmmyy, path)
        #setWallpaperForTheDay(ddmmyy, path)
        set_wallpaper(path + "wallpaperOfTheDay " + ddmmyy + ".jpg")
    else:
        print("Already downloaded")
    

def getImgurLink(): # This function returns the link to the top wallpaper of the day
    redditObject = praw.Reddit(client_id = "T46sr4defGPqYMYBntnRUA", client_secret = "H8Snte7389b2Jee8mtJZi_usK52X4g",  user_agent = 'Daily Wallpaper Retriver for a new Windows Wallpaper')

    # Get the subreddit
    subreddit = redditObject.get('r/wallpapers')

    for post in subreddit:
        url = str(post.url)

        if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):
            return url
            
    
def getDatesDownloaded(path): # This function returns a list of dates that have already been downloaded
    logList = []
    logFile = open(path + "wallpaperLog.txt" , 'r')
    for line in logFile.readlines():
        logList.append(line)
    return logList

def downloadImage(url , date, path): # This function downloads the image from the url and saves it in the path
    response = requests.get(url)

    dataWriter = io.FileIO(path + 'wallpaperOfTheDay ' + date + '.jpg', 'w') # This is the file that the image data will be written to
    dataWriter.write(response.content)
    dataWriter.close()
    updateDateFile(date, path)
    print("Downloaded and added to list")

    
def updateDateFile(date, path): # This function updates the log file with the date of the downloaded image
    logFile = open(path + 'wallpaperLog.txt','a')
    logFile.write(date + "\n")
    logFile.close()
    

def setWallpaperForTheDay(date, path): # This function sets the wallpaper for the day
    ctypes.windll.user32.SystemParametersInfoA(20,0,path + "wallpaperOfTheDay " + date + ".jpg", 0) # This is the function that sets the wallpaper

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

main()