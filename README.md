# AI CodeMentor

Pull Request 리뷰를 자동화하는 AI 기반 코드 리뷰 도구입니다. 개발자가 아닌 분들도 쉽게 설정하고 사용할 수 있습니다.

## 🌟 주요 기능

### 코드 품질 분석
- **코드 스타일 검사**: 가독성과 일관성 검사
- **버그 탐지**: 잠재적인 오류와 버그 식별
- **성능 최적화**: 코드 성능 향상을 위한 제안
- **보안 취약점**: 보안 관련 문제 감지

### 맞춤형 리뷰
- **프로젝트별 가이드라인**: 팀 고유의 코딩 표준 반영
- **다국어 지원**: 한국어, 영어 지원
- **리뷰 깊이 조정**: 간결한 리뷰부터 상세한 분석까지

### 자동화 및 알림
- **GitHub Actions 통합**: PR 생성/업데이트 시 자동 실행
- **실시간 알림**: Slack 및 Discord 연동 지원
- **리뷰 건너뛰기**: 특정 PR 라벨로 리뷰 제외 가능

## 📚 문서

자세한 안내는 다음 문서를 참조하세요:

- [설치 및 시작 가이드](docs/installation.md)
- [사용 방법](docs/usage.md)
- [설정 옵션](docs/configuration.md)
- [알림 설정](docs/notifications.md)
- [문제 해결](docs/troubleshooting.md)

## 🚀 빠른 시작

1. OpenAI API 키 획득
2. GitHub Secrets에 API 키 저장
3. 워크플로우 파일(`.github/workflows/ai-codementor.yml`) 설정
4. PR 생성하여 테스트

자세한 설정 방법은 [설치 및 시작 가이드](docs/installation.md)를 참조하세요.

## 📋 주요 설정 옵션

- **언어 설정**: `language` 옵션으로 한국어(`ko`) 또는 영어(`en`) 선택
- **리뷰 유형**: `review-type` 옵션으로 간결함 정도 조절
- **파일 필터링**: 특정 파일/경로 포함 또는 제외
- **알림 설정**: Slack/Discord 웹훅 URL 설정

전체 설정 옵션은 [설정 옵션 문서](docs/configuration.md)를 참조하세요.

## 🤝 기여하기

버그 리포트나 기능 제안은 Issue를 통해 해주세요. Pull Request도 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
