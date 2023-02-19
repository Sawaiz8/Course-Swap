def sendEmail(subject = "", body = "", recievers = ["shah.s.a.ahmed@gmail.com"]):
    import smtplib
    import os

    EMAIL_ADDRESS = "empowermonitor@gmail.com"
    EMAIL_PASSWORD = "strong1,"

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp: #Make an Stmp connection to Gmail
        smtp.ehlo() #Ehlo  
        smtp.starttls() #Here, we start TLS is encryption to protect data while transferring
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f"Subject: {subject}\n\n{body}"
        for reciever in recievers:
            smtp.sendmail(EMAIL_ADDRESS, reciever, msg)

