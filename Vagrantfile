# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/bionic64"

  config.vm.network "forwarded_port", host_ip: "127.0.0.1", guest: 8000, host: 8000

  config.vm.provider :virtualbox do |vb|

    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]

  end

  config.vm.provision "shell", inline: <<-SHELL
    # Update and upgrade the server packages.
    sudo apt-get update
    sudo apt-get -y upgrade
    # Set Ubuntu Language.
    sudo locale-gen en_GB.UTF-8
    # Install Python, SQLite and pip.
    sudo apt-get install -y python3-dev sqlite python-pip
    # Upgrade pip to the latest version.
    sudo pip install --upgrade pip
    # Install Docker requirements.
    sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
    # Add Docker’s official GPG key.
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    # Set up the stable Docker repository.
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    # Install the latest version of Docker CE and containerd.
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    # Verify that Docker CE is installed correctly.
    sudo docker run hello-world
    # Download the current stable release of Docker Compose.
    # Warning - make sure that the latest version is actually below.
    # Check the installation instructions at https://docs.docker.com/compose/install/
    sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    # Apply executable permissions to the Docker Compose binary
    sudo chmod +x /usr/local/bin/docker-compose
    # Give user Docker permissions.
    # Warning - you may need to log out and log back in again for this to work.
    sudo usermod -a -G docker vagrant
    # Install and configure python virtualenvwrapper.
    sudo pip install virtualenvwrapper
    if ! grep -q VIRTUALENV_ALREADY_ADDED /home/vagrant/.bashrc; then
        echo "# VIRTUALENV_ALREADY_ADDED" >> /home/vagrant/.bashrc
        echo "WORKON_HOME=~/.virtualenvs" >> /home/vagrant/.bashrc
        echo "PROJECT_HOME=/vagrant" >> /home/vagrant/.bashrc
        echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
    fi
  SHELL

end
