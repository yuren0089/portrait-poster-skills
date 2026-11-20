# 人物修图与海报延展 Skills

两套可独立使用的技能：

- `batch-speaker-portraits`：批量人物修图、透明半身素材、尺寸与头部比例统一、逐张验收。
- `speaker-poster-adaptation`：整合修图、议程核对、胸像裁剪及可编辑 PSD / PNG 海报交付；已有合格照片直接复用。

## 使用

将所需技能文件夹放入自己的 Codex 技能目录（通常为 `~/.codex/skills`），在加载技能的会话中使用 `$batch-speaker-portraits` 或 `$speaker-poster-adaptation`。按任务提供自己的照片、模板及议程。

## 环境

图像修复需要可用的图像编辑工具；原生 PSD 制作需要 Photoshop 或能保留并验证相应结构的工具。Python 辅助脚本依赖 Pillow；Swift 规格归一化脚本依赖 macOS AppKit。技能不包含软件、账号或服务额度。

## 数据范围

本仓库仅包含通用指引与辅助脚本，不包含客户照片、内部议程、海报模板、字体或账号凭据。生成式修图不保证恢复原图中不存在的真实细节，应逐张对照检查。
