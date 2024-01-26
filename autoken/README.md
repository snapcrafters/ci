# autoken

This repo contains a collection of scripts and tools for automating the distribution of secrets
to the Snapcrafters repositories.

There are three key components:

- [`autoken`](./autoken): The entrypoint for the automation.
- [`craft-token`](./craft-token): A Python script for generating Snap Store credentials for a given snap, on a given channel with some specified ACLs.
- [`gh-app-token`](./gh-app-token): A Python script for generating a Github Access Token from an App ID and secret key, for use with the Github API.

## Dependencies

The scripts assume the following tools are installed on the host:

- [`gh`](https://cli.github.com/): The GitHub CLI tool, logged into an account with privileges over the `snapcrafters` org.
- `python3`: for running the tools above.

Python dependencies are specified in [`requirements.txt`](./requirements.txt), and can be installed in a virtual environment like so:

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Credentials setup

Before running the script, create a `.env` file containing the credentials required, in this case the credentials are fetched securely from 1Password:

```bash
# Snap Store credentials
SNAPCRAFTERS_USER="op://<vault_id>/username"
SNAPCRAFTERS_PASSWORD="op://<vault_id>/password"

# Content from ~/.local/share/snapcraft/provider/launchpad/credentials
LP_AUTH="op://<vault_id>/Launchpad token"

# Github credentials for the snapcrafters-bot account
GITHUBFINEGRAINEDTOKENCLIENT_USERNAME="op://<vault_id>/username"
GITHUBFINEGRAINEDTOKENCLIENT_PASSWORD="op://<vault_id>/password"

# App ID and PEM content for a client to the snapcrafters-autoken Github App
AUTOKEN_APP_ID="op://<vault_id>/snapcrafters-autoken-app-id"
AUTOKEN_SECRET="op://<vault_id>/snapcrafters-autoken-client-key"
```

If you're not a 1Password user, you can write the credentials directly into the `.env` file, then add them to your environment like so, **but beware of leaking the credentials in this case**:

```bash
export $(grep -v "#" snapcrafters.env | xargs)
```

## Running the script

Run the script, injecting the environment variables from 1Password:

```bash
op run --env-file snapcrafters.env -- ./autotoken
```

Or with a plain-text `.env` file:

```bash
./autoken
```

## TODO

This was put together quickly, and I'm not especially proud of being spread across bash and Python. Ideally this would be reworked to be all in Python, or similar.
