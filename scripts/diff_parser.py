import subprocess
import os
import re
import json

class DiffChunk:
    def __init__(self, file_path, start_line, end_line, content):
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line
        self.content = content

class DiffParser:
    def get_diff(self):
        """현재 PR의 코드 변경사항을 가져옵니다."""
        try:
            # 방법 1: GitHub Event 데이터에서 브랜치 정보 가져오기
            event_path = os.getenv('GITHUB_EVENT_PATH')
            if event_path and os.path.exists(event_path):
                with open(event_path, 'r') as f:
                    event_data = json.load(f)
                
                if 'pull_request' in event_data:
                    base_branch = event_data['pull_request']['base']['ref']
                    head_branch = event_data['pull_request']['head']['ref']
                    
                    print(f"브랜치 정보: base={base_branch}, head={head_branch}")
                    
                    # 모든 브랜치 가져오기 시도
                    try:
                        subprocess.run(['git', 'fetch', '--all'], check=True)
                        subprocess.run(['git', 'fetch', 'origin', '+refs/heads/*:refs/remotes/origin/*'], check=True)
                    except Exception as e:
                        print(f"브랜치 가져오기 실패: {str(e)}")
                    
                    # git diff 명령 실행
                    result = subprocess.run(
                        ['git', 'diff', f'origin/{base_branch}...{head_branch}'],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        return result.stdout
            
            # 방법 2: 환경 변수에서 브랜치 정보 가져오기
            base_branch = os.getenv('GITHUB_BASE_REF')
            head_branch = os.getenv('GITHUB_HEAD_REF')
            
            if base_branch and head_branch:
                print(f"환경 변수 브랜치 정보: base={base_branch}, head={head_branch}")
                
                # git diff 명령 실행
                result = subprocess.run(
                    ['git', 'diff', f'origin/{base_branch}...{head_branch}'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return result.stdout
            
            # 방법 3: HEAD와 이전 커밋 비교 (가장 간단한 방법)
            print("HEAD와 이전 커밋 비교 시도")
            result = subprocess.run(
                ['git', 'diff', 'HEAD^', 'HEAD'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout
            
            # 방법 4: GitHub API 사용 (가장 안정적인 방법)
            print("GitHub API를 통해 diff 가져오기 시도")
            try:
                import requests
                
                github_token = os.getenv('GITHUB_TOKEN')
                repo_name = os.getenv('GITHUB_REPOSITORY')
                
                # PR 번호 가져오기
                pr_number = None
                if event_path and os.path.exists(event_path):
                    with open(event_path, 'r') as f:
                        event_data = json.load(f)
                        if 'pull_request' in event_data:
                            pr_number = event_data['pull_request']['number']
                
                if not pr_number and os.getenv('GITHUB_REF', '').startswith('refs/pull/'):
                    pr_number = os.getenv('GITHUB_REF').split('/')[2]
                
                if not pr_number:
                    raise Exception("PR 번호를 찾을 수 없습니다")
                
                print(f"PR 정보: repo={repo_name}, pr={pr_number}")
                
                # GitHub API를 통해 diff 가져오기
                response = requests.get(
                    f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}",
                    headers={"Authorization": f"token {github_token}",
                            "Accept": "application/vnd.github.v3.diff"}
                )
                
                if response.status_code == 200:
                    print("GitHub API를 통해 diff 가져오기 성공")
                    return response.text
                else:
                    raise Exception(f"GitHub API 요청 실패: {response.status_code} {response.text}")
            
            except Exception as e:
                print(f"GitHub API 사용 실패: {str(e)}")
            
            # 모든 방법이 실패한 경우
            raise Exception("모든 diff 가져오기 방법이 실패했습니다")
                
        except Exception as e:
            print(f"Error getting diff: {str(e)}")
            raise

    def parse_chunks(self, diff):
        """diff를 코드 청크로 파싱합니다."""
        chunks = []
        current_file = None
        current_chunk = None
        current_content = []
        
        for line in diff.split('\n'):
            # 파일 변경 감지
            if line.startswith('diff --git'):
                if current_chunk and current_content:
                    chunks.append(current_chunk)
                current_file = line.split(' ')[2][2:]  # a/ 제거
                current_chunk = None
                current_content = []
            
            # 청크 헤더 감지
            elif line.startswith('@@'):
                if current_chunk and current_content:
                    chunks.append(current_chunk)
                
                # @@ -start,count +start,count @@ 형식 파싱
                match = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', line)
                if match:
                    old_start, old_count, new_start, new_count = map(int, match.groups())
                    current_chunk = DiffChunk(
                        file_path=current_file,
                        start_line=new_start,
                        end_line=new_start + new_count - 1,
                        content=[]
                    )
            
            # 청크 내용 추가
            elif current_chunk and line.startswith(('+', '-', ' ')):
                current_chunk.content.append(line)
                current_content.append(line)
        
        # 마지막 청크 추가
        if current_chunk and current_content:
            chunks.append(current_chunk)
        
        return chunks 