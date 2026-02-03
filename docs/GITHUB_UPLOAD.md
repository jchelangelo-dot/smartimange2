# GitHub 업로드 가이드

## 📦 준비된 파일들

```
smart-namer-ocr/
├── app.py                      ✅ 메인 애플리케이션
├── requirements.txt            ✅ 의존성 목록
├── README.md                   ✅ 프로젝트 설명
├── LICENSE                     ✅ MIT 라이선스
├── CHANGELOG.md                ✅ 변경 이력
├── CONTRIBUTING.md             ✅ 기여 가이드
├── .gitignore                  ✅ Git 제외 파일
├── .streamlit/config.toml      ✅ Streamlit 설정
├── docs/                       ✅ 문서 폴더
│   ├── INSTALL.md             ✅ 설치 가이드
│   └── PROJECT_STRUCTURE.md   ✅ 프로젝트 구조
└── tests/                      ✅ 테스트 폴더
    └── test_app.py            ✅ 단위 테스트
```

---

## 🚀 GitHub에 업로드하는 방법

### 방법 1: 새 저장소 생성 (추천)

#### 1단계: GitHub에서 새 저장소 생성

1. [GitHub](https://github.com)에 로그인
2. 우측 상단 `+` → `New repository` 클릭
3. 저장소 정보 입력:
   - **Repository name**: `smart-namer-ocr`
   - **Description**: `🔍 AI-powered image OCR tool for smart file naming`
   - **Public** 또는 **Private** 선택
   - ✅ **Add README file** 체크 **하지 않기** (이미 있음)
   - ✅ **Add .gitignore** 체크 **하지 않기** (이미 있음)
   - **Choose a license**: MIT (또는 None)
4. `Create repository` 클릭

#### 2단계: 로컬 Git 초기화

터미널을 열고 프로젝트 폴더로 이동:

```bash
cd smart-namer-ocr
```

Git 초기화:

```bash
git init
git add .
git commit -m "Initial commit: Add Smart AI Namer v1.0.0"
```

#### 3단계: GitHub에 푸시

GitHub에 표시된 명령어 사용:

```bash
git remote add origin https://github.com/yourusername/smart-namer-ocr.git
git branch -M main
git push -u origin main
```

> **참고**: `yourusername`을 본인의 GitHub 사용자명으로 변경하세요!

---

### 방법 2: GitHub Desktop 사용 (초보자 추천)

#### 1단계: GitHub Desktop 설치

- [GitHub Desktop 다운로드](https://desktop.github.com/)

#### 2단계: 저장소 생성

1. GitHub Desktop 실행
2. `File` → `New repository`
3. 정보 입력:
   - **Name**: `smart-namer-ocr`
   - **Local path**: 프로젝트 폴더 선택
   - **Initialize with README**: 체크 해제
4. `Create repository` 클릭

#### 3단계: 변경사항 커밋

1. 좌측에서 변경된 파일 확인
2. 하단 Summary: `Initial commit`
3. `Commit to main` 클릭

#### 4단계: GitHub에 게시

1. 상단 `Publish repository` 클릭
2. **Keep this code private** 체크 여부 선택
3. `Publish repository` 클릭

---

### 방법 3: GitHub CLI 사용 (고급)

#### 1단계: GitHub CLI 설치

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows (Scoop)
scoop install gh
```

#### 2단계: 로그인

```bash
gh auth login
```

#### 3단계: 저장소 생성 및 푸시

```bash
cd smart-namer-ocr
git init
git add .
git commit -m "Initial commit"

# GitHub에 저장소 생성 및 푸시
gh repo create smart-namer-ocr --public --source=. --push
```

---

## ✅ 업로드 후 확인사항

### 1. README가 제대로 표시되는지 확인
- 이미지, 배지, 링크가 정상 작동하는지

### 2. Issues 탭 활성화
- `Settings` → `Features` → `Issues` 체크

### 3. Discussions 활성화 (선택)
- `Settings` → `Features` → `Discussions` 체크

### 4. Topics 추가
- 저장소 페이지 → `About` 옆 ⚙️ 클릭
- Topics 추가:
  - `ocr`
  - `streamlit`
  - `python`
  - `image-processing`
  - `tesseract`
  - `opencv`

### 5. Description 추가
```
🔍 AI-powered image OCR tool for smart file naming with advanced preprocessing
```

### 6. Website 추가 (배포 후)
- Streamlit Cloud 배포 후 URL 추가

---

## 🌟 다음 단계

### 1. Streamlit Cloud에 배포

1. [share.streamlit.io](https://share.streamlit.io) 접속
2. `New app` 클릭
3. GitHub 저장소 연결
4. **Main file path**: `app.py`
5. **Python version**: 3.9
6. `Deploy!` 클릭

배포 URL 예시: `https://smart-namer.streamlit.app`

### 2. 배지(Badge) 추가

README.md 상단에 추가:

```markdown
![GitHub stars](https://img.shields.io/github/stars/yourusername/smart-namer-ocr)
![GitHub forks](https://img.shields.io/github/forks/yourusername/smart-namer-ocr)
![GitHub issues](https://img.shields.io/github/issues/yourusername/smart-namer-ocr)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
```

### 3. 릴리즈 생성

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

GitHub에서:
1. `Releases` → `Create a new release`
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial Release`
4. Description: CHANGELOG.md 내용 복사
5. `Publish release`

### 4. 소셜 미디어 공유

- Twitter/X
- Reddit (r/Python, r/learnprogramming)
- LinkedIn
- 개발 커뮤니티

---

## 🔧 문제 해결

### 푸시 실패: Authentication failed

**해결방법:**

1. **Personal Access Token 생성**
   - GitHub → Settings → Developer settings
   - Personal access tokens → Generate new token
   - `repo` 권한 선택
   - 토큰 복사

2. **토큰으로 인증**
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/yourusername/smart-namer-ocr.git
   ```

### 대용량 파일 경고

**해결방법:**

```bash
# .gitignore에 추가
*.png
*.jpg
*.jpeg
large_files/
```

### 파일 권한 문제

**해결방법:**

```bash
chmod +x scripts/*.sh  # 스크립트 실행 권한
chmod 644 *.md         # 문서 읽기 권한
```

---

## 📞 도움이 필요하신가요?

- 💬 [GitHub Discussions](https://github.com/yourusername/smart-namer-ocr/discussions)
- 🐛 [Issues](https://github.com/yourusername/smart-namer-ocr/issues)
- 📧 your.email@example.com

---

## 🎉 축하합니다!

프로젝트가 GitHub에 성공적으로 업로드되었습니다!

다음을 잊지 마세요:
- ⭐ 스타 모으기 시작!
- 📣 프로젝트 공유하기
- 🔄 정기적인 업데이트
- 🤝 커뮤니티와 소통

**Happy Coding! 🚀**
