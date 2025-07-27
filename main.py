from datetime import datetime
from pathlib import Path
from scrapper import web_request

today_date = datetime.now()
format_date = today_date.strftime("%d-%m-%Y")

log_path = Path("logs")/f"{format_date}.txt"
Path("logs").mkdir(parents=True, exist_ok=True)

if not log_path.exists():
    url = "https://www.imdb.com/es-es/chart/moviemeter/?ref_=chttp_nv_menu"
    web_request(url, log_path)
    print("The log was saved correctly")
else:
    print("The log for this date already exists. It will not be run again")
