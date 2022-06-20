from email.mime import image
import urllib.request
import bs4 as bs
import random
import moviepy

class EditVideo:
    URL = 'https://www.istockphoto.com/search/2/image?excludenudity=false&mediatype=photography&phrase='
    def __init__(self, keywords, image_path):
        self.keywords = keywords
        self.image_path = image_path

        image_files = []
        for keyword in keywords:
            file_name = self.scrape_images(keyword)
            image_files.append(file_name)

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

        #TODO: pick top image instead of random
        random_num = random.randint(0, len(images) - 1)
        image = images[random_num]
        print(image.get('src'))

        #retrieve image
        #if problem with getting image print error
        try:
            source = image.get('src')
            file_name = self.image_path + term + ".jpeg"
            urllib.request.urlretrieve(source, file_name)
            return file_name
        except Exception as e:
            print(e)