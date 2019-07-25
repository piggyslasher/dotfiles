cd $HOME

sudo apt update

sudo apt install -yq \
  curl \
  ntfs-3g \
  font-manager \
  stow \
  jq \
  thefuck \
  software-properties-common

echo "Setting up Neovim"
sudo add-apt-repository -y ppa:neovim-ppa/stable
sudo apt update

sudo apt install -y neovim
sudo apt install -y python-dev python-pip python3-dev python3-pip
echo "Setting up Neovim...DONE"

echo "Setting up NodeJS"
curl -sL https://deb.nodesource.com/setup_12.x | sudo bash - && \
  sudo apt install -yq nodejs build-essential
echo "==> Setting up Yarn"
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get update && sudo apt-get install --no-install-recommends yarn

echo "==> Checking for versions"
node --version
npm --version
yarn --version

echo "==> Print binary paths"
which npm
which node
which yarn

echo "==> Setting up avn for node"
sudo npm install -g avn avn-nvm avn-n

echo "Setting up NodeJS...DONE"

echo "Cloning your dotfiles"
cd $HOME
git clone git@vviikk/dotfiles
git clone git:vviikk/dotfiles
echo "Cloning your dotfiles...DONE"

echo "Install Bat (cat with wings)!"
# BAT_LATEST_RELEASE="$(curl -ksL 'https://api.github.com/repos/sharkdp/bat/releases/latest' | jq -r '.assets[0].browser_download_url')"
BAT_LATEST_RELEASE="https://github.com/sharkdp/bat/releases/download/v0.11.0/bat-musl_0.11.0_amd64.deb"
TEMP_DEB="$(mktemp)" &&
  wget -O "$TEMP_DEB" "$BAT_LATEST_RELEASE" &&
  sudo dpkg -i "$TEMP_DEB"
rm -f "$TEMP_DEB"

echo "Installing zsh, antibody"
pushd $HOME/dotfiles/antibody
sudo apt install -yq zsh && \
	curl -sfL git.io/antibody | sudo sh -s - -b /usr/local/bin
pwd
cat ./install.sh | bash
popd
echo "Installing zsh, antibody...DONE"

echo "Installing SpaceNeoVim"
pushd $HOME/dotfiles/nvim
./install-spaceneovim.sh
popd
echo "Installing SpaceNeoVim...DONE"

echo "DONE"
