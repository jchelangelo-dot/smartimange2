# 프로젝트 구조

```
smart-namer-ocr/
├── app.py                      # 메인 애플리케이션
├── requirements.txt            # Python 의존성
├── README.md                   # 프로젝트 개요
├── LICENSE                     # MIT 라이선스
├── CHANGELOG.md                # 버전 히스토리
├── CONTRIBUTING.md             # 기여 가이드
├── .gitignore                  # Git 제외 파일
│
├── .streamlit/
│   └── config.toml            # Streamlit 설정
│
├── docs/
│   └── INSTALL.md             # 설치 가이드
│
├── tests/
│   └── test_app.py            # 단위 테스트
│
└── assets/                     # (선택) 이미지, 아이콘 등
```

## 파일 설명

### 핵심 파일

- **app.py**: Streamlit 웹 애플리케이션의 메인 파일
  - 이미지 업로드 UI
  - OCR 처리 로직
  - 파일명 생성 및 다운로드

- **requirements.txt**: 프로젝트에 필요한 Python 패키지 목록
  ```
  streamlit>=1.30.0
  pytesseract>=0.3.10
  Pillow>=10.0.0
  opencv-python>=4.8.0
  numpy>=1.24.0
  piexif>=1.1.3
  ```

### 문서

- **README.md**: 프로젝트 소개, 빠른 시작 가이드
- **docs/INSTALL.md**: 상세 설치 가이드 (OS별)
- **CONTRIBUTING.md**: 기여 방법, 코딩 스타일
- **CHANGELOG.md**: 버전별 변경사항

### 설정

- **.gitignore**: Git에서 추적하지 않을 파일들
  - `__pycache__/`, `*.pyc`
  - `venv/`, `.venv/`
  - `.DS_Store`, `Thumbs.db`

- **.streamlit/config.toml**: Streamlit 앱 설정
  - 테마 색상
  - 서버 포트
  - 업로드 크기 제한

### 테스트

- **tests/test_app.py**: 단위 테스트
  - 날짜 추출 테스트
  - 이미지 전처리 테스트
  - pytest로 실행

### 추가 디렉토리 (선택사항)

- **assets/**: 이미지, 아이콘 등 리소스
- **examples/**: 예제 이미지 및 사용 시나리오
- **scripts/**: 유틸리티 스크립트

## 개발 워크플로우

1. **코드 수정**: `app.py` 편집
2. **로컬 테스트**: `streamlit run app.py`
3. **테스트 실행**: `pytest tests/`
4. **커밋**: `git commit -m "메시지"`
5. **푸시**: `git push origin main`

## 배포

### Streamlit Cloud
- `app.py`, `requirements.txt`, `.streamlit/config.toml` 필요
- GitHub 저장소 연결하여 자동 배포

### Docker
```dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-kor
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Heroku
- `Procfile` 추가: `web: streamlit run app.py`
- `setup.sh` 추가: Tesseract 설치 스크립트

## 유지보수

- 정기적으로 의존성 업데이트: `pip list --outdated`
- 보안 취약점 체크: `pip-audit`
- 코드 품질 유지: `black`, `flake8`
