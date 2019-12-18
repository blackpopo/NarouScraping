import json
import requests
import os


from pathlib import Path
path = Path('.')
print(list(path.glob('jsons/*.json')))

for json_file in path.glob('jsons/*.json'):
    urls = []
    folder_name = json_file.parts[-1].split('.')[0]
    # print(folder_name)

    os.mkdir(folder_name)

    with json_file.open() as js:
        data = json.load(js)
        for line in data:
            for url in line['img_urls']:
                urls.append(url)
    for url in urls:
        try:
            response = requests.get(url)
            image = response.content
            filename = url.rsplit("/", 1)[1]
            with open(os.path.join(folder_name, filename), 'wb') as f:
                f.write(image)
        except:
            pass
    print(folder_name, 'is finished')