# 人物素材处理

## 参数与身份对应

未另行指定时，半身母版为 1200×1200 px、144 dpi、真实透明 PNG，腰部附近构图，头顶至下巴约 400 px，即画面高度的 1/3。此参数只适用于人物母版，不决定海报尺寸。

每次只编辑一个人，只引用该人的已核实原图。处理前查看原图并建立来源哈希；记录工具返回的实际生成路径，禁止猜测“最新生成文件”。沿用完整原文件名，仅更换扩展名；不同专场保持目录对应，同名冲突不得覆盖。

使用环境允许的图像编辑工具。优先保留原图已有的五官比例、肤色、表情、年龄、发型、眼镜、服装、角度与姿势。低清修复保守处理，不美颜或瘦脸。已有半身图主要去背景和调整布局；头像只补足缺失身体。保留胸牌、话筒和衣物标识等实际内容，不承诺恢复无法辨认的小字。

可参考提示词：

> Edit only this exact person's supplied source. Preserve facial proportions, eyes, nose, mouth, age, expression, skin tone, hairstyle, glasses, clothing, pose and camera angle. No beautification. Restore low-resolution detail conservatively. Remove background to genuine transparent alpha with natural clean hair and fabric edges, no opaque remnants or white fringe. Waist-up composition with full head and shoulders, waist near bottom, crown-to-chin approximately one third of canvas height. Extend only missing body, preserve existing hands, badges and microphone. No added text.

工具失败可针对错误重试一次；持续失败保存状态并说明缺项，不擅自使用收费外部服务。生成预览不能直接算交付。

## 确定性导出

生成后必须单独核对实际尺寸、透明度与密度。macOS 可使用随包脚本（路径相对于 skill）：

```sh
swift scripts/normalize.swift GENERATED.png STAGING.png CROWN_Y CHIN_Y 1200 144 0.3333333333
python3 scripts/audit_portrait.py STAGING.png --size 1200 --dpi 144
```

CROWN_Y、CHIN_Y 来自人工查看生成图后的坐标定位，原点在左上。Swift 脚本依赖 macOS AppKit；审计和胸像裁剪依赖 Python 3 + Pillow。没有这些环境时，使用可用的等价确定性操作，不声称脚本跨平台可运行。脚本只做几何或参数检查，不判断面部是否保真。

## 每张检查

- 逐张对照原图与最终图，检查眼睛、鼻子、嘴型、脸型、发际线、表情、眼镜及服装，没有串人。
- 最终图头顶和肩部完整，半身到腰附近，手臂与手指无明显畸形。
- 在最终图重新定位头顶与下巴，记录实际头部高度与占比；默认允许约 ±20 px 的人工定位误差。不以缩放公式的预期值冒充实际检查。
- 实际 PNG、1200×1200、144 dpi，存在全透明及不透明像素。PNG 密度的整数像素/米存储会有舍入误差，144 dpi 可显示为143.9926，允许 ±0.02 dpi。
- 在浅色与深色底上检查发丝和衣服边缘，无白边、残背景、透明破洞。仅有 alpha 通道不代表抠图合格。

保存技术检查与独立的视觉检查状态。失败原因、返工版本和最终选中路径保留在记录中；不承诺生成细节是真实恢复，也不称为像素级保真。

## 胸像派生

```sh
python3 scripts/crop_bust.py PORTRAIT.png BUST.png --remove-bottom 0.3333333333
```

该脚本按 alpha 可见区域确定人物范围，从其底部裁掉指定比例并修整外围透明留白，保留原文件，不改变脸部、不放大、不承担修图。它输出实际裁剪坐标 JSON。若原素材已经是胸像，应降低裁剪量或直接使用；若低头、举手或异常留白导致估算不适用，按实际视觉单独裁剪。上半身与海报胸像必须分开保存。
