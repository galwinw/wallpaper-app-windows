
import time 
import io
import ctypes
import http.client
import praw




def main():
    path = "C:/Users/galwi/redditWallpapers/"
    dateToday = time.localtime()
    ddmmyy = time.ctime()[0:11] + time.ctime()[-1:-5:-1][::-1] # This is to get the date in dd/mm/yy format, ex: 01/01/16
    listOfDates = getDatesDownloaded(path) # This is a list of dates that have already been downloaded
    if(not((ddmmyy + "\n") in listOfDates)): 
        pictureUrl = getImgurLink()    
        downloadImage(pictureUrl , ddmmyy, path)
        setWallpaperForTheDay(ddmmyy, path)
    else:
        print("Already downloaded")
    
def getImgurLink(): # This function returns the link to the top wallpaper of the day
    redditObject = praw.Reddit(client_id = "T46sr4defGPqYMYBntnRUA", client_secret = "H8Snte7389b2Jee8mtJZi_usK52X4g",  user_agent = 'Daily Wallpaper Retriver for a new Windows Wallpaper')

    while True:
        TopWallpaperSubmissions = redditObject.get('r/wallpapers')
        for submission in TopWallpaperSubmissions:
            try:
                print(submission.url)
                return submission.url
            except ConnectionError:
                continue

    
def getDatesDownloaded(path): # This function returns a list of dates that have already been downloaded
    logList = []
    logFile = open(path + "wallpaperLog.txt" , 'r')
    for line in logFile.readlines():
        logList.append(line)
    return logList

def downloadImage(url , date, path): # This function downloads the image from the url and saves it in the path
    if(url.startswith("http://i.imgur.com/")):
        url = url.replace("http://i.imgur.com/", "")
    else:
        url = url.replace("http://imgur.com/", "")

    connectionToImage = http.client.HTTPConnection("i.imgur.com") # This is the connection to the server 
    print ("Downloading image from " + url)
    connectionToImage.request("GET", url)  # This is the request to the server to get the image data from the server and return it 
    imageResponse = connectionToImage.getresponse() # This is the response from the server, ex 200 OK
    print (imageResponse.read()) # This is the response from the server
    imageData = imageResponse.read() # This is the actual image data, ex: a jpg file
    
    dataWriter = io.FileIO(path + 'wallpaperOfTheDay ' + date + '.jpg', 'w') # This is the file that the image data will be written to
    dataWriter.write(imageData)
    dataWriter.close()
    updateDateFile(date, path)
    print("Downloaded and added to list")


    
def updateDateFile(date, path): # This function updates the log file with the date of the downloaded image
    logFile = open(path + 'wallpaperLog.txt','a')
    logFile.write(date + "\n")
    logFile.close()

def setWallpaperForTheDay(date, path): # This function sets the wallpaper for the day
    ctypes.windll.user32.SystemParametersInfoA(20,0,path + "wallpaperOfTheDay " + date + ".jpg", 0) # This is the function that sets the wallpaper
    
main()