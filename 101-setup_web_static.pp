# File: web_servers_setup.pp

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create directories if they don't exist
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html><body>Hello, this is a test HTML file</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create/Recreate symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/hbnb_static':
  ensure  => present,
  content => "server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}",
  require => Package['nginx'],
}

# Enable the site
file { '/etc/nginx/sites-enabled/hbnb_static':
  ensure  => link,
  target  => '/etc/nginx/sites-available/hbnb_static',
  require => File['/etc/nginx/sites-available/hbnb_static'],
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-enabled/hbnb_static'],
}
