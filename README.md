### Sistema de Autenticação  em Python

O sistema é uma aplicação desktop simples com cadastro e recuperação  de contas de usuários. O software foi construido usando `MySql` como banco de dados e `PySimpleGUI` para interface gráfica. O sistema tem como objetivo fins de estudos práticos, para compreenção e o funcionamento de um sistema de login completo, todo projeto foi feito sem auxilio de framworks, apenas com python puro. 

___
#### Configurações do projeto

Crie e ative um ambiente virtual 


Windows 

`python3 -m venv C:\path\to\new\virtual\environment`


`PS C:\> <venv>\Scripts\Activate.ps1`

Instale a depêndencias do projeto

`python3 -m pip install -r requirements.txt`

Configurações das variáveis de ambiente para o servidor smtp:
Crie um arquivo `.env` nas pasta `\src\` em seguida insira as configurações. 

```
HOST=localhost
USER=root
PASSWORD="senha do servidor SMTP"
DATABASE="nome do banco de dados"
SMTPEMAIL="email do usuário"
SMTPPASS="senha do usuário"
```
Configurões do servidor SMTP no arquivo `validation.py`. 

Exemplos de domínio do servidor: 

smtp.gmail.com

smtp-mail.outlook.com

`host` é o domínio
`port` a porta do servidor

As opções de configuração incluem:
Porta 25, 465 ou 587. Protocolos SSL e TLS.

configure a instância:
```
self.smtp = SmtpServer(host, port) # Use a porta 587
```

Depois de todas as configurações feitas, execute o arquivo `windows.py`

### Telas do projeto

Tela de login

<img title="login" alt="tela de login" src="img/2025-04-04_21-42.png">

Tela de cadastro de usuário
<img title="register" alt="tela de cadastro" src="img/2025-04-04_21-42_1.png">

Tela para inserir o email de recuperação de conta
<img title="password_email_recovery_layout" alt="tela de email para recuperação de conta" src="img/2025-04-04_21-43.png">

Tela para inserir o código para alterar senha
<img title="recovery_code_layout" alt="tela do código de recuperação de conta" src="img/2025-04-04_21-43_1.png">

Tela para alterar a senha do usuário
<img title="change_password_layout" alt="tela para alterar a senha" src="img/2025-04-04_21-44.png">

____

### Contribuição do projeto

Solicitações `pull` são aceitas. Para ajudar no projeto abra uma Issues. 









