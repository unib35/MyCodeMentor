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
        github_ref = os.getenv('GITHUB_REF', '')
        
        # Pull Request 이벤트일 경우 (refs/pull/123/merge)
        if github_ref.startswith('refs/pull/'):
            pr_number = int(github_ref.split('/')[2])
            return self.repo.get_pull(pr_number)
        
        # GitHub Event 파일에서 PR 번호 가져오기 시도
        event_path = os.getenv('GITHUB_EVENT_PATH')
        if event_path and os.path.exists(event_path):
            import json
            with open(event_path, 'r') as f:
                event_data = json.load(f)
                if 'pull_request' in event_data:
                    pr_number = event_data['pull_request']['number']
                    return self.repo.get_pull(pr_number)
                    
        raise ValueError("GitHub PR 정보를 찾을 수 없습니다.")

    def get_pr_info(self):
        """PR의 제목, 내용, 라벨을 반환합니다."""
        return {
            'title': self.pr.title,
            'body': self.pr.body,
            'number': self.pr.number,
            'labels': [label.name for label in self.pr.get_labels()]
        }

    def post_review(self, review):
        """PR에 전체 리뷰를 게시합니다."""
        self.pr.create_issue_comment(review)
        
    def post_line_comment(self, file_path, line_number, comment):
        """PR의 특정 파일 라인에 코멘트를 게시합니다."""
        try:
            # GitHub API에서는 position 파라미터가 필요함
            # line_number는 실제 파일의 라인 번호이지만, 
            # position은 diff에서의 위치를 의미함
            
            # 방법 1: 단일 리뷰 생성하기 (최신 PyGithub 버전 지원)
            try:
                # PR의 diff 파일 목록 가져오기
                files = self.pr.get_files()
                
                # 해당 파일 찾기
                target_file = None
                for file in files:
                    if file.filename == file_path or file.filename.endswith(file_path):
                        target_file = file
                        break
                
                if target_file:
                    print(f"파일 찾음: {target_file.filename}")
                    # 통합 리뷰 생성
                    self.pr.create_review(
                        body="AI CodeMentor 리뷰",
                        event="COMMENT",
                        comments=[{
                            "path": target_file.filename,
                            "position": line_number,  # 여기서는 실제 라인 번호를 사용
                            "body": comment
                        }]
                    )
                    return
                else:
                    print(f"파일을 찾을 수 없음: {file_path}")
            except Exception as e:
                print(f"통합 리뷰 생성 실패: {str(e)}")
            
            # 방법 2: 개별 코멘트 달기
            # PR의 커밋을 가져옵니다
            commits = list(self.pr.get_commits())
            if not commits:
                print(f"PR에 커밋이 없습니다. 일반 코멘트로 추가합니다.")
                self.post_review(f"**파일: {file_path}, 라인: {line_number}**\n\n{comment}")
                return
                
            # 가장 최근 커밋을 사용합니다
            last_commit = commits[-1]
            
            # 먼저 PR 파일 목록에서 정확한 파일 경로 확인
            files = list(self.pr.get_files())
            file_found = False
            
            for file in files:
                if file.filename == file_path or file.filename.endswith(file_path):
                    file_path = file.filename
                    file_found = True
                    print(f"정확한 파일 경로 찾음: {file_path}")
                    break
            
            if not file_found:
                print(f"파일을 찾을 수 없어 일반 코멘트로 추가합니다: {file_path}")
                self.post_review(f"**파일: {file_path}, 라인: {line_number}**\n\n{comment}")
                return
            
            # GitHub API는 line_number가 아닌 position(diff 내 위치)가 필요합니다
            # 일반적으로 PR에서 diff 내의 위치를 찾는 것은 복잡하므로
            # 혹시 실패할 경우 일반 코멘트로 대체합니다
            try:
                print(f"파일 {file_path}의 라인 {line_number}에 코멘트를 추가합니다.")
                # 리뷰 코멘트 생성 시도: 실제 diff와 맞지 않으면 예외 발생
                self.pr.create_review_comment(
                    body=comment,
                    commit=last_commit,
                    path=file_path,
                    line=line_number  # PyGithub 버전에 따라 line 또는 position 사용
                )
            except Exception as e1:
                try:
                    # line 대신 position 파라미터 사용 시도
                    self.pr.create_review_comment(
                        body=comment,
                        commit=last_commit,
                        path=file_path,
                        position=line_number  # position 파라미터 사용
                    )
                except Exception as e2:
                    print(f"코드 라인 코멘트 실패: {str(e1)}, {str(e2)}")
                    # 모든 시도가 실패하면 일반 코멘트로 추가
                    fallback_comment = f"**파일: {file_path}, 라인: {line_number}**\n\n{comment}"
                    self.post_review(fallback_comment)
                
        except Exception as e:
            print(f"라인 코멘트 게시 중 오류 발생: {str(e)}")
            # 실패하면 일반 코멘트로 추가
            fallback_comment = f"**파일: {file_path}, 라인: {line_number}**\n\n{comment}"
            self.post_review(fallback_comment) 