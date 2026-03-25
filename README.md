# ⚓ ICON FORGE — 사내 벡터 아이콘 생성기

> GitHub Codespaces 기반 | Gemini API | SVG 벡터 아이콘

---

## 🚀 처음 시작하기

### 1단계 — 이 레포를 GitHub에 올리기
```
파일 3개를 GitHub 레포에 업로드:
  - server.py
  - index.html
  - .devcontainer/devcontainer.json
```

### 2단계 — Gemini API 키 발급
1. https://aistudio.google.com 접속
2. 상단 [Get API Key] 클릭 → [Create API Key]
3. 발급된 키 복사 (AIza...로 시작)

### 3단계 — Codespaces 시작
1. GitHub 레포 → [Code] → [Codespaces] → [Create codespace]
2. Codespace 열리면 터미널에 입력:
   ```
   python server.py
   ```
3. 하단에 포트 8080 포워딩 알림 → [브라우저에서 열기] 클릭

---

## 👥 부서원 공유 방법

Codespaces 포트 포워딩 URL을 부서원에게 공유하면 됩니다.

```
예시: https://xxxxxx-8080.app.github.dev
```

> ⚠️ Codespaces가 꺼지면 URL도 끊깁니다.
> 사용 시에만 켜두고, URL을 다시 공유하세요.

---

## 📁 아이콘 아카이브

생성된 모든 아이콘은 `archive.json` 파일에 자동 저장됩니다.
이 파일을 GitHub에 커밋하면 영구 보관됩니다.

```bash
git add archive.json
git commit -m "아이콘 추가: 컨테이너선, 원자로"
git push
```

---

## 💡 PPT 활용 팁

1. 아이콘 다운로드 (.svg 파일)
2. PowerPoint → 삽입 → 그림 → SVG 파일 선택
3. 삽입 후 색상 변경: 그림 서식 → 색 → 원하는 색상
4. 벡터이므로 어떤 크기로 늘려도 선명함

---

## 🔑 권장 프롬프트 형식

```
[사물] [방향/형태] [특징]

예시:
- container ship side view with cargo stacked on deck
- nuclear reactor cross section with control rods
- cargo crane at port with cable
- anchor with rope, minimalist
- compass rose eight directions
```

영어로 작성할수록 결과 품질이 좋습니다.
