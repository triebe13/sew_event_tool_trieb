FROM node:lts-alpine3.22

RUN apk update && apk upgrade --no-cache \
  && npm install -g pnpm

WORKDIR /app/
COPY . /app
ENV CI=true
RUN pnpm install

EXPOSE 3000
CMD ["pnpm", "dev"]
