FROM node:23-slim
ENV VITE_APP_YMAP_KEY=f45cd656-5a4f-471e-b22a-7d1c1fffc26e

WORKDIR /app

COPY package.json package-lock.json .
RUN npm i && npm cache clean --force

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "--port=8000"]`