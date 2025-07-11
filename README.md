# 🛎️ ping-ticketing-bot

A Discord bot that enables structured Jira ticket creation using slash commands. Built to streamline team workflows by generating well-formed ticket request embeds in specified channels.

---

## 🔧 Features

- `/ticket-request` – Create a detailed task or bug ticket with priority, story points, and optional assignee.
- `/epic-request` – Submit a high-level epic request for planning and tracking.
- Test and production bots are isolated by channel permissions and runtime environment (`MODE`).
- Deployable to services like Render.com.

---

## 🚀 Getting Started (Local Development)

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/ping-ticketing-bot.git
cd ping-ticketing-bot
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment

Create a `.env.test` file in the root directory with the following structure:

```env
MODE=test
DISCORD_TOKEN=your_staging_bot_token
GUILD_ID=your_discord_server_id
TEST_CHANNEL_ID=channel_id_for_testing
PROD_CHANNEL_ID=channel_id_for_production
```

If you're apart of the Ping team, reach out to David.

To run the bot in test mode:

```bash
MODE=test python bot.py
```

Or create a script (e.g. `run_test.sh`) with:

```bash
#!/bin/bash
MODE=test python bot.py
```

Make it executable:

```bash
chmod +x run_test.sh
```

---

## 🛠️ Commands

### `/ticket-request`

Used to submit a structured ticket request. Required fields include:

- `description` – 2+ sentence explanation
- `story_point_estimate` – must be greater than 0
- `priority` – Highest to Lowest
- `location` – Backlog or Current Sprint

Optional fields:

- `assignee` – mention a user
- `epic` – format like `PSB-57`
- `work_type` – Bug, Story, or Task

### `/epic-request`

Submit an epic with:

- `title`
- `description`
- `goal`
- optional `assignee`

---

## 🔐 Environment Variables

| Variable         | Description                                  |
|------------------|----------------------------------------------|
| `MODE`           | Set to `test` or `prod`                      |
| `DISCORD_TOKEN`  | Discord bot token                            |
| `GUILD_ID`       | ID of your Discord server                    |
| `TEST_CHANNEL_ID`| ID of the channel for testing (staging bot) |
| `PROD_CHANNEL_ID`| ID of the channel for real usage            |

---

## 🧪 Testing Notes

- The bot will **reject slash commands** from unauthorized channels depending on `MODE`.
- Staging bot shows a warning if used in production channel.
- Production bot only responds in `PROD_CHANNEL_ID`.

---

## ☁️ Deployment (Render.com)

- Create a new web service.
- Set `Start Command` to:

```bash
MODE=prod python bot.py
```

- Add the following environment variables to Render:
  - `MODE=prod`
  - `DISCORD_TOKEN`
  - `GUILD_ID`
  - `TEST_CHANNEL_ID`
  - `PROD_CHANNEL_ID`

---

## 🧼 Good Practices

- Add `__pycache__/` and `.env*` files to your `.gitignore`
- Never commit real tokens or `.env` files

```gitignore
__pycache__/
.env
.env.test
```

---

## 🙌 Credits

Made with ❤️ by the Ping team.  
Maintained by @your-discord-tag and collaborators.

---

## 🪪 License

MIT License (or specify if different)
