import sys
import json
from scraper import scrape_product_urls, scrape_product_review_url, scrape_product_reviews

def read_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
        return data

def save_json(data, path):
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def remove_dict_duplicates(my_list):
    seen = set()
    unique_list = []
    for item in my_list:
        # Mengubah dictionary menjadi tuple dari itemnya untuk membuatnya hashable
        item_tuple = tuple(item.items())
        if item_tuple not in seen:
            seen.add(item_tuple)
            unique_list.append(item)
    return unique_list

def get_product_urls():
    product_name = 'kamera'
    urls = read_json('data/product_urls.json')

    urls = scrape_product_urls(product_name)

    save_json(urls, 'data/product_urls.json')

def get_product_review_urls():
    product_urls = read_json('data/product_urls.json')
    review_urls = []
    for index, url in enumerate(product_urls):
        print(f'Mengambil {index + 1}/{len(product_urls)} url')
        url = scrape_product_review_url(url)
        if url is not None:
            print(url)
            review_urls.append(f"https://www.tokopedia.com{url}")

        save_json(review_urls, 'data/product_review_urls.json')

def get_product_reviews():
    product_review_urls = read_json('data/product_review_urls.json')
    reviews = read_json('data/product_reviews.json')
    for index, url in enumerate(product_review_urls):
        print(f'Mengambil {index + 1}/{len(product_review_urls)} url')
        results = scrape_product_reviews(url)
        reviews.extend(results)
        save_json(remove_dict_duplicates(reviews), 'data/product_reviews.json')
        print(f'Berhasil mendapatkan {len(remove_dict_duplicates(reviews))} data')
    

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 . <function_name>")
        sys.exit(1)

    function_name = sys.argv[1]

    if function_name == "product_url":
        get_product_urls()
    elif function_name == "review_url":
        get_product_review_urls()
    elif function_name == "reviews":
        get_product_reviews()
    else:
        print(f"No such function: {function_name}")
        sys.exit(1)

if __name__ == '__main__':
    main()
    

    # feedbackUrl = []
    # for url in urls:
    #     feedbackUrl.append(scrape_product_urls(url))
    
    # save_json(feedbackUrl, 'data/feedback_url.json')