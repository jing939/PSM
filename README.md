<img width="1583" height="1250" alt="스크린샷 2026-04-28 175905" src="https://github.com/user-attachments/assets/4960daa4-09d9-41de-9b58-da87098c4d13" />

## 🧠 AI 기반 개인화 글쓰기 어시스턴트

## 📌 프로젝트 소개

Ollama 기반 로컬 LLM을 활용하여 사용자의 글을 분석하고, 문맥에 맞게 자연스럽게 수정 및 개선하는 AI 글쓰기 어시스턴트입니다.
VS Code 환경에서 AI 코딩 도구(Continue)를 활용해 웹 기반 서비스 형태로 구현했습니다.

---

## ⚙️ 기술 스택

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: FastAPI (Python)
* **AI Model**: Llama3 (Ollama)
* **AI Tool**: Continue (VS Code Extension)
* **GPU**: NVIDIA RTX A4000 (16GB)

---

## 🧩 주요 기능

* 사용자 입력 문장 개선 및 자연스러운 문장 생성
* AI 기반 텍스트 요약 기능
* 로컬 LLM을 활용한 빠른 응답 처리
* 웹 UI를 통한 간단한 입력/출력 인터페이스

---

## 🚀 실행 방법

### 1. Ollama 실행

```bash
ollama serve
ollama run llama3
```

### 2. 백엔드 실행

```bash
uvicorn app.main:app --reload
```

### 3. 웹 실행

* `index.html` 실행 또는 브라우저에서 확인

---

## 🔗 API 엔드포인트

* `POST /summary/`
  → 입력 문장을 요약하여 반환

---

## 💡 프로젝트 특징

* 클라우드가 아닌 **로컬 환경에서 AI 실행**
* GPU(A4000)를 활용한 성능 최적화
* AI 코딩 도구를 활용한 개발 효율 향상

---

## 📈 기대 효과

* 개인 맞춤형 글쓰기 지원
* AI 기반 생산성 향상
* 로컬 AI 활용 사례 구현

---

## 🧪 향후 개선

* 문체 분석 기능 추가
* 사용자 맞춤 스타일 학습
* UI/UX 개선

---
