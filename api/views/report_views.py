import asyncio
from time import perf_counter
from django.http import HttpResponse 
from ..models.bigquery import BigQuery
import json

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