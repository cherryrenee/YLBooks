# -*- coding: utf-8 -*-
"""Enforce multi-level numbering for headers (H1, H2, H3) across all lessons."""
import os, re

LESSONS_DIR = r"C:\Users\shain\Documents\GitHub\YLBooks\book2\lessons"
FILES = sorted([x for x in os.listdir(LESSONS_DIR) if x.endswith(".md")])

def get_chapter_num(filename):
    if filename.startswith("00_"):
        return "0"
    if filename.startswith("15_2_"):
        return "15-2"
    m = re.match(r"(\d+)_", filename)
    if m:
        return str(int(m.group(1)))
    # For appendices
    if filename.startswith("A_"): return "A"
    if filename.startswith("B_"): return "B"
    if filename.startswith("C_"): return "C"
    if filename.startswith("D_"): return "D"
    return None

def standardize_headers(filepath, filename):
    ch_num = get_chapter_num(filename)
    if not ch_num:
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().split('\n')
        
    new_lines = []
    h2_idx = 0
    h3_idx = 0
    
    for line in lines:
        # 1. Heading 1: H1 (#)
        # Match: # 1차시 · 바이브코딩이 뭐예요? -> # CHAPTER 1 · 바이브코딩이 뭐예요?
        # Appendices: # 부록 A · 용어 사전 -> # APPENDIX A · 용어 사전
        if line.startswith("# "):
            title = line[2:].strip()
            # Clean existing prefix like "1차시 · " or "CHAPTER 1 · "
            title_clean = re.sub(r"^(\d+차시|CHAPTER\s+\d+|부록\s+[A-D]|APPENDIX\s+[A-D])\s*·\s*", "", title)
            if ch_num in ["A", "B", "C", "D"]:
                new_lines.append(f"# APPENDIX {ch_num} · {title_clean}")
            elif ch_num == "0":
                new_lines.append(f"# 서문 · {title_clean}")
            else:
                new_lines.append(f"# CHAPTER {ch_num} · {title_clean}")
            continue

        # 2. Heading 2: H2 (##)
        # Match: ## 왜 이걸 하나요? -> ## 1.1 왜 이걸 하나요?
        if line.startswith("## "):
            h2_idx += 1
            h3_idx = 0 # reset H3 counter
            title = line[3:].strip()
            # Clean existing numeric prefix like "1.1 " or "15-2.3 "
            title_clean = re.sub(r"^[\d\-a-zA-Z\.]+\s+", "", title)
            new_lines.append(f"## {ch_num}.{h2_idx} {title_clean}")
            continue

        # 3. Heading 3: H3 (###)
        # Match: ### 단계 ① 파일 탐색기를 엽니다 -> ### 4.1.1 단계 ① 파일 탐색기를 엽니다
        if line.startswith("### "):
            h3_idx += 1
            title = line[4:].strip()
            # Clean existing prefix like "4.1.1 "
            title_clean = re.sub(r"^[\d\-a-zA-Z\.]+\s+", "", title)
            new_lines.append(f"### {ch_num}.{h2_idx}.{h3_idx} {title_clean}")
            continue

        new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(new_lines))
    print(f"  + standardized headers for: {filename} (ch {ch_num})")

if __name__ == "__main__":
    print("Standardizing multi-level heading numbering...")
    for fn in FILES:
        standardize_headers(os.path.join(LESSONS_DIR, fn), fn)
    print("Done!")
