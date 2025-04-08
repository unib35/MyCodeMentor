import subprocess
import os
from typing import List, Dict

class StyleChecker:
    def __init__(self):
        self.exclude_patterns = [
            'docs/*',
            '.github/*',
            'requirements.txt',
            'README.md'
        ]

    def check_style(self, file_path: str) -> Dict[str, List[str]]:
        """파일의 코드 스타일을 검사합니다."""
        try:
            # flake8 명령 실행
            result = subprocess.run(
                ['flake8', '--exclude', ','.join(self.exclude_patterns), file_path],
                capture_output=True,
                text=True
            )
            
            # 에러 메시지 파싱
            errors = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    errors.append(line.strip())
            
            return {
                'file': file_path,
                'errors': errors
            }
            
        except Exception as e:
            print(f"Error checking style for {file_path}: {str(e)}")
            return {
                'file': file_path,
                'errors': [f"Style check failed: {str(e)}"]
            }

    def check_all_files(self, diff_files: List[str]) -> List[Dict[str, List[str]]]:
        """변경된 모든 파일의 코드 스타일을 검사합니다."""
        results = []
        for file_path in diff_files:
            if not any(file_path.startswith(pattern.replace('*', '')) for pattern in self.exclude_patterns):
                result = self.check_style(file_path)
                if result['errors']:
                    results.append(result)
        return results 