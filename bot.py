import os
import ast
import operator
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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
    expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")
    return evaluate(tree)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧮 Calculator Bot\n\n"
        "တွက်ချင်တာကို /calc နောက်မှာရေးပါ။\n\n"
        "ဥပမာများ:\n"
        "/calc 100+200\n"
        "/calc 500*3\n"
        "/calc (100+50)*2\n"
        "/calc 1000/4\n"
        "/calc 25%*800"
    )


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🧮 ဥပမာ — /calc 100+200"
        )
        return

    expression = "".join(context.args)

    try:
        result = calculate(expression)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        await update.message.reply_text(
            f"🧮 {expression} = {result}"
        )

    except ZeroDivisionError:
        await update.message.reply_text("❌ 0 နဲ့စားလို့မရပါ။")

    except Exception:
        await update.message.reply_text(
            "❌ တွက်ချက်မှု မမှန်ပါ။\n"
            "ဥပမာ — /calc 100+200*3"
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN မတွေ့ပါ။ Railway Variables မှာ ထည့်ပါ။")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("calc", calc))

    print("Calculator Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
