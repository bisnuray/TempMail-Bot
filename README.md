<h1 align="center">TempMail Telegram Bot 💌</h1>

<p align="center">
  <a href="https://github.com/bisnuray/TempMail-Bot/stargazers"><img src="https://img.shields.io/github/stars/bisnuray/TempMail-Bot?color=blue&style=flat" alt="GitHub Repo stars"></a>
  <a href="https://github.com/bisnuray/TempMail-Bot/issues"><img src="https://img.shields.io/github/issues/bisnuray/TempMail-Bot" alt="GitHub issues"></a>
  <a href="https://github.com/bisnuray/TempMail-Bot/pulls"><img src="https://img.shields.io/github/issues-pr/bisnuray/TempMail-Bot" alt="GitHub pull requests"></a>
  <a href="https://github.com/bisnuray/TempMail-Bot/graphs/contributors"><img src="https://img.shields.io/github/contributors/bisnuray/TempMail-Bot?style=flat" alt="GitHub contributors"></a>
  <a href="https://github.com/bisnuray/TempMail-Bot/network/members"><img src="https://img.shields.io/github/forks/bisnuray/TempMail-Bot?style=flat" alt="GitHub forks"></a>
</p>

<p align="center">
  <em>TempMail: An advanced Telegram bot script for generating temporary email addresses and checking received messages.</em>
</p>
<hr>

## Features

- Generate temporary email addresses.
- Check the inbox of the generated email.
- Read emails directly through Telegram.
- Supports custom username and password for email generation.
- Secure: your temporary emails and messages are private and accessible only to you.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher.
- `pyrofork`, `requests` and `beautifulsoup4` libraries.
- A Telegram bot token (you can get one from [@BotFather](https://t.me/BotFather) on Telegram).
- API ID and Hash: You can get these by creating an application on [my.telegram.org](https://my.telegram.org).

## Installation

To install `pyrofork`, `requests` and `beautifulsoup4` run the following command:

```bash
pip install pyrofork requests beautifulsoup4
```

**Note: If you previously installed `pyrogram`, uninstall it before installing `pyrofork`.**

## Configuration

1. Open the `config.py` file in your favorite text editor.
2. Replace the placeholders for `API_ID`, `API_HASH`, and `BOT_TOKEN` with your actual values:
   - **`API_ID`**: Your API ID from [my.telegram.org](https://my.telegram.org).
   - **`API_HASH`**: Your API Hash from [my.telegram.org](https://my.telegram.org).
   - **`BOT_TOKEN`**: The token you obtained from [@BotFather](https://t.me/BotFather).

## Deploy the Bot

```sh
git clone https://github.com/bisnuray/TempMail-Bot
cd TempMail-Bot
python tempmail.py
```

## Bot Commands

- `/start` - Welcome message with a usage guide
- `/tmail` - Command for Generate Random Mail with Pass
- `/tmail [username]:[password]` - Generate a temporary email. with a specify a username and password.
- `/cmail <token>` - Check the inbox of your temporary email by providing the token received during email generation.

✨ **Note**: When you generate a mail pass, then you will receive a mail token. With the token, you can check 10 recent mails, each mail has a different token, so keep it privately. The mail generator general quota limit is 8 queries per second (QPS) per IP address.

## Author

- Name: Bisnu Ray
- Telegram: [@itsSmartDev](https://t.me/itsSmartDev)

Feel free to reach out if you have any questions or feedback.
