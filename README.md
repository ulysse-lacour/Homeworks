# HOMEWORKS CLUB :)

- [Gunicorn](#gunicorn)
- [Nginx](#nginx)
- [Bash scripts and alias](#bash-scripts-and-alias)
- [Import csv to database](#import-csv-to-database)

<br/>
<br/>

## Gunicorn

- Create service file :

```bash
sudo nano /etc/systemd/system/my_project.service
```

Add :

```
[Unit]
Description= description_text_you_want
After=network.target

[Service]
User=user_name
Group=www-data
EnvironmentFile=.env_file_absolute_path
Environment="PATH=virtual_env_path"
WorkingDirectory=app_working_directory
ExecStart=gunicorn_path --workers 3 --bind unix:my_project.sock -m 007 project.wsgi:app

[Install]
WantedBy=multi-user.target
```

- To find virtual env path and gunicorn path use :

```bash
which gunicorn
```

- Start and enable app :

```bash
sudo systemctl start my_project
sudo systemctl enable my_project
```

- Check for status app :

```bash
sudo systemctl status my_project
```

- To restart app :

```bash
sudo systemctl daemon-reload
sudo systemctl restart my_project
```

<br/>
<br/>


## Nginx

- Create server block :

```bash
sudo nano /etc/nginx/sites-available/my_project
```

- Add :

```nginx
server {
    server_name IP adress or domain nam;

    access_log /path_to_myproject/logs/access.log;
    error_log /path_to_myproject/logs/error.log error;

    location / {
        proxy_pass http://unix:path_to_myproject/my_project.sock;
        include proxy_params;
    }
}
```

- Link to sites-enabled :

```bash
sudo ln -s /etc/nginx/sites-available/my_project /etc/nginx/sites-enabled
```

- Check for syntax errors :

```bash
    sudo nginx -t
```

- Restart nginx :

```bash
sudo systemctl restart nginx
```

Or you can restart nginx with _bash ~/restart_nginx.sh_

<br/>
<br/>

## Bash scripts and alias

For each project you cand add to _~/.profile_ :

```bash
alias my_project-log="sudo journalctl -u my_project -n 150"
alias my_project-reboot="sudo systemctl daemon-reload && sudo systemctl restart my_project"
alias my_project-status="sudo systemctl status my_project"
```

<br/>
<br/>

## Import csv to database

- Connect with superuser :

```bash
sudo -u postgres psql
```

- connect to databse :

```sql
\c databse_name
```

- copy :

```sql
COPY table_name FROM 'absolute_path_to_csv_file' delimiter 'delimiter' csv header;
```

