import asyncio
from django.core.mail import send_mail
from django.template.loader import render_to_string

async def send_blast_email(subject, message, recipient_list):
    tasks = []
    for recipient in recipient_list:
        task = send_single_email(subject, message, recipient)
        tasks.append(task)
    await asyncio.gather(*tasks)

async def send_single_email(subject, message, recipient):
    html_message = render_to_string('email_template.html', {'subject': subject, 'message': message})
    await send_mail(subject, '', 'your@example.com', [recipient], html_message=html_message)
