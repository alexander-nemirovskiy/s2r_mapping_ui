FROM node:14.13-alpine as build
RUN mkdir smart/ && \
    mkdir -p /var/www/smart_ui/dist
COPY ./package.json ./package-lock.json smart/
WORKDIR /smart/
RUN npm install && \
    npm install -g @angular/cli@9.1.12

COPY . /smart/app
WORKDIR /smart/app


# RUN npm build --prod --output-path=dist --build-optimizer=true
# RUN npm run build --prod --build-optimizer=true --output-path=/var/www/smart_ui/dist
RUN ng build --prod --build-optimizer=true --output-path=/smart/dist



FROM nginx:1.19.3-alpine
COPY --from=build /smart/dist /var/www/smart_ui/
# COPY ../../reverse_proxy/proxy.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
#  	root /var/www/s2r_mapping_tool/dist/angularUI;