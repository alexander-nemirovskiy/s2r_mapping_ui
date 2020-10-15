# Setting up automatic building process for angular frontend
# contents from dist/ dir will be used by the nginx service
FROM node:14.13-alpine as build
RUN mkdir /smart/ && \
    mkdir -p /var/www/smart_ui
COPY ./package.json ./package-lock.json /smart/
WORKDIR /smart/
RUN npm install && \
    npm install -g @angular/cli@9.1.12 && \
    npm install --save @angular/material @angular/cdk && \
    npm install --save @angular/animations

COPY . /smart/
RUN ng build --prod --build-optimizer=true --output-path=/smart/dist && \
    rm .dockerignore Dockerfile angular.json browserslist package*.json \
    tsconfig* && \
    rm -rf node_modules/ service_conf/ src/ 

# Setting up nginx service and its configuration
FROM nginx:1.19.3-alpine
COPY ./service_conf/proxy.conf /etc/nginx/conf.d/proxy.conf
COPY ./service_conf/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /smart/dist /var/www/smart_ui/
RUN rm /etc/nginx/conf.d/default.conf
