#!/usr/bin/env python
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from wpchanger import WallpaperChanger
import os
import shutil
from datetime import datetime
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    base_path = os.path.dirname(sys.executable)
    return os.path.join(base_path, relative_path)
    

class WelcomeScreen(Screen):
    def exit_app(self):
        App.get_running_app().stop()
        # if any random wallpapers are downloaded, delete them
        for file in os.listdir(resource_path('')):
            if file.startswith('randomWallpaper') and file.endswith('.jpg'):
                os.remove(resource_path(file))

class WallpaperScreen(Screen):
    pass

class RandomWallpaperScreen(Screen):
    image = ObjectProperty(None)
    path = resource_path('')
    randomWallpapers = []
    image_index = 0
    with open(os.path.join(path, 'Saved\savedIndex.txt'), 'r') as f:
        saved_index = int(f.read())
    current_image_source = 'randomWallpaper1.jpg'  # Initially set to the first image

    def on_pre_enter(self):
        self.get_random_wallpapers()
        self.download_random_wallpaper(True)

    def get_random_wallpapers(self):
        wallpaper_changer = WallpaperChanger()
        self.randomWallpapers = wallpaper_changer.get_random_wallpapers(self.randomWallpapers)

    def download_random_wallpaper(self, next):

        wallpaper_changer = WallpaperChanger()
        wallpaper_path = os.path.join(self.path, self.current_image_source)
        #delete the previous image
        if os.path.exists(wallpaper_path):
            os.remove(wallpaper_path)

        if next:
            self.image_index = (self.image_index + 1) % len(self.randomWallpapers)
        else:
            self.image_index = (self.image_index - 1) % len(self.randomWallpapers)

        self.current_image_source = 'randomWallpaper' + str(self.image_index) + '.jpg'
        wallpaper_path = os.path.join(self.path, self.current_image_source)
        wallpaper_changer.download_image(self.randomWallpapers[self.image_index], self.path, update=False, random=True, image_name= self.current_image_source)
        self.update_image(wallpaper_path)
        
    def update_image(self, wallpaper_path):
        print ("Setting image: " + wallpaper_path + " as wallpaper" + "Image index: " + str(self.image_index))
        if os.path.exists(wallpaper_path):
            self.image.source = wallpaper_path  # Set the image source again
            print ("Image set as wallpaper")

    def set_wallpaper(self):
        wallpaper_changer = WallpaperChanger()
        wallpaper_changer.set_wallpaper(os.path.join(self.path, self.current_image_source))
        wallpaper_set()

    def save_wallpaper(self):
        # Ensure the 'saved' folder exists
        saved_folder = os.path.join(self.path, 'Saved')
        if not os.path.exists(saved_folder):
            os.makedirs(saved_folder)

        
        # Construct the destination filename
        destination_filename = f"savedWallpaper{self.saved_index}.jpg"
        destination_path = os.path.join(saved_folder, destination_filename)

        try:
            # Copy the file to the 'saved' folder with the new name
            shutil.copyfile(os.path.join(self.path, self.current_image_source), destination_path)
            print(f"Image '{self.current_image_source}' saved as '{destination_filename}' in 'saved' folder.")
            wallpaper_saved()
            self.saved_index += 1
            update_saved_index(self.saved_index)
        except Exception as e:
            print(f"Error saving image: {e}")

