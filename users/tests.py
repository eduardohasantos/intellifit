from django.test import TestCase

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model

#Imports normais do selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

#Meus imports
import time
import string

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["user-data.json"]

    @classmethod
    def setUpTestData(cls):
        
        # Deve haver um rehashing, pois os IDs não são iguais!! (gerados em momentos diferentes)
        User = get_user_model()
        user_arthur = User.objects.get(username="arthur")
        
        # Define a senha com o texto puro, o Django a hasheia e a salva no DB do teste.
        # Use a senha que você tem certeza que usou (ex: 'minhasenha')
        cls.raw_password = 'arthur'
        user_arthur.set_password(cls.raw_password)
        user_arthur.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # AQUI, o usuário já existe e está pronto para ser usado
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    def running_page(self, page=""):
        self.selenium.get(f"{self.live_server_url}/{page}/")

    def test_login(self, username="", password=""):
        
        #Caso queira rodar apenas o login, descomente as linhas abaixo
        #self.running_page("login")
        # username = "arthur"
        # password = "arthur"
    
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(password)
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)        
        
    def test_register(self):
        
        email = "jones@gmail.com"
        username = "jonesManoel"
        password = "jamesBond"
        
        self.selenium.get(f"{self.live_server_url}/register/")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys(username)

        email_input = self.selenium.find_element(By.NAME, "email")
        email_input.send_keys(email)        

        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(password)

        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        #time.sleep(5)
        
        self.test_login(username, password)
    
    #=========POM=============
    
    def get_water_input(self):
        return self.selenium.find_element(By.NAME, "water_ml")
    
    def get_send_button(self):
        return self.selenium.find_elements(By.XPATH, "//button[@type='submit']")
    
    def find_by_name(self, name, size=0):
        if size == 0:
            return self.selenium.find_element(By.NAME, f"{name}")
        if size == 1:
            return self.selenium.find_elements(By.NAME, f"{name}")
        
    #===============REGISTRANDO PROGRESSO=============
    
    def test_register_progress(self):
        
        self.test_register()
        
        progress_button = self.selenium.find_element(By.XPATH, "/html/body/main/div/section/a[2]")
        progress_button.click()
        
        weight = 400
        water = 700
        calories = 12
        
        weight_label = self.selenium.find_element(By.NAME, "weight")
        weight_label.send_keys(weight)
        
        water_label = self.selenium.find_element(By.NAME, "water_ml")
        water_label.send_keys(water)
        
        calories_label = self.selenium.find_element(By.NAME, "calories")
        calories_label.send_keys(calories)
        
        send = self.selenium.find_elements(By.XPATH, "//button[@type='submit']")
        send[1].click()
        
        #Edição e exclusão
        edit = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[3]/ul/li[1]/div/a[1]")
        edit.click()
        
        self.get_water_input().clear()
        time.sleep(1)
        self.get_water_input().send_keys(10)
        self.get_send_button()[0].click()
        
        time.sleep(5)
        
        delete = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[3]/ul/li[1]/div/a[2]")
        delete.click()
        self.get_send_button()[0].click()
        
    def test_diet(self):
        
        self.test_register()
        
        dietTitle = "m"
        dietDescription = "p"
        index = 0
        add_qtd = 1
        entries = string.ascii_lowercase
        
        diet_button = self.selenium.find_element(By.XPATH, "/html/body/main/div/section/a[3]")
        diet_button.click()
        
        create_button = self.selenium.find_element(By.XPATH, "/html/body/main/div/div[2]/a")
        create_button.click()
        
        self.find_by_name("dietTitle").send_keys(dietTitle)
        self.find_by_name("dietDescription").send_keys(dietDescription)
        
        add_food_button = self.selenium.find_element(By.ID, "add-food-btn")
        for i in range(add_qtd):
            add_food_button.click()
        
        for prato in self.selenium.find_elements(By.NAME, "food_name[]"):
            prato.send_keys(entries[index])
            index += 1
        
        index = 0    
        for calorias in self.selenium.find_elements(By.NAME, "food_calories[]"):
            calorias.send_keys(index)
            index += 1
        
        self.get_send_button()[1].click()