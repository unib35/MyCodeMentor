# 설치 및 시작 가이드

이 가이드는 AI CodeMentor를 설치하고 설정하는 방법을 안내합니다.

## 사전 요구 사항

- GitHub 계정
- GitHub 저장소 관리자 권한
- OpenAI API 키 (또는 다른 지원 AI 제공자 키)

## 설치 단계

### 1. GitHub Secrets 및 Variables 설정

GitHub 저장소에서 다음 Secrets와 Variables를 설정하세요:

#### Secrets
- `OPENAI_API_KEY`: OpenAI API 키
- `SLACK_BOT_TOKEN`: Slack 알림을 위한 봇 토큰 (선택 사항)
- `DISCORD_WEBHOOK_URL`: Discord 알림을 위한 웹훅 URL (선택 사항)

#### Variables
- `LANGUAGE`: 코드베이스의 주요 프로그래밍 언어 (기본값: "python")
- `REVIEW_TYPE`: 리뷰 유형 (기본값: "comprehensive")
- `MAX_FILES`: 리뷰할 최대 파일 수 (기본값: 5)

### 2. GitHub Actions 워크플로우 설정

1. 저장소에 `.github/workflows` 디렉토리를 생성합니다.
2. 다음 내용으로 `code-review.yml` 파일을 생성합니다:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: AI Code Review
        uses: username/aicodementor@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          language: ${{ vars.LANGUAGE || 'python' }}
          review-type: ${{ vars.REVIEW_TYPE || 'comprehensive' }}
          max-files: ${{ vars.MAX_FILES || 5 }}
          slack-token: ${{ secrets.SLACK_BOT_TOKEN }}
          discord-webhook: ${{ secrets.DISCORD_WEBHOOK_URL }}
```

### 3. 설정 확인

설치가 완료되면 다음을 확인하세요:

1. GitHub Actions 탭에서 워크플로우가 나타납니다.
2. 테스트 Pull Request를 생성하여 리뷰가 제대로 작동하는지 확인합니다.

## 다음 단계

- [사용 방법](usage.md)을 참조하여 AI CodeMentor를 효과적으로 사용하는 방법을 알아보세요.
- [설정 옵션](configuration.md)을 참조하여 추가 설정 옵션을 확인하세요. 