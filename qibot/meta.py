from typing import Final

from botstrap import Botstrap, Color, ThemeColors

VERSION: Final[str] = "0.2.0"


def main() -> int:
    (
        Botstrap(colors := ThemeColors(Color.magenta))
        .register_token(
            uid="prod",
            requires_password=True,
            display_name=Color.green("production"),
        )
        .register_token(
            uid="dev",
            requires_password=False,
            display_name=Color.yellow("development"),
        )
        .parse_args(version=_get_display_version(colors))
        .run_bot("qibot.bot.QiBot")
    )
    return 0


def _get_display_version(colors: ThemeColors) -> str:
    return colors.primary(
        "\n               o|         |      "
        "\n          ,---..|---.,---.|---   "
        "\n          |   |||   ||   ||      "
        "\n          `---|``---'`---'`---'  "
        "\n              |  "
    ) + colors.highlight(f"VERSION {VERSION}\n")
