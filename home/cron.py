import datetime

def test_cron_job():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Run cronjob at: {formatted_datetime}")

