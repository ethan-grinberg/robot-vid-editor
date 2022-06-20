import urllib.request
import bs4 as bs
import random
from moviepy.editor import *
import os

class EditVideo:
    URL = 'https://www.istockphoto.com/search/2/image?excludenudity=false&mediatype=photography&phrase='
    LAST_VID = 10
    def __init__(self, keywords, image_path, title, audio_path):
        self.keywords = dict(sorted(keywords.items(), key=lambda item: item[1]))
        self.image_path = image_path
        self.title = title
        self.audio_file = audio_path
    
    def edit_video(self):
        timestamps =  list(self.keywords.values())
        last_duration = timestamps[0]
        images = []

        txt_clip = TextClip(self.title, fontsize=70, color='white')
        txt_clip = txt_clip.set_pos('center').set_duration(last_duration)
        images.append(txt_clip)

        i = 0
        for k,v in self.keywords.items():
            next_duration = self.LAST_VID
            if i != (len(self.keywords) - 1):
                next_duration = timestamps[i+1]
            
            file_name = self.scrape_images(k)
            image = ImageClip(file_name).set_duration(next_duration - last_duration)
            images.append(image)

            # delete image file
            os.remove(file_name)

            last_duration = next_duration
            i += 1
        
        audioclip = AudioFileClip(self.audio_file)
        video = concatenate(images, method="compose")
        video = video.set_audio(audioclip)
        video.write_videofile(self.title + ".mp4", fps=24, codec='libx264')

    def scrape_images(self,term):
        file_name = ""

        #scrape stock photos site
        url = self.URL+term 
        html = urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(html,'lxml')

        #Get a list of all images
        #valid image links from this website contain "photos"
        images = [img for img in soup.findAll('img') if "photos" in img.get('src')]

        #If no images were found
        if len(images) == 0:
            return "None"

        random_num = random.randint(0, len(images) - 1)
        image = images[random_num]

        #retrieve image
        #if problem with getting image print error
        try:
            source = image.get('src')
            file_name = self.image_path + term + ".jpg"
            urllib.request.urlretrieve(source, file_name)
            return file_name
        except Exception as e:
            print(e)