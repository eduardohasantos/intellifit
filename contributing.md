# 🏋️ Guia de Contribuição para o Projeto IntelliFit

Seja bem-vindo(a) à comunidade de desenvolvimento do **IntelliFit**! Agradecemos por seu interesse em contribuir com este projeto, uma plataforma de registros e gerenciamentos da sua rotina de atividades físicas personalizada, desenvolvida com o framework Django. O IntelliFit surgiu como um projeto acadêmico da CESAR School com o objetivo de ajudar pessoas a otimizarem seu tempo para fazer registros sobre seu treino e atividades físicas.

Este guia tem como objetivo orientá-lo sobre como colaborar com o projeto, seja implementando novas funcionalidades, corrigindo bugs ou propondo melhorias. Recomendamos a leitura completa antes de começar, para entender nosso fluxo de trabalho e as boas práticas adotadas pela equipe.

---

## 🚀 Como Você Pode Contribuir?

Você pode ajudar de diversas formas:

- Desenvolvendo novas funcionalidades (ex: Aba de Receitas Saudáveis, Alimentos não Calóricos, Treinos recomendados ...)
- Corrigindo erros e bugs detectados no sistema
- Sugerindo melhorias na interface (UI/UX)
- Melhorando a organização do backend
- Criando ou melhorando a documentação

> 💡 caso deseje relatar algum Bug, confira a aba [**Issues**](https://github.com/eduardohasantos/intellifit/issues/new) do repositório.

---

## ⚙️ Preparando Seu Ambiente

1. **Faça um fork do projeto**  
   Crie um fork do repositório [`eduardohasantos/intellifit`](https://github.com/eduardohasantos/intellifit) para a sua conta no GitHub.

2. **Clone o fork localmente**  
   ```bash
    git clone https://github.com/eduardohasantos/intellifit.git
   cd intellifit
   ```

3. **Crie uma nova branch para suas alterações**  
   ```bash
   git checkout -b nome-da-sua-nova-branch
   ```  
   Use nomes descritivos como `fix/bug-gerenciamento-treino` ou `feature/Receitas`.

---

## 🛠️ Configurando o Ambiente de Desenvolvimento

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Aplique as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

4. Execute o servidor local:

   ```bash
   python manage.py runserver
   ```

---

## ✅ Regras e Boas Práticas

- 🎨 Mantenha o estilo visual consistente .
- 🧪 Teste suas alterações antes de abrir um Pull Request.
- 📝 Utilize mensagens de commit claras e explicativas.

---


## 📄 Submetendo seu Pull Request

1. Commit suas alterações:

   ```bash
   git add .
   git commit -m "feat: adiciona funcionalidade X"
   ```

2. Envie sua branch para seu fork:

   ```bash
   git push origin nome-da-sua-branch-nova
   ```

3. Vá até o seu repositório no GitHub e clique em **"Compare & pull request"**.

4. Preencha o título e a descrição detalhando o que foi feito e por quê.

5. Aguarde a revisão e possíveis comentários da equipe.

---

## 👥 Revisão e Agradecimentos

Seu PR será revisado com atenção e carinho! A revisão poderá incluir:

- Sugestões de melhoria no código
- Solicitação de ajustes para manter a consistência do projeto
- Discussões sobre design ou funcionalidade

Agradecemos desde já pela sua contribuição! Cada colaboração nos aproxima de oferecer uma plataforma mais útil, bonita e funcional para os usuários.

---

## 📬 Contato

Dúvidas, sugestões ou problemas? Entre em contato com o time:

- [**Miguel Tojal Duarte**](https://github.com/mtojald) | [LinkedIn](https://www.linkedin.com/in/mtojald/) | E-mail: mtd@cesar.school
- [**Eduardo Henrique Alves dos Santos**](https://github.com/eduardohasantos) | [LinkedIn](https://www.linkedin.com/in/eduardohasantos/) | E-mail: ehas@cesar.school
- [**Yan Ribeiro Nunes**](https://github.com/yan791) | [LinkedIn](https://www.linkedin.com/in/yan-ribeiro-nunes/) | E-mail: yrn@cesar.school
- [**Sophia Maria Brito Serafim de Araujo**](https://github.com/sophiabritoa) | [LinkedIn](https://www.linkedin.com/in/sophia-brito-02b445346/) | E-mail: smbsa@cesar.school
- [**Mariana Maliu**](https://github.com/marianamaliu) | [LinkedIn](https://www.linkedin.com/in/mariana-maliu-montarroyos-6572a035a/) | E-mail: mmam@cesar.school
- [**Gabrielle Capezzera Vital de Castro**](https://github.com/marianamaliu) | [LinkedIn](https://www.linkedin.com/in/gabriellecvital/) | E-mail:gcvc@cesar.school
- [**Arthur Coelho**](https://github.com/ArthurMatias57) | [LinkedIn](https://www.linkedin.com/in/arthur-c-m-20079a335/) | E-mail:acmm@cesar.school
