
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/calcuttin/MerakiAutoRotatePSK)
# MerakiAutoRotatePSK

This python script is my first one i have done and doing it with Meraki API was a great experience. I took alot of the inspiration from this commmunity post [Automatic rotating PSK for wireless](https://community.meraki.com/t5/Wireless-LAN/Automatic-rotating-PSK-for-wireless/m-p/65991)
BrechtSchamp did an amazing job with the script and it was about as turn key a solution as you can get. Some main points on this script is that it assumes you know your organization ID and Network ID for your Meraki Environment. How i got my org ID was by accident on sandbox, here is the link i used [Get-Oraganizations](https://developer.cisco.com/meraki/api-v1/#!get-organizations)

1. Create Meraki API key for your user in Meraki Dashboard [Meraki API Overview](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)
Below is an example of the Always on Dev-Net Sandbox environment. As you can see this user already as 2 API keys.
<img width="1710" alt="Screen Shot 2022-09-09 at 4 17 35 PM" src="https://user-images.githubusercontent.com/20007352/189436210-b782095f-e754-4421-90ac-9ed01cbd126d.png">
2. Get your Org ID if you dont know it [Get-Oraganizations](https://developer.cisco.com/meraki/api-v1/#!get-organizations). Here is another way of getting orgID https://documenter.getpostman.com/view/897512/SzYXYfmJ#5ac4bfa9-de2b-4fc9-b242-514914cd6a11 
    <img width="1459" alt="Postman get organizations" src="https://user-images.githubusercontent.com/20007352/189436004-c3078852-02a4-40d1-9560-cdf3cd1a43f5.png">
    Run this in your browser after you logged into the dashBoard https://api.meraki.com/api/v1/organizations 
    <img width="1708" alt="API in Browser" src="https://user-images.githubusercontent.com/20007352/189435894-aa45ca03-926c-40ad-8743-ff125f7bca8b.png">
3. Get the Network ID of the network you want to use, [Get Networks](https://developer.cisco.com/meraki/api-v1/#!get-organization-networks)
<img width="1396" alt="Screenshot of get Organizations networks API on dev-net" src="https://user-images.githubusercontent.com/20007352/189436592-52d64dfc-d898-4a0e-b805-c424de9b34a5.png">
4. Copy and paste this code into Visual Studio. Here you can see i have my python virtual envionment setup in the project. i suggest to do the same, here is a link [Python Virtual Environments] https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
<img width="1301" alt="Screenshot of users VSCODE" src="https://user-images.githubusercontent.com/20007352/189437055-19b364f8-6e9a-4888-98d7-89c0f59a3e96.png">

 ```python
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
```

5. Import the Libraries needed on top.
    (See requirements.txt)

6. Fill out the obejcts under the import section. **Note** SSIDs are number start with 0 ( learned that the hard way )

7. In the img on line 53 input the SSID for the QR code and Encryption. Reference[QRcode info in Wikipedia](https://en.wikipedia.org/wiki/QR_code)
<img width="714" alt="image" src="https://user-images.githubusercontent.com/20007352/189437688-1349313b-f59a-4313-ae7a-fafbdb4626f1.png">

8. Next look at the email bodies, there are email types plain text and HTML. I recommend editing as needed the HTML body to brand it to your needs. 

9. Line 100 you have the SMTP server, in this example i used gmail as a proof of concept for the project but change as needed. 
```python
   context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, email_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
```

10. Office 365 Settings 

```python 
  with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, email_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        server.quit()
```

Here are some other links i used as well to research this. 
[Sending Emails with Python](https://realpython.com/python-send-email/) Great breakdown of the smtplib and ssl modules.

[Random String](https://pynative.com/python-generate-random-string/) Goes into more detail about the random string, take a look and customize as needed. 

[Sending Emails with images using python](https://www.pauldesalvo.com/sending-an-html-formatted-email-with-attachments-through-gmail-using-python/) Shows how to attach the image in the email 

[Stack overflow how to embed picture in email](https://stackoverflow.com/questions/7755501/embed-picture-in-email/60174103?noredirect=1#comment118270288_60174103) Another great example. 

[QRcode generation option 1](https://pypi.org/project/qrcode/) I used this one but the one below is just as good.

[QRcode generation option 2](https://www.geeksforgeeks.org/wi-fi-qr-code-generator-using-python/)

I hope this code helps you solve a problem in your environment. 

