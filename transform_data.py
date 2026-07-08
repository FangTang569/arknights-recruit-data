"""
将 recruit_data.json 转换为简化格式:
- 仅保留 name, rarity, tags
- tags 合并了原来的 tags + profession + position
"""

import json

INPUT_FILE = "recruit_data.json"
OUTPUT_FILE = "recruit_simple.json"


def transform():
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    operators = []
    for op in data["operators"]:
        tags = list(op["tags"])  # 原始标签
        tags.append(op["profession"])  # 合并职业
        tags.append(op["position"])  # 合并位置

        operators.append({
            "name": op["name"],
            "rarity": op["rarity"],
            "tags": tags,
        })

    output = {
        "source": data["source"],
        "fetchDate": data["fetchDate"],
        "totalCount": len(operators),
        "operators": operators,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"已生成 {OUTPUT_FILE}，包含 {len(operators)} 条干员数据")
    print(f"示例前 3 条:")
    for op in operators[:3]:
        print(f"  {op['name']} (★{op['rarity']}) tags={op['tags']}")


if __name__ == "__main__":
    transform()