class ViewImagesScreen(Screen):
    image = ObjectProperty(None)
    image_label = ObjectProperty(None)
    
    image_index = 0
    path = resource_path("wp-images/")
    image_files = [file for file in os.listdir(path) if file.startswith('wallpaperOfTheDay') and file.endswith('.jpg')]
    
    
    def on_pre_enter(self):
        self.update_folder()
        print(self.image_files)
        self.update_image()

    def update_folder(self):
        self.image_files = [file for file in os.listdir(self.path) if file.startswith('wallpaperOfTheDay') and file.endswith('.jpg')]
        if not self.image_files:
            self.image_label.text = "No Calendar Images, Set up "'Schedule Wallpaper Changes" to view Images'
            self.image.source = ""
        # Sort the image files by date
        self.image_files = sorted(self.image_files, key=lambda filename: self.extract_date(filename), reverse=True)

    def extract_date(self, filename):
        parts = filename.split(' ') 
        if parts[3] == '':
            parts.pop(3) 
            parts[3] = '0' + parts[3] 
        
        date_string = ' '.join(parts[-4:]) 
        date_string = date_string.replace('.jpg', '') 
        return datetime.strptime(date_string, '%a %b %d %Y') 

    def update_image(self):
        if self.image_files:
            image_file = self.image_files[self.image_index]
            image_path = os.path.join(self.path, image_file)
            self.image.source = image_path
            self.image_label.text = image_file
            
    def next_image(self):
        if self.image_files:
            self.image_index = (self.image_index + 1) % len(self.image_files)
            self.update_image()

    def previous_image(self):
        if self.image_files:
            self.image_index = (self.image_index - 1) % len(self.image_files)
            self.update_image()

    def set_wallpaper(self):
        wallpaper_changer = WallpaperChanger()
        if len(self.image_files) == 0:
            return
        image_file = self.image_files[self.image_index]
        wallpaper_changer.set_wallpaper(os.path.join(self.path, image_file))
        wallpaper_set()

    def delete_wallpaper(self):
        if self.image_files:
            image_file = self.image_files[self.image_index]
            image_path = os.path.join(self.path, image_file)
            os.remove(image_path)
            self.image_files.remove(image_file)
            if len(self.image_files) == 0:
                self.image_index = 0
            else:
                self.image_index = (self.image_index - 1) % len(self.image_files)
            wallpaper_deleted()
            self.update_image()

class SavedWallpaperScreen(Screen):
    image = ObjectProperty(None)
    image_label = ObjectProperty(None)
    
    image_index = 0

    path = resource_path("Saved/")
    image_files = [file for file in os.listdir(path) if file.startswith('savedWallpaper') and file.endswith('.jpg')]

    def on_pre_enter(self):
        self.update_folder()
        self.update_image()

    def update_folder(self):
        self.image_files = [file for file in os.listdir(self.path) if file.startswith('savedWallpaper') and file.endswith('.jpg')]
        if not self.image_files or len(self.image_files) == 0:
            self.image_label.text = "No saved wallpapers"
            self.image.source = ""


    def update_image(self):
        if self.image_files:
            image_file = self.image_files[self.image_index]
            image_path = os.path.join(self.path, image_file)
            self.image.source = image_path
            self.image_label.text = image_file
    
    def next_image(self):
        if self.image_files:
            self.image_index = (self.image_index + 1) % len(self.image_files)
            self.update_image()

    def previous_image(self):
        if self.image_files:
            self.image_index = (self.image_index - 1) % len(self.image_files)
            self.update_image()

    def set_wallpaper(self):
        wallpaper_changer = WallpaperChanger()
        if len(self.image_files) == 0:
            return
        image_file = self.image_files[self.image_index]
        wallpaper_changer.set_wallpaper(os.path.join(self.path, image_file))
        wallpaper_set()
    
    def delete_wallpaper(self):
        if self.image_files:
            image_file = self.image_files[self.image_index]
            image_path = os.path.join(self.path, image_file)
            os.remove(image_path)
            self.image_files.remove(image_file)
            if (len(self.image_files) == 0):
                self.image_index = 0
            else:
                self.image_index = (self.image_index - 1) % len(self.image_files)
            wallpaper_deleted()
            self.update_image()

class WindowManager(ScreenManager):
    pass

class InstructionScreen(Screen):
    #path to wpchanger.py
    path = resource_path('wpchanger.py')

def update_saved_index(index):
    with open(resource_path('Saved/savedIndex.txt'), 'w') as f:
        print("done")
        f.write(str(index))

def wallpaper_saved():
    pop = Popup(title='Wallpaper Saved', content=Label(text='Wallpaper saved to the "Saved Wallpapers"'), size_hint=(None, None), size=(400, 400))
    pop.open()

def wallpaper_set():
    pop = Popup(title='Wallpaper Set', content=Label(text='Wallpaper set Succesfully'), size_hint=(None, None), size=(400, 400))
    pop.open()

def wallpaper_deleted():
    pop = Popup(title='Wallpaper Deleted', content=Label(text='Wallpaper deleted Succesfully'), size_hint=(None, None), size=(400, 400))
    pop.open()



kv = Builder.load_file("my.kv")
sm = WindowManager()

screens = [WelcomeScreen(name="welcome"), WallpaperScreen(name="wallpaper"), ViewImagesScreen(name="viewimages"), RandomWallpaperScreen(name="random"), SavedWallpaperScreen(name="saved"), InstructionScreen(name="instructions")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "welcome"

class WallpaperApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    LabelBase.register(name='MyFont', fn_regular= 'Fonts/MyFont3.ttf')
    WallpaperApp().run()
