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

## 프로젝트 가이드라인 설정

### 가이드라인 파일 생성 및 활용

프로젝트 특화 리뷰 가이드라인을 설정하면 AI가 프로젝트의 코딩 표준과 관행을 고려하여 더 관련성 높은 피드백을 제공할 수 있습니다.

#### 가이드라인 파일 생성

1. `.github/review-guidelines.md` 파일을 생성합니다:
   ```bash
   mkdir -p .github
   touch .github/review-guidelines.md
   ```

2. 파일에 프로젝트 코딩 표준, 아키텍처 원칙, 테스트 요구사항 등을 작성합니다. 예시:
   ```markdown
   # 프로젝트 코드 리뷰 가이드라인

   ## 코딩 스타일
   - 들여쓰기는 2칸 공백을 사용합니다.
   - 최대 줄 길이는 100자를 넘지 않도록 합니다.
   - 변수/함수 이름은 camelCase를 사용합니다.

   ## 아키텍처 원칙
   - MVVM 패턴을 따릅니다.
   - 비즈니스 로직은 ViewModel에 작성합니다.
   - UI 로직은 View 컴포넌트에만 작성합니다.

   ## 테스트 요구사항
   - 모든 비즈니스 로직은 단위 테스트로 검증해야 합니다.
   - UI 테스트는 주요 사용자 흐름에 집중합니다.
   ```

#### 워크플로우에 가이드라인 파일 적용

가이드라인 파일을 AI 리뷰 프로세스에 적용하는 방법은 워크플로우 구현 방식에 따라 다릅니다.

##### 1. 환경 변수 방식 (스크립트 실행)

`.github/workflows/ai-codementor.yml` 파일에서 `env` 섹션에 가이드라인 파일 경로를 추가합니다:

```yaml
- name: Run AI Review
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    LANGUAGE: 'ko'
    PROJECT_GUIDELINES_FILE: '.github/review-guidelines.md'
  run: python scripts/review.py
```

##### 2. 액션 입력 매개변수 방식

커스텀 액션을 사용하는 경우 `with` 섹션에 가이드라인 파일 경로를 추가합니다:

```yaml
- uses: ./
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    openai-api-key: ${{ secrets.OPENAI_API_KEY }}
    project-guidelines-file: '.github/review-guidelines.md'
```

### With와 Env의 차이점

GitHub Actions에서 `with`와 `env`는 다른 목적과 상황에서 사용됩니다:

#### `with` (액션 입력 매개변수)
- **용도**: 재사용 가능한 액션에 입력 매개변수를 전달합니다.
- **사용 시점**: `uses:` 키워드로 액션을 실행할 때 사용합니다.
- **예시**:
  ```yaml
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0
  ```

#### `env` (환경 변수)
- **용도**: 실행 환경에 환경 변수를 설정합니다.
- **사용 시점**: `run:` 키워드로 스크립트나 명령을 실행할 때 사용합니다.
- **예시**:
  ```yaml
  - name: Run Script
    env:
      API_KEY: ${{ secrets.API_KEY }}
    run: ./script.sh
  ```

#### 현재 상황에 적합한 방식
현재 AI CodeMentor 워크플로우가 `run: python scripts/review.py`로 Python 스크립트를 직접 실행하는 경우, `env` 방식을 사용하는 것이 적합합니다.

### 프로젝트별 특화 가이드라인 작성 팁

효과적인 프로젝트 가이드라인 작성을 위한 팁:

1. **명확한 코딩 표준 정의**:
   - 명명 규칙, 들여쓰기, 주석 스타일 등 구체적인 기준 제시
   - 좋은 예시와 나쁜 예시 코드 포함

2. **아키텍처 패턴 설명**:
   - 프로젝트에서 사용하는 아키텍처 패턴(MVC, MVVM 등) 명시
   - 각 컴포넌트의 책임과 상호작용 방식 설명

3. **테스트 요구사항 구체화**:
   - 단위 테스트, 통합 테스트, UI 테스트의 범위와 기대치 정의
   - 테스트 커버리지 목표치 설정

4. **성능 고려사항 포함**:
   - 성능 병목 현상을 방지하기 위한 가이드라인
   - 메모리 관리, 비동기 처리 등에 대한 최적화 방법

5. **보안 요구사항 정의**:
   - 보안 취약점 예방을 위한 코딩 관행
   - 민감한 정보 처리 방법

6. **접근성 표준 설정**:
   - 접근성을 보장하기 위한 UI/UX 가이드라인
   - 스크린 리더 호환성, 키보드 접근성 등 고려사항

이러한 가이드라인을 프로젝트 특성에 맞게 조정하여 AI가 더 정확하고 관련성 높은 코드 리뷰를 제공할 수 있도록 합니다.

## 문제 해결

설정 관련 문제 해결은 [문제 해결 가이드](troubleshooting.md)를 참조하세요. 