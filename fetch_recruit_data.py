"""
从 PRTS Wiki 爬取明日方舟公招干员数据

数据来源: prts.wiki Cargo API
API: /api.php?action=cargoquery
表: chara, char_obtain
筛选条件: obtainMethod 包含"公开招募"
"""

import json
import urllib.request
import urllib.parse
from datetime import date

API_URL = "https://prts.wiki/api.php"

PARAMS = {
    "action": "cargoquery",
    "format": "json",
    "tables": "chara,char_obtain",
    "limit": "5000",
    "fields": "chara.profession,chara.position,chara.rarity,chara.tag,chara.cn,char_obtain.obtainMethod",
    "where": 'char_obtain.obtainMethod like "%公开招募%" AND chara.charIndex>0',
    "join_on": "chara._pageName=char_obtain._pageName",
}


def fetch_data() -> list[dict]:
    """从 API 获取原始数据"""
    url = f"{API_URL}?{urllib.parse.urlencode(PARAMS)}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())

    operators = []
    for item in data["cargoquery"]:
        row = item["title"]
        operators.append({
            "name": row["cn"],
            "profession": row["profession"],
            "position": row["position"],
            "rarity": int(row["rarity"]),
            "tags": row["tag"].split(),
            "obtainMethod": row["obtainMethod"].split(),
        })

    # 按职业和星级排序
    profession_order = ["先锋", "医疗", "术师", "特种", "狙击", "辅助", "近卫", "重装"]
    operators.sort(key=lambda o: (
        profession_order.index(o["profession"]) if o["profession"] in profession_order else 99,
        o["rarity"],
        o["name"],
    ))
    return operators


def build_output(operators: list[dict]) -> dict:
    """构建输出数据结构"""
    professions = ["近卫", "狙击", "重装", "医疗", "辅助", "术师", "特种", "先锋"]
    positions = ["近战位", "远程位"]

    all_tags = set()
    for op in operators:
        all_tags.update(op["tags"])
    tags = sorted(all_tags)
    if "新手" in tags:
        tags.remove("新手")
        tags.insert(0, "新手")

    return {
        "source": API_URL + "?" + urllib.parse.urlencode(PARAMS),
        "fetchDate": date.today().isoformat(),
        "totalCount": len(operators),
        "professions": professions,
        "positions": positions,
        "tags": tags,
        "operators": operators,
    }


def main():
    operators = fetch_data()
    output = build_output(operators)

    output_path = "recruit_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(operators)} 条干员公招数据到 {output_path}")

    # 统计
    by_profession = {}
    by_rarity = {}
    for op in operators:
        by_profession[op["profession"]] = by_profession.get(op["profession"], 0) + 1
        by_rarity[op["rarity"]] = by_rarity.get(op["rarity"], 0) + 1

    print("\n按职业统计:")
    for prof, count in sorted(by_profession.items(), key=lambda x: -x[1]):
        print(f"  {prof}: {count}")

    print("\n按星级统计:")
    for rarity in sorted(by_rarity):
        stars = "★" * max(rarity, 1)
        print(f"  {stars} (rarity={rarity}): {by_rarity[rarity]}")


if __name__ == "__main__":
    main()
