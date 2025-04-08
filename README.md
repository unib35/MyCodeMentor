# AI 팀장님 (AITeamjangnim)

Pull Request 리뷰를 자동화하는 AI 기반 코드 리뷰 도구입니다. 개발자가 아닌 분들도 쉽게 설정하고 사용할 수 있습니다.

## 🚀 시작하기

### 1. GitHub 저장소에 추가하기

1. GitHub 저장소의 `Settings` > `Secrets and variables` > `Actions` 메뉴로 이동합니다.
2. 다음 환경 변수들을 추가합니다:
   - `OPENAI_API_KEY`: [OpenAI](https://platform.openai.com/api-keys)에서 발급받은 API 키
   - `SLACK_BOT_TOKEN`: [Slack API](https://api.slack.com/apps)에서 생성한 봇 토큰
   - `SLACK_CHANNEL`: 알림을 받을 Slack 채널 이름 (예: #code-reviews)
   - `DISCORD_WEBHOOK_URL`: [Discord 웹훅 가이드](https://support.discord.com/hc/ko/articles/228383668-%EC%9B%B9%ED%9B%85-%EA%B0%80%EC%9D%B4%EB%93%9C)에 따라 생성한 웹훅 URL

### 2. GitHub Actions 워크플로우 설정

1. 저장소에 `.github/workflows/ai-teamjangnim.yml` 파일이 있는지 확인합니다.
2. 없다면, 이 저장소의 파일을 복사하여 추가합니다.

### 3. Pull Request 생성하기

1. 새로운 브랜치를 생성하고 코드를 수정합니다.
2. GitHub에서 Pull Request를 생성합니다.
3. AI 팀장님이 자동으로 리뷰를 시작합니다!

## 📝 리뷰 내용

AI 팀장님은 다음과 같은 리뷰를 제공합니다:

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
├── .github/workflows/ai-teamjangnim.yml  # GitHub Actions 설정
├── scripts/
│    ├── review.py           # 메인 리뷰 로직
│    ├── ai_service.py       # GPT 연동
│    ├── github_service.py   # GitHub 연동
│    ├── diff_parser.py      # 코드 변경 분석
│    ├── style_checker.py    # 코드 스타일 검사
│    ├── slack_service.py    # Slack 알림
│    └── discord_service.py  # Discord 알림
├── requirements.txt         # 필요한 패키지
└── README.md               # 사용 설명서
```

### 개발 계획
1. MVP Setup ✅
   - 기본 GitHub Actions 워크플로우
   - 기본 GPT 코드 리뷰
   - PR 코멘트 게시

2. File Exclusion & Label Handling ✅
   - 파일 제외 패턴 구현
   - 리뷰 스킵 라벨 처리

3. Line-by-line Comments ✅
   - 코드 청크 기반 리뷰
   - 라인별 코멘트 게시

4. Additional Checks & Notifications ✅
   - 코드 스타일 검사
   - Slack 알림 통합
   - Discord 알림 통합

## 🤝 기여하기

버그 리포트나 기능 제안은 Issue를 통해 해주세요. Pull Request도 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

