import time, os
from selenium import webdriver

# 데이터 저장 디렉토리 생성
save_dir = "data"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# 홈 URL
URL = 'https://teen.munjang.or.kr/archives/category/write/life'

# 셀레니움으로 창 열기
driver = webdriver.Chrome()
driver.get(URL)

# page가 309까지 있으므로 1~309까지 돌기
PAGE_start = 26
PAGE_end = 50
for i in range(PAGE_start, PAGE_end+1):

    # page별로 창 이동
    page_uri = URL + '/page/{}'.format(i)
    driver.get(page_uri)

    # 현재 페이지의 모든 포스트에 대한 article_id 수집 ("post-000000" 의 형태)
    article_ids = driver.find_elements_by_css_selector("article")
    article_ids = [i.get_attribute("id") for i in article_ids]

    # 포스트 내용 저장할 리스트
    contents = []

    # 각 포스트 별로 접근
    for id in article_ids:

        # id로 접근해서 클릭할 수 있는 'a' element 찾기
        article = driver.find_element_by_id(id)
        title = article.find_element_by_css_selector(".post_title > a")

        # 제목 텍스트 가져오기
        title_text = title.text

        # title 클릭해서 포스트 창 들어가기
        title.click()

        # 들어간 창에서 본문 내용 가져오기
        content = driver.find_element_by_css_selector(".entry-content").text

        # 제목과 본문내용 합친 string을 contents에 저장
        title_content = "--title: [{}]\n".format(title_text) + content
        contents.append(title_content)

        # 뒤로가기
        driver.back()
        time.sleep(0.5)

    # 한 페이지를 다 돌면 페이지별로 txt 파일 저장
    contents_txt = "\n\n".join(contents)
    file_path = os.path.join(save_dir, "page_{}.txt".format(i))
    with open(file_path, 'w') as f:
        f.write(contents_txt)
