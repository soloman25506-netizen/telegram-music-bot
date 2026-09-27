import os
import ast
import operator
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression):
    expression = (
        expression
        .replace("×", "*")
        .replace("÷", "/")
        .replace("^", "**")
    )

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](
                evaluate(node.left),
                evaluate(node.right)
            )

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](
                evaluate(node.operand)
            )

        raise ValueError()

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Calculator expression မဟုတ်ရင် မတုံ့ပြန်
    allowed = "0123456789+-*/().%^×÷ "

    if not text or any(char not in allowed for char in text):
        return

    # အနည်းဆုံး ဂဏန်းတစ်လုံး ပါရမယ်
    if not any(char.isdigit() for char in text):
        return

    try:
        result = calculate(text)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        await update.message.reply_text(str(result))

    except ZeroDivisionError:
        await update.message.reply_text("❌ 0 နဲ့ စားလို့မရပါ")

    except Exception:
        return


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN မတွေ့ပါ")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("Calculator Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
