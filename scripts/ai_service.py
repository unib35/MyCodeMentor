from openai import OpenAI
import os
from diff_parser import DiffChunk

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"  # 기본 모델

    def generate_review(self, pr_info, diff):
        """PR 정보와 코드 변경사항을 기반으로 AI 리뷰를 생성합니다."""
        prompt = self._build_prompt(pr_info, diff)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert code reviewer. Provide constructive feedback on code quality, potential bugs, and improvements."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    def generate_chunk_review(self, pr_info, chunk):
        """코드 청크별 리뷰를 생성합니다."""
        prompt = self._build_chunk_prompt(pr_info, chunk)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert code reviewer. Focus on specific lines of code and provide detailed feedback."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    def _build_prompt(self, pr_info, diff):
        """전체 리뷰 프롬프트를 구성합니다."""
        return f"""
Pull Request Review Request:

Title: {pr_info['title']}
Description: {pr_info['body']}

Code Changes:
{diff}

Please review the code changes and provide feedback on:
1. Code quality and best practices
2. Potential bugs or issues
3. Suggested improvements
4. Test coverage considerations

Format your response in a clear, constructive manner.
"""

    def _build_chunk_prompt(self, pr_info, chunk):
        """청크별 리뷰 프롬프트를 구성합니다."""
        return f"""
Pull Request Review Request:

Title: {pr_info['title']}
Description: {pr_info['body']}

File: {chunk.file_path}
Lines: {chunk.start_line}-{chunk.end_line}

Code Changes:
{''.join(chunk.content)}

Please review this specific code chunk and provide focused feedback on:
1. Code quality and best practices in this section
2. Potential bugs or issues in these lines
3. Suggested improvements for this specific part
4. Test coverage considerations for this change

Keep your feedback specific to these lines and actionable.
""" 