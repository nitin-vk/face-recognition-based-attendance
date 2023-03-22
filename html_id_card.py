import pandas as pd 
import pdfkit
from datetime import datetime, timedelta
import code128
import random

class HTML_ID_CARD():
    def __init__(self,usn,name,branch,year,section):
            self.usn=usn
            self.name=name
            self.branch=branch
            self.year=year
            self.section=section
    def HTMLgen(self):
        html= r"""<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="card.css"><body><div class="face face-front" ><img src="new_front.png"></div><div id="infoi"><img src="@picture" height="89.5" width="83" />
        <div style="margin-left: 1.3cm;margin-top: -0.6cm;">
            <br>
            <div style="font-size: 0.7em;margin-top: 5%;font-family: sans-serif;color: aliceblue;text-transform: uppercase;"><b>@fname</b></div><br>
        <div style="font-size: 0.7em;margin-top: -0.4cm;font-family: sans-serif;color: aliceblue;text-t ransform: capitalize;">@function</div>
        </div>
    </div>
    <div id="info">
        <br><div style="font-size: 0.7em;margin-top: 0.6%;font-family: sans-serif;text-transform: uppercase;">@code</div>
        <br><div style="font-size: 0.7em;margin-top: -0.6%;font-family: sans-serif;text-transform: capitalize;">@date_of_birth</div>
        <br><div style="font-size: 0.7em;margin-top: -0.6%;font-family: sans-serif;text-transform: capitalize;">@expiration_date</div>
    </div>
    <div id="BARCODE"><img src="../RES/bar.PNG"  height="20" width="120"/></div>

</body>"""
        html = html.replace("@picture",'face.jpg')
        html = html.replace("@code",self.branch)
        html = html.replace("@fname",self.name)
        html = html.replace("@function",self.usn)
        html = html.replace("@date_of_birth",self.year)
        html = html.replace("@expiration_date",self.section)
        f= open("index.html","w")
        f.write(html)
        f.close()
        return 
#generate a file bar.png contains barcode of the 10 digits code  
    def BARgen(code):
        code128.image(code).save("../RES/bar.png")
        return
#generate costum pdf file using the existing html file // code argument is only to name the file generated
    def PDFgen(self,code):
        print("code is {}".format(code))
        config = pdfkit.configuration(wkhtmltopdf='D:\\Downloads 2.0\\HTML TO PDF\\wkhtmltox\\bin\\wkhtmltopdf.exe')
        options = {'dpi': 365,'margin-top': '0in','margin-bottom': '0in','margin-right': '0in','margin-left': '0in','page-size': 'A8',"orientation": "Landscape",'disable-smart-shrinking': '',"enable-local-file-access": ""}
        pdfkit.from_file('index.html', "D:\ID_CARDS\\"+str(code)+".pdf",configuration=config , options = options)
        return       
#complete with random digits an integer x until it contains 10 digits
    def complete(x):
        x=str(x)
        while len(x)<10:
            x+=str(random.randint(0,9))
        return int(x)