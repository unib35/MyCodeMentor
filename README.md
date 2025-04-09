# AI CodeMentor

Pull Request 리뷰를 자동화하는 AI 기반 코드 리뷰 도구입니다. 개발자가 아닌 분들도 쉽게 설정하고 사용할 수 있습니다.

## 📚 문서

자세한 안내는 다음 문서를 참조하세요:

- [설치 및 시작 가이드](docs/installation.md)
- [사용 방법](docs/usage.md)
- [설정 옵션](docs/configuration.md)
- [알림 설정](docs/notifications.md)
- [문제 해결](docs/troubleshooting.md)

## 🚀 시작하기

### 사전 준비

- GitHub 계정과 저장소 관리자 권한
- [OpenAI API 키](https://platform.openai.com/api-keys)
- (선택) Slack 워크스페이스 또는 Discord 서버 - 알림 사용 시

### 1. OpenAI API 키 획득하기

1. [OpenAI 플랫폼](https://platform.openai.com/) 웹사이트에 로그인합니다.
2. 우측 상단의 계정 아이콘 > `API keys`를 클릭합니다.
3. `+ Create new secret key` 버튼을 클릭하고 키 이름을 입력합니다 (예: "AI CodeMentor").
4. 생성된 API 키를 안전한 곳에 저장합니다. **이 키는 한 번만 표시됩니다!**

### 2. GitHub Secrets 설정하기

API 키와 웹훅 URL을 안전하게 저장하기 위해 GitHub Secrets를 설정합니다:

1. GitHub 저장소 페이지 > `Settings` > `Secrets and variables` > `Actions`로 이동합니다.
2. `Secrets` 탭에서 `New repository secret` 버튼을 클릭합니다.
3. 다음 Secret을 추가합니다:

   **필수 Secret:**
   ```
   이름: OPENAI_API_KEY
   값: sk-xxxxxxxxxxxxxxxxxxxx (OpenAI API 키)
   ```
   
   **알림 기능 사용 시 (선택 사항):**
   ```
   이름: SLACK_WEBHOOK_URL
   값: https://hooks.slack.com/services/xxx/xxx/xxx
   ```
   
   ```
   이름: DISCORD_WEBHOOK_URL
   값: https://discord.com/api/webhooks/xxx/xxx
   ```

### 3. GitHub Actions 워크플로우 설정

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
          
      - name: AI Code Review
        uses: your-org/ai-codementor@main  # 여기를 자신의 조직/계정으로 변경하세요
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          # 아래 설정은 선택사항입니다
          # slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          # discord-webhook-url: ${{ secrets.DISCORD_WEBHOOK_URL }}
          # model: 'gpt-4' # 기본값: gpt-4
          # language: 'ko' # 기본값: en (영어)
          # max-files: 5 # 기본값: 7
```

### 4. 설치 확인하기

1. 새로운 PR을 생성합니다:
   - 새 브랜치 생성: `git checkout -b test-ai-review`
   - 간단한 변경 추가: 아무 파일이나 간단히 수정
   - 커밋 및 푸시: `git commit -m "테스트: AI 리뷰 테스트" && git push -u origin test-ai-review`
   - GitHub에서 PR 생성

2. PR이 생성되면 GitHub Actions에서 AI 리뷰가 시작됩니다:
   - PR 페이지에서 "Checks" 탭을 확인하세요
   - 몇 분 후 AI가 PR에 코드 리뷰 코멘트를 추가합니다
   - Slack이나 Discord를 설정한 경우 알림도 확인해보세요

### 빠른 설정 팁

- **별도의 저장소 사용**: AI CodeMentor를 위한 별도 저장소를 만들고 여러 프로젝트에서 참조하면 관리가 더 쉽습니다.
- **비용 관리**: OpenAI API는 사용량에 따라 비용이 발생합니다. 적절한 사용량 제한을 설정하세요.
- **리뷰 제외하기**: 특정 PR에 `no-ai-review` 라벨을 추가하면 리뷰를 건너뛸 수 있습니다.
- **맞춤 설정**: 프로젝트 가이드라인을 `.github/review-guidelines.md` 파일에 추가하여 AI가 프로젝트 특화 코딩 표준을 고려하도록 할 수 있습니다.

🔍 **자세한 내용은 [설치 및 시작 가이드](docs/installation.md)를 참조하세요!**

## 📝 리뷰 내용

AI CodeMentor는 다음과 같은 리뷰를 제공합니다:

### 코드 품질 검사
- 코드 스타일과 가독성
- 잠재적인 버그
- 성능 최적화 기회
- 보안 취약점

### 테스트 관련
- 테스트 커버리지
- 테스트 케이스 제안
- 엣지 케이스 고려사항

### 개선 제안
- 코드 구조 개선
- 디자인 패턴 적용
- 리팩토링 제안

## 🚀 여러 저장소에서 사용하기

AI CodeMentor는 중앙 저장소를 통해 여러 GitHub 저장소에서 쉽게 사용할 수 있습니다. 자세한 내용은 [설치 및 시작 가이드](docs/installation.md#여러-저장소에서-사용하기)를 참조하세요.

## 📨 알림 설정

### Slack 알림
Slack 알림 설정에 대한 자세한 내용은 [알림 설정 가이드](docs/notifications.md#slack-알림-설정)를 참조하세요.

### Discord 알림
Discord 알림 설정에 대한 자세한 내용은 [알림 설정 가이드](docs/notifications.md#discord-알림-설정)를 참조하세요.

## 🛠️ 문제 해결

자주 발생하는 문제와 해결 방법은 [문제 해결 가이드](docs/troubleshooting.md)를 참조하세요.

## 🤝 기여하기

버그 리포트나 기능 제안은 Issue를 통해 해주세요. Pull Request도 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

