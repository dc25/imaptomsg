#! /usr/bin/python
import imaplib, time
import os
from tempfile import NamedTemporaryFile

msgEmail = "" # text message email address here.
loginName = "" # imap login name ; gmail uses id@gmail.com
loginPassword = "" # imap password

def textMessage(msg):
    filehandle = NamedTemporaryFile()
    filehandle.write(msg)
    filehandle.flush()
    systemCmd = "mutt " + msgEmail + " > /dev/null 2>&1 < " + filehandle.name
    os.system(systemCmd)
    filehandle.close()


imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
imap.login(loginName, loginPassword)
imap.select()
typ, msgnums = imap.search(None, 'UNSEEN')
unseen0 = set(msgnums[0].split())
while 1:
    time.sleep(20)
    imap.select()
    typ, msgnums = imap.search(None, 'UNSEEN')
    unseen1 = set(msgnums[0].split())
    for n in unseen1 - unseen0:
        t, hdr_from    = imap.fetch(n, '(BODY.PEEK[HEADER.FIELDS (FROM)])')
        t, hdr_subject = imap.fetch(n, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
        t, text        = imap.fetch(n, '(BODY.PEEK[TEXT])')
        textMessage( hdr_from[0][1] + hdr_subject[0][1] + text[0][1])
    unseen0 = unseen1

imap.close()
imap.logout()
