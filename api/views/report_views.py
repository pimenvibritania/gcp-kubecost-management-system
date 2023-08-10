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
    # before = perf_counter()
    
    loop = asyncio.get_event_loop()
    
    async_tasks = [
        loop.run_in_executor(None, BigQuery.get_project, "2023-08-10"),
        loop.run_in_executor(None, BigQuery.get_project, "2023-08-10"),
    ]

    (bigquery_result, kubecost_result) = await asyncio.gather(*async_tasks)

    # for debug purpose
    # print(f"afterr ", perf_counter() - before)
    # with open("out.json", "w") as out_file:
    #     data = json.dumps(results2)
    #     out_file.write(data)
    
    
    send_report("bigquery", bigquery_result)
    send_report("kubecost", kubecost_result)
    
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
                'cc': "pirman.abdurohman@moladin.com",
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
            
            em_name = payload[data]['pic']
            project_name = f"({payload[data]['tech_family']} - {payload[data]['project']})"
            
            rate = payload[data]["data"]["conversion_rate"]
            cost_difference_idr = payload[data]['data']['summary']['cost_difference']
            
            gcp_percent_status = Conversion.get_percentage(total_gcp_current_total_idr, total_gcp_prev_total_idr)
            
            gcp_cost_status = ""
            if (total_gcp_current_total_idr > total_gcp_prev_total_idr):
                gcp_cost_status = f"""<span style="color:#e74c3c">⬆ {gcp_percent_status:.2f}%</span>"""
            elif (total_gcp_current_total_idr < total_gcp_prev_total_idr):
                gcp_cost_status = f"""<span style="color:#1abc9c">⬇ {gcp_percent_status:.2f}%</span>"""
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
                    
                    percentage_status = Conversion.get_percentage(cost_svc['cost_this_week'], cost_svc['cost_prev_week'])
                    
                    cost_status_service = ""
                    if (cost_svc['cost_status'] == 'UP'):
                        cost_status_service = f"""<span style="color:#e74c3c">⬆ {percentage_status:.2f}%</span>"""
                    elif (cost_svc['cost_status'] == "DOWN"):
                        cost_status_service = f"""<span style="color:#1abc9c">⬇ {percentage_status:.2f}%</span>"""
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
                            <td>{cost_status_service}</td>
                        </tr>"""
                    
                    table_template += row
                # break # TODO: delete this

            table_template += "</tbody>\n</table>"
            # exit(1) #TODO: delete this
            subject = "subject" # TODO: change subject
            # to_email = "pimenvibritania@gmail.com" # TODO: change to em_email
            to_email = "tjatur.permadi@moladin.com" # TODO: change to em_email
            template_path = 'bigquery_template.html'
            context = {
                'em_name': em_name,
                'project_name': project_name,
                'gcp_cost_status' : gcp_cost_status,
                'total_gcp_prev_total_idr': Conversion.idr_format(total_gcp_prev_total_idr),
                'total_gcp_prev_total_usd': Conversion.convert_usd(total_gcp_prev_total_idr, rate),
                'total_gcp_current_total_idr': Conversion.idr_format(total_gcp_current_total_idr),
                'total_gcp_current_total_usd': Conversion.convert_usd(total_gcp_current_total_idr, rate),
                'current_rate': rate,
                'cost_difference_idr': Conversion.idr_format(cost_difference_idr),
                'cost_difference_usd': Conversion.convert_usd(cost_difference_idr, rate),
                'services_gcp': table_template
                } 
            
            tasks.append(loop.create_task(send_email_task(subject, to_email, template_path, context)))
            # break # TODO: delete this
    # tasks = [loop.create_task(send_email_task(subject, body["to_email"], template_path, context)) for _ in range(2)]
    asyncio.gather(*tasks)


    return JsonResponse({'message': 'Email sent successfully.'})
