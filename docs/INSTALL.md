# 설치 가이드

## 시스템 요구사항

- Python 3.8 이상
- pip (Python 패키지 관리자)
- Tesseract OCR 5.0 이상
- 2GB 이상의 RAM (권장: 4GB+)

## 1. Python 설치 확인

```bash
python --version
# 또는
python3 --version
```

Python이 설치되어 있지 않다면:
- **Windows**: [python.org](https://www.python.org/downloads/)에서 다운로드
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt-get install python3 python3-pip`

## 2. Tesseract OCR 설치

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-kor  # 한글 지원
```

설치 확인:
```bash
tesseract --version
tesseract --list-langs  # 한글(kor) 확인
```

### macOS

```bash
brew install tesseract
brew install tesseract-lang  # 한글 포함 모든 언어
```

### Windows

1. [Tesseract 설치 프로그램](https://github.com/UB-Mannheim/tesseract/wiki) 다운로드
2. 설치 시 "Additional language data" → **Korean** 체크
3. 설치 경로를 환경 변수에 추가

**환경 변수 설정:**
- 시스템 속성 → 환경 변수
- Path에 추가: `C:\Program Files\Tesseract-OCR`

**코드에서 경로 지정 (필요시):**
```python
# app.py 상단에 추가
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## 3. 프로젝트 클론

```bash
git clone https://github.com/yourusername/smart-namer-ocr.git
cd smart-namer-ocr
```

## 4. 가상환경 생성 (권장)

### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## 5. 의존성 설치

```bash
pip install -r requirements.txt
```

**설치되는 패키지:**
- streamlit: 웹 앱 프레임워크
- pytesseract: Tesseract OCR Python 래퍼
- Pillow: 이미지 처리
- opencv-python: 컴퓨터 비전
- numpy: 수치 계산
- piexif: EXIF 데이터 처리

## 6. 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱 실행

## 문제 해결

### Tesseract를 찾을 수 없음

**에러:**
```
TesseractNotFoundError: tesseract is not installed
```

**해결:**
1. Tesseract 설치 확인: `tesseract --version`
2. 경로가 올바른지 확인
3. 환경 변수 설정 확인 (Windows)
4. 코드에서 직접 경로 지정

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # macOS/Linux
# 또는
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
```

### 한글 인식 안됨

**증상:** 영어는 인식되지만 한글은 인식 안됨

**해결:**
1. 한글 언어팩 설치 확인
   ```bash
   tesseract --list-langs
   ```
2. `kor`가 없으면 설치
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr-kor
   
   # macOS
   brew install tesseract-lang
   
   # Windows
   # 설치 프로그램에서 Korean 언어 데이터 선택
   ```

### OpenCV 설치 오류

**에러:**
```
Could not find a version that satisfies the requirement opencv-python
```

**해결:**
```bash
pip install --upgrade pip
pip install opencv-python-headless  # 헤드리스 버전 사용
```

### Streamlit 실행 오류

**에러:**
```
Command 'streamlit' not found
```

**해결:**
```bash
python -m streamlit run app.py  # 모듈로 직접 실행
```

### 메모리 부족

**증상:** 큰 이미지 처리 시 느려지거나 멈춤

**해결:**
1. 이미지 크기 제한 추가
   ```python
   # app.py에 추가
   if img.size[0] * img.size[1] > 4000000:  # 4MP
       img.thumbnail((2000, 2000))
   ```
2. 메모리 많은 서버 사용

## 개발 환경 설정

개발 시 추가 도구 설치:

```bash
pip install pytest black flake8 mypy
```

- **pytest**: 테스트 프레임워크
- **black**: 코드 포맷터
- **flake8**: 린터
- **mypy**: 타입 체커

## 배포

### Streamlit Cloud

1. GitHub에 푸시
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. 저장소 연결
4. 배포!

### Docker

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-kor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t smart-namer .
docker run -p 8501:8501 smart-namer
```

## 추가 도움말

- 📚 [Streamlit 문서](https://docs.streamlit.io/)
- 🔍 [Tesseract 문서](https://tesseract-ocr.github.io/)
- 🖼️ [OpenCV 튜토리얼](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

질문이 있으시면 [Issues](https://github.com/yourusername/smart-namer-ocr/issues)에 등록해주세요!
