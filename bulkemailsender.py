
# coding: utf-8

# In[1]:


import smtplib
import mimetypes
import email
import email.mime.text
from email.utils import COMMASPACE, formatdate 
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import unicodecsv


# In[2]:


details = []
config_details = []

with open('data/data.csv', 'rb') as data_file:
    reader = unicodecsv.DictReader( data_file )
    details = list( reader )
    
print( details )

with open('config/config.csv', 'rb') as config_file:
    reader = unicodecsv.DictReader( config_file )
    config_details = list( reader )
    
print( config_details[0]['from_email'] )
    


# In[3]:


From = config_details[0]['from_email']

print( From )

for data in details:
    to_email = data['email']
    img_path = data['img_path']
    
    msg = email.mime.multipart.MIMEMultipart()
    
    msg['From'] = From
    msg['To'] = to_email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = config_details[0]['subject']
    
    email_message = config_details[0]['message']
    
    msg.attach( email.mime.text.MIMEText( email_message ) )

    smtp = smtplib.SMTP( config_details[0]['smtp'] )
    smtp.starttls()
    smtp.login( From, config_details[0]['key']) # smtp email/password or key
    
    ctype, encoding = mimetypes.guess_type(img_path)
    
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    
    maintype, subtype = ctype.split('/', 1)
    
    fp = open(img_path, 'rb')
    part = email.mime.image.MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
    
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % img_path)
    msg.attach(part)

    try:
        smtp.sendmail(From, to_email, msg.as_string())
    except:
        print("Mail not sent for ", to_email )
    else:
        print("Mail sent to ", to_email )
    smtp.close()


