# Terraform files managing our organization

## Setup

1. Install terraform: `snap install terraform`
1. [Install the GitHub CLI](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
1. Login to the GitHub CLI and initialize terraform.

   ```shell

   cd tfcrafters
   terraform init
   gh auth cli
   ```

## Usage

From the directory `tfcrafters`, execute the following commands.

```shell
# Generate the list of repositories
echo "name" > repos.csv
gh repo list snapcrafters --no-archived --limit 1000 --json name |  jq .[].name -r >> repos.csv

# Apply the terraform config
terraform apply
```

## Viewing the plan before executing

When changing many repositories at once, it might be difficult to review the plan in the terminal. This is how you can easily investigate a plan using `less`.

```shell
terraform plan -out=tfplan
terraform show | less -R
terraform apply tfplan
```
