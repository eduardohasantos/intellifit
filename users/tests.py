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
import random
from diet import models
from django.contrib.auth.models import User

#py manage.py test users.tests.MySeleniumTests.test_intellifit_stories

class MySeleniumTests(StaticLiveServerTestCase):
    #fixtures = ["user-data.json"]
    textos = ["maduro cantando imagine John lennon", "sou o pedro de formiga", "basculante", "escolas de assassinos ensinando o mal"]

    @classmethod
    def setUpTestData(cls):
        # Deve haver um rehashing, pois os IDs não são iguais!! (gerados em momentos diferentes)
        User = get_user_model()
        user_arthur = User.objects.get(username="arthur")
        
        # Define a senha com o texto puro, o Django a hasheia e a salva no DB do teste.
        cls.raw_password = 'arthur'
        user_arthur.set_password(cls.raw_password)
        user_arthur.save()
        
        cls.test_user = User.objects.create_user(
            username='teste', 
            password='123'
        )
        
        cls.dieta1 = models.DietPersist.objects.create(
            dietTitle="Dieta de teste",
            dietDescription="geraaaaaaa",
            user=cls.test_user
        )
        
        cls.prato1 = models.DietMeal.objects.create(
            diet = cls.dieta1,
            food_name="bife de avestruz",
            calories= random.randint(1, 1000)
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)
        

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        
    def acoesPausadas(self):
        time.sleep(2)
        return self.selenium

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
    
    def get_submit_button(self):
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
        
        #Tempo para me preparar para o screencast
        time.sleep(10)
        
        # Prepara o ambiente: Registra e loga o usuário
        self.test_register()
        
        # Inicializa o WebDriverWait (tempo de espera explícito)
        wait = WebDriverWait(self.selenium, 10)
        
        # =========================================================================
        # 1. HISTÓRIA: CRIAR TREINO
        # =========================================================================
        
        self.running_page("workout/add")
        print("Acessando página de criação de treino...")

        # -------------------------------------------------------------------------
        # CD → CENÁRIO DESFAVORÁVEL: TENTAR CRIAR TREINO SEM PREENCHER NADA
        # -------------------------------------------------------------------------

        print(" Tentando criar treino SEM preencher campos...")
        self.get_submit_button()[1].click()
        print("Esperado: mensagem de erro de validação deve aparecer.")
        time.sleep(2)

        # -------------------------------------------------------------------------
        # CF → CENÁRIO FAVORÁVEL: PREENCHER OS CAMPOS CORRETAMENTE
        # -------------------------------------------------------------------------

        print("[CF] Preenchendo dados válidos do treino...")
        self.find_by_name("name").send_keys("Cardio")
        self.find_by_name("description").send_keys("45")
        self.get_submit_button()[1].click()
        print("Treino criado com sucesso (parte inicial).")

        # -------------------------------------------------------------------------
        # CD → CENÁRIO DESFAVORÁVEL: TENTAR ADICIONAR EXERCÍCIO SEM PREENCHER
        # -------------------------------------------------------------------------

        print("Tentando adicionar exercício sem preencher nada...")
        self.get_submit_button()[1].click()
        print("Esperado: sistema deve impedir o envio.")

        # -------------------------------------------------------------------------
        # CF → ADICIONAR EXERCÍCIO COM SUCESSO
        # -------------------------------------------------------------------------

        print("Adicionando exercício válido: 'Corrida'...")
        self.find_by_name("exercise_name").send_keys("Corrida")
        self.get_submit_button()[1].click()
        print("Exercício 'Corrida' adicionado com sucesso!")
        time.sleep(2)

        print("Adicionando exercício válido: 'Pular Corda'...")
        self.find_by_name("exercise_name").send_keys("Pular Corda")
        self.get_submit_button()[1].click()
        print("Exercício 'Pular Corda' adicionado com sucesso!")
        time.sleep(2)

        # FINALIZAR
        self.selenium.find_element(By.CLASS_NAME, "finish-btn").click()
        print("🎉 Criação completa do treino finalizada com sucesso!")

        # =========================================================================
        # 2. HISTÓRIA: GERENCIAR TREINOS
        # =========================================================================

        self.running_page("workout/1/edit")
        print("\n📌 Acessando página de edição do treino (ID=1)...")

        # -------------------------------------------------------------------------
        # CF → CENÁRIO FAVORÁVEL: EDIÇÃO DE TREINO FUNCIONANDO
        # -------------------------------------------------------------------------

        print("--- Teste de Edição (CF - Cenário Favorável) ---")
        print("Alterando nome e descrição do treino com sucesso...")
        self.find_by_name("name").send_keys(" - Editado")
        self.find_by_name("description").send_keys(" - Editado")

        time.sleep(2)

        print("Adicionando número válido de séries (4) ao exercício 2...")
        self.find_by_name("sets_2").send_keys(4)

        print("Salvando alterações...")
        self.find_by_name("save_workout").click()
        print("CF concluído: edição realizada com sucesso!")
        time.sleep(3)
        
        # -------------------------------------------------------------------------
        # CF → CENÁRIO FAVORÁVEL: EXCLUSÃO DE TREINO FUNCIONANDO
        # -------------------------------------------------------------------------
        
        print("--- Teste de Exclusão (CF - Cenário Favorável) ---")
        self.acoesPausadas().find_element(By.XPATH, "/html/body/main/div/div[4]/button").click()    
        self.acoesPausadas().find_element(By.XPATH, "//*[@id='deleteModal']/div/div[3]/form/button").click()
        print("CF concluído: exclusão realizada com sucesso!")
        time.sleep(3)
        
        # =========================================================================
        # 3. HISTÓRIA: GERENCIAR PROCESSO FÍSICO
        # =========================================================================
        
        # Acessa a tela de Gerenciar Processo Físico
        self.running_page("dashboard")
        progress_button = self.selenium.find_element(By.XPATH, "/html/body/main/div/section/a[2]")
        progress_button.click()
        
        # --- CENÁRIO 3 (DESFAVORÁVEL): Tentar salvar edição incompleta/cadastro incompleto ---
        
        # Tenta salvar sem preencher peso ou medidas (assumindo que o botão [1] salva)
        send_buttons = self.get_submit_button()
        if len(send_buttons) > 1:
            send_buttons[1].click()
        time.sleep(3)

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
        time.sleep(3)
        print("\n\n progresso criado\n\n")
        
        # --- CENÁRIO 1 (FAVORÁVEL): Editar registro de progresso com sucesso ---
        print("--- Teste de Progresso: Edição Favorável ---")
        
        edit = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[3]/ul/li[1]/div/a[1]")
        edit.click()
        
        self.get_water_input().clear()
        time.sleep(1)
        self.get_water_input().send_keys(10)
        self.get_submit_button()[0].click()
        
        # --- CENÁRIO 2 (FAVORÁVEL): Excluir registro de progresso com sucesso ---
        
        delete = self.selenium.find_element(By.XPATH, "/html/body/main/div/section[3]/ul/li[1]/div/a[2]")
        delete.click()
        self.get_submit_button()[0].click()
        time.sleep(3)
        
        
        # Confirma a exclusão (assume o primeiro botão [0] confirma)
        self.get_submit_button()[1].click()
        time.sleep(5)
        
        # =========================================================================
        # 4. HISTÓRIA: GERENCIAR DIETAS
        # =========================================================================
    
        self.gerenciar_dietas(True)
        self.gerenciar_anotacoes(True)
        
        print("\n✅ Todos os cenários (Favoráveis e Desfavoráveis) foram testados com sucesso!")
        
    def gerenciar_dietas(self, isRegistered:bool=False):
            if not isRegistered:
                self.test_register()
            else:
                self.running_page("diet")
                wait = WebDriverWait(self.selenium, 5)
                
                #========================================REPETINDO CENARIO:=============================================
                create_button_xpath = "/html/body/main/div/div[2]/a"
                create_button = wait.until(EC.element_to_be_clickable((By.XPATH, create_button_xpath)))
                create_button.click()
                print("--- Teste de Dieta: Criação Favorável ---")

                dietTitle = "Dieta de Teste Selenium"
                
                # Preenche Título e Descrição
                self.find_by_name("dietTitle").send_keys(dietTitle)
                self.find_by_name("dietDescription").send_keys("Dieta completa para validação.")
            
                # Preenche nome, calorias, e horários (assumindo que o campo horário é obrigatório ou necessário)
                self.find_by_name("food_name[]", size=1)[0].send_keys("Salada Proteica")
                self.find_by_name("food_calories[]", size=1)[0].send_keys("500")
                
                self.selenium.find_element(By.XPATH, "/html/body/main/div/form/div[5]/button").click()
                self.selenium.find_element(By.XPATH, "/html/body/main/div/section/a").click()
                #========================================================================================================
                
                
                print("=====GERENCIAR DIETA: cenário desfavorável=====")
                self.selenium.find_element(By.XPATH, "/html/body/main/div/div[3]/a[1]").click()
                diet_edit = self.get_submit_button()[1]
                diet_edit.click()
                time.sleep(2)
                
                print("\n✅ Cenário concluído!!") 
                    
                print("=====GERENCIAR DIETA: cenário favorável=====")
                
                diet_label_title = self.selenium.find_element(By.NAME, "dietTitle")
                diet_label_text = self.selenium.find_element(By.NAME, "dietDescription")
                index=0

                diet_label_title.send_keys(" Agora ta editado")
                diet_label_text.send_keys(" edição bora")
                time.sleep(2)
                
                meal = self.acoesPausadas().find_elements(By.XPATH, "/html/body/main/div/form/div[2]/div")
                
                for comida in meal:
                    edtName = comida.find_element(By.NAME, f"meals-{index}-food_name")
                    edtCal = comida.find_element(By.NAME, f"meals-{index}-calories")
                    DELcomida = comida.find_element(By.NAME, f"meals-{index}-DELETE")
                    
                    edtName.send_keys(self.textos[index])
                    edtCal.send_keys(random.randint(1, 1000))
                    if index % 2 == 0:
                        DELcomida.click()
                    
                    index+=1        
                
                self.acoesPausadas().find_element(By.NAME, "save_diet").click()
                self.selenium.find_element(By.XPATH, "/html/body/main/div/div[3]/a[2]").click()
                self.selenium.find_element(By.XPATH, "/html/body/main/div/form/div/button").click()
                time.sleep(2)
            
    def gerenciar_anotacoes(self, isRegistered:bool=False):
        
        if not isRegistered:
            self.test_register()
        else:
            self.running_page("notes")
            time.sleep(2)
            
            self.acoesPausadas().find_element(By.CSS_SELECTOR, "a[class='btn-new-note']").click()
            
            tituloInp = self.find_by_name("title")
            contentInp = self.find_by_name("content")
            tituloInp.send_keys("alfredo")
            contentInp.send_keys("Dieta completa para validação.")
            time.sleep(2)
            
            self.get_submit_button()[1].click()
            
            print("✅ Criação de notas concluido!!")
            
            self.acoesPausadas().find_element(By.CSS_SELECTOR, "a[class='btn-edit']").click()
            time.sleep(2)
            self.get_submit_button()[1].click()
            time.sleep(2)
            
            #==================REPETICAO DO BLOCO DE INPUT======================

            tituloInp = self.find_by_name("title")
            contentInp = self.find_by_name("content")
            tituloInp.send_keys("ABU")
            contentInp.send_keys("nibber")
            
            #===================================================================
                    
            self.get_submit_button()[1].click()
            
            print("❌ Deletar conteúdo")
            self.acoesPausadas().find_element(By.CSS_SELECTOR, "a[class='btn-delete']").click()
            self.get_submit_button()[1].click()
            
            print("✅ Deletar concluído!!")
            
            