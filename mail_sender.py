import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re
from key_event import Key_Event as ke
from colorama import Fore, Style, init

init(autoreset=True)

class Mail_Sender:

    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def send_email(company_emails):
        sender_email = os.getenv("EMAIL_SENDER")
        sender_password = os.getenv("EMAIL_PASSWORD")
        subject = "Açık Pozisyon Başvurusu Hk."
        body = """
        <html>
        <body>
            <p>Sayın Yetkili,</p>
            <p>Ben Ömer Özgür, yazılım geliştirme alanında bir Junior Developer olarak kariyerime devam ediyorum. Şu anda full stack, backend ve Flutter geliştirme konularında kendimi geliştirmekteyim. Çeşitli projelerde yer alarak edindiğim deneyimlerle, karmaşık sorunları sade ve anlaşılır çözümlerle basitleştirme yeteneğimi artırdım.</p>
            <p>Yazılım dünyasında hızlı öğrenme ve uygulama becerilerimle, kullanıcı dostu ve etkili çözümler üretmeye odaklanıyorum. Firmanızda yazılım geliştirici olarak çalışmak ve ekibinize değer katmak için sabırsızlanıyorum. Detaylı özgeçmişim ekte yer almaktadır.</p>
            <p>Değerlendirmeniz sonucunda bir görüşme imkanı sağlayabilirsek, sizi daha yakından tanımaktan memnuniyet duyarım. Vakit ayırdığınız için teşekkür eder, geri dönüşlerinizi sabırsızlıkla beklerim.</p>
            <p>Saygılarımla,<br>Ömer Özgür<br>0533 659 2385<br>
            <a href="https://www.linkedin.com/in/%C3%B6mer-%C3%B6zg%C3%BCr-0528282a5/">LinkedIn Profilim</a><br>
            <a href="https://github.com/omerozgur23">GitHub Profilim</a></p>
        </body>
        </html>
        """

        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        try:
            server = smtplib.SMTP(smtp_server, smtp_port) # SMTP Sunucusuna bağlanıldı
            server.starttls() # TLS(Güvenli Bağlantı) başlatıldı
            server.login(sender_email, sender_password) # Oturum açıldı

            pdf_filename = "Omer_Ozgur.pdf"
            pdf_filepath = "C:/Users/omero/Desktop/Omer_Ozgur.pdf"

            for company_email in company_emails:
                try:
                    msg = MIMEMultipart()
                    msg["From"] = sender_email
                    msg["To"] = company_email
                    msg["Subject"] = subject
                    msg.attach(MIMEText(body, "html"))

                    with open(pdf_filepath, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {pdf_filename}"
                    )

                    msg.attach(part)
                    server.sendmail(sender_email, company_email, msg.as_string())
                    print(f"{Fore.GREEN}\n[✓] Email successfully sent to {Fore.YELLOW}{company_email}")
                except Exception as e:
                    print(f"{Fore.RED}\n[X] Failed to send email to {company_email}: {e}")
            print(f"{Fore.GREEN}\nAll emails were processed!")
        except Exception as e:
            print(f"{Fore.RED}\n[X] Failed to connect to SMTP server: {e}")
        finally:
            server.quit()
            ke.hide_cursor()
            print(f"{Fore.YELLOW}\nPress Space to back menu")
            key = ke.get_key()
            while key == ord(' '):
                pass
            return
    
    def get_emails_from_txt(file_path):
        if not os.path.exists(file_path):
            print(f"{Fore.RED}{file_path} not found")
            return []
        
        with open(file_path, "r") as file:
            emails = [line.strip() for line in file]
        
        return emails
    
    def enter_email_manually():
        while True:
            ke.show_cursor()
            try:
                num_of_companies = int(input(f"{Fore.YELLOW}How many companies do you want to send an e-mail to? (Enter a number): {Style.RESET_ALL}"))
                break
            except ValueError:
                print(f"{Fore.RED}Invalid input! Please enter a valid number.{Style.RESET_ALL}")

        company_emails = []
        enter_email_text = "E-Mail: "
        for i in range(num_of_companies):
            while True:
                email = input(f"{Fore.YELLOW}{i+1}. {enter_email_text}{Style.RESET_ALL}")

                if Mail_Sender.is_valid_email(email):
                    company_emails.append(email)
                    break
                else:
                    print(f"{Fore.RED}Invalid email format! Please enter a valid e-mail address.{Style.RESET_ALL}")
        return company_emails
    
    def confirm_and_send_emails(company_emails):
        if not company_emails:
            print(f"\n{Fore.RED}File is empty!")
            print(f"{Fore.YELLOW}\nPress Space to go back to the menu")
            key = ke.get_key()
            ke.clear_screen()
            while key == ord(' '):
                pass
            return
        while True:
            ke.show_cursor()
            confirmation = input(f"\n{Fore.YELLOW}E-mails are sent to the e-mail addresses in the table. Do you approve this process? (Y/n) :{Style.RESET_ALL}").strip().lower()

            if confirmation == "" or confirmation == "y":
                print(f"\n{Fore.GREEN}Sending emails...")
                Mail_Sender.send_email(company_emails)
                ke.clear_screen()
                break
            elif confirmation == "n":
                ke.clear_screen()
                ke.hide_cursor()
                return
            else:
                print(f"{Fore.RED}Invalid entry. Please enter 'y' or 'n'.")