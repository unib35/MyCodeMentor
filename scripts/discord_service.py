from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from typing import Dict, List

class DiscordService:
    def __init__(self):
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not self.webhook_url:
            raise ValueError("DISCORD_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")

    def send_review_notification(self, pr_info: Dict, review_summary: str, style_issues: List[Dict] = None):
        """PR 리뷰 완료 알림을 Discord에 전송합니다."""
        try:
            # 웹훅 초기화
            webhook = DiscordWebhook(url=self.webhook_url)
            
            # 임베드 생성
            embed = DiscordEmbed(
                title=f"📝 PR 리뷰 완료: {pr_info['title']}",
                description=f"PR #{pr_info['number']}\n\n{pr_info['body']}",
                color="00ff00"  # 초록색
            )
            
            # 리뷰 요약 추가
            embed.add_embed_field(
                name="리뷰 요약",
                value=review_summary,
                inline=False
            )
            
            # 스타일 이슈가 있는 경우 추가
            if style_issues:
                style_text = ""
                for issue in style_issues:
                    style_text += f"**{issue['file']}**\n"
                    for error in issue['errors']:
                        style_text += f"- {error}\n"
                    style_text += "\n"
                
                embed.add_embed_field(
                    name="코드 스타일 이슈",
                    value=style_text,
                    inline=False
                )
            
            # GitHub PR 링크 추가
            embed.add_embed_field(
                name="PR 링크",
                value=f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/pull/{pr_info['number']}",
                inline=False
            )
            
            # 임베드 추가 및 전송
            webhook.add_embed(embed)
            webhook.execute()
            
        except Exception as e:
            print(f"Error sending Discord notification: {str(e)}")
            raise 