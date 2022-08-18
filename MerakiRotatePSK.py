import requests
import random
import string
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import qrcode 
#input path for QRcode image
image_paths = [""]

api_key = "e" # enter your meraki api key here
network_id = "" # enter the network id of the network you want to change here
ssid_number = 0 # enter the number of the ssid you want to change here 0 - 14
password_length = 15  # enter the desired length of the new PSK min 8 max 63
character_types = string.ascii_lowercase + string.ascii_uppercase + string.digits # remove or change according to needs
email_password = "" # enter a gmail app password here. (cannot use less secure access , use gmail app password process)
sender_email = "" # sending gmail address
receiver_email = "" # receiving address(es) use ["email1, email2, email3"] for multiple addresses



def random_string(stringlength=password_length):
    return ''.join(random.choice(character_types) for i in range(stringlength))


def set_new_psk(new_psk, ssid=ssid_number):
    url = "https://api.meraki.com/api/v0/networks/" + network_id + "/ssids/" + str(ssid)  #remove the spaces the I inserted to get around a community bug
    payload = "{\r\n    \"psk\": \""+str(new_psk)+"\"\r\n}"
    headers = {
        'Accept': "*/*",
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Cisco-Meraki-API-Key': api_key
    }

    response = requests.request("PUT", url, data=payload, headers=headers)

    print(str(response.status_code) + " - " + response.text)
    return(response.status_code)
 
    
def send_password_email(new_psk_param):    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Email Subject"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    #create QEcode Image for Email 
    #Formats:
    #Common format: WIFI:S:<SSID>;T:<WEP|WPA|blank>;P:<PASSWORD>;H:<true|false|blank>;;
    #sample : WIFI:S:MySSID;T:WPA;P:MyPassw0rd;;
    img = qrcode.make('WIFI:S:SSIDNAME;T:WPA;P:'+str(new_psk_param)+';;')
    type(img) # qrcode,image.pil.PilImage
    img.save("WIFI.png")
    
    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    We've changed the Wi-Fi password to: {new_psk}
    Kind regards,
    IT Team""".format(new_psk=new_psk_param)
    html = """\
    <html>
      <body>
      <img src="<add branding here>">
        <div>Hi,<br>
           <br>
           We've changed the Wi-Fi password for SSID to: <br>
           <h1>{new_psk}</h1>
           <p> QRcode scan for mobile phones.</p> <br>
           <img src="cid:image1"> </img> <br>
           Kind regards,<br>
           IT Team
        </div>
      </body>
    </html>
    """.format(new_psk=new_psk_param)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    
    #Attach Image 
    fp = open('WIFI.png', 'rb') #Read image 
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
 
new_psk = random_string(password_length)
if set_new_psk(new_psk) == 200:
    send_password_email(new_psk)