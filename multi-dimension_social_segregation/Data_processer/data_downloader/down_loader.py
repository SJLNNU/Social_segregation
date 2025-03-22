import os
import requests
from tqdm import tqdm

# 全部州缩写列表（48州 + DC + PR）
states = [
    'ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il',
    'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne',
    'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'pr', 'ri', 'sc', 'sd', 'tn', 'tx',
    'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy'
]

base_url = "https://lehd.ces.census.gov/data/lodes/LODES7"

# 下载保存路径
save_dir = "LODES_2019"
os.makedirs(save_dir, exist_ok=True)

# 文件模板
def build_url(state, mode):
    return f"{base_url}/{state}/{mode}/{state}_{mode}_S000_JT00_2019.csv.gz"

def download_file(url, output_path):
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ 成功下载：{output_path}")
    except Exception as e:
        print(f"❌ 下载失败：{url}，错误：{e}")

# 开始下载
for state in tqdm(states, desc="正在下载各州数据"):
    for mode in ['rac', 'wac']:
        url = build_url(state, mode)
        filename = url.split("/")[-1]
        out_path = os.path.join(save_dir, filename)
        download_file(url, out_path)
