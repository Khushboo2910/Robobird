import requests
from bs4 import BeautifulSoup
import json
import csv

def fetch_html(url):
    response = requests.get(url)
    return response.text

def extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.title.text if soup.title else 'No Title'
    images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]
    links = [a['href'] for a in soup.find_all('a') if 'href' in a.attrs]
    
    return {
        'title': title,
        'images': images,
        'links': links
    }


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title', 'Images', 'Links'])
        writer.writerow([data['title'], ', '.join(data['images']), ', '.join(data['links'])])


def main():
    url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
    html_content = fetch_html(url)
    data = extract_data(html_content)
  
    save_to_json(data, 'output.json')
    save_to_csv(data, 'output.csv')
    print("Data has been saved to output.json and output.csv")

if __name__ == '__main__':
    main()
