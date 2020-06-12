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

    def unfollow_user(self,user):
        self.user(user)
        sleep(random.randint(3,6))
        try:
            following_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Following')]")
        except:
            following_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Requested')]")
        
        following_button.click()
        sleep(random.randint(2,6))
        unfollow_button = self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]")
        unfollow_button.click()
        

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
        while scroll < 50:
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
        forbidden_words = ['stu','pod','make','off', 'gree','piz', 'rand','pro','up','gy','gen','love','prir','onl','yt','nature', 'mk', 'devoj', 'shop', 'skop', 'rabo','pisatel','fitness','sport','memes','macedoni','shoe','prod','mod']
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
        with open("output.txt", "a") as txt_file:
            for line in followers_list:
                txt_file.write(line + "\n")
                print("user added")
        
        print(len(followers_list))
        print("process finished")

    def user_followings(self,user):
        self.user(user)
        sleep(2)
        followers = self.driver.find_element_by_xpath("//a[contains(@href, '/following/')]")
        followers.click()
        sleep(random.randint(3,5))
        followers_body = self.driver.find_element_by_xpath("//div[@class='isgrP']")
        scroll = 0
        # 350 following acc scroll < 20
        # 1200 following scroll < 200
        while scroll < 30:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followers_body)
            scroll += 1
            sleep(random.randint(2,4))

        fList  = self.driver.find_elements_by_xpath("//div[@class='isgrP']//li")
        scrollLimit = len(fList)

        print("fList len is {}".format(len(fList)))
        followers_list_limit = scrollLimit
        print(int(followers_list_limit))
        followers_list = []
        for i in range(int(followers_list_limit)):    
            follower = self.driver.find_elements_by_class_name('FPmhX')[i]
            followers_list.append(follower.text)
         
        with open("followings.txt", "a") as txt_file:
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

    def get_followings_to_unfollow(self):
        self.driver.get('https://instagram.com/' + self.username)
        user_followers = open('output.txt', 'r')
        user_followers_lines = user_followers.readlines()
        user_followings = open('followings.txt', 'r')
        user_followings_lines = user_followings.readlines()
        found = False
        with open('users_to_unfollow', 'a') as txt_file:
            for followings_line in user_followings_lines:
                for followers_line in user_followers_lines:            
                    if(followings_line == followers_line):
                        found = True
                        break
                    else:
                        found = False
                if(found):
                    print("founded!") 
                    found = False    
                else:
                    txt_file.write(followings_line.strip() + "\n")  

                        

        print('all users added')



bot = Instabot('user', 'pass')





users_to_unfollow = open('followings.txt', 'r')
users_to_unfollow_lines = users_to_unfollow.readlines()
users_to_unfollow_limit = random.randint(40,54)
count = 0
total_unfollowed = 0
for line in users_to_unfollow_lines:
    try:
        if(count == users_to_unfollow_limit):
            rn = random.randint(3400,3600)
            print("pause for {} seconds".format(rn))
            sleep(rn)
            total_unfollowed += count
            print("Total unfollowed: ", total_unfollowed)  
            count = 0
        sleep_seconds = random.randint(2,6)
        print("second sleep seconds: ",sleep_seconds)
        bot.unfollow_user(line.strip())
        with open("unfollowed.txt", "a") as txt_file:
            txt_file.write(line.strip() + "\n")
        sleep(sleep_seconds)
        count +=1
    except:
        print('error user ', line.strip())
        with open("unfollowed_error_users.txt", "a") as txt_file:
            txt_file.write(line.strip() + "\n")
    
  



# users_to_follow = open('output.txt', 'r')
# lines = users_to_follow.readlines()
# users_to_follow_limit = random.randint(55,62)
# count = 0
# total_followed = 0
# for line in lines:
#     try:
#         if(count == users_to_follow_limit):
#             rn = random.randint(3400,3600)
#             print("pause for {} seconds".format(rn))
#             sleep(rn)
#             total_followed += count
#             count = 0
#         sleep_seconds = random.randint(2,6)
#         print("second sleep seconds: ",sleep_seconds)
#         bot.follow_user(line.strip())
#         with open("followed.txt", "a") as txt_file:
#             txt_file.write(line.strip() + "\n")
#         sleep(sleep_seconds)
#         count +=1
#     except:
#         print('error user ', line.strip())
#         with open("error_users.txt", "a") as txt_file:
#             txt_file.write(line.strip() + "\n")
    
# print("Total followed: ", total_followed)    
# print("main done")


