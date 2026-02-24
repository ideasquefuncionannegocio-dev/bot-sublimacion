import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIGURACIÓN ===
TOKEN = "8193083254:AAEEY6xMwMq-6IMKVPY8EM105GfUPUe2yeM"
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ====================================================
# BASES DE DATOS (TABLAS)
# ====================================================

# PRODUCTOS POR CATEGORÍA (39 productos)
PRODUCTOS = {
    "textiles": [
        "Camiseta Adulto", "Camiseta Niño", "Polo Adulto", "Polo Niño",
        "Gorra Adulto (frontal)", "Gorra Niño (frontal)"
    ],
    "ceramicas": [
        "Taza cerámica blanca 11 oz", "Taza cerámica blanca 15 oz",
        "Taza mágica", "Plato 8” (área 100%)", "Plato 8” (área central)"
    ],
    "termos_vasos": [
        "Termo sublimable", "Termos de Acero", "Vasos de Acero",
        "Vasos de Vidrio", "Tazas de Vidrio", "Tazas de Plástico"
    ],
    "accesorios": [
        "Llaveros de Aluminio", "Llaveros de MDF", "Llaveros de Plástico",
        "Portavasos de Neopreno", "Portavasos de PVC", "Posavasos de Plástico"
    ],
    "decoracion": [
        "Portaretratos de MDF", "Láminas de Aluminio 0,30 x 0,30",
        "Mouse Pad de Neopreno"
    ],
    "metales_vidrio": [
        "Botellas de Aluminio", "Latas de Acero", "Latas de Aluminio",
        "Tarros de Vidrio", "Tequileros de Vidrio"
    ],
    "otros": [
        "Accesorios pequeños de PVC", "Cajitas de Cartón", "Carpetas de Cartón",
        "Coolers de Neopreno", "Rompecabezas de Cartón",
        "Rompecabezas de MDF", "Vinilos Blancos", "Vinilos Transparentes"
    ]
}

# PRECIOS EN USD (costo directo)
PRECIOS_USD = {
    "Accesorios pequeños de PVC": 1.04,
    "Botellas de Aluminio": 6.23,
    "Cajitas de Cartón": 1.77,
    "Camiseta Adulto": 6.77,
    "Camiseta Niño": 6.20,
    "Carpetas de Cartón": 2.14,
    "Coolers de Neopreno": 4.16,
    "Gorra Adulto (frontal)": 3.30,
    "Gorra Niño (frontal)": 2.84,
    "Láminas de Aluminio 0,30 x 0,30": 4.21,
    "Latas de Acero": 3.59,
    "Latas de Aluminio": 2.47,
    "Llaveros de Aluminio": 2.02,
    "Llaveros de MDF": 1.48,
    "Llaveros de Plástico": 1.35,
    "Mouse Pad de Neopreno": 3.94,
    "Plato 8” (área 100%)": 5.34,
    "Plato 8” (área central)": 5.01,
    "Polo Adulto": 10.09,
    "Polo Niño": 7.69,
    "Portaretratos de MDF": 3.59,
    "Portavasos de Neopreno": 1.93,
    "Portavasos de PVC": 1.27,
    "Posavasos de Plástico": 1.36,
    "Rompecabezas de Cartón": 4.44,
    "Rompecabezas de MDF": 5.37,
    "Tarros de Vidrio": 5.35,
    "Taza cerámica blanca 11 oz": 2.69,
    "Taza cerámica blanca 15 oz": 3.82,
    "Taza mágica": 4.12,
    "Tazas de Plástico": 1.97,
    "Tazas de Vidrio": 4.44,
    "Tequileros de Vidrio": 2.80,
    "Termo sublimable": 7.56,
    "Termos de Acero": 14.38,
    "Vasos de Acero": 7.22,
    "Vasos de Vidrio": 3.68,
    "Vinilos Blancos": 4.17,
    "Vinilos Transparentes": 4.92
}

