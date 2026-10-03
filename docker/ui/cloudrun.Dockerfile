FROM nginx:alpine

COPY docker/ui/cloudrun.conf.template /etc/nginx/templates/default.conf.template
COPY demo/static/ /usr/share/nginx/html/static/
COPY docker/ui/maintenance.html /usr/share/nginx/html/maintenance.html
