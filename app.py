import streamlit as st
import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from datetime import datetime
import io
import re
import piexif
import cv2

# 1. 페이지 설정
st.set_page_config(
    page_title="스마트 AI 네이머",
    page_icon="📂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# [디자인] 모바일 최적화 및 요소 간격 확보
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; padding-bottom: 5rem !important; }
    .main-title { font-size: 1.6rem !important; font-weight: bold; margin-bottom: 1rem; }
    
    /* 요소 간격 확보 */
    div.stButton, div.stDownloadButton, div.stTextInput { margin-top: 10px; margin-bottom: 10px; }

    /* 파일명 표시 박스 */
    .filename-box {
        background-color: #f0f7ff;
        border: 2px solid #007AFF;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        color: #007AFF;
        word-break: break-all;
        margin: 15px 0;
    }
    
    /* 이미지 크기 조절 */
    .stImage > img { max-width: 100%; height: auto; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">📂 스마트 AI 네이머</div>', unsafe_allow_html=True)

# [함수] 개선된 이미지 전처리 - 메모리 효율적이면서 인식률 높음
def preprocess_image_advanced(image):
    """
    다양한 전처리 기법을 조합하여 OCR 인식률 향상
    - 적응형 이진화: 조명 불균일 대응
    - 노이즈 제거: 작은 점들 제거
    - 자동 해상도 조정: 너무 작은 이미지 확대
    - 모폴로지 연산: 글자 선명화
    """
    # PIL -> OpenCV 변환 (메모리 효율적)
    img_array = np.array(image)
    
    # 그레이스케일 변환
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # 해상도 체크 및 조정 (너무 작으면 확대)
    height, width = gray.shape
    if height < 1000 or width < 1000:
        scale = max(1000 / height, 1000 / width)
        # 메모리 절약을 위해 2배 이상 확대는 제한
        scale = min(scale, 2.0)
        new_width = int(width * scale)
        new_height = int(height * scale)
        gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    # 노이즈 제거 (작은 점이나 잡티 제거)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # 적응형 이진화 (조명이 불균일한 이미지에 효과적)
    binary = cv2.adaptiveThreshold(
        denoised, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 2
    )
    
    # 모폴로지 연산으로 글자 더 선명하게
    kernel = np.ones((1, 1), np.uint8)
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # OpenCV -> PIL 변환
    return Image.fromarray(morph)

# [함수] 여러 OCR 설정으로 시도하여 최상의 결과 추출
def extract_text_multi_config(image):
    """
    여러 PSM(Page Segmentation Mode) 모드를 시도하여 가장 많은 단어 찾기
    - 이미지 레이아웃에 따라 최적 모드가 다르므로 여러 모드 시도
    - 메모리 효율을 위해 전처리는 한 번만 수행
    """
    # 전처리된 이미지 한 번만 생성
    processed = preprocess_image_advanced(image)
    
    # 시도할 PSM 모드들 (이미지 레이아웃에 따라 효과가 다름)
    psm_modes = [
        ('--psm 3', 'auto'),          # 자동 페이지 분할
        ('--psm 11', 'sparse'),       # 희소 텍스트 (여기저기 흩어진 텍스트)
        ('--psm 6', 'uniform'),       # 균일한 텍스트 블록
        ('--psm 4', 'single_column'), # 단일 컬럼 텍스트
    ]
    
    all_words = set()  # 중복 제거를 위해 set 사용
    
    for config, mode_name in psm_modes:
        try:
            # 한글+영문+숫자 인식
            text = pytesseract.image_to_string(
                processed, 
                lang='kor+eng',  # 한글 인식을 위해 'kor' 언어팩 설치 필요
                config=f'{config} --oem 3'  # LSTM 엔진 사용
            )
            
            # 2글자 이상 단어만 추출
            words = re.findall(r'[가-힣a-zA-Z0-9]{2,}', text)
            all_words.update(words)
            
        except Exception as e:
            # 특정 모드에서 오류가 나도 다른 모드 계속 시도
            continue
    
    # 중복 제거 후 최대 8개 반환
    return list(all_words)[:8]

# [함수] 파일명 또는 메타데이터에서 날짜 추출
def extract_date(uploaded_file, image):
    """
    1. 파일명에서 YYYY-MM-DD 패턴 검색
    2. 없으면 EXIF 메타데이터 확인
    3. 모두 없으면 현재 날짜 사용
    """
    # 1. 파일 이름에서 날짜 형식 (YYYY-MM-DD) 검색
    filename = uploaded_file.name
    date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    
    if date_match:
        return f"{date_match.group(1)}.{date_match.group(2)}.{date_match.group(3)}"
    
    # 2. EXIF 메타데이터 확인
    try:
        exif_dict = piexif.load(image.info.get('exif', b''))
        date_str = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S').strftime('%Y.%m.%d')
    except:
        # 3. 오늘 날짜 반환
        return datetime.now().strftime('%Y.%m.%d')

# 파일 업로드
uploaded_file = st.file_uploader(
    "사진을 선택하세요", 
    type=["jpg", "jpeg", "png"], 
    label_visibility="collapsed",
    help="JPG, JPEG, PNG 파일만 지원됩니다"
)

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # 날짜 인식
    final_date_prefix = extract_date(uploaded_file, img)
    
    st.image(img, use_container_width=True)
    st.write(f"📅 **인식된 날짜:** {final_date_prefix}")

    if st.button("🔍 이미지 분석 시작", use_container_width=True):
        with st.spinner("단어를 분석 중..."):
            # 개선된 OCR 실행 (여러 PSM 모드 시도)
            keywords = extract_text_multi_config(img)
            
            if keywords:
                st.session_state.keywords = keywords
                st.toast(f"✅ {len(keywords)}개 키워드 발견!")
            else:
                st.session_state.keywords = []
                st.warning("⚠️ 인식된 단어가 없습니다. 다른 이미지를 시도해보세요.")

    if 'keywords' in st.session_state and st.session_state.keywords:
        st.write("▼ 키워드 선택")
        selected = st.pills(
            "키워드", 
            st.session_state.keywords, 
            selection_mode="multi", 
            label_visibility="collapsed"
        )
        st.session_state.selected_list = selected

    st.write("---")
    custom_name = st.text_input(
        "📝 직접 이름 입력", 
        placeholder="추가 내용을 입력하세요",
        help="추가로 포함할 내용을 입력하세요"
    )

    # 파일명 조합 (YYYY.MM.DD_ 형식)
    selected_list = st.session_state.get('selected_list', [])
    selected_str = "_".join(selected_list).replace(" ", "")
    
    name_parts = [final_date_prefix]  # 인식된 날짜 (YYYY.MM.DD)
    if selected_str: 
        name_parts.append(selected_str)
    if custom_name: 
        name_parts.append(custom_name.strip().replace(" ", "_"))
    
    # 부품들을 '_'로 연결하고 확장자 추가
    final_filename = f"{'_'.join(name_parts)}.png"

    # 최종 파일명 강조 표시
    st.markdown(f'<div class="filename-box">{final_filename}</div>', unsafe_allow_html=True)
    
    # 메모리 효율적 저장
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.download_button(
        label="💾 이 이름으로 저장하기",
        data=buf.getvalue(),
        file_name=final_filename,
        mime="image/png",
        use_container_width=True
    )
else:
    # 사용 가이드 표시
    st.info("""
    ### 📖 사용 방법
    
    1. **이미지 업로드**: 위 버튼을 클릭하여 이미지를 선택하세요
    2. **분석 시작**: "이미지 분석 시작" 버튼을 눌러 텍스트를 추출하세요
    3. **키워드 선택**: 인식된 단어 중 원하는 것을 선택하세요
    4. **이름 추가**: 필요시 추가 내용을 입력하세요
    5. **저장**: 생성된 파일명으로 다운로드하세요
    
    💡 **팁**: 파일명에서 날짜를 자동으로 인식합니다!
    """)
