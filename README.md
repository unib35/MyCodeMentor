# AI CodeMentor (AICodeMentor)

Pull Request 리뷰를 자동화하는 AI 기반 코드 리뷰 도구입니다. 개발자가 아닌 분들도 쉽게 설정하고 사용할 수 있습니다.

## 🚀 여러 저장소에서 사용하기

AI CodeMentor는 중앙 저장소를 통해 여러 GitHub 저장소에서 쉽게 사용할 수 있습니다.

### 중앙 저장소 설정 (조직 또는 개인 계정)

1. GitHub 조직 또는 개인 계정에 `ai-codementor` 저장소를 생성합니다.
2. 이 저장소의 모든 코드를 해당 저장소에 복사합니다. 다음 방법 중 하나를 선택하세요:

   **방법 1: GitHub 포크(Fork) 사용하기** (가장 쉬운 방법)
   - 이 저장소 페이지 상단의 "Fork" 버튼을 클릭합니다.
   - 포크할 계정(조직 또는 개인)을 선택합니다.
   - 저장소 이름을 `ai-codementor`로 변경합니다.
   - "Create fork" 버튼을 클릭합니다.

   **방법 2: GitHub CLI 사용하기** (명령줄 사용자용)
   ```bash
   # 이 저장소를 로컬에 클론합니다
   gh repo clone 원본저장소주소 ai-codementor
   cd ai-codementor
   
   # 새로운 저장소를 생성하고 코드를 푸시합니다
   gh repo create your-org/ai-codementor --public
   git push -u origin main
   ```

   **방법 3: 수동 복사하기**
   
   **Windows에서:**
   - 이 저장소를 ZIP 파일로 다운로드:
     1. 저장소 페이지에서 초록색 "Code" 버튼을 클릭합니다.
     2. "Download ZIP"을 선택합니다.
     3. 다운로드된 ZIP 파일을 적절한 위치에 압축 해제합니다.
   - 새 GitHub 저장소 생성:
     1. GitHub 웹사이트에서 "New" 버튼을 클릭합니다.
     2. 저장소 이름을 `ai-codementor`로 입력합니다.
     3. "Create repository"를 클릭합니다.
   - 파일 업로드:
     1. 새로 생성된 저장소에서 "uploading an existing file" 링크를 클릭합니다.
     2. 압축 해제한 폴더에서 모든 파일을 선택하여 끌어다 놓거나 "choose your files" 버튼을 클릭하여 선택합니다.
     3. "Commit changes" 버튼을 클릭합니다.

   **Mac OS에서:**
   - 이 저장소를 ZIP 파일로 다운로드:
     1. 저장소 페이지에서 초록색 "Code" 버튼을 클릭합니다.
     2. "Download ZIP"을 선택합니다.
     3. 다운로드된 ZIP 파일은 보통 Downloads 폴더에 저장됩니다.
     4. Finder에서 ZIP 파일을 더블클릭하여 압축을 풀거나, 터미널에서 `unzip ~/Downloads/저장소이름.zip`을 실행합니다.
   - 새 GitHub 저장소 생성:
     1. GitHub 웹사이트에서 우측 상단의 "+" 아이콘을 클릭하고 "New repository"를 선택합니다.
     2. 저장소 이름을 `ai-codementor`로 입력합니다.
     3. "Create repository"를 클릭합니다.
   - 파일 업로드:
     1. 새로 생성된 저장소에서 "uploading an existing file" 링크를 클릭합니다.
     2. Finder에서 압축 해제된 폴더의 파일들을 선택하여 브라우저 창으로 드래그하거나, "choose your files" 버튼을 클릭하여 선택합니다.
     3. "Commit changes" 버튼을 클릭합니다.

### 개별 저장소에서 사용하기

1. 개별 저장소에 `.github/workflows/ai-review.yml` 파일을 생성합니다.
2. 아래 템플릿을 사용하여 워크플로우를 설정합니다:

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
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          # 아래 설정은 선택사항입니다
          # slack_bot_token: ${{ secrets.SLACK_BOT_TOKEN }}
          # slack_channel: '#code-reviews'
          # discord_webhook_url: ${{ secrets.DISCORD_WEBHOOK_URL }}
          # model: 'gpt-4' # 기본값: gpt-4
          # skip_labels: 'no-ai-review,skip-review' # 기본값
          # exclude_patterns: 'docs/*.md,.github/*,requirements.txt,README.md' # 기본값
```

3. `your-org/ai-codementor@main`을 실제 조직이나 계정 이름으로 변경합니다.
4. GitHub Secrets에 필요한 API 키를 설정합니다.

> **💡 팁:** 이 저장소에는 `workflow-template.yml` 파일이 포함되어 있습니다. 이 파일을 복사하여 자신의 저장소에 그대로 사용할 수 있습니다. 이 템플릿에는 필요한 모든 설정이 포함되어 있으며, 자신의 환경에 맞게 약간의 수정만 하면 됩니다.

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
   - 이름: `SLACK_BOT_TOKEN`
     설명: Slack 연동용 봇 토큰
     값: Slack API에서 발급받은 봇 토큰
     
   - 이름: `DISCORD_WEBHOOK_URL`
     설명: Discord 웹훅 URL
     값: Discord 채널에서 생성한 웹훅 URL

7. 각 Secret을 추가할 때마다:
   - `Name` 필드에 위의 이름(예: `OPENAI_API_KEY`)을 정확히 입력합니다.
   - `Secret` 필드에 해당 값을 붙여넣습니다.
   - `Add secret` 버튼을 클릭하여 저장합니다.

8. 저장이 완료되면 Secret 목록에 추가한 항목이 표시됩니다.

![GitHub Secrets 설정 예시](https://docs.github.com/assets/cb-41625/mw-1440/images/help/repository/actions-secret-create.webp)

**참고:**
- Secret은 암호화되어 저장되며, 추가 후에는 값을 볼 수 없습니다. 필요 시 업데이트만 가능합니다.
- Secret 값에는 특수 문자가 포함될 수 있으니 복사-붙여넣기 시 공백이 추가되지 않도록 주의하세요.
- 조직 수준의 Secret을 설정하려면 조직의 Settings > Secrets and variables > Actions에서 동일한 방식으로 추가할 수 있습니다.

### 2. Variables 설정 (선택사항)

GitHub Variables를 사용하여 Slack 채널 같은 선택적 설정을 저장할 수 있습니다:

1. `Secrets and variables` > `Actions` 페이지에서 `Variables` 탭을 클릭합니다.
2. `New repository variable` 버튼을 클릭합니다.
3. 다음 Variable을 추가할 수 있습니다:
   
   - 이름: `SLACK_CHANNEL`
     값: `#code-reviews` (또는 원하는 Slack 채널 이름)

