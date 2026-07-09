# -*- coding: utf-8 -*-
"""Safely unify captions, headers, and formal tone across all lessons in book2."""
import os, re

LESSONS_DIR = r"C:\Users\shain\Documents\GitHub\YLBooks\book2\lessons"
FILES = sorted([x for x in os.listdir(LESSONS_DIR) if x.endswith(".md")])

# 1. Helper to parse chapter number
def get_chapter_num(filename):
    if filename.startswith("00_"):
        return "0"
    if filename.startswith("15_2_"):
        return "15-2"
    m = re.match(r"(\d+)_", filename)
    if m:
        return str(int(m.group(1)))
    if filename.startswith("A_"): return "A"
    if filename.startswith("B_"): return "B"
    if filename.startswith("C_"): return "C"
    if filename.startswith("D_"): return "D"
    return None

# 2. Tone map replacements (Haeyo-style to strict Habsida-style)
TONE_MAP = {
    # Verb conversions
    "입력해 보세요": "입력해 확인합니다",
    "입력해보세요": "입력해 확인합니다",
    "눌러 보세요": "눌러 확인합니다",
    "눌러보세요": "눌러 확인합니다",
    "클릭해 보세요": "클릭해 확인합니다",
    "클릭해보세요": "클릭해 확인합니다",
    "확인해 보세요": "확인합니다",
    "확인해 봅니다": "확인합니다",
    "열어 보세요": "열어봅니다",
    "열어보세요": "열어봅니다",
    "사용해 보세요": "사용해 봅니다",
    "사용해 보세요": "사용해 봅니다",
    "말해 보세요": "말해 확인합니다",
    "말해보세요": "말해 확인합니다",
    "조절해 보세요": "조절해 확인합니다",
    "조절해보세요": "조절해 확인합니다",
    "바꿔 보세요": "바꿔 확인합니다",
    
    "누르세요": "누릅니다",
    "클릭하세요": "클릭합니다",
    "입력하세요": "입력합니다",
    "고르세요": "고릅니다",
    "여세요": "엽니다",
    "쓰세요": "씁니다",
    "두세요": "둡니다",
    "보세요": "확인합니다",
    "넘어가세요": "넘어갑니다",
    "붙여넣으세요": "붙여넣습니다",
    "하지 마세요": "하지 마십시오",
    "마세요": "마십시오",
    
    "지어 주세요": "지어 줍니다",
    "지어주세요": "지어 줍니다",
    "넣어 주세요": "넣어 둡니다",
    "넣어주세요": "넣어 둡니다",
    "클릭해 주세요": "클릭합니다",
    "클릭해주세요": "클릭합니다",
    "눌러 주세요": "누릅니다",
    "눌러주세요": "누릅니다",
    "띄워 주세요": "띄워 둡니다",
    "띄워주세요": "띄워 둡니다",
    "기다려 주세요": "기다립니다",
    "기다려주세요": "기다립니다",
    "보여주세요": "보여줍니다",
    "보여 주세요": "보여줍니다",
    
    # Specific sentences
    "준비물: 없음 (읽고 이해하는 차시입니다)": "준비물: 없음 (읽고 이해하는 차시)",
    "준비물: 윈도우 컴퓨터": "준비물: Windows PC",
    "준비물: 11~15-2차시에서 만든 게임": "준비물: 11~15-2차시 제작 결과물",
    "준비물: 15차시까지 완성된 게임": "준비물: 15차시 제작 결과물",
    "준비물: 17차시에서 연결한 키링 키보드": "준비물: 17차시 페어링 완료된 키링 키보드",
    "여정을 머릿속에 그려 보는 시간입니다. 편하게 읽어만 주세요.": "여정을 머릿속에 그려 보는 시간입니다. 편하게 읽어 둡니다.",
    "처음이라 겁이 날 수 있지만, 명령을 잘못 쳐도 컴퓨터가 망가지지 않습니다.": "명령을 잘못 입력해도 시스템 오류가 발생하거나 고장 나지 않습니다.",
    "그냥 느낌대로 원하는 걸 말하며 만드는 새로운 방식": "원하는 바를 자연어로 설명하여 코드를 얻는 방식",
    "그냥 붙여넣기(`Ctrl+V`)만 하면 바로 보낼 수 있습니다.": "붙여넣기(`Ctrl+V`)를 통해 즉시 전송할 수 있습니다.",
    "눈으로 본 느낌 그대로 말하면 AI가 알아듣습니다.": "의도하는 동작을 자연스럽게 설명하면 AI가 알아서 처리합니다."
}

