FROM python:3
RUN apt-get update -y
# Library for httpClient
RUN apt-get install -yyq ca-certificates
RUN apt-get install -yyq libappindicator1 libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6
RUN apt-get install -yyq gconf-service lsb-release wget xdg-utils

# Install Google Chrome
RUN apt-get update && apt-get install curl gnupg -y \
  && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
  && apt-get update \
  && apt-get install google-chrome-stable -y --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

# tzdata for timzone
RUN apt-get install -y tzdata
# timezone env with default
ENV TZ=America/New_York
RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata
# Container Port To Map to Load Balancer FOR NODEJS
EXPOSE 8080
# Container Port to Map to Load Balancer FOR REDIS
EXPOSE 6379
# Create app directory (CHANGE BASED ON YOUR FILE PATH)
WORKDIR /Users/taishanlin/Desktop/Portfolios/Options
# Add app source code
ADD . /Users/taishanlin/Desktop/Portfolios/Options

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Run the app
CMD [ "python", "main.py" ]