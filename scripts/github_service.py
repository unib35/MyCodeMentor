from github import Github
import os

class GitHubService:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.repo = self._get_repo()
        self.pr = self._get_pr()

    def _get_repo(self):
        # GitHub Actions 환경 변수에서 리포지토리 정보 가져오기
        repo_name = os.getenv('GITHUB_REPOSITORY')
        return self.github.get_repo(repo_name)

    def _get_pr(self):
        # PR 번호 가져오기
        pr_number = int(os.getenv('GITHUB_REF').split('/')[-2])
        return self.repo.get_pull(pr_number)

    def get_pr_info(self):
        """PR의 제목, 내용, 라벨을 반환합니다."""
        return {
            'title': self.pr.title,
            'body': self.pr.body,
            'number': self.pr.number,
            'labels': [label.name for label in self.pr.get_labels()]
        }

    def post_review(self, review):
        """PR에 리뷰를 게시합니다."""
        self.pr.create_issue_comment(review) 