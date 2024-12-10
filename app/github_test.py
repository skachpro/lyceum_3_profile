from github import Github

g = Github("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")  # Укажите ваш токен GitHub
for repo in g.get_user().get_repos():
    print(repo.name)