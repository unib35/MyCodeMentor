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

### 1. GitHub Secrets 설정하기

AI CodeMentor가 작동하려면 필요한 API 키를 GitHub Secrets에 설정해야 합니다:

1. GitHub 저장소 페이지에서 상단 탭의 `Settings`를 클릭합니다.
2. 좌측 사이드바에서 `Secrets and variables`를 확장합니다.
3. `Actions`를 클릭합니다.
4. `Secrets` 탭이 선택되어 있는지 확인합니다.
5. `New repository secret` 버튼을 클릭합니다.
6. 다음 Secret을 하나씩 추가합니다:

   **필수 Secret:**
   - 이름: `OPENAI_API_KEY`
     설명: OpenAI API 키
     값: [OpenAI 대시보드](https://platform.openai.com/api-keys)에서 발급받은 API 키
     
   **선택적 Secret (알림 기능 사용 시):**
   - 이름: `SLACK_WEBHOOK_URL`
     설명: Slack 연동용 웹훅 URL
     값: Slack API에서 발급받은 웹훅 URL
     
   - 이름: `DISCORD_WEBHOOK_URL`
     설명: Discord 웹훅 URL
     값: Discord 채널에서 생성한 웹훅 URL (형식: `https://discord.com/api/webhooks/1234567890123456789/X...`)

### 2. GitHub Actions 워크플로우 설정

1. 저장소에 `.github/workflows/ai-codementor.yml` 파일을 생성합니다:

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
      - name: AI Code Review
        uses: your-org/ai-codementor@main  # 여기를 자신의 조직/계정으로 변경하세요
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          # 아래 설정은 선택사항입니다
          # slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          # discord-webhook-url: ${{ secrets.DISCORD_WEBHOOK_URL }}
          # model: 'gpt-4' # 기본값: gpt-4
          # language: 'korean' # 기본값: english
          # max-files: 5 # 기본값: 7
```

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