def process_file(filepath, filename):
    ch_num = get_chapter_num(filename)
    if not ch_num:
        return
        
    # Step 1: Read completely to memory
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    h2_idx = 0
    h3_idx = 0
    
    # Step 2: Parse headers and adjust multi-level numbering
    for line in lines:
        # Heading 1 (#)
        if line.startswith("# "):
            title = line[2:].strip()
            # Remove any existing prefixes like "CHAPTER X · "
            title_clean = re.sub(r"^(CHAPTER\s+[\d\-]+|APPENDIX\s+[A-D]|서문|부록\s+[A-D]|[\d\-]+차시)\s*·\s*", "", title)
            title_clean = re.sub(r"^(CHAPTER\s+[\d\-]+|APPENDIX\s+[A-D]|서문|부록\s+[A-D]|[\d\-]+차시)\s*·\s*", "", title_clean)
            if ch_num in ["A", "B", "C", "D"]:
                new_lines.append(f"# APPENDIX {ch_num} · {title_clean}")
            elif ch_num == "0":
                new_lines.append(f"# 서문 · {title_clean}")
            else:
                new_lines.append(f"# CHAPTER {ch_num} · {title_clean}")
            continue

        # Heading 2 (##)
        if line.startswith("## "):
            h2_idx += 1
            h3_idx = 0
            title = line[3:].strip()
            title_clean = re.sub(r"^[\d\-a-zA-Z\.]+\s+", "", title)
            new_lines.append(f"## {ch_num}.{h2_idx} {title_clean}")
            continue

        # Heading 3 (###)
        if line.startswith("### "):
            h3_idx += 1
            title = line[4:].strip()
            title_clean = re.sub(r"^[\d\-a-zA-Z\.]+\s+", "", title)
            new_lines.append(f"### {ch_num}.{h2_idx}.{h3_idx} {title_clean}")
            continue

        new_lines.append(line)

    new_content = '\n'.join(new_lines)

    # Step 3: Apply caption transformations (Dot + double spaces)
    # Match: 그림 4.1 — -> 그림 4-1.  
    new_content = re.sub(r"그림\s*(\d+)\.(\d+)\s*—\s*", r"그림 \1-\2.  ", new_content)
    new_content = re.sub(r"표\s*(\d+)\.(\d+)\s*—\s*", r"표 \1-\2.  ", new_content)
    new_content = re.sub(r"그림\s*(\d+)-(\d+)\s*—\s*", r"그림 \1-\2.  ", new_content)
    new_content = re.sub(r"표\s*(\d+)-(\d+)\s*—\s*", r"표 \1-\2.  ", new_content)
    
    # Handle chapter 15-2 specifically to avoid decimal splitting issues
    new_content = new_content.replace("그림 15-2.  1", "그림 15_2-1")
    new_content = new_content.replace("그림 15-2.  2", "그림 15_2-2")
    new_content = new_content.replace("그림 15_2-1.  ", "그림 15_2-1.  ")
    new_content = new_content.replace("그림 15_2-2.  ", "그림 15_2-2.  ")
    
    # Force double space for any 그림 X-Y. or 표 X-Y. followed by single space
    new_content = re.sub(r"그림\s*(\d+)-(\d+)\.\s*(?!\s)", r"그림 \1-\2.  ", new_content)
    new_content = re.sub(r"표\s*(\d+)-(\d+)\.\s*(?!\s)", r"표 \1-\2.  ", new_content)

    # Step 4: Apply tone mappings
    for orig, repl in TONE_MAP.items():
        new_content = new_content.replace(orig, repl)
        
    # Clean leftovers
    new_content = new_content.replace("이대로 입력해 보세요", "이대로 입력해 확인합니다")
    new_content = new_content.replace("이대로 복사해서 붙여넣으세요", "이대로 복사해서 붙여넣습니다")
    new_content = new_content.replace("복사해 쓰세요.", "복사해 사용합니다.")
    new_content = new_content.replace("확인하세요.", "확인합니다.")
    new_content = new_content.replace("보여주세요.", "보여줍니다.")
    new_content = new_content.replace("바꿔 두세요.", "바꿔 둡니다.")
    new_content = new_content.replace("승인하세요.", "승인합니다.")
    new_content = new_content.replace("새로 여세요.", "새로 엽니다.")
    new_content = new_content.replace("만드세요.", "생성합니다.")
    new_content = new_content.replace("로그인하세요.", "로그인합니다.")
    new_content = new_content.replace("공식 사이트에서 최신 금액을 확인하세요.", "공식 사이트에서 최신 금액을 확인합니다.")
    new_content = new_content.replace("그대로 따르세요.", "그대로 따릅니다.")
    new_content = new_content.replace("챙기세요.", "챙깁니다.")
    new_content = new_content.replace("바꿔 두세요.", "바꿔 둡니다.")

    # Step 5: Save safely back to file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  + Unified styles/headers for: {filename}")

if __name__ == "__main__":
    print("Starting Style & Header Unification...")
    for fn in FILES:
        process_file(os.path.join(LESSONS_DIR, fn), fn)
    print("Completed successfully!")
