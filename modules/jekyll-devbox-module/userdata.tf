  
####################################################  
# Below we create the USERDATA to get the instance ready to run Jekyll.
# The Terraform local simplifies Base64 encoding.  
locals {

  jekyll-host-userdata = <<USERDATA
#!/bin/bash -xe
### Install software
yum -y update
amazon-linux-extras install -y epel
yum -y install awscli
yum install -y telnet
yum install -y git
### Create user for Jekyll
groupadd -g 2002 jekyll-host
useradd -u 2002 -g 2002 -c "Jekyll-Host Account" -s /bin/bash -m -d /home/jekyll-host jekyll-host
# Configure SSH for the user
mkdir -p /home/jekyll-host/.ssh
cp -pr /home/ec2-user/.ssh/authorized_keys /home/jekyll-host/.ssh/authorized_keys
chown -R jekyll-host:jekyll-host /home/jekyll-host/.ssh
chmod 700 /home/jekyll-host/.ssh
# Add user to sudoers with no password, ssh-only authentication
cat << 'EOF' > /etc/sudoers.d/jekyll-host
User_Alias JEKYLL_AUTOMATION = %jekyll-host
JEKYLL_AUTOMATION ALL=(ALL)      NOPASSWD: ALL
EOF
chmod 400 /etc/sudoers.d/jekyll-host
cat << 'EOF' >> /etc/ssh/sshd_config
Match User jekyll-host
        PasswordAuthentication no
        AuthenticationMethods publickey

EOF
# restart sshd
systemctl restart sshd

### Configure jekyll-host workspace with template
####
# Change to new user and navigate to someplace where we can store downloads.  
su - jekyll-host
cd /home/jekyll-host
#Create directories for source and destination of Jekyll operations
mkdir /home/jekyll-host/jekyll-files/
mkdir /home/jekyll-host/jekyll-files/_site
mkdir /home/jekyll-host/jekyll-files/_plugins
mkdir /home/jekyll-host/jekyll-files/_layouts
mkdir /home/jekyll-host/jekyll-files/_data
mkdir /home/jekyll-host/jekyll-files/_includes
mkdir /home/jekyll-host/jekyll-files/_sass
sudo chown -R jekyll-host:jekyll-host /home/jekyll-host/jekyll-files/
#Create location into which to download repos containing jekyll code that will be moved into the jekyll source directory by other processes separately later.
mkdir /home/jekyll-host/cloned-repos
sudo chown -R jekyll-host:jekyll-host /home/jekyll-host/cloned-repos
#The following 4 lines are added March 19, 2020 as an experiment to install Jekyll
sudo yum update -y 
sudo amazon-linux-extras install -y ruby2.6
sudo yum install -y ruby-rdoc ruby-devel gcc gcc-c++ make
gem install jekyll bundler
#The following should print a valid version of ruby, jekyll, and bundler 
ruby -v 
gem -v
gcc -v 
g++ -v 
make -v 
jekyll -v 
bundler -v
#The following 3 lines prevent an error that occurred when working with themes in Jekyll 
sudo yum install -y zlib-devel
sudo chown -R jekyll-host:jekyll-host /usr/share/gems/
sudo chown -R jekyll-host:jekyll-host /usr/lib64/gems/

#Insert the config file for Jekyll next.
cat << 'EOF' >> /home/jekyll-host/jekyll-files/_config.yaml
# Where things are
source              : /home/jekyll-host/jekyll-files/
destination         : /home/jekyll-host/jekyll-files/_site
collections_dir     : /home/jekyll-host/jekyll-files/
plugins_dir         : /home/jekyll-host/jekyll-files/_plugins
layouts_dir         : /home/jekyll-host/jekyll-files/_layouts
data_dir            : /home/jekyll-host/jekyll-files/_data
includes_dir        : /home/jekyll-host/jekyll-files/_includes
sass:
  sass_dir: /home/jekyll-host/jekyll-files/_sass
collections:
  posts:
    output          : true

# Handling Reading
safe                : false
include             : [".htaccess"]
exclude             : ["Gemfile", "Gemfile.lock", "node_modules", "vendor/bundle/", "vendor/cache/", "vendor/gems/", "vendor/ruby/"]
keep_files          : [".git", ".svn"]
encoding            : "utf-8"
markdown_ext        : "markdown,mkdown,mkdn,mkd,md"
strict_front_matter : false

# Filtering Content
show_drafts         : null
limit_posts         : 0
future              : false
unpublished         : false

# Plugins
whitelist           : []
plugins             : []

# Conversion
markdown            : kramdown
highlighter         : rouge
lsi                 : false
excerpt_separator   : "\n\n"
incremental         : true

# Serving
detach              : false
port                : 4000
host                : 0.0.0.0
baseurl             : "" # does not include hostname
show_dir_listing    : false

# Outputting
permalink           : date
paginate_path       : /page:num
timezone            : null

quiet               : false
verbose             : false
defaults            : []

liquid:
  error_mode        : warn
  strict_filters    : false
  strict_variables  : false

# Markdown Processors
rdiscount:
  extensions        : []

redcarpet:
  extensions        : []

kramdown:
  auto_ids          : true
  entity_output     : as_char
  toc_levels        : [1, 2, 3, 4, 5, 6]
  smart_quotes      : lsquo,rsquo,ldquo,rdquo
  input             : GFM
  hard_wrap         : false
  footnote_nr       : 1
  show_warnings     : false

EOF

#Create a new empty Gemfile and install any gems indicated in the gem file for the site.  This is good practice before running jekyll serve below.
cd /home/jekyll-host/jekyll-files/

cat << 'EOF' >> /home/jekyll-host/jekyll-files/Gemfile

source 'https://rubygems.org'

gem 'jekyll'

EOF

# Run bundle to add the gems related to Jekyll to the project.  This will enable you to prefix all commands with bundle exec so that the version of jekyll defined in the gemfile will be used.
bundle
#Now create an initial simple page to confirm Jekyll is running.

cat << 'EOF' >> /home/jekyll-host/jekyll-files/index.html

<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Test Page</title>
  </head>
  <body>
    <h1>Jekyll works!  Change this and other files in this directory, and watch the site content change on http://localhost:4000</h1>
  </body>
</html>

EOF
#Change permissions now in order to avoid a problem later when the jekyll service tries to use this path.
sudo chown -R jekyll-host:jekyll-host /usr/local/lib
sudo chmod 777 /usr/local/lib

#Become root in order to create the jekyll.service file 
sudo -i 

cat << 'EOF' >> /usr/lib/systemd/system/jekyll.service
[Unit]
Description=Jekyll service
After=syslog.target
After=network.target

[Service]
User=jekyll-host
Type=simple
ExecStart=/bin/sh -c 'cd /home/jekyll-host/jekyll-files/ && /usr/local/bin/bundle exec jekyll serve --source /home/jekyll-host/jekyll-files/'
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=jekyll

[Install] 
WantedBy=multi-user.target

EOF

#The following line prevents an error that was inadvertantly caused by this userdata script.  The error was preventing the jekyll-host user from running sudo commands.
chown root:root /usr/bin/sudo && chmod 4755 /usr/bin/sudo

#revert to sudo user.  Stop being root.
su - jekyll-host
sudo systemctl daemon-reload
sudo systemctl start jekyll 
sudo systemctl enable jekyll
sudo systemctl status jekyll

USERDATA

}
