# MerakiAutoRotatePSK
<<<<<<< HEAD

This python script is my first one i have done and doing it with Meraki API was a great experience. I took alot of the inspiration from this commmunity post [Automatic rotating PSK for wireless](https://community.meraki.com/t5/Wireless-LAN/Automatic-rotating-PSK-for-wireless/m-p/65991)
BrechtSchamp did an amazing job with the script and it was about as turn key a solution as you can get. Some main points on this script is that it assumes you know your organization ID and Network ID for your Meraki Environment. How i got my org ID was by accident on sandbox, here is the link i used [Get-Oraganizations](https://developer.cisco.com/meraki/api-v1/#!get-organizations)

1. Create Meraki API key for your user in Meraki Dashboard [Meraki API Overview](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API)
2. Get your Org ID if you dont know it [Get-Oraganizations](https://developer.cisco.com/meraki/api-v1/#!get-organizations).
3. Get the Network ID of the network you want to use, [Get Networks](https://developer.cisco.com/meraki/api-v1/#!get-organization-networks), I had a template and used this to get the template Network ID.
4. Copy and paste this code into Visual Studio.
5. Import the Libraries needed on top.
6. Fill out the obejcts under the import section. **Note** SSIDs are number start with 0 ( learned that the hard way )
7. In the img on line 53 input the SSID for the QR code and Encryption. Reference[QRcode info in Wikipedia](https://en.wikipedia.org/wiki/QR_code)
8. Next look at the email bodies, there are email types plain text and HTML. I recommend editing as needed the HTML body to brand it to your needs. 
9. Line 100 you have the SMTP server, in this example i used gmail as a proof of concept for the project but change as needed. 

Here are some other links i used as well to research this. 
[Sending Emails with Python](https://realpython.com/python-send-email/) Great breakdown of the smtplib and ssl modules.
[Random String](https://pynative.com/python-generate-random-string/) Goes into more detail about the random string, take a look and customize as needed. 
[Sending Emails with images using python](https://www.pauldesalvo.com/sending-an-html-formatted-email-with-attachments-through-gmail-using-python/) Shows how to attach the image in the email 
[Stack overflow how to embed picture in email](https://stackoverflow.com/questions/7755501/embed-picture-in-email/60174103?noredirect=1#comment118270288_60174103) Another great example. 
[QRcode generation option 1](https://pypi.org/project/qrcode/) I used this one but the one below is just as good. 
[QRcode generation option 2](https://www.geeksforgeeks.org/wi-fi-qr-code-generator-using-python/)

I hope this code helps you solve a problem in your environment. 


## License 

## MIT License

Copyright (c) [2022] [Nicholas Calcutti]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
=======
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/calcuttin/MerakiAutoRotatePSK)

Meraki Auto rotate psk on SSID and email out new password with QRcode
>>>>>>> f75932131d12217c0d739a15e1ca5e484980ed25
