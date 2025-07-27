import requests
from bs4 import BeautifulSoup

def web_request(url, log_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to make request: {e}")
    else:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"[ERROR] Error processing HTML: {e}")
        else:
            scrap(soup, log_path)

def scrap(soup, log_path):
    
    html_text = soup.find_all("div", class_="sc-15ac7568-0 jQHOho cli-children")
    for i in html_text:
        try:
            ranking_tag = i.find("div", class_="sc-9e9aed54-0 ldNYNW meter-const-ranking sc-15ac7568-5 cvldMO cli-meter-title-header")
            movie_ranking = ranking_tag.text.split()[0] if ranking_tag else "Not available"

            title_tag = i.find("h3", class_="ipc-title__text ipc-title__text--reduced")
            movie_title = title_tag.text if title_tag else "No title"

            duration_tag = list(i.find("div", class_="sc-15ac7568-6 fqJJPW cli-title-metadata").strings)
            movie_duration = duration_tag[1] if len(duration_tag) > 1 and len(duration_tag[1]) > 1 else "Not available"

            rating_tag = i.find("span", class_="ipc-rating-star--rating")
            movie_rating = rating_tag.text if rating_tag else "Not available"

            movie_info = {
                "movie_ranking": movie_ranking,
                "movie_title": movie_title,
                "movie_duration": movie_duration,
                "movie_rating": movie_rating,
            }
            log_writer(movie_info, log_path)

        except Exception as e:
            print(f"[ERROR] Error processing a movie: {e}")

def log_writer(web_info, log_path):
    try:
        with open(log_path, "a", encoding="utf-8") as file:
            file.write(f"""
 Position: {web_info["movie_ranking"]}
 {web_info["movie_title"]}
 Duration: {web_info["movie_duration"]}
 Rating: {web_info["movie_rating"]}
-------------------------------------\n""")
    except Exception as e:
        print(f"[ERROR] Error writing file: {e}")
