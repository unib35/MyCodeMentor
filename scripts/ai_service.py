from openai import OpenAI
import os
from diff_parser import DiffChunk

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('AI_MODEL', 'gpt-4')  # 환경 변수에서 모델을 가져옵니다
        self.language = os.getenv('LANGUAGE', 'ko')  # 언어 설정을 가져옵니다 (기본값: 한국어)

    def generate_review(self, pr_info, diff):
        """PR 정보와 코드 변경사항을 기반으로 AI 리뷰를 생성합니다."""
        prompt = self._build_prompt(pr_info, diff)
        
        # 시스템 메시지에 언어 설정 추가
        system_message = self._get_system_message()
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    def generate_chunk_review(self, pr_info, chunk):
        """코드 청크별 리뷰를 생성합니다."""
        prompt = self._build_chunk_prompt(pr_info, chunk)
        
        # 시스템 메시지에 언어 설정 추가
        system_message = self._get_system_message(for_chunk=True)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    def _get_system_message(self, for_chunk=False):
        """언어 설정에 따른 시스템 메시지를 반환합니다."""
        base_message = "You are an expert code reviewer."
        
        if for_chunk:
            additional_instruction = "Focus on specific lines of code and provide detailed feedback."
        else:
            additional_instruction = "Provide constructive feedback on code quality, potential bugs, and improvements."
        
        language_instruction = ""
        if self.language.lower() == 'ko':
            language_instruction = " Please provide your review in Korean."
        elif self.language.lower() == 'en':
            language_instruction = " Please provide your review in English."
        
        return f"{base_message} {additional_instruction}{language_instruction}"

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