resource "github_repository_collaborators" "repo_collaborators" {
  for_each = {
    for repo in csvdecode(file("repos.csv")) :
    repo.name => repo
  }

  repository = each.value.name

  user {
    permission = "push"
    username  = "snapcrafters-bot"
  }

  team {
    permission = "push"
    team_id = "reviewers"
  }

  team {
    permission = "admin"
    team_id = "administrators"
  }
}
