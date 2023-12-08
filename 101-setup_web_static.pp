# 101-setup_web_static.pp

# Install nginx package
package { 'nginx':
  ensure => 'installed',
}

# Create directories for web_static
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

# Create a symbolic link for 'current'
file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static/releases/test'],
}

# Create a sample index.html file
file { '/data/web_static/releases/test/index.html':
  content => '<html>
                <head>
                </head>
                <body>
                  Holberton School
                </body>
              </html>',
  require => File['/data/web_static/releases/test'],
}

# Ensure proper permissions for web_static directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared']:
  owner => 'ubuntu',
  group => 'ubuntu',
  mode  => '0755',
}

# Configure nginx to serve web_static
file { '/etc/nginx/sites-available/default':
  content => "server {
                listen 80 default_server;
                listen [::]:80 default_server;

                location /hbnb_static {
                    alias /data/web_static/current;
                }

                location / {
                    proxy_pass http://localhost:5000;
                    proxy_set_header Host \$host;
                    proxy_set_header X-Real-IP \$remote_addr;
                    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                }
              }",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Remove default nginx welcome page
file { '/var/www/html/index.nginx-debian.html':
  ensure => 'absent',
  notify => Service['nginx'],
}

# Restart nginx after configuration changes
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}

