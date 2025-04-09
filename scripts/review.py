import os
import sys
import re
from github_service import GitHubService
from ai_service import AIService
from diff_parser import DiffParser, DiffChunk
from style_checker import StyleChecker
from slack_service import SlackService
from discord_service import DiscordService

class ReviewConfig:
    # 제외할 파일 패턴
    EXCLUDE_PATTERNS = [p.strip() for p in os.getenv('EXCLUDE_PATTERNS', 'docs/*.md,.github/*,requirements.txt,README.md').split(',')]
    
    # 리뷰를 건너뛸 라벨
    SKIP_LABELS = [l.strip() for l in os.getenv('SKIP_LABELS', 'no-ai-review,skip-review').split(',')]
    
    # 청크별 리뷰 최대 크기 (라인 수)
    MAX_CHUNK_SIZE = int(os.getenv('MAX_CHUNK_SIZE', '50'))

def should_skip_review(pr_info):
    """PR의 라벨을 확인하여 리뷰를 건너뛸지 결정합니다."""
    return any(label in pr_info.get('labels', []) for label in ReviewConfig.SKIP_LABELS)

def should_exclude_file(file_path):
    """파일 경로가 제외 패턴에 해당하는지 확인합니다."""
    return any(re.match(pattern, file_path) for pattern in ReviewConfig.EXCLUDE_PATTERNS)

def split_large_chunks(chunks):
    """큰 청크를 더 작은 청크로 분할합니다."""
    split_chunks = []
    for chunk in chunks:
        if len(chunk.content) > ReviewConfig.MAX_CHUNK_SIZE:
            # 청크를 MAX_CHUNK_SIZE 크기로 분할
            for i in range(0, len(chunk.content), ReviewConfig.MAX_CHUNK_SIZE):
                split_content = chunk.content[i:i + ReviewConfig.MAX_CHUNK_SIZE]
                split_chunks.append(DiffChunk(
                    file_path=chunk.file_path,
                    start_line=chunk.start_line + i,
                    end_line=chunk.start_line + i + len(split_content) - 1,
                    content=split_content
                ))
        else:
            split_chunks.append(chunk)
    return split_chunks

def get_changed_files(diff):
    """diff에서 변경된 파일 목록을 추출합니다."""
    files = set()
    for line in diff.split('\n'):
        if line.startswith('diff --git'):
            file_path = line.split(' ')[2][2:]  # a/ 제거
            if not should_exclude_file(file_path):
                files.add(file_path)
    return list(files)

def main():
    # 환경 변수 확인
    required_env_vars = ['OPENAI_API_KEY', 'GITHUB_TOKEN']
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Error: {var} environment variable is not set")
            sys.exit(1)

    # 서비스 초기화
    github_service = GitHubService()
    ai_service = AIService()
    diff_parser = DiffParser()
    style_checker = StyleChecker()
    
    # 선택적 서비스 초기화
    slack_service = None
    discord_service = None
    
    if os.getenv('SLACK_BOT_TOKEN'):
        slack_service = SlackService()
        
    if os.getenv('DISCORD_WEBHOOK_URL'):
        discord_service = DiscordService()

    try:
        # PR 정보 가져오기
        pr_info = github_service.get_pr_info()
        
        # 리뷰 스킵 라벨 확인
        if should_skip_review(pr_info):
            print("Skipping review due to skip label")
            sys.exit(0)
        
        # 코드 변경사항 가져오기
        diff = diff_parser.get_diff()
        
        # 제외할 파일 필터링
        filtered_diff = []
        for line in diff.split('\n'):
            if line.startswith('diff --git'):
                current_file = line.split(' ')[2][2:]  # a/ 제거
                if should_exclude_file(current_file):
                    continue
            filtered_diff.append(line)
        
        filtered_diff = '\n'.join(filtered_diff)
        
        if not filtered_diff.strip():
            print("No relevant changes to review after filtering")
            sys.exit(0)
        
        # 코드 스타일 검사
        changed_files = get_changed_files(filtered_diff)
        style_issues = style_checker.check_all_files(changed_files)
        
        # 코드 청크 파싱
        chunks = diff_parser.parse_chunks(filtered_diff)
        chunks = split_large_chunks(chunks)
        
        # 청크별 리뷰 생성 및 게시
        for chunk in chunks:
            review = ai_service.generate_chunk_review(pr_info, chunk)
            github_service.post_line_comment(chunk.file_path, chunk.start_line, review)
        
        # 전체 리뷰 요약 생성
        summary_review = ai_service.generate_review(pr_info, filtered_diff)
        github_service.post_review(summary_review)
        
        # Slack 알림 전송
        if slack_service:
            try:
                slack_service.send_review_notification(pr_info, summary_review, style_issues)
            except Exception as e:
                print(f"Failed to send Slack notification: {str(e)}")
        
        # Discord 알림 전송
        if discord_service:
            try:
                discord_service.send_review_notification(pr_info, summary_review, style_issues)
            except Exception as e:
                print(f"Failed to send Discord notification: {str(e)}")
        
    except Exception as e:
        print(f"Error during review process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 