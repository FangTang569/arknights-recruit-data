# arknights-recruit-data

《明日方舟》公开招募干员数据，数据来源 [PRTS Wiki](https://prts.wiki/w/%E5%85%AC%E6%8B%9B%E8%AE%A1%E7%AE%97)，遵循 MIT 协议。

## 文件说明

| 文件 | 说明 |
|------|------|
| `recruit_data.json` | 完整数据，含职业、位置、标签、获取方式 |
| `recruit_simple.json` | 精简版，仅含 `name` / `rarity` / `tags`（职业和位置已合并入tags） |
| `fetch_recruit_data.py` | 爬取脚本，从 PRTS Wiki Cargo API 获取最新数据 |
| `transform_data.py` | 转换脚本，将完整数据转为精简格式 |

## 数据格式

### recruit_data.json
```json
{
  "name": "芬",
  "profession": "先锋",
  "position": "近战位",
  "rarity": 2,
  "tags": ["费用回复"],
  "obtainMethod": ["公开招募", "标准寻访", "中坚寻访", "主线剧情"]
}
```

### recruit_simple.json
```json
{
  "name": "芬",
  "rarity": 2,
  "tags": ["费用回复", "先锋", "近战位"]
}
```

## 统计

- 总干员：158
- 职业：近卫(31)、狙击(29)、术师(19)、特种(19)、先锋(17)、重装(17)、医疗(14)、辅助(12)
- 标签：17 种（支援机械、控场、爆发、治疗、支援、费用回复、输出、生存、群攻、防护、减速、削弱、快速复活、位移、召唤、元素、新手）

## 更新数据
```bash
python fetch_recruit_data.py   # 重新爬取
python transform_data.py       # 重新生成精简版
```
