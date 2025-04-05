# IMPORTAÇÕES 
import hashlib
import re
import PySimpleGUI as sg
from database import DatabaseConnector
from smtp_server import SmtpServer

# Classe com funções regex
class RegularExpression:
    def __init__(self):
        self.username_regex = r"^[A-Za-záàâãéèêíïóôõöúçñ]{6,}$"
        self.email_regex = r"^[\.A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+\.[a-z]{3}(\.[a-z]{2})?$"
        self.phone_number_regex = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
        self.password_regex = r"[0-9A-Za-záàâãéèêíïóôõöúçñ@#$%¨&*\"()-+={}\[\]~^,.]{4,}$"
        self.code_regex = r"^[A-Z0-9]{4}$"

# Classe para transformar a senha em sha256 base64
class Hash:
    def __init__(self, password):
        self.password = str(password).encode()
    
    def encrypt(self):
        hash_password = hashlib.sha256(self.password).hexdigest()
        return hash_password

# Classe principal para validar dados, tratar erros exceções
class DataValidation(Hash):
    def __init__(self):
        self.regex = RegularExpression()
        self.database = DatabaseConnector()
        self.smtp = SmtpServer("smtp.gmail.com", 587)


    def register_validation(self, username, email, phone_number, data, password, sexo):
        if re.search(self.regex.username_regex, username) == None:
            sg.PopupError("Nome de usuário inválido! (mínimo 6 letras, sem números)")
            return False
        
        if re.search(self.regex.email_regex, email) == None:
            sg.PopupError("E-mail inválido! (digite um e-mail válido para continuar)")
            return False

        if re.search(self.regex.phone_number_regex, phone_number) == None:
            sg.PopupError("Telefone inválido! (formato esperado: XX XXXXX-XXXX)")
            return False

        if re.search(self.regex.password_regex, password) == None:
            sg.PopupError("Senha Inválida! (senha com no mínimo 4 caracteres)")
            return False
        
        else:
            match sexo:
                case True:
                    sexo = "M"
                case False:
                    sexo = "F"

            self.database.insert_register(username, email, phone_number, data, Hash(password).encrypt(), sexo)
            return True
        
    def login_validation(self, email, password):
        if re.search(self.regex.email_regex, email) == None:
            sg.PopupError("E-mail inválido!")
            return False
        
        if re.search(self.regex.password_regex, password) == None:
            sg.PopupError("Senha Inválida! (senha com no mínimo 4 caracteres)")
            return False
        
        else:
            try:
                self.database.select_change_email(email)
                self.database.select_change_password(Hash(password).encrypt())
            except IndexError:
                sg.PopupError("Dados invalidos! (tente novamente)")
            else:
                sg.Popup("Login feito com sucesso!")
                return True
        
    def password_email_recovery_layout_validation(self, email):
        if re.search(self.regex.email_regex, email) == None:
            sg.PopupError("E-mail inválido! (digite um e-mail válido para continuar)")
            return False
        
        else:
            user_id = self.database.select_id_users(email)
            if user_id == None:
                sg.PopupError("Usuário não encontrado")
                return False
            else:
                self.smtp.send_email(email)
                code = self.smtp.code_generator()
                self.database.insert_table_codes_user_id(user_id[0] ,code)
                sg.Popup("Enviamos um código para o seu e-mail")
                return True
            

    def recovery_code_validation(self, code):
        if re.search(self.regex.code_regex, code) == None:
            sg.PopupError("Código inváido (digite um código valido para continuar)")
            return False
        else:
            user_code = self.database.select_code_user_id(code)
            if user_code == []:
                sg.PopupError("Código não encotrado (digite um código valido)")
            else:
                return True

    def change_password_validation(self, password_01, password_02):
        if re.search(self.regex.password_regex, password_01) == None or re.search(self.regex.password_regex, password_02) == None:
            sg.PopupError("Senha Inválida! (senha com no mínimo 4 caracteres)")  
            return False
        if password_02 != password_01:
            sg.PopupError("Você está usando uma senha diferente (coloque senhas iguais!)")       
            return False   
        else:
            passoword_database = self.database.select_change_password(password_01)
            if password_01 == passoword_database:
                sg.PopupError("Senha Inválida! (tente outra)")
            else:
                sg.Popup("Senha alterada com sucesso!")
                return True
    
