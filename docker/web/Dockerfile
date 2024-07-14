#######################################
# Stage 0: Build frontend application #
#######################################
FROM node:20-alpine as build

WORKDIR /data

# Install dependencies
COPY package.json /data
COPY yarn.lock /data

RUN set -ex && \
    yarn install

# Build frontend application
COPY . /data
RUN set -ex && \
    yarn build


##########################################################################
# Stage 1: Build nginx runtime environment to serve frontend application #
##########################################################################
FROM nginx:stable-alpine

# Inject frontend application and config files
COPY --from=build /data/dist /usr/share/nginx/html
COPY docker/web/nginx.conf /etc/nginx/nginx.conf
COPY docker/web/templates /etc/nginx/templates

# Setup permissions to allow nginx to run as unprivileged user
RUN set -ex && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid

USER nginx:nginx
EXPOSE 8080