# RENDIMIENTO (unidades por día) - ¡DIRECTAMENTE DE TU TABLA!
RENDIMIENTO = {
    "Accesorios pequeños de PVC": 138.41,
    "Botellas de Aluminio": 52.36,
    "Cajitas de Cartón": 84.39,
    "Camiseta Adulto": 65.66,
    "Camiseta Niño": 73.15,
    "Carpetas de Cartón": 74.84,
    "Coolers de Neopreno": 53.33,
    "Gorra Adulto (frontal)": 73.15,
    "Gorra Niño (frontal)": 82.56,
    "Láminas de Aluminio 0,30 x 0,30": 98.40,
    "Latas de Acero": 64.00,
    "Latas de Aluminio": 69.81,
    "Llaveros de Aluminio": 134.68,
    "Llaveros de MDF": 118.17,
    "Llaveros de Plástico": 138.41,
    "Mouse Pad de Neopreno": 66.78,
    "Plato 8” (área 100%)": 58.18,
    "Plato 8” (área central)": 66.78,
    "Polo Adulto": 65.09,
    "Polo Niño": 69.19,
    "Portaretratos de MDF": 70.11,
    "Portavasos de Neopreno": 87.24,
    "Portavasos de PVC": 91.43,
    "Posavasos de Plástico": 102.17,
    "Rompecabezas de Cartón": 66.78,
    "Rompecabezas de MDF": 58.78,
    "Tarros de Vidrio": 55.13,
    "Taza cerámica blanca 11 oz": 61.44,
    "Taza cerámica blanca 15 oz": 56.06,
    "Taza mágica": 51.20,
    "Tazas de Plástico": 68.55,
    "Tazas de Vidrio": 59.52,
    "Tequileros de Vidrio": 68.55,
    "Termo sublimable": 50.50,
    "Termos de Acero": 42.74,
    "Vasos de Acero": 58.18,
    "Vasos de Vidrio": 59.52,
    "Vinilos Blancos": 425.53,
    "Vinilos Transparentes": 425.53
}

# PAÍSES (para verificar existencia)
PAISES = [
    "Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda",
    "Arabia Saudita", "Argelia", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaiyán", "Bahamas", "Bangladés", "Barbados", "Baréin", "Bélgica",
    "Belice", "Benín", "Bielorrusia", "Birmania", "Bolivia", "Bosnia y Herzegovina",
    "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso", "Burundi",
    "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Catar",
    "Ciudad del Vaticano", "Chad", "Chile", "China", "Chipre", "Colombia",
    "Comoras", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica",
    "Croacia", "Cuba", "Dinamarca", "Dominica", "Ecuador", "Egipto",
    "El Salvador", "Emiratos Árabes Unidos", "Eritrea", "Eslovaquia", "Eslovenia",
    "España", "Estados Unidos", "Estonia", "Etiopía", "Filipinas", "Finlandia",
    "Fiyi", "Francia", "Gabón", "Gambia", "Georgia", "Ghana", "Granada",
    "Grecia", "Guatemala", "Guinea", "Guinea-Bisáu", "Guinea Ecuatorial", "Guyana",
    "Haití", "Honduras", "Hungría", "India", "Indonesia", "Irak", "Irán",
    "Irlanda", "Islandia", "Islas Marshall", "Islas Salomón", "Israel", "Italia",
    "Jamaica", "Japón", "Jordania", "Kazajistán", "Kenia", "Kirguistán",
    "Kiribati", "Kuwait", "Laos", "Lesoto", "Letonia", "Líbano", "Liberia",
    "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Madagascar", "Malasia",
    "Malaui", "Maldivas", "Malí", "Malta", "Marruecos", "Mauricio", "Mauritania",
    "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montenegro",
    "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger", "Nigeria",
    "Noruega", "Nueva Zelanda", "Omán", "Países Bajos", "Pakistán", "Palaos",
    "Panamá", "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia", "Portugal",
    "Reino Unido", "República Centroafricana", "República Checa",
    "República de Macedonia del Norte", "República del Congo",
    "República Democrática del Congo", "República Dominicana", "Ruanda", "Rumanía",
    "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino",
    "San Vicente y las Granadinas", "Santa Lucía", "Santo Tomé y Príncipe",
    "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", "Siria",
    "Somalia", "Sri Lanka", "Esuatini", "Sudáfrica", "Sudán", "Sudán del Sur",
    "Suecia", "Suiza", "Surinam", "Tailandia", "Taiwán", "Tayikistán",
    "Tanzania", "Timor Oriental", "Togo", "Tonga", "Trinidad y Tobago", "Túnez",
    "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda", "Uruguay",
    "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yibuti",
    "Zambia", "Zimbabue"
]

