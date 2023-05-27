from alpine
run apk add --update nodejs npm
workdir /app
copy . .
cmd ["npm", "start"]
expose 3000