import re
from pathlib import Path

# 파일 경로 설정
base_dir = Path(r'c:\gitprac\Lecture')
lecture_files = [
    'Lecture1.html',
    'Lecture2.html',
    'Lecture3-1.html',
    'Lecture3-2.html',
    'Lecture3-3.html',
    'Lecture4.html'
]

# 모든 슬라이드를 저장할 리스트
all_slides = []
page_number = 1

# 각 파일에서 슬라이드 추출
for filename in lecture_files:
    file_path = base_dir / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # <div class="slide"> 태그 찾기 (정규식 사용)
    # 슬라이드는 <div class="slide"...> 로 시작하고 </div> 로 끝남
    # 중첩된 div도 고려해야 함
    
    # 더 정확한 방법: BeautifulSoup 없이 간단하게 처리
    # class="slide"를 포함하는 div 찾기
    pattern = r'<div class="slide[^"]*"[^>]*>.*?(?=<div class="slide|<script>|</body>|$)'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        slide_html = match.group(0)
        # 슬라이드가 완전히 닫히지 않았을 수 있으므로 </div> 개수 확인
        open_divs = slide_html.count('<div')
        close_divs = slide_html.count('</div>')
        
        # 닫히지 않은 div 개수만큼 </div> 추가
        missing_closes = open_divs - close_divs
        if missing_closes > 0:
            slide_html += '</div>' * missing_closes
        
        # 페이지 번호 추가
        if '<div class="page-number">' not in slide_html:
            slide_html = slide_html.rstrip('</div>').rstrip() + f'\n    <div class="page-number">{page_number}</div>\n</div>'
        
        all_slides.append(slide_html)
        page_number += 1

print(f"총 {len(all_slides)}개의 슬라이드를 추출했습니다.")

