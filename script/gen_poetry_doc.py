import os
import json
from opencc import OpenCC

converter = OpenCC('t2s')
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(script_dir, '..', 'rank', 'poet/')

poetry_rank_path = os.path.join(script_dir, 'poet_rank.json')


def gen_poetry_rank_dict():
    all_poet_ranks = []
    for root, dirs, files in os.walk(out_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding="utf-8") as f:
                data = json.load(f)
                for poet in data:
                    author = converter.convert(poet['author'])
                    title = converter.convert(poet['title'])
                    num = int(poet['baidu'])
                    all_poet_ranks.append((author, title, num))

    all_poet_ranks.sort(key=lambda x: x[2], reverse=True)
    return [x for x in all_poet_ranks if x[2] > 10000]


def save_poetry_rank_json(all_poet_ranks):
    poet_rank_dicts = []
    for rank in all_poet_ranks:
        poet_rank_dicts.append({
            'author': rank[0],
            'title': rank[1],
            'count': rank[2]
        })
    with open(poetry_rank_path, 'w', encoding='utf-8') as f:
        for poet in poet_rank_dicts:
            f.write(json.dumps(poet, ensure_ascii=False)+"\n")


if __name__ == '__main__':
    all_poet_ranks = gen_poetry_rank_dict()
    save_poetry_rank_json(all_poet_ranks)
