import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIGURACIÓN ===
TOKEN = "8193083254:AAEEY6xMwMq-6IMKVPY8EM105GfUPUe2yeM"  # <-- REEMPLAZA ESTO CON TU TOKEN REAL

# === LOGS ===
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# === COMANDOS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy el asistente de la guía **'PRECIO REAL: APU para Sublimación'**.\n\n"
        "Comandos disponibles:\n"
        "/precio - Costo y enlace de compra\n"
        "/taza - Costo de taza 11 oz\n"
        "/materiales - Materiales y precios\n"
        "/rendimiento - Explicación de rendimientos\n"
        "/descuento - Cómo calcular descuentos\n"
        "/eficiencia - Factores de eficiencia\n"
        "/clima - Ajuste por clima\n"
        "/ayuda - Todos los comandos"
    )

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 **Guía completa + Excel**\n"
        "Precio: **$37 USD**\n"
        "Adquiérela aquí:\n"
        "https://go.hotmart.com/V104219195N"
    )

async def taza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "**Taza 11 oz (negocio equilibrado):**\n"
        "- Costo directo: $2.55\n"
        "- Indirectos (30%): $0.77\n"
        "- Utilidad (80%): $2.66\n"
        "➡️ **PVP sugerido: $5.98**\n"
        "(Ver página 11 de la guía)"
    )
    await update.message.reply_text(texto)

async def materiales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "**Materiales principales:**\n"
        "• Taza 11 oz: $1.06\n"
        "• Papel sublimable A4: $0.138/hoja\n"
        "• Tinta (kit 4 colores): $0.056/ml\n"
        "• Cinta térmica 5mm: $0.06/m\n"
        "• Papel siliconado A4: $0.062/hoja\n"
        "(Ver apéndices del libro)"
    )
    await update.message.reply_text(texto)

async def rendimiento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "**Rendimiento final (cuello de botella):**\n"
        "Se toma el menor entre diseñador (85%) y operario (80%).\n"
        "Ejemplo taza 11 oz: **61.44 uds/día** → **0.1301 h/ud**.\n"
        "(Capítulo 5)"
    )
    await update.message.reply_text(texto)

async def descuento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "**Descuento máximo rentable:**\n"
        "Fórmula: % utilidad final = [(1+%APU) × (1-%desc) -1] × 100\n"
        "Ejemplo: 80% utilidad con 10% descuento → 62% utilidad final.\n"
        "No bajar del 60% de utilidad sobre costo total.\n"
        "(Página 13)"
    )
    await update.message.reply_text(texto)

async def eficiencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "**Factores de eficiencia (FER):**\n"
        "• Diseñador gráfico: 85%\n"
        "• Operario de prensa: 80%\n"
        "Ajustan la capacidad teórica a la realidad."
    )
    await update.message.reply_text(texto)

async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "**Ajuste por clima (consumo energético):**\n"
        "• Templado: factor 1.00\n"
        "• Frío: factor 1.05\n"
        "• Cálido: factor 1.00\n"
        "(Capítulo 7)"
    )
    await update.message.reply_text(texto)

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos:\n"
        "/precio - Costo y enlace\n"
        "/taza - Costo taza 11 oz\n"
        "/materiales - Materiales\n"
        "/rendimiento - Rendimientos\n"
        "/descuento - Descuentos\n"
        "/eficiencia - Eficiencias\n"
        "/clima - Clima\n"
        "/ayuda - Este mensaje"
    )

# === RESPUESTA A MENSAJES NO COMANDOS ===
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if any(p in texto for p in ["precio", "costo", "comprar", "$37"]):
        await precio(update, context)
    elif "taza" in texto:
        await taza(update, context)
    elif "material" in texto:
        await materiales(update, context)
    elif "rendimiento" in texto:
        await rendimiento(update, context)
    elif "descuento" in texto:
        await descuento(update, context)
    elif "eficiencia" in texto:
        await eficiencia(update, context)
    elif "clima" in texto:
        await clima(update, context)
    else:
        await update.message.reply_text("No entendí. Usa /ayuda para ver los comandos.")

# === INICIO DEL BOT ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("taza", taza))
    app.add_handler(CommandHandler("materiales", materiales))
    app.add_handler(CommandHandler("rendimiento", rendimiento))
    app.add_handler(CommandHandler("descuento", descuento))
    app.add_handler(CommandHandler("eficiencia", eficiencia))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("✅ Bot iniciado correctamente. Presiona Ctrl+C para detener.")
    app.run_polling()

if __name__ == "__main__":
    main()