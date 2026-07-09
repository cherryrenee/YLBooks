# -*- coding: utf-8 -*-
"""Enforce strict Habsida style and formal captions across all book2 markdown chapters."""
import os, re

LESSONS_DIR = r"C:\Users\shain\Documents\GitHub\YLBooks\book2\lessons"
FILES = [x for x in os.listdir(LESSONS_DIR) if x.endswith(".md")]

# 1. Caption regex replacements (Double spaces after dot for 그림 X-Y.  and 표 X-Y.  )
CAPTIONS = [
    (r"그림\s*(\d+)\.(\d+)\s*—\s*", r"그림 \1-\2.  "),
    (r"표\s*(\d+)\.(\d+)\s*—\s*", r"표 \1-\2.  "),
    (r"그림\s*(\d+)-(\d+)\s*—\s*", r"그림 \1-\2.  "),
    (r"표\s*(\d+)-(\d+)\s*—\s*", r"표 \1-\2.  "),
    (r"그림\s*(\d+)-(\d+)\.\s*(?!\s)", r"그림 \1-\2.  "),
    (r"표\s*(\d+)-(\d+)\.\s*(?!\s)", r"표 \1-\2.  "),
]

# 2. Sequential tone transformations
def apply_tone_rules(text):
    # a. Specific user-defined changes to ensure exact matches first
    text = text.replace("이대로 입력해 보세요", "이대로 입력해 확인합니다")
    text = text.replace("이대로 복사해서 붙여넣으세요", "이대로 복사해서 붙여넣습니다")
    text = text.replace("준비물: 없음 (읽고 이해하는 차시입니다)", "준비물: 없음 (읽고 이해하는 차시)")
    text = text.replace("준비물: 윈도우 컴퓨터", "준비물: Windows PC")
    text = text.replace("준비물: 11~15-2차시에서 만든 게임", "준비물: 11~15-2차시 제작 결과물")
    text = text.replace("준비물: 15차시까지 완성된 게임", "준비물: 15차시 제작 결과물")
    text = text.replace("준비물: 17차시에서 연결한 키링 키보드", "준비물: 17차시 페어링 완료된 키링 키보드")
    text = text.replace("여정을 머릿속에 그려 보는 시간입니다. 편하게 읽어만 주세요.", "여정을 머릿속에 그려 보는 시간입니다. 편하게 읽어 둡니다.")
    
    # b. Core Verb replacements (Convert ~세요/하세요 to ~합니다/~하십시오)
    # Regex for ~하세요. -> ~합니다.
    text = re.sub(r"([가-힣]+)하세요\.", r"\1합니다.", text)
    text = re.sub(r"([가-힣]+)하세요!", r"\1합니다!", text)
    text = re.sub(r"([가-힣]+)하세요\?", r"\1합니까?", text)
    text = re.sub(r"([가-힣]+)하세요\s", r"\1합니다 ", text)
    
    # Common verb mappings (literal replacements)
    tone_dict = {
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
        "넣어 주세요": "넣어 둡니다",
        "기다려 주세요": "기다립니다",
        "눌러 주세요": "누릅니다",
        "클릭해 주세요": "클릭합니다",
        "띄워 주세요": "띄워 둡니다",
        "확인하세요": "확인합니다",
        "체험해보세요": "체험해 봅니다",
        "확인해두세요": "확인해 둡니다",
        "가입해 두고 오세요": "가입해 두고 옵니다",
        "더블클릭하세요": "더블클릭합니다",
        "선택하세요": "선택합니다",
        "빠져나오세요": "빠져나옵니다",
        "클릭해서 그 창이 선택된 상태(포커스)인지 확인하세요": "클릭해서 그 창이 선택된 상태(포커스)인지 확인합니다",
        "불빛이 아예 안 켜지거나 반응이 없으면 충전이 됐는지부터 확인하세요": "불빛이 아예 안 켜지거나 반응이 없으면 충전이 되었는지 확인합니다",
        "혼자 끙끙대지 마세요": "혼자 고민하지 않아도 됩니다",
    }
    
    for orig, repl in tone_dict.items():
        text = text.replace(orig, repl)
        
    return text

def standardize_file(filepath):
    # Do not parse tools, only original lessons
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Apply caption regex
    for pattern, repl in CAPTIONS:
        content = re.sub(pattern, repl, content)

    # Apply tone conversion
    content = apply_tone_rules(content)
    
    # Double check for leftover "하세요" or "요." or "세요." 
    # to avoid common tone drops in note/success boxes
    content = content.replace("복사해 쓰세요.", "복사해 사용합니다.")
    content = content.replace("확인하세요.", "확인합니다.")
    content = content.replace("보여주세요.", "보여줍니다.")
    content = content.replace("바꿔 두세요.", "바꿔 둡니다.")
    content = content.replace("승인하세요.", "승인합니다.")
    content = content.replace("새로 여세요.", "새로 엽니다.")
    content = content.replace("만드세요.", "생성합니다.")
    content = content.replace("로그인하세요.", "로그인합니다.")
    content = content.replace("붙여넣고 엔터를 누릅니다.", "붙여넣고 엔터를 누릅니다.")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("  + standardized:", os.path.basename(filepath))

if __name__ == "__main__":
    print("Standardizing all lessons to strictly match DOCX (Formal tone & spaced captions)...")
    for fn in FILES:
        standardize_file(os.path.join(LESSONS_DIR, fn))
    print("Done!")
