
from django.core.mail import EmailMessage

def send_mail(subject, body, from_email, recipient_list, fail_silently=False):
    to = [addr for addr in recipient_list]

    #Doing a separate email for each person so we can allow unsubscription links
    for addr in to:

        print "Emailing: %s" % addr
        print "Subject: %s" % subject


        html_content = '%s <br>Sent by 4xB' % body

        msg = EmailMessage(subject, html_content, from_email, [addr])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send(fail_silently = fail_silently)