### 3. GitHub Actions 워크플로우 설정

1. 저장소에 `.github/workflows/ai-codementor.yml` 파일이 있는지 확인합니다.
2. 없다면, 이 저장소의 템플릿 파일(`workflow-template.yml`)을 복사하여 사용하세요.
   - 템플릿 파일은 필요한 모든 구성이 이미 설정되어 있습니다.
   - 조직/사용자 이름만 변경하면 바로 사용할 수 있습니다.

### 4. Pull Request 생성하기

1. 새로운 브랜치를 생성하고 코드를 수정합니다.
2. GitHub에서 Pull Request를 생성합니다.
3. AI CodeMentor가 자동으로 리뷰를 시작합니다!

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

## ⚙️ 설정 옵션

### 파일 제외 설정
다음 파일들은 기본적으로 리뷰에서 제외됩니다:
- `docs/*.md`: 문서 파일
- `.github/*`: GitHub 설정 파일
- `requirements.txt`: 의존성 파일
- `README.md`: 프로젝트 설명 파일

### 리뷰 스킵 설정
다음 라벨을 PR에 추가하면 리뷰를 건너뛸 수 있습니다:
- `no-ai-review`
- `skip-review`

#### 사용 예시
1. GitHub에서 PR 페이지로 이동합니다.
2. 오른쪽 사이드바에서 "Labels" 드롭다운을 클릭합니다.
3. `no-ai-review` 또는 `skip-review` 라벨을 선택합니다.

![리뷰 스킵 설정 예시](https://github.com/github/docs/assets/images/help/pull_requests/labels-drop-down.png)

```yaml
# 이미 PR이 생성된 후 GitHub CLI를 사용하여 라벨 추가하기
gh pr edit 123 --add-label "no-ai-review"
```

**참고:** PR에 이러한 라벨이 있으면 AI CodeMentor는 다음 메시지를 출력하고 즉시 종료합니다:
```
Skipping review due to skip label
```

이 기능은 다음과 같은 경우에 유용합니다:
- 문서만 수정한 경우
- 임시 PR을 생성하는 경우
- 자동 리뷰가 필요하지 않은 작은 수정사항
- 직접 코드 리뷰를 받고자 하는 경우

## 📨 알림 설정

### Slack 알림
1. [Slack API](https://api.slack.com/apps)에서 새 앱을 생성합니다.
2. `Bot User OAuth Token`을 발급받습니다.
3. GitHub Secrets에 토큰을 추가합니다.
4. 원하는 채널에 봇을 초대합니다.

### Discord 알림
1. Discord 서버에서 알림을 받을 채널을 선택합니다.
2. 채널 설정에서 웹훅을 생성합니다.
3. 생성된 웹훅 URL을 GitHub Secrets에 추가합니다.

## 🛠️ 문제 해결

### 일반적인 문제
- **리뷰가 실행되지 않음**: GitHub Actions 권한을 확인하세요.
- **알림이 오지 않음**: 토큰과 채널 설정을 확인하세요.
- **코드 스타일 검사 실패**: flake8이 설치되어 있는지 확인하세요.

### 도움말
문제가 발생하면 다음을 확인하세요:
1. GitHub Actions 로그
2. 환경 변수 설정
3. 토큰 유효성
4. 채널 권한

## 📚 추가 정보

### 프로젝트 구조
```
├── .github/workflows/ai-codementor.yml  # GitHub Actions 설정
├── scripts/                           # 코드 리뷰 스크립트
│    ├── review.py                     # 메인 리뷰 로직
│    ├── ai_service.py                 # GPT 연동
│    ├── github_service.py             # GitHub 연동
│    ├── diff_parser.py                # 코드 변경 분석
│    ├── style_checker.py              # 코드 스타일 검사
│    ├── slack_service.py              # Slack 알림
│    └── discord_service.py            # Discord 알림
├── requirements.txt                   # 필요한 패키지
├── action.yml                         # GitHub Action 정의
├── workflow-template.yml              # 다른 저장소용 템플릿
└── README.md                          # 사용 설명서
```

### 주요 파일 역할
- **ai-codementor.yml**: 이 저장소에서 AI 코드 리뷰를 실행하는 워크플로우
- **action.yml**: 다른 저장소에서 이 코드를 재사용할 수 있게 하는 GitHub Action 정의
- **workflow-template.yml**: 다른 저장소에서 복사하여 사용할 수 있는 템플릿 파일


## 🤝 기여하기

버그 리포트나 기능 제안은 Issue를 통해 해주세요. Pull Request도 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