# HTML 템플릿 생성
html_template = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>게임 프로그래밍 강의 전체 - PDF 출력용</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        /* CORE THEME & RESET */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: #0d1117;
            color: #e6edf3;
            font-family: 'Noto Sans KR', sans-serif;
        }

        /* PDF 출력용 설정 */
        @media print {
            @page {
                size: A4 landscape;
                margin: 0;
            }
            
            body {
                background-color: #0d1117;
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }
            
            .slide {
                page-break-after: always;
                page-break-inside: avoid;
                display: flex !important;
                opacity: 1 !important;
                visibility: visible !important;
                position: relative !important;
                height: 100vh;
                width: 100vw;
                min-height: 100vh;
            }
            
            .slide:last-child {
                page-break-after: auto;
            }
            
            .nav-bar, .nav-buttons, .nav-btn, .slider-container {
                display: none !important;
            }
            
            .page-number {
                display: block !important;
            }
        }

        /* SLIDE CONTAINER */
        .slide {
            min-height: 100vh;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            border-bottom: 1px solid #30363d;
            overflow: hidden;
            position: relative;
            padding: 60px;
        }

        /* CONTENT WRAPPER */
        .content {
            width: 1200px;
            max-width: 90%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            z-index: 1;
        }

        /* BACKGROUND DECORATION */
        .slide::before {
            content: '';
            position: absolute;
            top: -10%;
            right: -10%;
            width: 40vw;
            height: 40vw;
            background: radial-gradient(circle, rgba(46, 160, 67, 0.05) 0%, rgba(0,0,0,0) 70%);
            border-radius: 50%;
            z-index: 0;
        }

        /* TYPOGRAPHY */
        h1 { font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; line-height: 1.2; }
        h2 { font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem; color: #7ee787; border-left: 5px solid #7ee787; padding-left: 1rem; }
        h3 { font-size: 1.8rem; margin-bottom: 1rem; color: #a5d6ff; }
        p, li { font-size: 1.4rem; line-height: 1.6; color: #c9d1d9; margin-bottom: 0.8rem; }
        strong { color: #fff; font-weight: 700; }
        
        /* CODE BLOCK STYLE */
        pre {
            background: #161b22;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #30363d;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
            overflow-x: auto;
            margin: 1.5rem 0;
            color: #e6edf3;
        }
        code { font-family: 'JetBrains Mono', monospace; color: #ff7b72; }
        .comment { color: #8b949e; }

        /* LISTS */
        ul { list-style: none; padding-left: 1rem; }
        ul li::before {
            content: "\\f054";
            font-family: "Font Awesome 6 Free";
            font-weight: 900;
            color: #7ee787;
            display: inline-block;
            width: 1.5em;
            margin-left: -1.5em;
        }

        ol { padding-left: 2rem; }

        /* LAYOUTS */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; }
        .card { background: #21262d; padding: 2rem; border-radius: 12px; border: 1px solid #30363d; height: 100%; }
        .center-text { text-align: center; }
        
        /* VISUAL ELEMENTS */
        .big-icon { font-size: 4rem; color: #7ee787; margin-bottom: 1rem; }
        .highlight-box { border: 2px solid #7ee787; padding: 2rem; border-radius: 12px; text-align: center; margin-top: 2rem; }
        .highlight { background-color: rgba(126, 231, 135, 0.2); color: #7ee787; padding: 2px 6px; border-radius: 4px; }

        /* TREE DIAGRAM */
        .tree-node { margin-left: 20px; border-left: 2px solid #30363d; padding-left: 20px; position: relative; }
        .tree-node::before { content: ''; position: absolute; left: 0; top: 15px; width: 20px; height: 2px; background: #30363d; }
        .tree-item { background: #161b22; padding: 10px; margin-bottom: 10px; border-radius: 6px; display: inline-block; border: 1px solid #30363d; font-family: 'JetBrains Mono'; }
        .tree-node-item {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.3rem;
            line-height: 1.8;
            color: #c9d1d9;
            margin-left: 0;
        }
        .tree-indent { margin-left: 30px; }
        .tree-symbol { color: #79c0ff; margin-right: 10px; }

        /* Lecture3 styles */
        .main-title { font-size: 2.8rem; color: #fff; margin-bottom: 1.5rem; }
        .slide-title { font-size: 2rem; color: #7ee787; margin-bottom: 1.5rem; border-left: 4px solid #7ee787; padding-left: 1rem; }
        .instruction-col { display: flex; flex-direction: column; justify-content: flex-start; padding-top: 20px; }
        .image-col { display: flex; align-items: center; justify-content: center; }
        .image-container { 
            background: rgba(255,255,255,0.02); 
            border: 1px solid #30363d; 
            border-radius: 8px; 
            padding: 20px; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            min-height: 300px;
        }
        .image-container img { max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 4px; }
        .placeholder-text { color: #8b949e; text-align: center; }
        .path-text { font-family: 'JetBrains Mono', monospace; color: #79c0ff; font-weight: 600; }
        .step-list { list-style: none; padding-left: 0; line-height: 1.8; }
        .step-list li { margin-bottom: 12px; padding-left: 8px; }
        .code-block { background: #161b22; padding: 1.5rem; border-radius: 8px; border: 1px solid #30363d; overflow-x: auto; }
        .col-left, .col-right { display: flex; flex-direction: column; justify-content: center; }
        .tree-view { background: #161b22; padding: 20px; border-radius: 8px; border: 1px solid #30363d; }
        .tree-view .tree-item { display: block; margin-bottom: 8px; padding: 8px 12px; }
        .indent-1 { margin-left: 0; }
        .indent-2 { margin-left: 30px; }
        .tree-icon { margin-right: 10px; color: #79c0ff; }
        .page-indicator { color: #8b949e; font-family: 'JetBrains Mono'; }
        .nav-buttons { display: flex; gap: 15px; }

        /* 페이지 번호 */
        .page-number {
            position: absolute;
            bottom: 20px;
            right: 30px;
            font-size: 1rem;
            color: #8b949e;
            font-family: 'JetBrains Mono', monospace;
            z-index: 100;
        }

        /* Slide-specific link styles */
        .slide--intro a {
            color: #58a6ff;
            text-decoration: none;
            border-bottom: 2px solid rgba(88,166,255,0.12);
            padding-bottom: 2px;
            transition: color 150ms ease, border-color 150ms ease;
        }
        .slide--intro a:hover { color: #9ad1ff; border-color: rgba(154,209,255,0.35); }
        .slide--intro .card a { font-weight: 600; }
    </style>
</head>
<body>

{SLIDES}

<script>
console.log('PDF 출력용 강의 자료가 로드되었습니다.');
console.log('총 슬라이드 수: {SLIDE_COUNT}');
console.log('브라우저의 인쇄 기능(Ctrl+P 또는 Cmd+P)을 사용하여 PDF로 저장하세요.');
console.log('인쇄 설정: A4 가로(Landscape), 여백 없음, 배경 그래픽 포함');
</script>

</body>
</html>
'''

# 슬라이드 삽입
final_html = html_template.replace('{SLIDES}', '\n\n'.join(all_slides))
final_html = final_html.replace('{SLIDE_COUNT}', str(len(all_slides)))

# 파일 저장
output_path = base_dir / 'LectureForPdf.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"파일이 생성되었습니다: {output_path}")
print(f"총 페이지 수: {len(all_slides)}")
