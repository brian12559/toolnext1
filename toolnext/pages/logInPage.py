'''
Created on August 31, 2018

@filename logInPage.py
@author: bmurray
'''

from pages.base import Page
from locators.loginLocators import *
import logging, time, os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Page objects are written in this module.
# Depends on the page functionality we can have more functions for new classes

class MainPage(Page):
    def check_page_loaded(self):
        return True if self.find_element(*MainPageLocators.LOGO) else False

     
class LoginPage1(Page):
    def check_xray_loaded(self):
        return True if self.find_element(*LoginPageLocators.ISSUEKEYXRAY) else False

    def check_pt_loaded(self):
        return True if self.find_element(*LoginPageLocators.TESTCASEPT) else False

    def check_Test_Library(self):
        return True if self.find_element(*LoginPageLocators.TESTLIBRARYPT) else False

    def check_tl_loaded(self):
        return True if self.find_element(*LoginPageLocators.TESTCASEICONTL) else False

    def check_page_loaded(self):
        return True if self.find_element(*LoginPageLocators.USERNAME) else False
    
    def enter_username(self, username):
        self.driver.find_element(*LoginPageLocators.USERNAMEXRAY).send_keys(username)

    def enter_usernamePT(self, username):
        self.driver.find_element(*LoginPageLocators.USERNAMEPT).send_keys(username)

    def enter_usernameTL(self, username):
        actions = ActionChains(self.driver)
        actions.send_keys('stester1')
        actions.perform()
        #self.driver.find_element(*LoginPageLocators.USERNAMETL).send_keys(username)

    def clear_username(self):
        self.driver.find_element(*LoginPageLocators.USERNAMEXRAY).clear()
        
    def enter_password(self, pw):
        self.driver.find_element(*LoginPageLocators.PASSWORDXRAY).send_keys(pw)

    def enter_passwordPT(self, pw):
        self.driver.find_element(*LoginPageLocators.PASSWORDPT).send_keys(pw)

    def enter_passwordTL(self, pw):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB + 'rhtoolnext')
        actions.perform()
       # self.driver.find_element(*LoginPageLocators.PASSWORDTL).send_keys(pw)

    def clear_password(self):
        self.driver.find_element(*LoginPageLocators.PASSWORDXRAY).clear()
    
    def click_login_button(self):
        self.driver.find_element(*LoginPageLocators.SUBMITXRAY).click()

    def click_login_buttonPT(self):
        self.driver.find_element(*LoginPageLocators.SUBMITPT).click()

    def click_login_buttonTL(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB + Keys.TAB + Keys.ENTER)
        actions.perform()
        #self.driver.find_element(*LoginPageLocators.SUBMITTL).click()

    def click_rememeberme_box(self):
        self.driver.find_element(*LoginPageLocators.REMEMBERME).click()
        
    def loginuserxrayOLD(self, username, pw): #for devel and sr2
        logging.info("Entering username: %s using %s" %(username, LoginPageLocators.USERNAMEXRAY))
        #might need clear
        self.enter_username(username)
        logging.info("Entering password: %s using %s" %(pw, LoginPageLocators.PASSWORDXRAY))
        self.enter_password(pw)
        logging.info("clicking 'LOG IN' button using {0}".format(LoginPageLocators.SUBMITXRAY))
        self.click_login_button()
        time.sleep(5)

    def loginuserxrayOLD(self, username, pw):
        homedir = os.path.expanduser('~')
        logging.info("Entering username: %s using %s" % (username, LoginPageLocators.USERNAMEXRAY))
        # might need clear
        self.enter_username(username)
        logging.info("Entering password: %s using %s" % (pw, LoginPageLocators.PASSWORDTL))
        self.enter_password(pw)
        logging.info("clicking 'LOG IN' button using {0}".format(LoginPageLocators.SUBMITYL))
        startloading = time.time()
        self.click_login_button()
        elapsedtime = time.time() - startloading
        while not (self.driver.find_element(*LoginPageLocators.ISSUEKEYXRAY)):
            elapsedtime = time.time() - startloading
            logging.info("still waiting...%s" % str(elapsedtime))
            time.sleep(1)
        ltime = str((time.time() - startloading))
        logging.info("time to load XRAY -> %s" % ltime)
        with open("%s/LoginTime.csv" % homedir, "a") as myfile:
            myfile.write(time.ctime() + "," + ltime +  "\n")

    def loginuserxray(self, username, pw):
        homedir = os.path.expanduser('~')
        logging.info("Entering username: %s using %s" % (username, LoginPageLocators.USERNAMEXRAY))
        # might need clear
        self.enter_username(username)
        logging.info("Entering password: %s using %s" % (pw, LoginPageLocators.PASSWORDXRAY))
        self.enter_password(pw)
        logging.info("clicking 'LOG IN' button using {0}".format(LoginPageLocators.SUBMITXRAY))
        startloading = time.time()
        self.click_login_button()
        elapsedtime = time.time() - startloading
        #time.sleep(2)  # it always takes at least 2 secs
        while elapsedtime < 60:
            try:
                self.driver.find_element(*LoginPageLocators.ISSUEKEYXRAY).clear()
                logging.info("Jira issue field exists, so Xray is loaded")
                break
            except:
                elapsedtime = time.time() - startloading
                logging.info("still waiting...%s" % str(elapsedtime))
                time.sleep(1)
        if self.check_xray_loaded():
            ltime = str((time.time() - startloading))
            logging.info("time to load XRAY -> %s" % ltime)
            with open("%s/LoginTime.csv" % homedir, "a") as myfile:
                myfile.write(time.ctime() + "," + ltime + "\n")
        else:
            Logging.info("Xray never loaded")

    def loginuserTL(self, username, pw):
        time.sleep(1)
        homedir = os.path.expanduser('~')
        logging.info("Entering username: %s using %s" % (username, LoginPageLocators.USERNAMETL))
        # might need clear
        self.enter_usernameTL(username)
        logging.info("Entering password: %s using %s" % (pw, LoginPageLocators.PASSWORDTL))
        self.enter_passwordTL(pw)
        logging.info("clicking 'LOG IN' button using {0}".format(LoginPageLocators.SUBMITTL))
        startloading = time.time()
        self.click_login_buttonTL()
        elapsedtime = time.time() - startloading
        # time.sleep(2)  # it always takes at least 2 secs
        while elapsedtime < 60:
            try:
                if self.check_tl_loaded():
                    logging.info("TestLab icons exist, so TestLab is loaded")
                    break
            except:
                elapsedtime = time.time() - startloading
                logging.info("still waiting...%s" % str(elapsedtime))
                time.sleep(1)
        if self.check_tl_loaded():
            ltime = str((time.time() - startloading))
            logging.info("time to load TestLab -> %s" % ltime)
            with open("%s/LoginTime.csv" % homedir, "a") as myfile:
                myfile.write(time.ctime() + "," + ltime + "\n")
        else:
            Logging.info("TestLab never loaded")

    def loginuserPT(self, username, pw):
        time.sleep(1)
        homedir = os.path.expanduser('~')
        logging.info("Entering username: %s using %s" % (username, LoginPageLocators.USERNAMEPT))
        # might need clear
        self.enter_usernamePT(username)
        logging.info("clicking 'LOG IN' button using {0}".format(LoginPageLocators.SUBMITPT))
        self.click_login_buttonPT()
        #time.sleep(1)
        logging.info("Entering password: %s using %s" % (pw, LoginPageLocators.PASSWORDPT))
        try:
            #sometimes its too fast and pw box isnt there yet
            self.enter_passwordPT(pw)
        except:
            time.sleep(1)
            self.enter_passwordPT(pw)
        logging.info("clicking 'LOG IN' button using {0}".format(LoginPageLocators.SUBMITPT))
        startloading = time.time()
        self.click_login_buttonPT()
        elapsedtime = time.time() - startloading
        # time.sleep(2)  # it always takes at least 2 secs
        while elapsedtime < 60:
            try:
                if self.check_pt_loaded():
                    logging.info("PractiTest Link exist, so PractiTest is loaded")
                    break
            except:
                elapsedtime = time.time() - startloading
                logging.info("still waiting...%s" % str(elapsedtime))
                time.sleep(1)
        if self.check_pt_loaded():
            ltime = str((time.time() - startloading))
            logging.info("time to load PractiTest -> %s" % ltime)
            with open("%s/LoginTime.csv" % homedir, "a") as myfile:
                myfile.write(time.ctime() + "," + ltime + "\n")
        else:
            Logging.info("PractiTest never loaded")

    def createTCPT(self, testname):
        logging.info("clicking Test Library Link")
        try:
            self.driver.find_element(*LoginPageLocators.TESTLIBRARYPT).click()
        except:
            self.driver.find_element(*LoginPageLocators.TESTLIBRARYPT2).click()
        logging.info("clicking New Test Link")
        try:
            self.driver.find_element(*LoginPageLocators.NEWTESTPT).click()
        except:
            time.sleep(1)
            self.driver.find_element(*LoginPageLocators.NEWTESTPT).click()
        logging.info("entering test title")
        try:
            self.driver.find_element(*LoginPageLocators.TESTIDPT).send_keys(testname)
        except:
            time.sleep(1)
            self.driver.find_element(*LoginPageLocators.TESTIDPT).send_keys(testname)
        logging.info("clicking Save Test Case")
        self.driver.find_element(*LoginPageLocators.TESTCASESUBMITPT).click()

    def login_with_valid_user(self, username, pw):
        self.loginuserxray(username, pw)
        return HomePage(self.driver)

    def login_with_valid_userTL(self, username, pw):
        self.loginuserTL(username, pw)
        return HomePage(self.driver)


    def login_with_valid_userPT(self, username, pw):
        self.loginuserPT(username, pw)
        return HomePage(self.driver)

    def login_with_invalid_user(self, username, pw, rememberme=False):
        self.loginuser(username, pw, rememberme)
        return self.find_element(*LoginPageLocators.ERROR_MESSAGE).text  
    

class LogoutPage(Page):
    def check_page_loaded(self):
        return True if self.find_element(*LogoutPageLocators.GEARICON) else False
    
    def click_gearicon (self):
        self.driver.find_element(*LogoutPageLocators.GEARICON).click()
    
    def wait_for_settings (self):
        self.driver.find_element(*LogoutPageLocators.SETTINGS)
        
    def click_logout (self):
        self.driver.find_element(*LogoutPageLocators.LOGOUT).click()
        
    def click_hide (self):
        self.driver.find_element(*LogoutPageLocators.HIDE).click()        
        
    def logout(self):
        logging.info("clicking gear icon using {0}".format(LogoutPageLocators.GEARICON))
        self.click_gearicon()
        #self.wait_for_settings()
        logging.info("clicking Logout using {0}".format(LogoutPageLocators.LOGOUT))
        self.click_logout()
        
        

class HomePage(Page):
    pass
    
class SignUpPage(Page):
    pass


        
        
        
