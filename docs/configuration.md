# 설정 옵션

이 문서는 AI CodeMentor의 다양한 설정 옵션과 커스터마이징 방법을 설명합니다.

## GitHub 워크플로우 설정

워크플로우 파일(`.github/workflows/code-review.yml`)에서 AI CodeMentor의 동작을 구성할 수 있습니다.

### 기본 설정

기본 워크플로우 파일에는 다음과 같은 필수 구성 요소가 포함되어 있습니다:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]
    
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          language: 'ko'
          max-files: 50
```

### 주요 매개변수

| 매개변수 | 필수 여부 | 기본값 | 설명 |
|---------|---------|-------|------|
| `github-token` | 필수 | - | GitHub API와 상호작용하기 위한 토큰 |
| `openai-api-key` | 필수 | - | OpenAI API 키 |
| `language` | 선택 | `en` | 리뷰 언어 (`ko` 또는 `en`) |
| `review-type` | 선택 | `standard` | 리뷰 유형 (`standard`, `concise`, `detailed` 중 선택) |
| `max-files` | 선택 | `20` | 리뷰할 최대 파일 수 |
| `max-file-size` | 선택 | `500` | 리뷰할 최대 파일 크기(KB) |
| `exclude-patterns` | 선택 | 기본 패턴 | 리뷰에서 제외할 파일 패턴 (콤마로 구분) |
| `include-patterns` | 선택 | 없음 | 리뷰에 포함할 파일 패턴 (콤마로 구분) |
| `skip-labels` | 선택 | `no-ai-review,skip-review` | 리뷰를 건너뛸 라벨 목록 |
| `review-comment-lgtm` | 선택 | `false` | 문제가 없는 파일에도 LGTM 코멘트 추가 여부 |

## 고급 설정

### 리뷰 유형 설정

`review-type` 매개변수로 리뷰의 자세함 정도를 설정할 수 있습니다:

- `concise`: 간결한 리뷰, 주요 문제점만 지적
- `standard`: 기본 리뷰 수준
- `detailed`: 상세한 리뷰, 작은 문제점도 지적하고 더 많은 개선 제안 제공

```yaml
with:
  review-type: 'detailed'
```

### 파일 포함/제외 패턴

특정 파일 유형이나 경로를 리뷰에 포함하거나 제외하는 패턴을 설정할 수 있습니다:

```yaml
with:
  exclude-patterns: '*.md,*.json,docs/*,test/fixtures/*'
  include-patterns: 'src/*.js,src/*.ts'
```

기본적으로 제외되는 패턴:
```
.github/**,*.md,package-lock.json,yarn.lock,pnpm-lock.yaml,*.log,*.svg,*.png,*.jpg,*.jpeg,*.gif,*.ico
```

### 리뷰 최대 파일 수 조정

대규모 PR에서 리뷰할 파일의 최대 수를 조정할 수 있습니다:

```yaml
with:
  max-files: 100
```

**참고**: 파일 수가 많을수록 GitHub Actions 실행 시간이 길어지고 OpenAI API 사용량이 증가할 수 있습니다.

## 알림 설정

알림 설정에 대한 자세한 내용은 [알림 설정 문서](notifications.md)를 참조하세요.

## 팀 프로젝트를 위한 설정

### 프로젝트 특화 리뷰 가이드

프로젝트 특화 리뷰 가이드를 설정하여 AI가 프로젝트의 코딩 표준과 관행을 고려하도록 할 수 있습니다:

```yaml
with:
  project-guidelines-file: '.github/review-guidelines.md'
```

`review-guidelines.md` 파일에는 다음과 같은 내용을 포함할 수 있습니다:
- 코딩 스타일 가이드
- 아키텍처 원칙
- 테스트 요구사항
- 성능 고려사항
- 보안 요구사항
- 릴리스 프로세스

### 커스텀 프롬프트 템플릿

고급 사용자의 경우, 커스텀 프롬프트 템플릿을 사용하여 AI 리뷰 프로세스를 세밀하게 조정할 수 있습니다:

```yaml
with:
  custom-prompt-template: '.github/review-prompt.md'
```

## 세부 설정 예시

다음은 자세한 설정 예시입니다:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]
    
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          language: 'ko'
          review-type: 'detailed'
          max-files: 30
          max-file-size: 1000
          exclude-patterns: '*.md,*.json,docs/*,test/fixtures/*'
          include-patterns: 'src/*.js,src/*.ts'
          skip-labels: 'no-ai-review,skip-review,maintenance'
          slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          discord-webhook-url: ${{ secrets.DISCORD_WEBHOOK_URL }}
          review-comment-lgtm: true
          project-guidelines-file: '.github/review-guidelines.md'
```

## 문제 해결

설정 관련 문제 해결은 [문제 해결 가이드](troubleshooting.md)를 참조하세요. 