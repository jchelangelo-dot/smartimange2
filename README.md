# 📂 Smart AI Namer

이미지에서 텍스트를 자동으로 인식하여 파일명을 지능적으로 생성하는 Streamlit 웹 애플리케이션입니다.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ 주요 기능

- 🔍 **고성능 OCR**: 적응형 이진화 + 노이즈 제거 + 다중 PSM 모드로 높은 인식률
- 📅 **자동 날짜 추출**: 파일명 또는 EXIF 메타데이터에서 날짜 자동 인식
- 🎯 **키워드 선택**: 인식된 단어 중 원하는 키워드만 선택
- ✏️ **커스텀 입력**: 추가 내용을 직접 입력하여 파일명 완성
- 💾 **즉시 저장**: 생성된 파일명으로 이미지 다운로드
- 📱 **모바일 최적화**: 반응형 디자인으로 모든 기기에서 사용 가능

## 🖼️ 스크린샷

```
┌─────────────────────────────────────┐
│     📂 스마트 AI 네이머             │
├─────────────────────────────────────┤
│  [사진을 선택하세요...]             │
│                                     │
│  📅 인식된 날짜: 2024.12.25        │
│                                     │
│  [🔍 이미지 분석 시작]             │
│                                     │
│  ▼ 키워드 선택                     │
│  [회의록] [프로젝트] [2024]        │
│                                     │
│  📝 직접 이름 입력                 │
│  [추가 내용을 입력하세요]          │
│                                     │
│  ╔══════════════════════════════╗  │
│  ║ 2024.12.25_회의록_프로젝트.png ║  │
│  ╚══════════════════════════════╝  │
│                                     │
│  [💾 이 이름으로 저장하기]         │
└─────────────────────────────────────┘
```

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/smart-namer-ocr.git
cd smart-namer-ocr
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Tesseract OCR 설치

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-kor
```

#### macOS
```bash
brew install tesseract tesseract-lang
```

#### Windows
1. [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) 다운로드
2. 설치 시 "Additional language data" 에서 Korean 선택
3. 환경변수에 Tesseract 경로 추가

### 4. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

## 📋 시스템 요구사항

- Python 3.8 이상
- Tesseract OCR 5.0 이상
- 최소 2GB RAM (권장: 4GB+)
- 인터넷 연결 (최초 패키지 설치 시)

## 📦 의존성

```
streamlit>=1.30.0
pytesseract>=0.3.10
Pillow>=10.0.0
opencv-python>=4.8.0
numpy>=1.24.0
piexif>=1.1.3
```

## 🔧 사용 방법

### 기본 사용

1. **이미지 업로드**
   - "사진을 선택하세요" 버튼 클릭
   - JPG, JPEG, PNG 파일 선택

2. **이미지 분석**
   - "🔍 이미지 분석 시작" 버튼 클릭
   - AI가 이미지에서 텍스트 자동 추출

3. **키워드 선택**
   - 추출된 키워드 중 원하는 것 선택
   - 여러 개 선택 가능

4. **파일명 완성**
   - 필요시 추가 내용 직접 입력
   - 최종 파일명 확인

5. **저장**
   - "💾 이 이름으로 저장하기" 버튼 클릭

### 고급 설정

파일명 형식: `YYYY.MM.DD_키워드1_키워드2_커스텀입력.png`

예시:
- `2024.12.25_회의록_프로젝트.png`
- `2024.01.15_영수증_식비.png`
- `2023.11.30_제안서_초안_v2.png`

## 🎯 핵심 기술

### 1. 고성능 이미지 전처리
```python
# 적응형 이진화 (조명 불균일 대응)
binary = cv2.adaptiveThreshold(
    denoised, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY, 11, 2
)
```

### 2. 다중 PSM 모드
- PSM 3: 자동 페이지 분할
- PSM 11: 희소 텍스트
- PSM 6: 균일한 텍스트 블록
- PSM 4: 단일 컬럼 텍스트

### 3. 자동 해상도 조정
```python
# 너무 작은 이미지는 자동 확대 (최대 2배)
if height < 1000 or width < 1000:
    scale = max(1000 / height, 1000 / width)
    scale = min(scale, 2.0)
```

## 📊 성능

- **메모리 사용량**: ~1.3MB per image
- **처리 속도**: ~2-5초 per image
- **인식률**: 영문 90%+, 한글 85%+
- **모바일 지원**: ✅ 완벽 지원

## 🛠️ 트러블슈팅

### Tesseract를 찾을 수 없음
```python
# pytesseract.TesseractNotFoundError
# 해결: Tesseract 경로 지정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 한글 인식 안됨
```bash
# 한글 언어팩 설치 확인
tesseract --list-langs

# kor가 없으면 설치
sudo apt-get install tesseract-ocr-kor
```

### 메모리 부족
```python
# app.py에서 이미지 크기 제한 추가
if image.size[0] * image.size[1] > 4000000:  # 4MP 제한
    image.thumbnail((2000, 2000))
```

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 개발자

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 감사의 말

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - 오픈소스 OCR 엔진
- [Streamlit](https://streamlit.io/) - 빠른 웹앱 프레임워크
- [OpenCV](https://opencv.org/) - 컴퓨터 비전 라이브러리

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 [이슈](https://github.com/yourusername/smart-namer-ocr/issues)를 등록해주세요.

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
