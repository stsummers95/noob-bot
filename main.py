import sys
from bot import Bot

def send(channel: str, *args):
    payload = args[0] if len(args) > 0 else None

    message = "\n<<zilch>>." + channel

    if payload is not None:
        message += "." + payload

    message += "\n"

    print(message, end="", file=sys.stderr)

def parse_board(board):
    return list(map(
        lambda row: row.split(","),
        board.split("|")
    ))

send("ready")

bot: Bot = None

while True:
    data = sys.stdin.readline().strip()
    channel, payload = data.split(".", 1)

    if channel == "start":
        standard_config, custom_config = payload.split(".", 1)
        game_time_limit, turn_time_limit, player = standard_config.split(",", 2)
        config = {
            "game_time_limit": int(game_time_limit),
            "turn_time_limit": int(turn_time_limit),
            "player": "x" if player == "0" else "o",
            "starting_position": parse_board(custom_config)
        }
        bot = Bot(config)
        send("start")
        continue

    if channel == "move":
        x, y = bot.move(parse_board(payload))
        send("move", str(x) + "," + str(y))
        continue

    if channel == "end":
        bot.end(parse_board(payload))
        continue