# ====================================================
# FUNCIONES DE COMANDOS
# ====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy **Alexander**, el asistente técnico de la guía **'PRECIO REAL: APU para Sublimación'**.\n\n"
        "📌 **Comandos disponibles:**\n"
        "/precio - Link de compra de la guía\n"
        "/productos - Ver productos por categoría\n"
        "/materiales - Lista de materiales en USD\n"
        "/rendimiento [producto] - Unidades por día\n"
        "/descuento - Descuento en guía o fórmula APU\n"
        "/eficiencia - Factores de eficiencia\n"
        "/clima - Ajuste por clima\n"
        "/pais [nombre] - Verificar si un país está en la base\n"
        "/ayuda - Muestra este mensaje"
    )

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📘 **Guía completa + Excel automatizado**\n"
        "💰 Precio: **$37 USD**\n"
        "🔗 Adquiérela aquí:\n"
        "https://go.hotmart.com/V104219195N"
    )

async def productos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "📦 **Categorías de productos:**\n\n"
    texto += "1. 🧥 Textiles\n"
    texto += "2. ☕ Cerámicas\n"
    texto += "3. 🧴 Termos y Vasos\n"
    texto += "4. 🔑 Accesorios\n"
    texto += "5. 🖼️ Decoración\n"
    texto += "6. 🥫 Metales y Vidrio\n"
    texto += "7. 🧩 Otros\n\n"
    texto += "Responde con el **número** o **nombre** de la categoría para ver sus productos."
    await update.message.reply_text(texto)

async def materiales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "📦 **MATERIALES EN USD (referencia):**\n\n"
        "📄 **Papel sublimable:**\n"
        "• A4: $0.138/hoja\n"
        "• A3: $0.205/hoja\n\n"
        "📄 **Papel siliconado:**\n"
        "• A4: $0.062/hoja (12 usos)\n"
        "• A3: $0.125/hoja (12 usos)\n\n"
        "🖨️ **Tinta:**\n"
        "• Kit 4 colores 100ml c/u: $22.57\n"
        "• Por ml: $0.056\n\n"
        "📏 **Cinta térmica:**\n"
        "• 5mm: $0.060/m\n"
        "• 10mm: $0.091/m\n\n"
        "💡 *Precios en USD. Para moneda local, adquiere la guía con Excel automatizado.*"
    )
    await update.message.reply_text(texto)

async def rendimiento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Debes especificar un producto. Ej: /rendimiento taza 11 oz")
        return
    producto = " ".join(context.args).lower()
    encontrado = None
    for prod in RENDIMIENTO:
        if prod.lower() == producto or any(p in prod.lower() for p in producto.split() if len(p) > 3):
            encontrado = prod
            break
    if not encontrado:
        await update.message.reply_text("❌ Producto no encontrado. Revisa el nombre.")
        return
    unidades = RENDIMIENTO[encontrado]
    await update.message.reply_text(
        f"📊 **{encontrado}**\n"
        f"• En una jornada de 8 horas puedes producir:\n"
        f"👉 **{unidades:.2f} unidades/día**"
    )

async def descuento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🎁 **¿Descuento para comprar la guía?**\n"
        "Envía el comprobante de pantalla por WhatsApp a:\n"
        "📱 **+593983930901**\n"
        "*Antes de realizar la compra* para aplicar el 20% de descuento.\n\n"
        "📉 **¿Cómo calcular descuentos en productos?**\n"
        "Fórmula APU: % utilidad final = [(1+%APU) × (1-%desc) -1] × 100\n"
        "Ejemplo: 80% utilidad con 10% descuento → 62% utilidad final."
    )
    await update.message.reply_text(texto)

