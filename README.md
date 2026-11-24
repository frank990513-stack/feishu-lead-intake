# 多渠道询盘归集到飞书

把百度爱番番推送和 Gmail 收到的官网询盘整理成同一张飞书多维表格。这个 Agent Skill 提供字段模板、接入指南和离线演练，帮助检查重复投递、未替换的字段和意外丢失的留言。

## 先跑离线演练

1. 从 [GitHub Releases](https://github.com/frank990513-stack/feishu-lead-intake/releases/tag/v1.0.0) 下载 Skill ZIP 并解压。
2. 让支持 Agent Skills 的助手读取 `feishu-lead-intake/SKILL.md`，再请它用包内样例做离线演练。也可以在解压后的 `feishu-lead-intake` 目录运行 `python3 -I scripts/demo.py`。
3. 对照 [字段与验收说明](feishu-lead-intake/references/field-mapping-and-checks.md) 检查结果。演练脚本只读虚构样例，不访问邮箱、飞书或网络。

真实接入时，按 [接入指南](feishu-lead-intake/references/connectors.md) 配置你有权使用的来源和飞书测试表，再从来源端提交单独的测试询盘并回查结果。
