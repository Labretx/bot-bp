# Discord Bot Blueprint

`This repo is used to setup bot development and add generic functions as well as filestructure.`

### It includes the following:

- Dockerfile, .dockerignore, docker-compose.yml templates (only names have to be changed)
- Requirements file for Docker to install the needed modules
- Basic bot with start event
- Prebuilt variables to insert into the bot and extensions like the token, guilds and a path to the database (which in my case is the same for the docker container)
- Generic bot functionalities (Error Handler, Moderation Commands and an Extension-Manager to reload extensions and debug the bot while it is running)
- Database file

### Get Started

1. Create an application in the [discord developer portal](https://discord.com/developers/applications) by clicking the button **New Application**.
2. Here you can give your application a name and add a description aswell as a profile picture (for the developer portal)
3. Click on **Bot** on the left side and click on **Add Bot**
4. Here you can choose the actual Discord Username and profile picture.
5. Click on **Reset Token**, copy it and save it somewhere.
6. Scroll down and check **Presence Intent**, **Server Members Intent** and **Message Content Intent**.
7. If you don't want other people to add your bot to their server you can uncheck **Public Bot**.
8. Now on the left side click on **0Auth2** and then select **URL Generator**.
9. Tick the options **bot** and **application.commands** in the **Scopes** section and for ease of use check **Administrator** in the **Bot Permissions** section.
10. Copy the URL at the very bottom and paste it into a new browser tab. This will invite the bot to a server you own or have the permissions to invite bots to.

This concludes the actual creation and setup of the bot in the developer portal, you can close it now.

Now you need to make sure you have Python3 installed, since this is the language in which the bot is written.
You can download the latest version on the [official Python website](https://www.python.org/downloads/) then just follow the installation instructions.

If Python is successfully installed open the directory where you want to save your bot and open the command line in the directory.
Then use this command to download the template:

``` git clone https://www.github.com/labret55/bot-bp ```

Now you have copied the template into the destination folder.
Use `cd bot-bp` followed by `code .` to start VS Code and work on the bot.

Make sure you copy your token into the appropriate variable `token` in `/vol/data.py`.

Now open a console inside VS Code and type:

``` py -m venv venv```

This will create a virtual environment in your workspace which is separated by the rest of your python installation.
If it doesn't activate on its own try:

``` .\venv\Scripts\activate ```

If you don't have the permissions to do so use and then try again:

``` Set-ExecutionPolicy Unrestricted -Scope CurrentUser ```

Now install the needed modules + whatever modules you need with:

``` pip install hikari, hikari-lightbulb, hikari-miru, aiosqlite ```

And you are done and can start adding functionality to the bot!

If you decide to install some more modules make sure to use:

``` pip freeze > requirements.txt ```

This will update the dependencies for your Dockerfile, so everything runs as intended.
