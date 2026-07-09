# -*- coding: utf-8 -*-
import os, re
LESS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lessons")
files = sorted(x for x in os.listdir(LESS) if re.match(r'\d\d_', x))
out = ["# 부록 D · 프롬프트 모음집\n",
       "\n!!! note \"이 부록은\"\n    책에 나온 **🗣️ 프롬프트(AI에게 하는 말)**를 차시별로 한곳에 모았습니다. 필요한 것을 찾아 그대로 복사해 쓰세요.\n",
       "\n---\n"]
total = 0
for fn in files:
    lines = open(os.path.join(LESS, fn), encoding="utf-8").read().split("\n")
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), fn)
    prompts = []
    i = 0
    while i < len(lines):
        m = re.match(r'!!!\s+quote\s+"(.*)"', lines[i].strip())
        if m:
            i += 1
            # find opening fence (indented)
            while i < len(lines) and "```" not in lines[i]:
                i += 1
            i += 1
            body = []
            while i < len(lines) and "```" not in lines[i]:
                body.append(lines[i][4:] if lines[i].startswith("    ") else lines[i])
                i += 1
            prompts.append("\n".join(body).strip())
        i += 1
    if prompts:
        out.append(f"\n## {title}\n")
        for p in prompts:
            out.append("\n```\n" + p + "\n```\n")
            total += 1
open(os.path.join(LESS, "D_prompts.md"), "w", encoding="utf-8").write("\n".join(out))
print("D_prompts.md written — prompts collected:", total, "from", len(files), "lessons")
