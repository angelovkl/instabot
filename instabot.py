from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

import random
import os

class Instabot:

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('./chromedriver')
        self.login()

    def login(self):
        self.driver.get('https://instagram.com/accounts/login')
        sleep(3)
        self.driver.find_element_by_name('username').send_keys(self.username)
        password_field = self.driver.find_element_by_name('password')
        password_field.send_keys(self.password)
        sleep(2)
        password_field.send_keys(Keys.RETURN)
        sleep(2)

    def user(self,user):
        sleep(random.randint(2,4))
        self.driver.get('https://instagram.com/' + user)

    def follow_user(self,user):
        self.user(user)
        sleepsec = random.randint(3,6)
        sleep(sleepsec)
        follow_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")
        follow_button.click()

    # def unfollow_user(self,user):
    #     self.user(user)
    #     sleep(2)
    #     following_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Following')]")[0]
    #     following_button.click()
    #     sleep(2)
    #     unfollow_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")[0]
    #     unfollow_button.click()
        

    def like_user_post(self,user):
        self.user(user)
        photo = self.driver.find_element_by_class_name('eLAPa')
        photo.click()
  
    def user_followers(self,user):
        self.user(user)
        sleep(2)
        followers = self.driver.find_element_by_xpath("//a[contains(@href, '/followers/')]")
        followers.click()
        sleep(random.randint(3,5))
        followers_body = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        # 350 followers acc scroll < 20
        # 1200 followers scroll < 200
        while scroll < 55:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followers_body)
            scroll += 1
            sleep(random.randint(2,4))

        fList  = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        scrollLimit = len(fList)

        # write the number of users followers
        
        print("fList len is {}".format(len(fList)))
        followers_list_limit = scrollLimit
        print(int(followers_list_limit))
        followers_list = []
        forbidden_followers=[]
        forbidden_words = ['up','gy','gen','love','prir','onl','yt','nature', 'mk', 'devoj', 'shop', 'skop', 'rabo','pisatel','fitness','sport','memes','macedoni','shoe','prod','mod']
        is_forbidden = 0
        for i in range(int(followers_list_limit)):    
            follower = self.driver.find_elements_by_class_name('FPmhX')[i]
            for word in forbidden_words:
                if word in follower.text:
                    print('user contains forbidden word')
                    forbidden_followers.append(follower.text)
                    is_forbidden = 1
                    break
                else:
                    is_forbidden = 0

            if is_forbidden == 0:
                followers_list.append(follower.text)

        with open("forbidden_followers", "a") as txt_file:
            for l in forbidden_followers:
                txt_file.write(l + "\n")
        with open("output.txt", "w") as txt_file:
            for line in followers_list:
                txt_file.write(line + "\n")
                print("user added")
        
        print(len(followers_list))
        print("process finished")

    def photo_likes(self, url):
        self.driver.get('https://instagram.com/' + url)
        sleep(5)
        bc = self.driver.find_element_by_class_name('Nm9Fw')
        sleep(3)
        like_button = bc.find_element_by_class_name('sqdOP')
        self.driver.execute_script("arguments[0].click();", like_button)
        sleep(4)
        follow_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]")[1]
        sleep(2)
        self.driver.execute_script("arguments[0].click();", follow_button)

        



bot = Instabot('svashtarija', 'Svastarija123!')
# jovana_markovska
# gocanin_a

# bot.user_followers('slagjan.arsovski')
# print("main done")
users_to_follow = open('output.txt', 'r')
lines = users_to_follow.readlines()
users_to_follow_limit = random.randint(55,62)
count = 0
total_followed = 0
for line in lines:
    try:
        if(count == users_to_follow_limit):
            rn = random.randint(3400,3600)
            print("pause for {} seconds".format(rn))
            sleep(rn)
            total_followed += count
            count = 0
        sleep_seconds = random.randint(2,6)
        print("second sleep seconds: ",sleep_seconds)
        bot.follow_user(line.strip())
        with open("followed.txt", "a") as txt_file:
            txt_file.write(line.strip() + "\n")
        sleep(sleep_seconds)
        count +=1
    except:
        print('error user ', line.strip())
        with open("error_users.txt", "a") as txt_file:
            txt_file.write(line.strip() + "\n")
    
print("Total followed: ", total_followed)    
print("main done")


