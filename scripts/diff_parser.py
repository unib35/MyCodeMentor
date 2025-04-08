import subprocess
import os
import re

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
            # GitHub Actions 환경에서 기본 브랜치와 현재 브랜치의 diff를 가져옵니다
            base_branch = os.getenv('GITHUB_BASE_REF', 'main')
            head_branch = os.getenv('GITHUB_HEAD_REF', 'HEAD')
            
            # git diff 명령 실행
            result = subprocess.run(
                ['git', 'diff', f'origin/{base_branch}...{head_branch}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"Git diff failed: {result.stderr}")
                
            return result.stdout
            
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