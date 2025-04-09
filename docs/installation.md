# AI CodeMentor 설치 및 시작 가이드

이 가이드는 AI CodeMentor를 설치하고 설정하는 방법을 상세하게 안내합니다.

## 목차
- [사전 요구사항](#사전-요구사항)
- [OpenAI API 키 획득 방법](#openai-api-키-획득-방법)
- [GitHub Secrets 및 Variables 설정](#github-secrets-및-variables-설정)
- [GitHub Actions 워크플로우 설정](#github-actions-워크플로우-설정)
- [설치 검증하기](#설치-검증하기)
- [자주 묻는 질문(FAQ)](#자주-묻는-질문)
- [문제 해결](#문제-해결)
- [다음 단계](#다음-단계)

## 사전 요구사항

### 기본 요구사항
- GitHub 계정
- GitHub 저장소 관리자 권한 (Admin 또는 Write 권한)
- OpenAI API 키 (또는 다른 지원 AI 제공자 키)

### 권장 사항
- GitHub Actions가 활성화된 저장소
- 프로젝트의 코딩 표준 또는 가이드라인 문서
- (선택 사항) Slack 워크스페이스 또는 Discord 서버 - 알림 기능 사용 시

### GitHub 환경 확인
1. GitHub 저장소에서 "Settings" 탭으로 이동합니다.
2. 왼쪽 사이드바에서 "Actions" > "General"을 선택합니다.
3. "Actions permissions" 섹션에서 Actions가 활성화되어 있는지 확인합니다.
4. "Workflow permissions" 섹션에서 "Read and write permissions"가 선택되어 있는지 확인합니다.

## OpenAI API 키 획득 방법

AI CodeMentor는 코드 리뷰를 위해 OpenAI의 GPT 모델을 사용합니다. 다음 단계에 따라 API 키를 획득하세요:

1. [OpenAI 웹사이트](https://platform.openai.com/)에 접속하여 계정을 생성하거나 로그인합니다.
2. 대시보드에서 오른쪽 상단의 프로필 아이콘을 클릭하고 "View API keys"를 선택합니다.
3. "Create new secret key" 버튼을 클릭합니다.
4. (선택 사항) 키에 대한 설명을 입력합니다 (예: "AI CodeMentor").
5. "Create secret key" 버튼을 클릭합니다.
6. 생성된 API 키를 안전한 곳에 복사해 둡니다. **주의: 이 키는 한 번만 표시되므로 반드시 저장해두세요!**

### API 사용량 및 비용 고려사항
- OpenAI API는 사용량에 따라 비용이 발생합니다. 
- 처음 가입 시 일정 금액의 무료 크레딧이 제공될 수 있습니다.
- 자세한 가격 정보는 [OpenAI 가격 페이지](https://openai.com/pricing)에서 확인할 수 있습니다.
- 예상치 못한 과도한 비용을 방지하기 위해 API 사용량 제한을 설정하는 것이 좋습니다.

## GitHub Secrets 및 Variables 설정

### GitHub Secrets 설정 (필수)

1. GitHub 저장소 페이지에서 "Settings" 탭을 클릭합니다.
2. 왼쪽 사이드바에서 "Secrets and variables" > "Actions"를 선택합니다.
3. "Secrets" 탭을 선택합니다.
4. "New repository secret" 버튼을 클릭합니다.
5. 다음 Secret을 추가합니다:

   **필수 Secret:**
   - 이름: `OPENAI_API_KEY`
     설명: OpenAI API 키
     값: 앞서 획득한 OpenAI API 키

   **알림 기능 사용 시 선택적 Secrets:**
   - 이름: `SLACK_BOT_TOKEN` 또는 `SLACK_WEBHOOK_URL`
     설명: Slack 연동용 토큰
     값: Slack API에서 발급받은 Bot 토큰 또는 웹훅 URL
     
   - 이름: `DISCORD_WEBHOOK_URL`
     설명: Discord 웹훅 URL
     값: Discord 채널에서 생성한 웹훅 URL

   **각 Secret 추가 후 "Add secret" 버튼을 클릭합니다.**

### GitHub Variables 설정 (선택 사항)

1. "Variables" 탭을 선택합니다.
2. "New repository variable" 버튼을 클릭합니다.
3. 다음 Variables를 필요에 따라 추가합니다:

   - 이름: `LANGUAGE`
     설명: 리뷰 언어 설정
     값: `ko` (한국어) 또는 `en` (영어)
     
   - 이름: `REVIEW_TYPE`
     설명: 리뷰 유형
     값: `standard`, `concise`, 또는 `detailed`
     
   - 이름: `MAX_FILES`
     설명: 리뷰할 최대 파일 수
     값: 원하는 숫자 (기본값: 5)

   - 이름: `EXCLUDE_PATTERNS`
     설명: 리뷰에서 제외할 파일 패턴
     값: 콤마로 구분된 패턴 (예: `*.md,*.json,docs/*`)

   **각 Variable 추가 후 "Add variable" 버튼을 클릭합니다.**

## GitHub Actions 워크플로우 설정

### 기본 워크플로우 설정

1. 저장소에 `.github/workflows` 디렉토리가 없다면 생성합니다:
   ```bash
   mkdir -p .github/workflows
   ```

2. `.github/workflows/ai-codementor.yml` 파일을 생성하고 다음 내용을 추가합니다:

```yaml
name: AI CodeMentor Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run AI Review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
        run: python scripts/review.py
```

### 워크플로우 파일 사용자 지정

더 세밀한 제어를 위해 다음과 같은 추가 환경 변수를 설정할 수 있습니다:

```yaml
- name: Run AI Review
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    
    # 언어 및 리뷰 유형 설정
    LANGUAGE: 'ko'  # 'ko' 또는 'en'
    REVIEW_TYPE: 'detailed'  # 'standard', 'concise', 또는 'detailed'
    
    # 파일 제한 설정
    MAX_FILES: '10'
    MAX_FILE_SIZE: '500'  # KB 단위
    
    # 포함/제외 패턴
    EXCLUDE_PATTERNS: '*.md,*.json,docs/*,test/fixtures/*'
    INCLUDE_PATTERNS: 'src/*.js,src/*.ts'
    
    # 리뷰 건너뛰기 옵션
    SKIP_LABELS: 'no-ai-review,skip-review,maintenance'
    
    # 알림 설정
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
    SLACK_CHANNEL: '#code-reviews'
    DISCORD_WEBHOOK_URL: ${{ secrets.DISCORD_WEBHOOK_URL }}
    
    # AI 모델 설정
    MODEL: 'gpt-4'  # 'gpt-3.5-turbo', 'gpt-4', 'gpt-4o' 등
    REVIEW_COMMENT_LGTM: 'true'  # 문제가 없는 파일에도 코멘트 추가
  run: python scripts/review.py
```

### 프로젝트 가이드라인 설정 (선택 사항)

AI가 프로젝트 특화 코딩 표준을 고려하도록 가이드라인 파일을 추가할 수 있습니다:

1. `.github` 디렉토리에 `review-guidelines.md` 파일을 생성합니다.
2. 다음과 같은 내용을 추가합니다:

```markdown
# 프로젝트 코드 리뷰 가이드라인

## 코딩 스타일
- 들여쓰기는 2칸 공백을 사용합니다.
- 파일 끝에는 항상 빈 줄을 추가합니다.
- 변수 명명 규칙: camelCase 사용

## 아키텍처 원칙
- 컴포넌트는 단일 책임 원칙을 따릅니다.
- 비즈니스 로직은 UI 컴포넌트와 분리합니다.
- 전역 상태는 최소한으로 사용합니다.

## 테스트 요구사항
- 모든 비즈니스 로직에는 단위 테스트가 필요합니다.
- UI 컴포넌트에는 스냅샷 테스트를 추가합니다.
- 통합 테스트는 주요 사용자 흐름을 다루어야 합니다.

## 성능 고려사항
- 불필요한 렌더링을 피합니다.
- 대규모 목록에는 가상화를 사용합니다.
- 비용이 많이 드는 계산에는 메모이제이션을 사용합니다.

## 보안 요구사항
- 사용자 입력은 항상 검증합니다.
- API 응답은 적절히 오류 처리합니다.
- 민감한 정보는 하드코딩하지 않습니다.
```

## 설치 검증하기

설치가 제대로 되었는지 확인하려면:

1. 테스트 Pull Request 생성하기:
   - 새 브랜치를 생성합니다: `git checkout -b test-ai-review`
   - 간단한 코드 변경을 수행합니다 (예: 주석 추가 또는 함수 수정)
   - 변경 사항을 커밋하고 푸시합니다: `git commit -m "테스트: AI 리뷰 확인" && git push -u origin test-ai-review`
   - GitHub 웹사이트에서 해당 브랜치에 대한 Pull Request를 생성합니다

2. GitHub Actions 실행 확인:
   - PR 페이지의 "Checks" 탭에서 AI 리뷰 워크플로우가 실행 중인지 확인합니다
   - 또는 저장소의 "Actions" 탭으로 이동하여 워크플로우 실행 상태를 확인합니다

3. 리뷰 결과 확인:
   - 워크플로우가 완료된 후 PR에 AI의 코드 리뷰 코멘트가 추가되었는지 확인합니다
   - Slack 또는 Discord 알림이 구성된 경우 해당 채널에서 알림을 확인합니다

4. 로그 확인:
   - 문제가 있는 경우 "Actions" 탭에서 워크플로우를 클릭하고 로그를 확인합니다
   - 오류 메시지를 검토하고 필요한 경우 설정을 조정합니다

## 자주 묻는 질문

### Q: OpenAI API 키 외에 다른 AI 제공자를 사용할 수 있나요?
A: 현재 버전에서는 OpenAI API가 기본적으로 지원됩니다. 향후 업데이트에서 다른 제공자가 추가될 수 있습니다.

### Q: 워크플로우 실행 시간이 너무 길어요. 어떻게 최적화할 수 있나요?
A: `MAX_FILES`와 `MAX_FILE_SIZE` 환경 변수를 조정하여 처리되는 파일 수와 크기를 제한할 수 있습니다. 또한 `EXCLUDE_PATTERNS`를 사용하여 불필요한 파일을 제외하세요.

### Q: PR이 매우 큰 경우 어떻게 해야 하나요?
A: 큰 PR은 여러 개의 작은 PR로 나누는 것이 좋습니다. 불가피하게 큰 PR이 필요한 경우 `MAX_FILES` 값을 높이고 `INCLUDE_PATTERNS`을 사용하여 중요한 파일에 집중하세요.

### Q: 특정 PR에 대해 AI 리뷰를 건너뛰고 싶어요.
A: PR에 `no-ai-review` 또는 `skip-review` 라벨을 추가하거나, 환경 변수에서 `SKIP_LABELS`을 사용하여 추가 라벨을 정의할 수 있습니다.

### Q: AI 리뷰의 언어를 변경할 수 있나요?
A: 네, `LANGUAGE` 환경 변수를 사용하여 언어를 설정할 수 있습니다. 현재 `ko`(한국어)와 `en`(영어)이 지원됩니다.

### Q: Secrets가 노출되지 않도록 하려면 어떻게 해야 하나요?
A: GitHub Secrets는 워크플로우 로그에 자동으로 마스킹됩니다. 하지만 코드 내에서 절대 API 키나 토큰을 하드코딩하지 마세요.

## 문제 해결

### 워크플로우가 실행되지 않음
- GitHub Actions가 저장소에서 활성화되어 있는지 확인하세요.
- PR이 `opened` 또는 `synchronize` 이벤트를 트리거하는지 확인하세요.
- 워크플로우 파일 구문이 올바른지 확인하세요.

### API 키 오류
- GitHub Secrets에 `OPENAI_API_KEY`가 올바르게 설정되어 있는지 확인하세요.
- OpenAI API 키가 유효하고 활성 상태인지 확인하세요.
- API 키에 충분한 크레딧이 있는지 확인하세요.

### 알림이 작동하지 않음
- Slack/Discord 웹훅 URL이 올바르게 설정되어 있는지 확인하세요.
- 웹훅 권한이 적절히 구성되어 있는지 확인하세요.
- 워크플로우 파일에서 알림 환경 변수가 올바르게 지정되었는지 확인하세요.

더 자세한 문제 해결 가이드는 [문제 해결](troubleshooting.md) 문서를 참조하세요.

## 다음 단계

설치가 완료되었다면 다음 단계를 확인하세요:

- [사용 방법](usage.md): AI CodeMentor를 효과적으로 사용하는 방법 알아보기
- [설정 옵션](configuration.md): 추가 설정 옵션 및 커스터마이징 방법 확인하기
- [알림 설정](notifications.md): Slack과 Discord 알림 상세 설정 방법 알아보기 