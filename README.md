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

To run the bot in test mode use the start-test.sh script.

Make it executable:

```bash
chmod +x run_test.sh
```

Then run it, using:
```
./start-test.sh
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

## 🧪 Testing Notes

- Staging bot shows a warning if used in production channel.
- Production bot only responds in `PROD_CHANNEL_ID`.

---

## ☁️ Deployment (Render.com)

If apart of the Ping team don't worry about this section.

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

## 🙌 Credits

Made with ❤️ by the Ping team.  
Maintained by dkaplanskybrimmer@gmail.com

---

## 🪪 License

This project is licensed under the [MIT License](https://github.com/daveedkap/ping-ticketing-bot/tree/main?tab=MIT-1-ov-file).
