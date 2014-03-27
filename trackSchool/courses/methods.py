import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(subject, body, from_email, recipient_list, fail_silently=False):
    to = [addr for addr in recipient_list]
    username = os.getenv("smptusername")
    password = os.getenv("smptpass")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)

    #Doing a separate email for each person so we can allow unsubscription links
    for addr in to:

        print "Emailing: %s" % addr
        print "Subject: %s" % subject

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = addr

        # Create the body of the message (a plain-text and an HTML version).
        """text = body"""
        html = body

        # Record the MIME types of both parts - text/plain and text/html.
        """part1 = MIMEText(text, 'plain')"""
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        """msg.attach(part1)"""
        msg.attach(part2)

        server.sendmail(from_email, addr, msg.as_string())

    server.quit()


