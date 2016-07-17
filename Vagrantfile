# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.require_version ">= 1.8.1"

# use dns manager
$windows = (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil

# make sure the dns plugin is loaded
$pluginToCheck = $windows ? "vagrant-hostmanager" : "landrush"
unless Vagrant.has_plugin?($pluginToCheck)
  raise 'Please type this command then try again: vagrant plugin install ' + $pluginToCheck
end

# main vagrant script
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # DNS settings
  tld = ENV['TLD'] || 'v8'

  # Landrush is used together with wildcard dns entries to map all
  # routes to the proper services
  if $windows
    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.hostmanager.ignore_private_ip = false
    config.hostmanager.include_offline = true
  else
    config.landrush.enabled = true
    config.landrush.guest_redirect_dns = false
    config.landrush.tld = tld
  end

  if Vagrant.has_plugin?("vagrant-proxyconf")
    if ENV["PROXY_ENABLED"] =~ (/^(true|yes|y|1)$/i)
      # enabled =~ (/^(true|t|yes|y|1)$/i) ? true : false,
      config.proxy.enabled = { apt: false, chef: false, docker: false, git: false, npm: false, pear: false, svn: false }
      config.proxy.http     = "http://#{ENV['PROXY_USERNAME']}:#{ENV['PROXY_PASSWORD']}@#{ENV['PROXY_HOST']}:#{ENV['PROXY_PORT']}"
      config.proxy.https    = "http://#{ENV['PROXY_USERNAME']}:#{ENV['PROXY_PASSWORD']}@#{ENV['PROXY_HOST']}:#{ENV['PROXY_PORT']}"
      config.proxy.no_proxy = "localhost,127.0.0.1,.virginblue.internal,.virginblue.com.au,.virginaustralia.internal"
    else
      # need to set to empty to clear
      config.proxy.enabled = true
      config.proxy.http     = ""
      config.proxy.https    = ""
      config.proxy.no_proxy = ""
    end
  end

  if Vagrant.has_plugin?("vagrant-vbguest")
    # we are using https://github.com/dotless-de/vagrant-vbguest
    # disable autoupdate of the VB guest
    config.vbguest.auto_update = false
  end

  config.vm.define "jyboss", primary: true do |node|
    node.vm.box      = "boxcutter/ol72"
    node.vm.hostname = "jyboss.vagrant.#{tld}"
    # web.vm.synced_folder "#{Dir.home}/Downloads", "/tmp/downloads", :mount_options => ["dmode=777","fmode=666"]
    node.vm.network "private_network", ip: "192.168.33.233"

    # virtualbox image configuration
    node.vm.provider "virtualbox" do |vb|
      vb.gui = false
      vb.name = "ansible-jyboss"
      vb.memory = 768
      vb.cpus = 2
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end

    # provisioning ansible node individually
    node.vm.provision "ansible" do |ansible|
      ansible.playbook = "site.yml"
      ansible.verbose = "vvvv"
      ansible.limit = "#{node.vm.hostname}"
      ansible.inventory_path = "./inventory"
      ansible.sudo = true
    end # ansible provisioning

  end

end
