# AI CodeMentor 문제 해결 가이드

AI CodeMentor를 설치하고 사용하는 과정에서 발생할 수 있는 일반적인 문제와 해결 방법을 안내합니다.

## 목차
- [설치 및 설정 문제](#설치-및-설정-문제)
- [워크플로우 실행 문제](#워크플로우-실행-문제)
- [API 키 문제](#api-키-문제)
- [리뷰 결과 문제](#리뷰-결과-문제)
- [알림 문제](#알림-문제)
- [권한 문제](#권한-문제)
- [Git 및 브랜치 문제](#git-및-브랜치-문제)

## 설치 및 설정 문제

### 워크플로우 파일 설정 오류

**증상:** 워크플로우 파일 생성 후 GitHub Actions에서 YAML 구문 오류가 표시됩니다.

**해결 방법:**
1. `.github/workflows/ai-codementor.yml` 파일의 들여쓰기가 올바른지 확인합니다.
2. 모든 YAML 키-값 쌍이 올바르게 구성되었는지 확인합니다.
3. GitHub 웹 인터페이스에서 파일을 편집할 때는 자동으로 YAML 유효성 검사가 이루어집니다.

### 필수 파일 누락

**증상:** 워크플로우는 실행되지만 "File not found" 오류와 함께 실패합니다.

**해결 방법:**
1. 저장소에 다음 파일들이 모두 포함되어 있는지 확인합니다:
   - `.github/workflows/ai-codementor.yml`
   - `requirements.txt`
   - `scripts/` 디렉토리와 그 안의 Python 파일들

2. 필요한 파일 구조:
```
.github/
└── workflows/
    └── ai-codementor.yml
scripts/
├── review.py
├── ai_service.py
├── github_service.py
├── diff_parser.py
├── style_checker.py
├── slack_service.py
└── discord_service.py
requirements.txt
```

## 워크플로우 실행 문제

### 워크플로우가 실행되지 않음

**증상:** PR을 생성했지만 AI 리뷰 워크플로우가 실행되지 않습니다.

**해결 방법:**
1. GitHub 저장소의 "Actions" 탭에서 워크플로우 활성화 상태를 확인합니다.
2. 저장소 설정 > Actions > General에서 "Allow all actions and reusable workflows"가 선택되어 있는지 확인합니다.
3. 워크플로우 파일에 `pull_request` 이벤트와 타입이 올바르게 설정되어 있는지 확인합니다:

```yaml
on:
  pull_request:
    types: [opened, synchronize]
```

### 워크플로우 실행 시간 초과

**증상:** 대규모 PR에서 워크플로우가 시간 초과로 실패합니다.

**해결 방법:**
1. 환경 변수 `MAX_FILES`를 사용하여 리뷰할 파일 수를 제한합니다.
2. 환경 변수 `EXCLUDE_PATTERNS`를 사용하여 불필요한 파일을 제외합니다.
3. PR을 더 작은 단위로 나누어 제출합니다.

## API 키 문제

### OpenAI API 키 오류

**증상:** `Invalid API key` 또는 `Authentication error` 오류가 발생합니다.

**해결 방법:**
1. GitHub Secrets에 `OPENAI_API_KEY`가 올바르게 설정되어 있는지 확인합니다:
   - 저장소 설정 > Secrets and variables > Actions로 이동
   - Repository secrets 확인

2. API 키 형식이 올바른지 확인합니다:
   - OpenAI API 키는 `sk-`로 시작해야 합니다
   - 키에 공백이나 따옴표가 포함되어 있지 않아야 합니다

3. API 키가 활성 상태인지 OpenAI 대시보드에서 확인합니다.

### API 사용량 한도 초과

**증상:** `Rate limit exceeded` 또는 `You exceeded your current quota` 오류가 발생합니다.

**해결 방법:**
1. OpenAI 계정에 결제 수단이 등록되어 있는지 확인합니다.
2. OpenAI 대시보드에서 사용량 및 한도를 확인합니다.
3. 환경 변수 `MODEL`을 `gpt-3.5-turbo`와 같이 더 저렴한 모델로 설정합니다.

## 리뷰 결과 문제

### 리뷰가 생성되지 않음

**증상:** 워크플로우는 성공적으로 실행되지만 PR에 리뷰 코멘트가 나타나지 않습니다.

**해결 방법:**
1. 워크플로우 권한 설정 확인:
```yaml
permissions:
  pull-requests: write
  contents: read
```

2. GitHub 저장소 설정 > Actions > General에서 "Workflow permissions"가 "Read and write permissions"로 설정되어 있는지 확인합니다.

3. 환경 변수 `GITHUB_TOKEN`이 자동으로 제공되는지 확인합니다.

### 리뷰 품질 문제

**증상:** AI 리뷰가 관련 없거나 유용하지 않은 내용을 제공합니다.

**해결 방법:**
1. 환경 변수 `MODEL`을 `gpt-4` 또는 `gpt-4o`와 같은 더 강력한 모델로 설정합니다.
2. PR 설명에 더 명확한 컨텍스트와 목적을 제공합니다.
3. 환경 변수 `REVIEW_TYPE`을 `detailed`로 설정하여 더 자세한 리뷰를 받습니다.

## 알림 문제

### Slack 알림 문제

**증상:** PR 리뷰는 작동하지만 Slack 알림이 오지 않습니다.

**해결 방법:**
1. GitHub Secrets에 `SLACK_WEBHOOK_URL` 또는 `SLACK_BOT_TOKEN`이 올바르게 설정되어 있는지 확인합니다.
2. 환경 변수 `SLACK_CHANNEL`이 올바른 채널 이름(예: `#code-reviews`)으로 설정되어 있는지 확인합니다.
3. Slack 앱 설정에서 필요한 권한이 부여되어 있는지 확인합니다:
   - `chat:write`
   - `incoming-webhook`

### Discord 알림 문제

**증상:** PR 리뷰는 작동하지만 Discord 알림이 오지 않습니다.

**해결 방법:**
1. GitHub Secrets에 `DISCORD_WEBHOOK_URL`이 올바르게 설정되어 있는지 확인합니다.
2. Discord 웹훅 URL이 유효한지 확인합니다:
   - Discord 서버 설정 > 연동 > 웹후크에서 확인
   - 필요시 새 웹훅을 생성하고 URL을 업데이트합니다
3. 웹훅 URL 형식은 `https://discord.com/api/webhooks/...`여야 합니다.

## 권한 문제

### GitHub 권한 부족

**증상:** 워크플로우가 `Resource not accessible by integration` 오류와 함께 실패합니다.

**해결 방법:**
1. 저장소 설정 > Actions > General에서 "Workflow permissions"를 "Read and write permissions"로 설정합니다.
2. 워크플로우 파일에 권한 설정을 추가합니다:
```yaml
permissions:
  pull-requests: write
  contents: read
```

3. Organization 설정의 경우, Organization Settings > Actions > General에서 "Workflow permissions"를 확인합니다.

### 조직 수준 제한

**증상:** 조직 저장소에서 워크플로우가 실행되지 않거나 권한 오류가 발생합니다.

**해결 방법:**
1. 조직 관리자에게 문의하여 다음 사항을 확인합니다:
   - 워크플로우 실행 권한
   - Action 사용 권한
   - Secret 접근 권한
2. Organization Settings > Actions > General에서 "Allowed actions"가 "Allow all actions"로 설정되어 있는지 확인합니다.

## Git 및 브랜치 문제

### 브랜치 참조 오류

**증상:** 워크플로우가 `fatal: ambiguous argument` 오류와 함께 실패합니다.

**해결 방법:**
1. 워크플로우 파일에 모든 브랜치를 가져오는 단계 추가:
```yaml
- uses: actions/checkout@v3
  with:
    fetch-depth: 0
    ref: ${{ github.event.pull_request.head.sha }}  # PR의 헤드를 명시적으로 체크아웃

- name: Fetch all branches
  run: |
    git fetch --all
    git fetch origin +refs/heads/*:refs/remotes/origin/*
```

2. 기본 브랜치가 `main`이 아닌 경우 해당 브랜치 이름을 환경 변수로 설정:
```yaml
env:
  BASE_BRANCH: develop  # 또는 master, production 등
```

### 워크플로우 파일이 없는 브랜치 문제

**증상:** PR을 생성했지만 AI CodeMentor가 리뷰를 수행하지 않고, GitHub Actions에서 워크플로우가 실행되지 않습니다.

**원인:** 
GitHub Actions는 PR의 대상 브랜치(base branch)가 아닌 **PR을 생성한 브랜치(head branch)의 워크플로우 파일**을 사용합니다. 따라서 `.github/workflows/code-review.yml` 파일이 PR을 생성한 브랜치에 없으면 워크플로우가 실행되지 않습니다.

**해결 방법:**
1. 기본 브랜치(main 또는 develop)에 `.github/workflows/code-review.yml` 파일을 먼저 추가합니다.
2. 기본 브랜치에 워크플로우 파일을 추가하는 PR을 생성하고 병합합니다.
3. 이후 모든 새 브랜치는 반드시 워크플로우 파일이 포함된 기본 브랜치에서 분기합니다:
   ```bash
   git checkout main  # 또는 develop
   git pull
   git checkout -b feature/my-new-feature
   ```
4. 이제 이 브랜치에서 PR을 생성하면 AI 리뷰가 정상적으로 실행됩니다.

**주의사항:**
* 이미 생성된 오래된 브랜치의 경우, 해당 브랜치를 기본 브랜치와 동기화하여 워크플로우 파일을 포함시켜야 합니다:
  ```bash
  git checkout my-existing-branch
  git merge main  # 또는 develop
  git push
  ```
* 팀원들에게 항상 최신 기본 브랜치에서 새 브랜치를 생성하도록 안내하세요.

### 특수 브랜치 전략 문제

**증상:** 특정 브랜치 전략(Git Flow, GitHub Flow 등)을 사용할 때 워크플로우가 올바르게 작동하지 않습니다.

**해결 방법:**
1. 브랜치 명명 규칙이 일관되게 적용되었는지 확인합니다.
2. PR이 올바른 브랜치 간에 생성되었는지 확인합니다(예: feature -> develop, develop -> main).
3. 위의 브랜치 참조 오류 해결 방법을 적용합니다. 