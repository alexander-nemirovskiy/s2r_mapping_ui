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
# WORKDIR /smart/app


# RUN npm build --prod --output-path=dist --build-optimizer=true
# RUN npm run build --prod --build-optimizer=true --output-path=/var/www/smart_ui/dist
RUN ng build --prod --build-optimizer=true --output-path=/smart/dist



FROM nginx:1.19.3-alpine
#COPY ./service_conf/proxy_conf /etc/nginx/proxy_conf
COPY ./service_conf/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /smart/dist /var/www/smart_ui/

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
#  	root /var/www/s2r_mapping_tool/dist/angularUI;