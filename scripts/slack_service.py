from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from typing import Dict, List

class SlackService:
    def __init__(self):
        self.client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
        self.channel = os.getenv('SLACK_CHANNEL', '#code-reviews')

    def send_review_notification(self, pr_info: Dict, review_summary: str, style_issues: List[Dict] = None):
        """PR 리뷰 완료 알림을 Slack에 전송합니다."""
        try:
            # 메시지 블록 구성
            blocks = [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"📝 PR 리뷰 완료: {pr_info['title']}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*PR #{pr_info['number']}*\n{pr_info['body']}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*리뷰 요약:*\n{review_summary}"
                    }
                }
            ]

            # 스타일 이슈가 있는 경우 추가
            if style_issues:
                style_text = "*코드 스타일 이슈:*\n"
                for issue in style_issues:
                    style_text += f"• {issue['file']}:\n"
                    for error in issue['errors']:
                        style_text += f"  - {error}\n"
                
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": style_text
                    }
                })

            # Slack에 메시지 전송
            self.client.chat_postMessage(
                channel=self.channel,
                blocks=blocks,
                text=f"PR #{pr_info['number']} 리뷰 완료"
            )
            
        except SlackApiError as e:
            print(f"Error sending Slack notification: {str(e)}")
            raise 