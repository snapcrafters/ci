resource "github_branch_protection" "list" {
  for_each = {
    for repo in csvdecode(file("repos.csv")) :
    repo.name => repo
  }

  repository_id = each.value.name


  pattern          = "*"

  required_pull_request_reviews {
    required_approving_review_count = 1
    dismiss_stale_reviews  = true
    pull_request_bypassers = [
        "/snapcrafters-bot"
    ]
  }
}
