# IMPORTS 
import PySimpleGUI as sg
from validations import *

class WindowConstructs:
    def __init__(self):
        # Carregando a janela principal
        self.window = self.login_layout()

        # Instância para validar dados
        self.data_validation = DataValidation()

    # Janela de login
    def login_layout(self):
        layout = [
            [sg.Text("Faço login na sua conta", font=("Arial",18))],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Text("Email:"),sg.Push()],
            [sg.Push(),sg.Input(size=35, key="-EMAIL-LOGIN-"),sg.Push()],
            [sg.Push(),sg.Text("Senha:"),sg.Push()],
            [sg.Push(),sg.Input(password_char="*", size=35, key="-PASSWORD-LOGIN-"),sg.Push()],
            [sg.Push(),sg.Checkbox("Mantenha-me conectado"),sg.Push()],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Button("Entrar", key="-ENTER-ACCOUNT-"),sg.Button("Cadastrar", key="-REGISTER-"),sg.Button("Recuperar Conta", key='-RECOVERY-PASSWORD-'),sg.Push()]
        ]

        return sg.Window("Login",size=(372,300),layout=layout)

    # Janela de Registro
    def register_layout(self):
        layout_radio_button = sg.Column([[sg.Frame("Gênero:",[[sg.Radio("Masculino",default=True,size=(10,1),group_id=1, key="-SEXO-"),
        sg.Radio("Feminino",size=(10,1),group_id=1)]])]])
        INPUT_SIZE = 30

        layout_register = [
            [sg.Push(),sg.Text('Usuário:'),sg.Input(size=INPUT_SIZE, key="-USER-NAME-REGISTER-")],
            [sg.Push(),sg.Text('Email:'),sg.Input(size=INPUT_SIZE, key="-EMAIL-REGISTER-")],
            [sg.Push(),sg.Text('Telefone:'),sg.Input(size=INPUT_SIZE, key="-PHONE-REGISTER-")],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Text("Nascimento:"),sg.Input(key="-IN1-",size=23),
            sg.CalendarButton("data",target="-IN1-",format='%y-%m-%d',default_date_m_d_y=(1,None,2000),size=4)],
            [sg.Push(),sg.Text('Senha:'),sg.Input(size=INPUT_SIZE, key="-PASSWORD-REGISTER-")],
            [sg.Push(),layout_radio_button],
            [sg.Push(),sg.Button("Enviar", key="-REGISTER-USER-"),sg.Button("Entrar",key="-LOGIN-"),sg.Push()],
        ]

        return sg.Window("Cadastro",size=(372,300), layout=layout_register)
   
    # Janela para inserir o email de recuperação de conta
    def password_email_recovery_layout(self):
        layout = [
            [sg.Text("Recuperar Conta",font=24)],
            [sg.Text("Por favor, digite seu email para recuperar sua conta", colors="yellow")],
            [sg.Sizer(1,12)],
            [sg.Text("Email:"),sg.Input(key="-EMAIL-CODE-PASSWORD-RECOVERY-")],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Button("Obter Código", key="-OBTAIN-CODE-"),sg.Button("Entrar", key="-LOGIN-"),sg.Push()]
        ]
       
        return sg.Window("Email da Conta",size=(372,150),layout=layout)

    # Janela para inserir o código de recuperação de conta
    def recovery_code_layout(self):
        layout = [
            [sg.Text("Alterar senha",font=(18))],
            [sg.Text("Digite o código para alterar sua senha",colors="yellow")],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Text("Código:"),sg.Push()],
            [sg.Push(),sg.Input(size=18, key="-CODE-"),sg.Push()],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Button("Enviar Código", button_color="red", key="-SEND-CODE-"),sg.Button("Entrar",key="-ENTRAR-"),sg.Push()],
            [sg.Sizer(1,12)],
            [sg.Text("Não recebeu o código?"),sg.Text("Testando link no texto")]
        ]
       
        return sg.Window("Código",size=(372,215),layout=layout)
   
   # Janela para alterar a senha 
    def change_password_layout(self):
        layout = [
            [sg.Text("Senha",font=20)],
            [sg.Text("""senhas fortes incluem números, letras e sinais de pontuação""")],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Text("Digite uma nova senha:"),sg.Push()],
            [sg.Push(),sg.Input(size=24,key="-CHANGE-PASSWORD-01-"),sg.Push()],
            [sg.Push(),sg.Text("Confirmar a nova senha:"),sg.Push()],
            [sg.Push(),sg.Input(size=24,key="-CHANGE-PASSWORD-02-"),sg.Push()],
            [sg.Sizer(1,12)],
            [sg.Push(),sg.Button("Alter Senha",button_color="red", key="-ALTER-PASSWORD-"),sg.Button("Cancelar", key="-LOGIN-"),sg.Push()]
        ]


        return sg.Window("Senha",size=(388,230),layout=layout)

    def main(self):
        while True:
            event, value = self.window.read()
            match event:
                case "-LOGIN-":   
                    self.window.close()
                    self.window = self.login_layout()

                case "-ENTER-ACCOUNT-":
                    self.data_validation.login_validation(value["-EMAIL-LOGIN-"], value["-PASSWORD-LOGIN-"])

                case "-REGISTER-USER-":
                    self.data_validation.register_validation(value["-USER-NAME-REGISTER-"], 
                                                            value["-EMAIL-REGISTER-"],
                                                            value["-PHONE-REGISTER-"],
                                                            value["-IN1-"],
                                                            value["-PASSWORD-REGISTER-"],
                                                            value["-SEXO-"])
                    
                case "-REGISTER-":
                    self.window.close()
                    self.window = self.register_layout()

                case '-RECOVERY-PASSWORD-':
                    self.window.close()
                    self.window = self.password_email_recovery_layout()

                case "-OBTAIN-CODE-":
                    match self.data_validation.password_email_recovery_layout_validation(value["-EMAIL-CODE-PASSWORD-RECOVERY-"]):
                        case True:
                            self.window.close()
                            self.window = self.recovery_code_layout()      

                case "-SEND-CODE-":
                    match self.data_validation.recovery_code_validation(value["-CODE-"]):  
                        case True:
                            self.window.close()
                            self.window = self.change_password_layout()                  

                case "-ALTER-PASSWORD-":
                    self.data_validation.change_password_validation(value["-CHANGE-PASSWORD-01-"], value["-CHANGE-PASSWORD-02-"])

                case sg.WIN_CLOSED:
                    break
        self.window.close()

if __name__ == "__main__":
    ui = WindowConstructs()
    ui.main()