async def eficiencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚙️ **Factores de eficiencia (FER):**\n"
        "• Diseñador gráfico: 85%\n"
        "• Operario de prensa: 80%\n\n"
        "Ajustan la capacidad teórica a la realidad operativa."
    )

async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌡️ **Ajuste por clima (consumo energético):**\n"
        "• Templado: factor 1.00\n"
        "• Frío: factor 1.05\n"
        "• Cálido: factor 1.00\n\n"
        "Influye en el costo del Split (climatización)."
    )

async def pais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Debes escribir un país. Ej: /pais colombia")
        return
    nombre = " ".join(context.args).strip().lower()
    for p in PAISES:
        if p.lower() == nombre or nombre in p.lower():
            await update.message.reply_text(f"✅ **{p}** está en la base del APU.")
            return
    await update.message.reply_text("❌ Ese país no está en la lista. Usa /paises para ver los disponibles.")

async def paises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lista = "\n".join(PAISES[:20])
    await update.message.reply_text(
        f"🌎 **Primeros 20 países de la base APU:**\n\n{lista}\n\n... y {len(PAISES)-20} más.\n"
        "Usa /pais [nombre] para consultar uno específico."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# ====================================================
# MANEJADOR DE MENSAJES (CATEGORÍAS)
# ====================================================

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower().strip()
    # Primero verificar si es número de categoría
    if texto == "1" or "textiles" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["textiles"]])
        await update.message.reply_text(f"🧥 **Textiles:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    elif texto == "2" or "cerámicas" in texto or "ceramicas" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["ceramicas"]])
        await update.message.reply_text(f"☕ **Cerámicas:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    elif texto == "3" or "termos" in texto or "vasos" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["termos_vasos"]])
        await update.message.reply_text(f"🧴 **Termos y Vasos:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    elif texto == "4" or "accesorios" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["accesorios"]])
        await update.message.reply_text(f"🔑 **Accesorios:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    elif texto == "5" or "decoración" in texto or "decoracion" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["decoracion"]])
        await update.message.reply_text(f"🖼️ **Decoración:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    elif texto == "6" or "metales" in texto or "vidrio" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["metales_vidrio"]])
        await update.message.reply_text(f"🥫 **Metales y Vidrio:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    elif texto == "7" or "otros" in texto:
        prods = "\n".join([f"• {p}" for p in PRODUCTOS["otros"]])
        await update.message.reply_text(f"🧩 **Otros:**\n\n{prods}\n\nEscribe el nombre exacto del producto.")
    else:
        # Buscar si es un producto exacto
        for prod, precio in PRECIOS_USD.items():
            if prod.lower() == texto or any(p in prod.lower() for p in texto.split() if len(p) > 3):
                await update.message.reply_text(
                    f"🌎 **{prod}**\n"
                    f"💰 Precio USD: ${precio:.2f}\n\n"
                    f"💡 *Este es el costo de producción en dólares americanos.*\n"
                    f"📌 Para precio en tu moneda, adquiere la guía con Excel automatizado:\n"
                    f"https://go.hotmart.com/V104219195N"
                )
                return
        await update.message.reply_text("❌ No entendí. Usa /ayuda para ver los comandos.")

# ====================================================
# CONFIGURACIÓN Y ARRANQUE
# ====================================================

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("productos", productos))
    app.add_handler(CommandHandler("materiales", materiales))
    app.add_handler(CommandHandler("rendimiento", rendimiento))
    app.add_handler(CommandHandler("descuento", descuento))
    app.add_handler(CommandHandler("eficiencia", eficiencia))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("pais", pais))
    app.add_handler(CommandHandler("paises", paises))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("✅ Bot Alexander iniciado correctamente.")
    app.run_polling()

if __name__ == "__main__":
    main()

