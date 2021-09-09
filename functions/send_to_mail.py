from zipfile import ZipFile
import os, smtplib
from email import encoders
from email.message import Message
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from time import sleep


LOGIN = 'testingfor0219@gmail.com'
PASSWORD = 'ghjcnj1818'

def do_zip_file(folder_path, last_four_numbers_wincode):
    zip_name = last_four_numbers_wincode + '.zip'
    with ZipFile(folder_path + zip_name, 'w') as myzip:
        os.chdir(folder_path)
        for elem in os.listdir():
            if elem[-4:] != '.zip':
                myzip.write(elem)
                os.remove(elem)
    zip_name = os.path.abspath(zip_name)
    send_message_to_user(zipname=zip_name)

def send_message_to_user(zipname):
    message = MIMEMultipart()
    message['From'] = LOGIN
    message['To'] = 'i_konov@ukr.net'
    message['Subject'] = 'Тема письма'
    body = '''Текст письма'''
    name_to_file_on_mail = 'Имя файла'
    message.attach(MIMEText(body, 'plain'))
    binary_zip = open(zipname, 'rb')
    payload = MIMEBase('application', 'zip', Name=name_to_file_on_mail+'.zip')
    payload.set_payload((binary_zip).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=zipname)
    message.attach(payload)
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(LOGIN, PASSWORD)
    text = message.as_string()
    session.sendmail(LOGIN, 'i_konov@ukr.net', text)
    binary_zip.close()
    session.quit()
    os.remove(zipname)
    # empty_folder = os.path.dirname(zipname)
    # os.close(empty_folder)
    # os.rmdir(empty_folder)

   
