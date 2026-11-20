# 提示词和验收记录

## 单人编辑提示词

Edit target: this exact source photograph of [source filename]. Preserve original face identity, facial proportions, eyes, nose, mouth, expression, age, skin tone, hairstyle, glasses, clothing, pose and camera angle. No beautification. Remove background to genuine transparent alpha with clean hair and clothing edges. Square waist-up portrait, full shoulders, entire head visible, waist near bottom. Crown-to-chin height approximately one third of canvas height, small top margin. Extend only missing body naturally; preserve existing hands and pose. Restore low-resolution detail conservatively. Preserve existing microphone, badge and clothing markings where legible. No added text. Target [size] PNG.

只引用当前人的原图。必要时同一人的上一轮结果可作编辑目标，但原始面部仍以原图核对；不要将其他人的照片作为参考。提示词无法确保像素、DPI或占比，必须导出后检查。

## 单条记录示例

```json
{
  "source": "专场/原文件名.jpg",
  "source_sha256": "实际哈希",
  "generated": "工具返回的实际路径",
  "output": "输出/专场/原文件名.png",
  "status": "awaiting_visual_review",
  "geometry": {
    "generated_crown_y": 30,
    "generated_chin_y": 450,
    "final_crown_y": null,
    "final_chin_y": null,
    "final_head_ratio": null
  },
  "technical_check": null,
  "visual_review": {
    "source_mapping": null,
    "face": null,
    "half_body": null,
    "head_ratio": null,
    "light_and_dark_edges": null,
    "notes": ""
  }
}
```

空值表示未检查，只有实际完成后填写。保留每次返工原因及选中版本，成品目录不放被替代版本。

## 易错点

- 目录遍历顺序不是姓名映射；输入记录应直接携带输出路径。
- 144 dpi只是输出密度信息，不能增加照片细节。
- 缩放必须等比，画布尺寸固定；当头部偏小时放大可能导致顶部裁切，需要保留顶边余量后再检查腰部范围。
- 导出仍偏胸像时，需要补全身体，不能用透明留白冒充半身。
- 缩略总览适合查漏及构图，不能替代原尺寸面部/边缘检查。
- 原始照片太小，无法确认新增细节真实时，在说明中准确标注生成修复，不把主观相似度描述为身份认证。
