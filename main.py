import os
import requests
import time
import concurrent.futures
import argparse
import asyncio

# Функция для скачивания изображения с заданного URL и сохранения его на диск
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = os.path.basename(url)  # Получаем имя файла из URL
            with open(image_name, 'wb') as f:
                f.write(response.content)
            time.sleep(0.1)  # Добавляем задержку в 0.1 секунду
            return True
        else:
            return False
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return False

# Функция для последовательного скачивания изображений
def sync_download(urls):
    start_time = time.time()
    for url in urls:
        download_image(url)
    end_time = time.time()
    return end_time - start_time

# Функция для многопоточного скачивания изображений
def threaded_download(urls):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(download_image, urls)
    end_time = time.time()
    return end_time - start_time

# Функция для многопроцессорного скачивания изображений
def process_download(urls):
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(download_image, urls)
    end_time = time.time()
    return end_time - start_time

# Функция для асинхронного скачивания изображений
async def async_download(urls):
    start_time = time.time()
    tasks = [asyncio.create_task(async_download_image(url)) for url in urls]
    await asyncio.gather(*tasks)
    end_time = time.time()
    return end_time - start_time

async def async_download_image(url):
    try:
        response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
        if response.status_code == 200:
            image_name = url.split('/')[-1]
            with open(image_name, 'wb') as f:
                f.write(response.content)
            await asyncio.sleep(0.1)  # Добавляем задержку в 0.1 секунду
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Download images from URLs.')
    parser.add_argument('urls', nargs='+', type=str, help='List of image URLs')
    return parser.parse_args()

def main():
    args = parse_arguments()
    urls = args.urls

    sync_time = sync_download(urls)
    print(f"Sync download time: {sync_time} seconds")

    threaded_time = threaded_download(urls)
    print(f"Threaded download time: {threaded_time} seconds")

    process_time = process_download(urls)
    print(f"Process download time: {process_time} seconds")

    async_time = asyncio.run(async_download(urls))
    print(f"Async download time: {async_time} seconds")

if __name__ == '__main__':
    main()
