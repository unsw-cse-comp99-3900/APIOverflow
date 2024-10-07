FROM node:16

WORKDIR /app/src/frontend

ENV PATH /app/src/frontend/node_modules/.bin:$PATH

COPY package*.json ./
RUN npm config set unsafe-perm true

RUN npm install

COPY . .

RUN chown -R node /app/src/frontend/node_modules
USER node

EXPOSE 3000
CMD ["npm", "start"]