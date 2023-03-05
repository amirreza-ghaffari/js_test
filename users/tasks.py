import imaplib
from django.conf import settings
import email
from email.header import decode_header
from celery import shared_task
from bs4 import BeautifulSoup
from .models import Member, CustomUser, EmailResponse
from notifications.signals import notify


@shared_task()
def email_response(n=5):
    imap = imaplib.IMAP4_SSL('mail.digikala.com')
    imap.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    # total number of emails
    messages = int(messages[0])
    if messages < n:
        n = messages

    for i in range(messages, messages - n, -1):
        # fetch the email message by ID
        body = None
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                from_, encoding = decode_header(msg.get("From"))[0]
                if isinstance(from_, bytes):
                    from_ = from_.decode(encoding)
                # print("Subject:", subject)
                # print("From:", from_)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                else:
                    body = msg.get_payload(decode=True).decode()
                if body:
                    soup = BeautifulSoup(body, "html.parser")
                    res_text = soup.find("body").text.split("From: Digikala Crisis.software")[0].strip().replace('\n\n', '')
                    member_email = from_.split('<')[1][:-1]
                    try:
                        member = Member.objects.get(email__iexact=member_email.lower())
                        email_res_obj, created = EmailResponse.objects.get_or_create(member=member, message=res_text)
                        if created:
                            notify.send(CustomUser.objects.first(), recipient=CustomUser.objects.all(), verb='you reached level 10', description=res_text)

                    except Member.DoesNotExist:
                        pass

    # close the connection and logout
    imap.close()
    imap.logout()
