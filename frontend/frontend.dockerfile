FROM node:22

WORKDIR /app/frontend

COPY frontend/astro/package*.json ./

RUN npm install

COPY frontend/astro/ .

EXPOSE 4321

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]