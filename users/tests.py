from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth import get_user_model

# Imports normais do selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait # Importado para esperas explícitas
from selenium.webdriver.support import expected_conditions as EC

# Meus imports
import time
import string
import unittest # Necessário para asserções


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["user-data.json"]

    @classmethod
    def setUpTestData(cls):
        # Deve haver um rehashing, pois os IDs não são iguais!! (gerados em momentos diferentes)
        User = get_user_model()
        user_arthur = User.objects.get(username="arthur")
        
        # Define a senha com o texto puro, o Django a hasheia e a salva no DB do teste.
        cls.raw_password = 'arthur'
        user_arthur.set_password(cls.raw_password)
        user_arthur.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def running_page(self, page=""):
        self.selenium.get(f"{self.live_server_url}/{page}/")

    # --- Métodos de Autenticação reutilizados ---
    
    def test_login(self, username="jonesManoel", password="jamesBond"):
        self.running_page("login")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys(password)
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        # time.sleep(5) # Uso do WebDriverWait é preferível para estabilidade

    def test_register(self):
        email = "jones@gmail.com"
        username = "jonesManoel"
        password = "jamesBond"
        
        self.running_page("register")
        self.selenium.find_element(By.NAME, "username").send_keys(username)
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys(password)

        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        
        # O registro deve levar ao login, então forçamos o login em seguida
        self.test_login(username, password)
    
    # --- POM: Métodos Auxiliares ---
    
    def get_water_input(self):
        return self.selenium.find_element(By.NAME, "water_ml")
    
    def get_send_button(self):
        return self.selenium.find_elements(By.XPATH, "//button[@type='submit']")
    
    def find_by_name(self, name, size=0):
        if size == 0:
            return self.selenium.find_element(By.NAME, f"{name}")
        if size == 1:
            return self.selenium.find_elements(By.NAME, f"{name}")

    def get_message_element(self):
        """
        Retorna o elemento que contém a mensagem de sucesso/erro.
        ADJUSTAR ESTE XPATH/SELETOR de acordo com o seu layout (ex: .alert, #message-box)
        """
        wait = WebDriverWait(self.selenium, 5)
        # Tentando encontrar um elemento comum de mensagem, como uma div de alerta ou div de flash
        try:
            return wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert') or contains(@class, 'message')] | //p[contains(@class, 'error')] | //li[contains(@class, 'error')]")))
        except:
            raise Exception("Elemento de mensagem de feedback (sucesso/erro) não encontrado.")


    # --- MÉTODO PRINCIPAL DE TESTE CONSOLIDADO ---

    def test_intellifit_stories(self):
        
        # Prepara o ambiente: Registra e loga o usuário
        self.test_register()
        
        # Inicializa o WebDriverWait (tempo de espera explícito)
        wait = WebDriverWait(self.selenium, 10)
        
        # =========================================================================
        # 1. HISTÓRIA: GERENCIAR PROCESSO FÍSICO
        # =========================================================================
        
        # Acessa a tela de Gerenciar Processo Físico
        progress_button = self.selenium.find_element(By.XPATH, "/html/body/main/div/section/a[2]")
        progress_button.click()
        
        # --- CENÁRIO 3 (DESFAVORÁVEL): Tentar salvar edição incompleta/cadastro incompleto ---
        
        # Tenta salvar sem preencher peso ou medidas (assumindo que o botão [1] salva)
        send_buttons = self.get_send_button()
        if len(send_buttons) > 1:
            send_buttons[1].click()
        time.sleep(5)

        weight = 400
        water = 700
        calories = 12
        
        weight_label = self.selenium.find_element(By.NAME, "weight")
        weight_label.send_keys(weight)
        
        water_label = self.selenium.find_element(By.NAME, "water_ml")
        water_label.send_keys(water)
        
        calories_label = self.selenium.find_element(By.NAME, "calories")
        calories_label.send_keys(calories)
        
        register = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[1]/form/button")
        register.click()
        time.sleep(5)
        print("\n\n progresso criado\n\n")
        
        # --- CENÁRIO 1 (FAVORÁVEL): Editar registro de progresso com sucesso ---
        print("--- Teste de Progresso: Edição Favorável ---")
        
        edit = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[3]/ul/li[1]/div/a[1]")
        edit.click()
        
        self.get_water_input().clear()
        time.sleep(1)
        self.get_water_input().send_keys(10)
        self.get_send_button()[0].click()
        
        time.sleep(5)
        
        # --- CENÁRIO 2 (FAVORÁVEL): Excluir registro de progresso com sucesso ---
        
        delete = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[3]/ul/li[1]/div/a[2]")
        delete.click()
        self.get_send_button()[0].click()
        
        
        # Confirma a exclusão (assume o primeiro botão [0] confirma)
        self.get_send_button()[1].click()
        time.sleep(5)
        
        # =========================================================================
        # 2. HISTÓRIA: GERENCIAR DIETAS
        # =========================================================================
        
        # Volta para a dashboard (assumindo que o caminho mais seguro é clicar na home/dietas)
        self.running_page("dashboard") 
        
        # Acessa a tela de Dietas
        diet_button = self.selenium.find_element(By.XPATH, "/html/body/main/div/section/a[3]")
        diet_button.click()
        
        # Clica no botão de 'Criar Dieta'
        create_button_xpath = "/html/body/main/div/div[2]/a"
        create_button = wait.until(EC.element_to_be_clickable((By.XPATH, create_button_xpath)))
        create_button.click()
        
        # --- CENÁRIO 3 (DESFAVORÁVEL): Tentar salvar sem preencher todos os dados ---
        print("\n--- Teste de Dieta: Salvar Incompleto ---")
        
        # Tenta salvar sem preencher nada. (Botão de envio está em [1] na tela de criação de dieta)
        self.get_send_button()[1].click() 
        
        time.sleep(3)
        print("\n\n erro criar dieta\n\n")
        # --- CENÁRIO 1 (FAVORÁVEL): Criar dieta personalizada com sucesso ---
        print("--- Teste de Dieta: Criação Favorável ---")
        
        dietTitle = "Dieta de Teste Selenium"
        
        # Preenche Título e Descrição
        self.find_by_name("dietTitle").send_keys(dietTitle)
        self.find_by_name("dietDescription").send_keys("Dieta completa para validação.")
    
        # Preenche nome, calorias, e horários (assumindo que o campo horário é obrigatório ou necessário)
        self.find_by_name("food_name[]", size=1)[0].send_keys("Salada Proteica")
        self.find_by_name("food_calories[]", size=1)[0].send_keys("500")
        
        # Salva a dieta
        self.selenium.find_element(By.XPATH, "/html/body/main/div/form/div[5]/button").click()
            
        print("\n\nDieta criada\n\n")
        time.sleep(5)
    
        # Acessa a página de dietas novamente (após o salvamento)
        
        # --- CENÁRIO 2 (FAVORÁVEL): Consultar dieta já criada ---
        print("--- Teste de Dieta: Consulta Favorável ---")
        
        
        # Espera até que o título da dieta recém-criada apareça na lista para consulta.
        diet_link_xpath = "/html/body/main/div/section/a"
        diet_link = wait.until(EC.element_to_be_clickable((By.XPATH, diet_link_xpath)))
        diet_link.click()
        
        time.sleep(3)
        
        print("\n✅ Todos os cenários (Favoráveis e Desfavoráveis) foram testados com sucesso!")
        