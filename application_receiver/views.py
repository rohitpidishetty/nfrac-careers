from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# from dotenv import load_dotenv # Development

# load_dotenv() # Development


@csrf_exempt
def receviver(req):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv("EMAIL")
    EMAIL_PASSWORD = os.getenv("EMAIL_KEY")

    if req.method != "POST":
        return JsonResponse({"message": "does not support this method"})

    try:
        jobid = req.POST.get("jobid")
        firstname = req.POST.get("firstname")
        lastname = req.POST.get("lastname")
        email = req.POST.get("email")
        phone = req.POST.get("phone")
        resume = req.FILES.get("resume")
        date = req.POST.get("time")
        division = req.POST.get("division")

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = "rohitpidishetty@gmail.com"
        msg["Subject"] = f"Job Application for {division}"

        body = f"""
        New Job Application

        Name: {firstname} {lastname}
        Email: {email}
        Phone: {phone}
        Job ID: {jobid}
        Date: {date}
        """
        msg.attach(MIMEText(body, "plain"))

        msg2 = MIMEMultipart()
        msg2["From"] = EMAIL_ADDRESS
        msg2["To"] = email
        msg2["Subject"] = f"We've Received Your Job Application - Team {division}"

        body = f"""
Dear {firstname},

Thank you for applying for the position with Job ID: {jobid}.

We have successfully received your application and appreciate your interest in joining our team.

Our team will carefully review your profile, and if your qualifications match our requirements, we will reach out to you for the next steps in the hiring process.

We wish you the best of luck.

Sincerely,  
{division} Recruitment Team"""
        msg2.attach(MIMEText(body, "plain"))

        if resume:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(resume.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{resume.name}"',
            )

            msg.attach(part)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, "rohitpidishetty@gmail.com", msg.as_string())
        server.sendmail(
            EMAIL_ADDRESS, email, msg2.as_string()
        )  # Recipient acknowledgement
        server.quit()

        return JsonResponse({"message": "sent"})

    except Exception as e:
        return JsonResponse({"message": "err", "payload": str(e)})
