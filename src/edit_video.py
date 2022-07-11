import urllib.request
import bs4 as bs
import random
from moviepy.editor import *
import os

class EditVideo:
    URL = 'https://www.istockphoto.com/search/2/image?excludenudity=false&mediatype=photography&phrase='
    LAST_VID = 5
    DEFAULT_TERM = 'blue'

    def __init__(self, keywords, image_path, title, audio_path):
        # sort keywords in increasing order of timestamps
        self.keywords = dict(sorted(keywords.items(), key=lambda item: item[1]))
        self.image_path = image_path
        self.title = title
        self.audio_file = audio_path
    
    def edit_video(self):
        timestamps =  list(self.keywords.values())
        curr_time = timestamps[0]
        images = []

        txt_clip = TextClip(self.title, fontsize=70, color='white')
        txt_clip = txt_clip.set_pos('center').set_duration(curr_time)
        images.append(txt_clip)

        i = 0
        for k,v in self.keywords.items():
            duration = self.LAST_VID
            if i != (len(self.keywords) - 1):
                next_time = timestamps[i+1]
                duration = next_time - curr_time
                curr_time = next_time
            
            file_name = self.scrape_images(k)
            image = ImageClip(file_name).set_duration(duration)
            images.append(image)
            
            os.remove(file_name)

            i += 1
        
        audioclip = AudioFileClip(self.audio_file)
        video = concatenate(images, method="compose")
        video = video.set_audio(audioclip)
        video.write_videofile(self.title + ".mp4", fps=24, codec='libx264')

    def scrape_images(self,term):        
        images = self.__get_list_images(term)

        #If no images were found try simpler terms
        if len(images) == 0:
            all_terms = term.split(" ")
            found_image = False
            for i in range(len(all_terms) - 1):
                simple_term = " ".join(all_terms[:len(all_terms) - i - 1])
                images = self.__get_list_images(simple_term)

                if len(images) != 0:
                    found_image = True
                    break
            
            if not found_image:
                images = self.__get_list_images(self.DEFAULT_TERM)
                print("no images found for " + term)
        
        return self.__save_image(images, term)

    def __get_list_images(self, term):
        cleaned_term = term.replace(" ", "+")

        #scrape stock photos site
        url = self.URL+cleaned_term 
        html = urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(html,'lxml')

        #Get a list of all images
        #valid image links from this website contain "photos"
        images = [img for img in soup.findAll('img') if "photos" in img.get('src')]
        return images

    def __save_image(self, images, term):
        cleaned_term = term.replace(" ", "_")
        # pick random image
        random_num = random.randint(0, len(images) - 1)
        image = images[random_num]

        #retrieve image
        #if problem with getting image print error
        try:
            source = image.get('src')
            file_name = self.image_path + cleaned_term + ".jpg"
            urllib.request.urlretrieve(source, file_name)
            return file_name
        except Exception as e:
            print(e)

