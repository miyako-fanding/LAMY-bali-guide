import os
import re

def update_html_to_cdn(directory, github_id, repo_name):
    # 1. CDN 마스터 주소 조립 (f-string이 아래에서 받은 변수를 자동으로 끼워 넣어줌!)
    cdn_base_url = f"https://cdn.jsdelivr.net/gh/{github_id}/{repo_name}"
    
    # 2. 폴더 안의 모든 HTML 파일 스캔
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    # 3. 뼈대 교정기(정규식): src=" 또는 image: " 형태를 모두 타겟팅하도록 로봇의 시야 확장
    pattern = r'((?:src|image)\s*(?:=|:)\s*["\'])(?!http|//)([^"\']+?\.(?:jpg|jpeg|png|gif|svg))(["\'])'
    
    success_count = 0
    for file_name in html_files:
        filepath = os.path.join(directory, file_name)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 4. 일괄 치환: src="banner.jpg" -> src="https://cdn.jsdelivr.net/.../banner.jpg"
        updated_content, num_subs = re.subn(pattern, rf'\g<1>{cdn_base_url}/\g<2>\g<3>', content)
        
        # 5. 교정된 내용으로 파일 덮어쓰기
        if num_subs > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            success_count += 1
            
    print(f"🎉 성공! 총 {len(html_files)}개의 HTML 파일 중 {success_count}개 파일 변환 완료!")

# 👇 "지금 네가 있는 방(.)의 HTML들을 찾아서, 사진은 'LAMY-bali-cdn' 공장에서 가져오라고 적어라!"
update_html_to_cdn('.', 'miyako-fanding', 'LAMY-bali-cdn')

# 🛑 창이 바로 꺼지는 걸 막아주는 일시정지 버튼 (에러가 나든 성공하든 창을 유지해줌)
input("\n모든 작업이 끝났습니다. 창을 닫으려면 엔터 키를 누르세요...")