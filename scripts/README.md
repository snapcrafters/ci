# Useful scripts

This folder contains a bunch of useful links, scripts and commands for automating and managing Snapcrafters stuff.

## Handy links

* Show all open pull requests in our org: https://github.com/pulls?q=is%3Aopen+is%3Apr+org%3Asnapcrafters
* Show all open calls for testing: https://github.com/issues?q=is%3Aopen+is%3Aissue+org%3Asnapcrafters+label%3Atesting

## Get all distros that have the Discord snap installed

```bash
snapcraft metrics discord --name installed_base_by_operating_system --format table | cat > installed-base-raw.txt
tail -n +2 installed-base-raw.txt | cut -d/ -f1 | uniq > unique-oses.txt
```

## Get credentials

For more information on how to generate the credentials we use, take a look at [Permissions and Secrets](https://github.com/snapcrafters/.github/wiki/Permissions-and-Secrets)

## Show contributor activity

Admins can download an audit log of all activity in a repository. The URL takes the time period as GET parameter. For example, to get all activity in 2023, go to https://github.com/organizations/snapcrafters/settings/audit-log?q=created%3A2023 and download the CSV.

The following oneliners are useful to get some interesting metrics.

```shell
# Useful columns
# * actor: 11
# * timestamp: 1

# Get all unique contributors
cat export-snapcrafters-1701710994.csv | cut -d "," -f 11 | sort | uniq > contributors-2023.txt

# Get all active members
comm -13 contributors-2023.txt members.txt

# Get all members of our org that are not actually snapcrafters
comm -13 members.txt snapcrafters-github-org-members.txt > non-member-org-members.txt
```

## Getting collaborators of snaps

The snap store doesn't have an API to get or change the collaborators. The underlying commands scrape the HTML pages and simulate button clicks. The `<FILL>` stuf needs to be extracted from your browser by clicking on a button and looking at the cookies with the developer console.

```shell
COOKIE="csrftoken=<FILL>; sessionid=<FILL>"

readarray -t array < merlijn-snapcrafters-snaps.txt

# Get all collaborators of all snaps
for SNAP in "${array[@]}"
do
   echo "# Collaborators of $SNAP"
   curl -s https://dashboard.snapcraft.io/snaps/$SNAP/collaboration/ --cookie "${COOKIE}"  | sed '/data-test="shares-actions"/q' | grep @ | tr -d " " | cut -c 5- | rev | cut -c 6- | rev
   echo
done


# Add a collaborator to all snaps
for SNAP in "${array[@]}"
do
   echo "Adding bot to $SNAP"

   curl -s https://dashboard.snapcraft.io/snaps/$SNAP/collaboration/ --cookie "${COOKIE}" -X POST -d "csrfmiddlewaretoken=<FILL>&emails=merlijn.sebrechts%2Bsnapcrafters-bot%40gmail.com&send-invites=" -H "Referer: https://dashboard.snapcraft.io/snaps/$SNAP/collaboration/"
done
```
