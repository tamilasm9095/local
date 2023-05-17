import smtplib
from email.mime.text import MIMEText
def errorEmail(e,subj):
    # Send an email with the error message and traceback
    msg = MIMEText(e)
    msg['From'] = 'tamilasm9095@gmail.com'
    msg['To'] = 'tamilselvan.s@asmltd.com'
    msg['Subject'] = f'{subj}'
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('tamilasm9095@gmail.com', 'esxxurifnzqvljsd')
    smtp.sendmail('tamilasm9095@gmail.com', 'tamilselvan.s@asmltd.com', msg.as_string())
    smtp.quit()
