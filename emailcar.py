import smtplib
from email.message import EmailMessage

def send_email(receiving_email, cardict, senders_email, password):
    car = cardict['name']
    link = cardict['link']
    email = EmailMessage()
    email['from'] = 'Craigslist Updater'
    email['to'] = receiving_email
    email['subject'] = f'Craigslist: {car}'

    email.set_content(f'{car} just got posted on craigslist. {link}')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(senders_email, password)
        smtp.send_message(email)
        print('email sent')


