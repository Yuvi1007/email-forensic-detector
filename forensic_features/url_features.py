import re

def extract_url_features(email_content):

    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, email_content)

    num_urls = len(urls)

    ip_url_flag = 0
    shortened_url = 0

    shorteners = ["bit.ly","tinyurl","t.co","goo.gl"]

    for url in urls:

        if re.search(r'https?://\d+\.\d+\.\d+\.\d+', url):
            ip_url_flag = 1

        for short in shorteners:
            if short in url:
                shortened_url = 1

    return {
        "num_urls": num_urls,
        "ip_url_flag": ip_url_flag,
        "shortened_url": shortened_url
    }