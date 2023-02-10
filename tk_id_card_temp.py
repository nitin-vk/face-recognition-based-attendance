from reportlab.lib.units import inch
def my_temp(c):
    c.translate(inch,inch)
    c.setFont("Helvetica",14)

    c.setStrokeColorRGB(0.1,0.8,0.1)
    c.setFillColorRGB(0,0,1)
    #c.drawImage('D:\\top2.jpg',-0.9*inch,2.6*inch)
    #####
    c.rotate(35)
    c.setFillColorCMYK(0,0,0,0.08) # font colour
    c.setFont("Helvetica", 100)
    c.drawString(-1.1*inch, -0.5*inch, "SAMPLE") # watermarking
    c.rotate(-35)
    #####
    c.setFillColorRGB(1,0,0)
    c.setFont("Helvetica", 25)
    c.drawRightString(1.7*inch,2.3*inch,'Identity Card')
    ######
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica", 24)
    c.drawRightString(0.3*inch,1.7*inch,'USN:')
    c.drawRightString(0.3*inch,1.3*inch,'Name:')
    #c.drawRightString(0.3*inch,0.9*inch,'Class:')
    #c.drawRightString(0.3*inch,0.5*inch,'Gender:')
    #c.drawRightString(4.0*inch,-0.5*inch,'Signature')
    #####
    c.line(-1.1,-0.7*inch,5*inch,-0.7*inch)
    c.setFont("Helvetica",8)
    c.setFillColorRGB(1,0,0) # font colour
    c.drawString(0, -0.9*inch, u"\u00A9"+" JSSATEB")
    ####
    return c