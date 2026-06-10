FROM node:22

WORKDIR /app/frontend

COPY package*.json ./

RUN npm install

COPY frontend/ .

EXPOSE 4321

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]