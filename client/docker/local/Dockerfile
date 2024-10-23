from docker.io/node:20.11-alpine3.18 as base 

from base as node-build-stage

RUN apk add --no-cache lib6-compact

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

# Installing the requriemtns files
RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json]l; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
    else echo "Lockfile is not found! ." && exit 1; \
    fi

# Configuring and coping the requirements, code from the local machine to docker container 
from base as node-run-stage
ARG APP_HOME=/app
WORKDIR ${APP_HOME}
COPY --from=node-build-stage /node_modules ./node_modules
COPY . ${APP_HOME}

# Create a new user nextjs belongs to the new group nodejs
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# change the ownership of the working dir in the container to the new user nextjs
RUN chown -R nextjs:nodejs ${APP_HOME}

# Swich to nextjs user
USER nextjs 

# Runing the development server 
CMD [ "npm", "run", "dev" ]