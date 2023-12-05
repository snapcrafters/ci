#!/usr/bin/bash
repos=("discord" "ffmpeg-sdk" "ci-screenshots" ".github" "mattermost-desktop" "signal-desktop" "ci" "ghvmctl" "sublime-text" "webkitgtk-sdk" "jenkins" "eclipse" "sentry" "obs-studio" "tmnationsforever" "scummvm" "xonotic" "atom" "offlineimap" "sommelier-core" "android-studio" "ffmpeg" "opentyrian" "spelunky" "flightgear" "sdlpop" "mumble" "corsixth" "magic-wormhole" "alacritty" "gimp" "helm" "sublime-merge" "minetest" "opentoonz" "fork-and-rename-me" "axel" "dosbox-x" "ddgr" "term2048" "arduino" "photoscape" "sommelier" "gradle" "s4a" "cumulonimbus" "android-studio-canary" "cassandra" "cryptool" "thelounge" "irssi" "marktext" "fkill" "pyradio" "mdl" "mosaic" "pogo" "unifi" "nano" "opentoonz-morevna" "kompozer" "get-iplayer" "simplenote" "mutt" "inadyn" "duckmarines" "brackets" "wordpress-desktop" "mrrescue" "wire" "tcpie" "slack-term" "links" "wethr" "qtctl" "bridge-designer" "climate-trail" "hello-snap-travis-ci")

for repo in ${repos[@]}; do
  terraform import github_branch_protection.list['"'$repo'"'] $repo:main
done
