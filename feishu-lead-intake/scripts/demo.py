"""Replay only the bundled fictional samples against an in-memory table."""

import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import quote

ASSETS = Path(__file__).resolve().parents[1] / "assets"
PLACEHOLDER = re.compile(r"\$\{[^{}]+\}")
MAIL_LABEL = re.compile(r"(?:^|\s)(Email|Product|Inquiry)\s*[:：]", re.IGNORECASE)


class ConversationText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.hidden_tag = None

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.hidden_tag = tag
        if tag == "br" and self.hidden_tag is None:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag == self.hidden_tag:
            self.hidden_tag = None
        if tag in {"p", "div"} and self.hidden_tag is None:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.hidden_tag is None:
            self.parts.append(data)

    def text(self):
        lines = (line.strip() for line in "".join(self.parts).splitlines())
        return "\n".join(line for line in lines if line)


def field_row(source, scope, channel, original_id, summary, body, email):
    if any(PLACEHOLDER.search(value) for value in (original_id, summary, body, email)):
        raise ValueError("unresolved-placeholder")
    if not original_id.strip():
        raise ValueError("missing-id")
    if not summary.strip() or not body.strip():
        raise ValueError("empty-inquiry")
    key = ":".join(quote(part, safe="") for part in (source, scope, original_id))
    return {
        "去重键": key,
        "来源渠道": channel,
        "原始编号": original_id,
        "询盘摘要": summary,
        "原始正文": body,
        "联系邮箱": email,
    }


def baidu_row(sample):
    conversation = ConversationText()
    conversation.feed(sample["formDetail"])
    conversation.close()
    body = conversation.text()
    return field_row(
        "baidu-aiff", "demo-site", "百度爱番番·示例站", sample["clueId"],
        sample["additionalContent"].strip() or body.split("\n", 1)[0], body,
        sample.get("emailAccount", "").strip(),
    )


def gmail_row(sample):
    body = sample["body_text"].strip()
    labels = list(MAIL_LABEL.finditer(body))
    fields = {}
    for index, current in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(body)
        label = current.group(1).lower()
        if label in fields:
            raise ValueError("ambiguous-mail-label")
        fields[label] = body[current.end():end].strip()
    return field_row(
        "gmail", "demo-mailbox", "官网表单·示例 Google Ads 来源", sample["id"],
        fields.get("inquiry", ""), body, fields.get("email", ""),
    )


def apply_sample(convert, sample, table):
    try:
        row = convert(sample)
    except ValueError as exc:
        return str(exc)
    key = row["去重键"]
    if key in table:
        return "duplicate" if table[key] == row else "key-conflict"
    table[key] = row
    return "inserted"


def main():
    baidu = json.loads((ASSETS / "baidu-aiff-samples.json").read_text(encoding="utf-8"))
    gmail = json.loads((ASSETS / "gmail-samples.json").read_text(encoding="utf-8"))
    with (ASSETS / "feishu-fields.csv").open(encoding="utf-8", newline="") as template:
        expected_rows = list(csv.DictReader(template))

    table = {}
    cases = [
        ("爱番番正常入表", baidu_row, baidu["normal"], "inserted", 1),
        ("Gmail 正常入表", gmail_row, gmail["normal"], "inserted", 2),
        ("爱番番重送", baidu_row, baidu["normal"], "duplicate", 2),
        ("Gmail 重送", gmail_row, gmail["normal"], "duplicate", 2),
        ("爱番番占位符", baidu_row, baidu["unresolved_placeholder"], "unresolved-placeholder", 2),
        ("Gmail 空留言", gmail_row, gmail["empty_inquiry"], "empty-inquiry", 2),
        ("Gmail 单行通知", gmail_row, gmail["flat_body"], "inserted", 3),
    ]
    for label, convert, sample, expected, count in cases:
        actual = apply_sample(convert, sample, table)
        if actual != expected or len(table) != count:
            raise SystemExit(f"失败 · {label} · {actual} · {len(table)} 行")
        print(f"通过 · {label} · {actual} · {len(table)} 行")

    rows = list(table.values())
    if rows[:2] != expected_rows:
        raise SystemExit("失败 · 正常入表的字段与 CSV 样例不一致")
    flat = rows[2]
    if (
        flat["询盘摘要"] != "希望了解 2 台的交付周期。"
        or flat["联系邮箱"] != "buyer-c@example.invalid"
        or flat["原始正文"] != gmail["flat_body"]["body_text"]
    ):
        raise SystemExit("失败 · 单行通知的字段不符合预期")
    print("\n离线入表预览（虚构数据）")
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
