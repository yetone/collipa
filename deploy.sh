ansible-playbook --ask-vault-pass -i provisioning/production -u $(whoami) provisioning/collipa.yml -e app_version=$(git fetch upstream && git rev-parse upstream/master) --tags deploy
