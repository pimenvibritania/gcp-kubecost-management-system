import asyncio
from time import perf_counter
from django.http import HttpResponse 
from ..models.bigquery import BigQuery

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
   
    return HttpResponse("TEST HTTP request")