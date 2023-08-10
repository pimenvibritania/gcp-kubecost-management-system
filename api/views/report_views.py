from time import perf_counter
from django.http import HttpResponse 
from ..models.bigquery import BigQuery
from django.shortcuts import render
from ..utils.mailer import send_blast_email
from ..utils.conversion import Conversion
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
        loop.run_in_executor(None, BigQuery.get_project, "2023-08-01"),
        loop.run_in_executor(None, BigQuery.get_project, "2023-08-01"),
    ]

    (bigquery_result, results2) = await asyncio.gather(*async_tasks)

    # for debug purpose
    # print(f"afterr ", perf_counter() - before)
    # with open("out.json", "w") as out_file:
    #     data = json.dumps(results2)
    #     out_file.write(data)
    
    
    send_report("bigquery", bigquery_result)
    # send_report("kubecost", bigquery_payload)
    
    return HttpResponse("TEST HTTP request")

async def send_email_task(subject, to_email, template_path, context):
    email_content = render_to_string(template_path, context)
    print("email content: ", email_content)
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

def send_report(report_type, payload):
    loop = asyncio.get_event_loop()
    tasks = []
    
    if report_type == 'bigquery':
        
        for data in payload:
            
            total_gcp_current_total_idr = payload[data]['data']['summary']['current_week']
            total_gcp_prev_total_idr = payload[data]['data']['summary']['previous_week']
            
            em_email = payload[data]['pic_email']
            project_name = f"({payload[data]['tech_family']} - {payload[data]['project']})"
            
            rate = payload[data]["data"]["conversion_rate"]
            cost_difference_idr = payload[data]['data']['summary']['cost_difference']
            
            gcp_cost_status = ""
            if (total_gcp_current_total_idr > total_gcp_prev_total_idr):
                gcp_cost_status = """<span style="color:#e74c3c">⬆</span>"""
            elif (total_gcp_current_total_idr < total_gcp_prev_total_idr):
                gcp_cost_status = """<span style="color:#1abc9c">⬇</span>"""
            else:
                gcp_cost_status = """<strong><span style="font-size:16px">Equal&nbsp;</span></strong>"""
            
            table_template = """
                <table>
                    <thead>
                        <tr>
                            <th>Service</th>
                            <th>Current IDR</th>
                            <th>Current USD</th>
                            <th>Previous IDR</th>
                            <th>Previous USD</th>
                            <th>GCP Project</th>
                            <th>Environment</th>
                            <th>Index Weight</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            gcp_services = payload[data]['data']['services']
            
            for service in gcp_services:
                svc_name = service['name']
                
                for index, cost_svc in enumerate(service['cost_services']):
                    if index == 0:
                        tr_first = f"""
                            <tr>
                                <td class="centered-text" rowspan="{len(service['cost_services'])}">{svc_name}</td>
                        """
                    else:
                        tr_first = "<tr>"
                    
                    cost_status_service = ""
                    if (cost_svc['cost_status'] == 'UP'):
                        cost_status_service = """<span style="color:#e74c3c">⬆</span>"""
                    elif (cost_svc['cost_status'] == "DOWN"):
                        cost_status_service = """<span style="color:#1abc9c">⬇</span>"""
                    else:
                        cost_status_service = """Equal"""
                        
                    row = f"""
                        {tr_first}
                            <td>{Conversion.idr_format(cost_svc['cost_this_week'])}</td>
                            <td>{Conversion.convert_usd(cost_svc['cost_this_week'], rate)} USD</td>
                            <td>{Conversion.idr_format(cost_svc['cost_prev_week'])}</td>
                            <td>{Conversion.convert_usd(cost_svc['cost_prev_week'], rate)} USD</td>
                            <td>{cost_svc['gcp_project']}</td>
                            <td>{cost_svc['environment']}</td>
                            <td>{cost_svc['index_weight']}</td>
                            <td>{cost_status_service}</td>
                        </tr>"""
                    
                    table_template += row

            table_template += "</tbody>\n</table>"
            
            subject = "subject"
            to_email = "pimenvibritania@gmail.com"
            template_path = 'bigquery_template.html'
            context = {
                'em_email': em_email,
                'project_name': project_name,
                'gcp_cost_status' : gcp_cost_status,
                'total_gcp_prev_total_idr': Conversion.idr_format(total_gcp_prev_total_idr),
                'total_gcp_prev_total_usd': Conversion.usd_format(total_gcp_prev_total_idr),
                'total_gcp_current_total_idr': Conversion.idr_format(total_gcp_current_total_idr),
                'total_gcp_current_total_usd': Conversion.usd_format(total_gcp_current_total_idr),
                'current_rate': rate,
                'cost_difference_idr': Conversion.idr_format(cost_difference_idr),
                'cost_difference_usd': Conversion.usd_format(cost_difference_idr),
                'services_gcp': table_template
                } 
            
            tasks.append(loop.create_task(send_email_task(subject, to_email, template_path, context)))
            break
    
    # tasks = [loop.create_task(send_email_task(subject, body["to_email"], template_path, context)) for _ in range(2)]
    asyncio.gather(*tasks)


    return JsonResponse({'message': 'Email sent successfully.'})
