from time import perf_counter
from django.http import HttpResponse 
from ..models.bigquery import BigQuery
from django.shortcuts import render
from ..utils.mailer import send_blast_email
from httpx import AsyncClient
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from ..serializers import MailSerializer
import json
import asyncio
import os

async def test_async(request):
    before = perf_counter()
    
    loop = asyncio.get_event_loop()
    
    async_tasks = [
        loop.run_in_executor(None, BigQuery.get_project),
        loop.run_in_executor(None, BigQuery.get_project),
        loop.run_in_executor(None, BigQuery.get_project),
        loop.run_in_executor(None, BigQuery.get_project),
        loop.run_in_executor(None, BigQuery.get_project),
        loop.run_in_executor(None, BigQuery.get_project),
        loop.run_in_executor(None, BigQuery.get_project),
    ]

    results = await asyncio.gather(*async_tasks)

    print(results)
    print(f"afterr ", perf_counter() - before)
    with open("out.json", "w") as out_file:
        data = json.dumps(results)
        out_file.write(data)
    return HttpResponse("TEST HTTP request")

async def send_email_task(subject, to_email, template_path, context):
    email_content = render_to_string(template_path, context)
    
    async with AsyncClient() as client:
        response = await client.post(
            os.getenv("MAILGUN_URL"),
            auth=('api', os.getenv("MAILGUN_API_KEY")),
            data={
                'from': "pirman.abdurohman@moladin.com",
                'to': to_email,
                'subject': subject,
                'html': email_content
            }
        )
        if response.status_code != 200:
            raise ValueError(response.content)
        return response

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        to_email = request.POST.get('to_email')
        
        body = json.loads(request.body)
        
        if "subject" not in body or "to_email" not in body:
            return JsonResponse({"error": "subject & to_email parameter is required."}, status=400)

        gcp_cost_status = ""
        if (total_gcp_current_total_idr > total_gcp_prev_total_idr):
            gcp_cost_status = """<span style="color:#e74c3c">⬆</span>"""
        elif (total_gcp_current_total_idr < total_gcp_prev_total_idr):
            gcp_cost_status = """<span style="color:#1abc9c">⬇</span>"""
        else:
            gcp_cost_status = """<strong><span style="font-size:16px">Equal&nbsp;</span></strong>"""
        
        template_path = 'email_template.html'
        context = {
            'em_email': 'Recipient Name',
            'project_name': 'Project Name',
            'gcp_cost_status' : gcp_cost_status,
            'total_gcp_prev_total_idr': 'total_gcp_prev_total_idr',
            'total_gcp_prev_total_usd': 'total_gcp_prev_total_usd',
            'total_gcp_current_total_idr': 'total_gcp_current_total_idr',
            'total_gcp_current_total_usd': 'total_gcp_current_total_usd',
            'current_rate': 'current_rate',
            'cost_difference_idr': 'cost_difference_idr',
            'cost_difference_usd': 'cost_difference_usd'
            } 
        
        asyncio.run(send_email_task(body["subject"], body["to_email"], template_path, context))
        
        return JsonResponse({'message': 'Email sent successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
