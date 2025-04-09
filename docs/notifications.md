# 알림 설정

AI CodeMentor는 PR 리뷰가 완료되면 팀에 알림을 보낼 수 있습니다. 현재 Slack과 Discord를 통한 알림을 지원합니다.

## Slack 알림 설정

### 기본 설정

Slack 알림을 설정하려면 워크플로우 파일에 `slack-webhook-url` 매개변수를 추가하세요:

```yaml
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}
  openai-api-key: ${{ secrets.OPENAI_API_KEY }}
  slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Slack 웹훅 URL 설정 방법

1. Slack 워크스페이스 관리자 권한이 있는 계정으로 로그인합니다.
2. [Slack API 웹사이트](https://api.slack.com/apps)에서 "Create New App"을 클릭합니다.
3. "From scratch"를 선택하고 앱 이름과 워크스페이스를 설정합니다.
4. 왼쪽 메뉴에서 "Incoming Webhooks"를 선택합니다.
5. "Activate Incoming Webhooks"를 "On"으로 설정합니다.
6. "Add New Webhook to Workspace"를 클릭합니다.
7. 알림을 받을 채널을 선택하고 "Allow"를 클릭합니다.
8. 생성된 웹훅 URL을 복사합니다.

### GitHub Secrets에 웹훅 URL 저장

1. GitHub 저장소의 "Settings" 탭으로 이동합니다.
2. "Secrets and variables" > "Actions"를 선택합니다.
3. "New repository secret"을 클릭합니다.
4. 이름을 `SLACK_WEBHOOK_URL`로 설정하고, 값에 복사한 웹훅 URL을 붙여넣습니다.
5. "Add secret"을 클릭합니다.

### 고급 Slack 설정

추가 Slack 설정을 구성할 수 있습니다:

```yaml
with:
  slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
  slack-username: 'AI CodeMentor'
  slack-icon-emoji: ':robot_face:'
  slack-channel: '#code-reviews'
```

| 매개변수 | 필수 여부 | 기본값 | 설명 |
|---------|---------|-------|------|
| `slack-webhook-url` | 필수 | - | Slack 웹훅 URL |
| `slack-username` | 선택 | `AI CodeMentor` | Slack에 표시될 봇 이름 |
| `slack-icon-emoji` | 선택 | `:robot_face:` | 봇 아이콘으로 사용할 이모지 |
| `slack-channel` | 선택 | 웹훅 설정의 기본 채널 | 알림을 보낼 채널 (예: `#code-reviews`) |

## Discord 알림 설정

### 기본 설정

Discord 알림을 설정하려면 워크플로우 파일에 `discord-webhook-url` 매개변수를 추가하세요:

```yaml
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}
  openai-api-key: ${{ secrets.OPENAI_API_KEY }}
  discord-webhook-url: ${{ secrets.DISCORD_WEBHOOK_URL }}
```

### Discord 웹훅 URL 설정 방법

1. Discord 서버 관리자 권한이 있는 계정으로 로그인합니다.
2. 웹훅을 추가할 채널로 이동합니다.
3. 채널 이름 옆의 설정 아이콘(⚙️)을 클릭합니다.
4. "Integrations" > "Webhooks"로 이동합니다.
5. "New Webhook"을 클릭합니다.
6. 웹훅 이름을 설정하고 아바타를 선택합니다 (선택 사항).
7. "Copy Webhook URL"을 클릭하여 웹훅 URL을 복사합니다.

### GitHub Secrets에 웹훅 URL 저장

1. GitHub 저장소의 "Settings" 탭으로 이동합니다.
2. "Secrets and variables" > "Actions"를 선택합니다.
3. "New repository secret"을 클릭합니다.
4. 이름을 `DISCORD_WEBHOOK_URL`로 설정하고, 값에 복사한 웹훅 URL을 붙여넣습니다.
5. "Add secret"을 클릭합니다.

### 고급 Discord 설정

추가 Discord 설정을 구성할 수 있습니다:

```yaml
with:
  discord-webhook-url: ${{ secrets.DISCORD_WEBHOOK_URL }}
  discord-username: 'AI CodeMentor'
  discord-avatar-url: 'https://example.com/avatar.png'
```

| 매개변수 | 필수 여부 | 기본값 | 설명 |
|---------|---------|-------|------|
| `discord-webhook-url` | 필수 | - | Discord 웹훅 URL |
| `discord-username` | 선택 | `AI CodeMentor` | Discord에 표시될 봇 이름 |
| `discord-avatar-url` | 선택 | 기본 아바타 | 봇 아바타로 사용할 이미지 URL |

## 동시에 여러 알림 플랫폼 사용

Slack과 Discord 알림을 동시에 설정할 수 있습니다:

```yaml
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}
  openai-api-key: ${{ secrets.OPENAI_API_KEY }}
  slack-webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
  discord-webhook-url: ${{ secrets.DISCORD_WEBHOOK_URL }}
```

## 알림 커스터마이징

### 알림 템플릿 설정

알림 메시지의 형식을 커스터마이징하려면 템플릿 파일을 사용할 수 있습니다:

```yaml
with:
  notification-template-file: '.github/notification-template.md'
```

템플릿 파일에서는 다음과 같은 변수를 사용할 수 있습니다:
- `{{pr_title}}`: PR 제목
- `{{pr_number}}`: PR 번호
- `{{pr_author}}`: PR 작성자
- `{{pr_url}}`: PR URL
- `{{review_summary}}`: 리뷰 요약
- `{{review_files_count}}`: 리뷰된 파일 수
- `{{repository}}`: 저장소 이름

예시 템플릿:
```md
# 새로운 PR 리뷰: {{pr_title}}

**PR #{{pr_number}}** by {{pr_author}}
**저장소:** {{repository}}

## 리뷰 요약
{{review_summary}}

총 {{review_files_count}}개 파일이 리뷰되었습니다.

[PR 보기]({{pr_url}})
```

## 알림 비활성화

특정 PR에 대한 알림을 비활성화하려면 해당 PR에 'no-notification' 라벨을 추가하세요.

또는 워크플로우 설정에서 알림 관련 매개변수를 제거하여 전체 프로젝트에 대한 알림을 비활성화할 수 있습니다.

## 문제 해결

알림이 작동하지 않는 경우 다음을 확인하세요:

1. 웹훅 URL이 올바르게 설정되었는지 확인
2. GitHub Secrets에 웹훅 URL이 올바르게 저장되었는지 확인
3. 워크플로우 파일에서 매개변수 이름을 정확하게 입력했는지 확인
4. GitHub Actions 로그에서 알림 관련 오류 메시지 확인

자세한 문제 해결 방법은 [문제 해결 가이드](troubleshooting.md)를 참조하세요. 