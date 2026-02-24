import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIGURACIÓN ===
TOKEN = "8193083254:AAEEY6xMwMq-6IMKVPY8EM105GfUPUe2yeM"
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ====================================================
# BASES DE DATOS COMPLETAS
# ====================================================

# ========== PRODUCTOS ==========
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

PVP = {
    "Accesorios pequeños de PVC": 1.87,
    "Botellas de Aluminio": 11.21,
    "Cajitas de Cartón": 3.19,
    "Camiseta Adulto": 12.18,
    "Camiseta Niño": 11.16,
    "Carpetas de Cartón": 3.85,
    "Coolers de Neopreno": 7.49,
    "Gorra Adulto (frontal)": 5.94,
    "Gorra Niño (frontal)": 5.11,
    "Láminas de Aluminio 0,30 x 0,30": 7.58,
    "Latas de Acero": 6.46,
    "Latas de Aluminio": 4.45,
    "Llaveros de Aluminio": 3.64,
    "Llaveros de MDF": 2.66,
    "Llaveros de Plástico": 2.43,
    "Mouse Pad de Neopreno": 7.09,
    "Plato 8” (área 100%)": 9.61,
    "Plato 8” (área central)": 9.02,
    "Polo Adulto": 18.16,
    "Polo Niño": 13.84,
    "Portaretratos de MDF": 6.46,
    "Portavasos de Neopreno": 3.47,
    "Portavasos de PVC": 2.29,
    "Posavasos de Plástico": 2.45,
    "Rompecabezas de Cartón": 7.99,
    "Rompecabezas de MDF": 9.67,
    "Tarros de Vidrio": 9.63,
    "Taza cerámica blanca 11 oz": 4.84,
    "Taza cerámica blanca 15 oz": 6.88,
    "Taza mágica": 7.42,
    "Tazas de Plástico": 3.55,
    "Tazas de Vidrio": 7.99,
    "Tequileros de Vidrio": 5.04,
    "Termo sublimable": 13.61,
    "Termos de Acero": 25.88,
    "Vasos de Acero": 13.00,
    "Vasos de Vidrio": 6.62,
    "Vinilos Blancos": 7.51,
    "Vinilos Transparentes": 8.86
}

COSTO_DIRECTO = {
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

PRENSADO = {
    "Accesorios pequeños de PVC": 90,
    "Botellas de Aluminio": 200,
    "Cajitas de Cartón": 130,
    "Camiseta Adulto": 150,
    "Camiseta Niño": 140,
    "Carpetas de Cartón": 140,
    "Coolers de Neopreno": 180,
    "Gorra Adulto (frontal)": 150,
    "Gorra Niño (frontal)": 135,
    "Láminas de Aluminio 0,30 x 0,30": 120,
    "Latas de Acero": 160,
    "Latas de Aluminio": 150,
    "Llaveros de Aluminio": 90,
    "Llaveros de MDF": 100,
    "Llaveros de Plástico": 90,
    "Mouse Pad de Neopreno": 150,
    "Plato 8” (área 100%)": 180,
    "Plato 8” (área central)": 160,
    "Polo Adulto": 155,
    "Polo Niño": 145,
    "Portaretratos de MDF": 140,
    "Portavasos de Neopreno": 120,
    "Portavasos de PVC": 120,
    "Posavasos de Plástico": 110,
    "Rompecabezas de Cartón": 150,
    "Rompecabezas de MDF": 160,
    "Tarros de Vidrio": 190,
    "Taza cerámica blanca 11 oz": 180,
    "Taza cerámica blanca 15 oz": 200,
    "Taza mágica": 210,
    "Tazas de Plástico": 160,
    "Tazas de Vidrio": 180,
    "Tequileros de Vidrio": 160,
    "Termo sublimable": 210,
    "Termos de Acero": 220,
    "Vasos de Acero": 180,
    "Vasos de Vidrio": 180,
    "Vinilos Blancos": 30,
    "Vinilos Transparentes": 30
}

TEMPERATURA = {
    "Accesorios pequeños de PVC": 190,
    "Botellas de Aluminio": 190,
    "Cajitas de Cartón": 190,
    "Camiseta Adulto": 190,
    "Camiseta Niño": 190,
    "Carpetas de Cartón": 190,
    "Coolers de Neopreno": 190,
    "Gorra Adulto (frontal)": 180,
    "Gorra Niño (frontal)": 180,
    "Láminas de Aluminio 0,30 x 0,30": 190,
    "Latas de Acero": 190,
    "Latas de Aluminio": 190,
    "Llaveros de Aluminio": 190,
    "Llaveros de MDF": 190,
    "Llaveros de Plástico": 190,
    "Mouse Pad de Neopreno": 190,
    "Plato 8” (área 100%)": 190,
    "Plato 8” (área central)": 190,
    "Polo Adulto": 190,
    "Polo Niño": 190,
    "Portaretratos de MDF": 190,
    "Portavasos de Neopreno": 190,
    "Portavasos de PVC": 190,
    "Posavasos de Plástico": 190,
    "Rompecabezas de Cartón": 190,
    "Rompecabezas de MDF": 190,
    "Tarros de Vidrio": 190,
    "Taza cerámica blanca 11 oz": 190,
    "Taza cerámica blanca 15 oz": 190,
    "Taza mágica": 190,
    "Tazas de Plástico": 190,
    "Tazas de Vidrio": 190,
    "Tequileros de Vidrio": 190,
    "Termo sublimable": 190,
    "Termos de Acero": 190,
    "Vasos de Acero": 190,
    "Vasos de Vidrio": 190,
    "Vinilos Blancos": 180,
    "Vinilos Transparentes": 180
}

# ========== MATERIALES ==========
MATERIALES_PAPEL = {
    "Papel sublimable A4": 0.138,
    "Papel sublimable A3": 0.205,
    "Papel siliconado A4": 0.062,
    "Papel siliconado A3": 0.125
}

MATERIALES_TINTA = {
    "Kit 4 colores 100ml": 22.57,
    "Tinta por ml": 0.056,
    "Tinta por litro (cada color)": 45.00
}

MATERIALES_CINTA = {
    "Cinta térmica 5mm": 0.060,
    "Cinta térmica 10mm": 0.091
}

MATERIALES_BASE = {
    "Taza 11 oz": 1.06,
    "Taza 15 oz": 2.00,
    "Taza mágica": 2.15,
    "Plato 8” 100%": 3.50,
    "Plato 8” central": 3.50,
    "Termo sublimable": 5.49,
    "Termo acero": 12.00,
    "Camiseta adulto": 4.90,
    "Camiseta niño": 4.53,
    "Polo adulto": 8.20,
    "Polo niño": 6.00,
    "Gorra adulto": 1.99,
    "Gorra niño": 1.67
}

MATERIALES_INSUMOS = {
    "Guantes": 15.00,
    "Tijera": 13.00,
    "Cinta métrica": 0.75
}

MATERIALES_OTROS = {
    "Vinilos blancos": 3.75,
    "Vinilos transparentes": 4.50,
    "Llaveros aluminio": 1.25,
    "Llaveros MDF": 0.60,
    "Llaveros plástico": 0.60,
    "Portavasos neopreno": 0.70,
    "Portavasos PVC": 0.10,
    "Posavasos plástico": 0.30,
    "Accesorios PVC": 0.30,
    "Cajitas cartón": 0.48,
    "Carpetas cartón": 0.65,
    "Coolers neopreno": 2.00,
    "Rompecabezas cartón": 2.75,
    "Rompecabezas MDF": 3.50,
    "Láminas aluminio": 3.00,
    "Latas acero": 2.00,
    "Latas aluminio": 1.00,
    "Tarros vidrio": 3.50,
    "Tequileros vidrio": 1.40,
    "Vasos acero": 5.50,
    "Vasos vidrio": 2.00,
    "Tazas plástico": 0.50,
    "Tazas vidrio": 2.75
}

# ========== EQUIPOS ==========
EQUIPOS = {
    "Cizalla": {"precio": 40, "costo_hora": 0.02},
    "Computador": {"precio": 750, "costo_hora": 0.40},
    "Impresora": {"precio": 220, "costo_hora": 0.12},
    "Monitor": {"precio": 320, "costo_hora": 0.17},
    "Prensa de Gorras": {"precio": 185, "costo_hora": 0.10},
    "Prensa de Platos 10\"": {"precio": 260, "costo_hora": 0.14},
    "Prensa de Platos 8\"": {"precio": 220, "costo_hora": 0.12},
    "Prensa Plana 38x38": {"precio": 425, "costo_hora": 0.23},
    "Prensa Plana 40x60": {"precio": 565, "costo_hora": 0.30},
    "Prensa Tazas 11 oz": {"precio": 100, "costo_hora": 0.05},
    "Prensa Tazas 15 oz": {"precio": 150, "costo_hora": 0.08},
    "Prensa Tazas doble 11 oz": {"precio": 256.68, "costo_hora": 0.14},
    "Router": {"precio": 396, "costo_hora": 0.21},
    "Split 12.000 BTU": {"precio": 280, "costo_hora": 0.15}
}
COSTO_KWH = 0.097

# ========== MANO DE OBRA ==========
MANO_OBRA = {
    "Dibujante": 4.64,
    "Operario de prensa térmica": 4.39
}

# ========== PAÍSES POR CONTINENTE ==========
PAISES_AMERICA = [
    "Argentina", "Bolivia", "Brasil", "Canadá", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Ecuador", "El Salvador", "Estados Unidos", "Guatemala", "Haití",
    "Honduras", "México", "Nicaragua", "Panamá", "Paraguay", "Perú",
    "República Dominicana", "Uruguay", "Venezuela"
]
PAISES_EUROPA = [
    "Alemania", "Andorra", "Austria", "Bélgica", "Bulgaria", "Croacia", "Dinamarca",
    "Eslovaquia", "Eslovenia", "España", "Estonia", "Finlandia", "Francia", "Grecia",
    "Hungría", "Irlanda", "Islandia", "Italia", "Letonia", "Lituania", "Luxemburgo",
    "Malta", "Noruega", "Países Bajos", "Polonia", "Portugal", "Reino Unido",
    "República Checa", "Rumanía", "Rusia", "Serbia", "Suecia", "Suiza", "Ucrania"
]
PAISES_ASIA = [
    "Afganistán", "Arabia Saudita", "Armenia", "Azerbaiyán", "Bangladés", "Birmania",
    "Brunéi", "Bután", "Camboya", "Catar", "China", "Chipre", "Corea del Norte",
    "Corea del Sur", "Emiratos Árabes Unidos", "Filipinas", "Georgia", "India",
    "Indonesia", "Irak", "Irán", "Israel", "Japón", "Jordania", "Kazajistán",
    "Kirguistán", "Kuwait", "Laos", "Líbano", "Malasia", "Maldivas", "Mongolia",
    "Nepal", "Omán", "Pakistán", "Rusia", "Singapur", "Siria", "Sri Lanka",
    "Tailandia", "Taiwán", "Tayikistán", "Timor Oriental", "Turkmenistán", "Turquía",
    "Uzbekistán", "Vietnam", "Yemen"
]
PAISES_AFRICA = [
    "Angola", "Argelia", "Benín", "Botsuana", "Burkina Faso", "Burundi", "Cabo Verde",
    "Camerún", "Chad", "Comoras", "Costa de Marfil", "Egipto", "Eritrea", "Esuatini",
    "Etiopía", "Gabón", "Gambia", "Ghana", "Guinea", "Guinea-Bisáu", "Guinea Ecuatorial",
    "Kenia", "Lesoto", "Liberia", "Libia", "Madagascar", "Malaui", "Malí", "Marruecos",
    "Mauricio", "Mauritania", "Mozambique", "Namibia", "Níger", "Nigeria",
    "República Centroafricana", "República del Congo", "República Democrática del Congo",
    "Ruanda", "Santo Tomé y Príncipe", "Senegal", "Seychelles", "Sierra Leona",
    "Somalia", "Sudáfrica", "Sudán", "Sudán del Sur", "Tanzania", "Togo", "Túnez",
    "Uganda", "Yibuti", "Zambia", "Zimbabue"
]
PAISES_OCEANIA = [
    "Australia", "Fiyi", "Islas Marshall", "Islas Salomón", "Kiribati", "Micronesia",
    "Nauru", "Nueva Zelanda", "Palaos", "Papúa Nueva Guinea", "Samoa", "Tonga", "Tuvalu",
    "Vanuatu"
]

# ====================================================
# FUNCIONES DE COMANDOS
# ====================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 ¡Hola **{nombre}**! Soy **Alexander**, el asistente técnico de la guía **'PRECIO REAL: APU para Sublimación'**.\n\n"
        "📌 **¿Cómo usar la asistencia técnica?**\n"
        "Escribe **/ seguido del comando** que necesites.\n"
        "Ejemplo: /productos\n\n"
        "📌 **Comandos disponibles:**\n"
        "/precio - Link de compra de la guía\n"
        "/productos - Ver productos por categoría\n"
        "/materiales - Materiales por categoría\n"
        "/rendimiento - Unidades/día por categoría\n"
        "/prensado - Tiempo de prensado (seg) por categoría\n"
        "/temperatura - Temperatura (°C) por categoría\n"
        "/equipos - Lista de equipos\n"
        "/luz - Costo de energía ($/kWh)\n"
        "/manoobra - Costo de mano de obra\n"
        "/paises - Menú de países\n"
        "/clima - Ajuste por clima\n"
        "/descuento - Descuento en guía o fórmula APU\n"
        "/eficiencia - Factores de eficiencia\n"
        "/ayuda - Muestra este mensaje"
    )

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"📘 **{nombre}**, aquí tienes el link de compra de la guía:\n\n"
        "📘 **Guía completa + Excel automatizado**\n"
        "💰 Precio: **$37 USD**\n"
        "🔗 Adquiérela aquí:\n"
        "https://go.hotmart.com/V104219195N"
    )

async def productos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"📦 **{nombre}**, estas son las categorías de productos:\n\n"
    cats = list(PRODUCTOS.keys())
    for i, cat in enumerate(cats, 1):
        nombre_cat = cat.replace("_", " ").title()
        texto += f"{i}. {nombre_cat}\n"
    texto += "\n🔁 *Si deseas ver otra categoría, escribe nuevamente /productos.*"
    context.user_data['menu'] = 'productos'
    context.user_data['categorias'] = cats
    await update.message.reply_text(texto)

async def materiales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"📦 **{nombre}**, estas son las categorías de materiales:\n\n"
    texto += "1. 📄 Papeles\n"
    texto += "2. 🖨️ Tintas\n"
    texto += "3. 📏 Cintas térmicas\n"
    texto += "4. 🟤 Productos base\n"
    texto += "5. 🔧 Insumos\n"
    texto += "6. ⚙️ Otros\n\n"
    texto += "🔁 *Si deseas ver otra categoría, escribe nuevamente /materiales.*"
    context.user_data['menu'] = 'materiales'
    await update.message.reply_text(texto)

async def rendimiento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"📊 **{nombre}**, selecciona una categoría para ver unidades/día:\n\n"
    cats = list(PRODUCTOS.keys())
    for i, cat in enumerate(cats, 1):
        nombre_cat = cat.replace("_", " ").title()
        texto += f"{i}. {nombre_cat}\n"
    texto += "\n🔁 *Si deseas consultar otra categoría, escribe nuevamente /rendimiento.*"
    context.user_data['menu'] = 'rendimiento'
    context.user_data['categorias'] = cats
    await update.message.reply_text(texto)

async def prensado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"⏱️ **{nombre}**, selecciona una categoría para ver tiempo de prensado:\n\n"
    cats = list(PRODUCTOS.keys())
    for i, cat in enumerate(cats, 1):
        nombre_cat = cat.replace("_", " ").title()
        texto += f"{i}. {nombre_cat}\n"
    texto += "\n🔁 *Si deseas consultar otra categoría, escribe nuevamente /prensado.*"
    context.user_data['menu'] = 'prensado'
    context.user_data['categorias'] = cats
    await update.message.reply_text(texto)

async def temperatura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"🌡️ **{nombre}**, selecciona una categoría para ver temperatura:\n\n"
    cats = list(PRODUCTOS.keys())
    for i, cat in enumerate(cats, 1):
        nombre_cat = cat.replace("_", " ").title()
        texto += f"{i}. {nombre_cat}\n"
    texto += "\n🔁 *Si deseas consultar otra categoría, escribe nuevamente /temperatura.*"
    context.user_data['menu'] = 'temperatura'
    context.user_data['categorias'] = cats
    await update.message.reply_text(texto)

async def equipos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"⚙️ **{nombre}**, estos son los equipos disponibles:\n\n"
    for eq, datos in EQUIPOS.items():
        texto += f"• {eq}: ${datos['precio']} (${datos['costo_hora']}/h)\n"
    texto += f"\n⚡ **Costo energía:** ${COSTO_KWH}/kWh"
    await update.message.reply_text(texto)

async def luz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(f"⚡ **{nombre}**, el costo de energía es ${COSTO_KWH}/kWh")

async def manoobra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"👷 **{nombre}**, estos son los costos de mano de obra por hora:\n\n"
    texto += f"• Dibujante: ${MANO_OBRA['Dibujante']}/h\n"
    texto += f"• Operario de prensa térmica: ${MANO_OBRA['Operario de prensa térmica']}/h"
    await update.message.reply_text(texto)

async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"🌡️ **{nombre}**, estos son los ajustes por clima:\n\n"
        "• Templado: factor 1.00\n"
        "• Frío: factor 1.05\n"
        "• Cálido: factor 1.00"
    )

async def descuento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = (
        f"🎁 **{nombre}**, sobre descuentos:\n\n"
        "**¿Descuento para comprar la guía?**\n"
        "Envía el comprobante de pantalla antes de hacer la compra para obtener el código de descuento al WhatsApp:\n"
        "📱 **+593983930901**\n\n"
        "**¿Cómo calcular descuentos en productos?**\n"
        "Fórmula APU:\n"
        "% utilidad final = [(1 + %APU) × (1 - %desc) - 1] × 100\n\n"
        "Ejemplo con taza 11 oz:\n"
        "• %APU (utilidad base): 80%\n"
        "• Descuento ofrecido: 10%\n"
        "• % utilidad final = [(1 + 0.80) × (1 - 0.10) - 1] × 100\n"
        "• % utilidad final = 62%"
    )
    await update.message.reply_text(texto)

async def eficiencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"⚙️ **{nombre}**, estos son los factores de eficiencia:\n\n"
        "• Diseñador gráfico: 85%\n"
        "• Operario de prensa: 80%"
    )

async def paises(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    texto = f"🌎 **{nombre}**, estas son las opciones para consultar países:\n\n"
    texto += "1. 🌎 Consultar país específico (usar /pais [nombre])\n"
    texto += "2. 🌍 Ver lista por continente\n\n"
    texto += "🔁 *Si deseas realizar otra consulta, escribe nuevamente /paises.*"
    context.user_data['menu'] = 'paises'
    await update.message.reply_text(texto)

async def pais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    if not context.args:
        await update.message.reply_text(f"❌ **{nombre}**, debes escribir un país. Ejemplo: /pais colombia")
        return
    pais = " ".join(context.args).strip().lower()
    todos = PAISES_AMERICA + PAISES_EUROPA + PAISES_ASIA + PAISES_AFRICA + PAISES_OCEANIA
    for p in todos:
        if p.lower() == pais or pais in p.lower():
            await update.message.reply_text(f"✅ **{nombre}**, **{p}** está en la base del APU.")
            return
    await update.message.reply_text(f"❌ **{nombre}**, ese país no está en la lista.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# ====================================================
# MANEJADOR DE MENSAJES (MENÚS NUMERADOS)
# ====================================================

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    user_data = context.user_data
    nombre = update.effective_user.first_name

    # === PRODUCTOS: selección de categoría ===
    if user_data.get('menu') == 'productos' and texto.isdigit():
        idx = int(texto) - 1
        cats = user_data.get('categorias', [])
        if 0 <= idx < len(cats):
            cat = cats[idx]
            prods = PRODUCTOS[cat]
            resp = f"📦 **{nombre}**, estos son los productos de **{cat.replace('_', ' ').title()}:**\n\n"
            for i, prod in enumerate(prods, 1):
                resp += f"{i}. {prod}\n"
            resp += "\n🔁 *Si deseas consultar otro producto, escribe nuevamente /productos.*"
            user_data['menu'] = 'producto_detalle'
            user_data['productos_cat'] = prods
            await update.message.reply_text(resp)
            return
        else:
            await update.message.reply_text(f"❌ **{nombre}**, número no válido. Intenta de nuevo.")
            return

    # === PRODUCTOS: detalle del producto ===
    if user_data.get('menu') == 'producto_detalle' and texto.isdigit():
        idx = int(texto) - 1
        prods = user_data.get('productos_cat', [])
        if 0 <= idx < len(prods):
            prod = prods[idx]
            pvp = PVP.get(prod, 0)
            cd = COSTO_DIRECTO.get(prod, 0)
            rend = RENDIMIENTO.get(prod, 0)
            prens = PRENSADO.get(prod, 0)
            temp = TEMPERATURA.get(prod, 0)
            resp = (
                f"💰 **{prod}**\n\n"
                f"• PVP sugerido USD: ${pvp:.2f}\n\n"
                f"• Insumo {prod} C.D.: ${cd:.2f}\n"
                f"• Unidades/día: {rend:.2f} u/día\n"
                f"• Tiempo prensado: {prens} seg\n"
                f"• Temperatura: {temp}°C\n\n"
                f"💡 *Precio en dólares americanos (USD).*\n"
                f"📌 *Para obtener el valor en tu moneda local, adquiere la guía con Excel automatizado:*\n"
                f"https://go.hotmart.com/V104219195N"
            )
            await update.message.reply_text(resp)
            user_data.pop('menu', None)
            return
        else:
            await update.message.reply_text(f"❌ **{nombre}**, número no válido.")
            return

    # === MATERIALES: selección de categoría ===
    if user_data.get('menu') == 'materiales' and texto.isdigit():
        idx = int(texto)
        if idx == 1:
            resp = f"📄 **{nombre}**, estos son los papeles:\n\n" + "\n".join([f"• {k}: ${v}" for k, v in MATERIALES_PAPEL.items()])
        elif idx == 2:
            resp = f"🖨️ **{nombre}**, estas son las tintas:\n\n" + "\n".join([f"• {k}: ${v}" for k, v in MATERIALES_TINTA.items()])
        elif idx == 3:
            resp = f"📏 **{nombre}**, estas son las cintas térmicas:\n\n" + "\n".join([f"• {k}: ${v}/m" for k, v in MATERIALES_CINTA.items()])
        elif idx == 4:
            resp = f"🟤 **{nombre}**, estos son los productos base:\n\n" + "\n".join([f"• {k}: ${v}" for k, v in MATERIALES_BASE.items()])
        elif idx == 5:
            resp = f"🔧 **{nombre}**, estos son los insumos:\n\n" + "\n".join([f"• {k}: ${v}" for k, v in MATERIALES_INSUMOS.items()])
        elif idx == 6:
            resp = f"⚙️ **{nombre}**, estos son otros materiales:\n\n" + "\n".join([f"• {k}: ${v}" for k, v in MATERIALES_OTROS.items()])
        else:
            resp = f"❌ **{nombre}**, opción no válida."
        resp += "\n\n🔁 *Si deseas ver otra categoría, escribe nuevamente /materiales.*"
        await update.message.reply_text(resp)
        user_data.pop('menu', None)
        return

    # === RENDIMIENTO: selección de categoría ===
    if user_data.get('menu') == 'rendimiento' and texto.isdigit():
        idx = int(texto) - 1
        cats = user_data.get('categorias', [])
        if 0 <= idx < len(cats):
            cat = cats[idx]
            prods = PRODUCTOS[cat]
            resp = f"📊 **{nombre}**, rendimiento de **{cat.replace('_', ' ').title()}:**\n\n"
            for prod in prods:
                resp += f"• {prod}: {RENDIMIENTO.get(prod, 0):.2f} u/día\n"
            resp += "\n🔁 *Si deseas consultar otra categoría, escribe nuevamente /rendimiento.*"
            await update.message.reply_text(resp)
            user_data.pop('menu', None)
            return
        else:
            await update.message.reply_text(f"❌ **{nombre}**, número no válido.")
            return

    # === PRENSADO: selección de categoría ===
    if user_data.get('menu') == 'prensado' and texto.isdigit():
        idx = int(texto) - 1
        cats = user_data.get('categorias', [])
        if 0 <= idx < len(cats):
            cat = cats[idx]
            prods = PRODUCTOS[cat]
            resp = f"⏱️ **{nombre}**, tiempo de prensado de **{cat.replace('_', ' ').title()}:**\n\n"
            for prod in prods:
                resp += f"• {prod}: {PRENSADO.get(prod, 0)} seg\n"
            resp += "\n🔁 *Si deseas consultar otra categoría, escribe nuevamente /prensado.*"
            await update.message.reply_text(resp)
            user_data.pop('menu', None)
            return
        else:
            await update.message.reply_text(f"❌ **{nombre}**, número no válido.")
            return

    # === TEMPERATURA: selección de categoría ===
    if user_data.get('menu') == 'temperatura' and texto.isdigit():
        idx = int(texto) - 1
        cats = user_data.get('categorias', [])
        if 0 <= idx < len(cats):
            cat = cats[idx]
            prods = PRODUCTOS[cat]
            resp = f"🌡️ **{nombre}**, temperatura de **{cat.replace('_', ' ').title()}:**\n\n"
            for prod in prods:
                resp += f"• {prod}: {TEMPERATURA.get(prod, 0)}°C\n"
            resp += "\n🔁 *Si deseas consultar otra categoría, escribe nuevamente /temperatura.*"
            await update.message.reply_text(resp)
            user_data.pop('menu', None)
            return
        else:
            await update.message.reply_text(f"❌ **{nombre}**, número no válido.")
            return

    # === PAÍSES: opción 1 o 2 ===
    if user_data.get('menu') == 'paises' and texto.isdigit():
        if texto == "1":
            await update.message.reply_text(f"🌎 **{nombre}**, usa el comando /pais seguido del nombre. Ejemplo: /pais colombia")
            user_data.pop('menu', None)
            return
        elif texto == "2":
            resp = f"🌍 **{nombre}**, elige un continente:\n\n"
            resp += "1. 🌎 América\n"
            resp += "2. 🌍 Europa\n"
            resp += "3. 🌏 Asia\n"
            resp += "4. 🌍 África\n"
            resp += "5. 🌏 Oceanía\n\n"
            resp += "🔁 *Si deseas volver al menú anterior, escribe nuevamente /paises.*"
            user_data['menu'] = 'continente'
            await update.message.reply_text(resp)
            return
        else:
            await update.message.reply_text(f"❌ **{nombre}**, opción no válida.")
            return

    # === CONTINENTES: lista de países ===
    if user_data.get('menu') == 'continente' and texto.isdigit():
        idx = int(texto)
        if idx == 1:
            paises = PAISES_AMERICA
            nombre_cont = "América"
        elif idx == 2:
            paises = PAISES_EUROPA
            nombre_cont = "Europa"
        elif idx == 3:
            paises = PAISES_ASIA
            nombre_cont = "Asia"
        elif idx == 4:
            paises = PAISES_AFRICA
            nombre_cont = "África"
        elif idx == 5:
            paises = PAISES_OCEANIA
            nombre_cont = "Oceanía"
        else:
            await update.message.reply_text(f"❌ **{nombre}**, opción no válida.")
            user_data.pop('menu', None)
            return
        resp = f"🌍 **{nombre}**, estos son los países de **{nombre_cont}:**\n\n"
        resp += "\n".join([f"• {p}" for p in paises])
        resp += "\n\n🔁 *Si deseas consultar otro continente, escribe nuevamente /paises.*"
        await update.message.reply_text(resp)
        user_data.pop('menu', None)
        return

    # === Si no es ningún comando ni menú, recordatorio ===
    await update.message.reply_text(
        f"Recuerda poner /ayuda para más información u otro dato."
    )
    return

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
    app.add_handler(CommandHandler("prensado", prensado))
    app.add_handler(CommandHandler("temperatura", temperatura))
    app.add_handler(CommandHandler("equipos", equipos))
    app.add_handler(CommandHandler("luz", luz))
    app.add_handler(CommandHandler("manoobra", manoobra))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("descuento", descuento))
    app.add_handler(CommandHandler("eficiencia", eficiencia))
    app.add_handler(CommandHandler("paises", paises))
    app.add_handler(CommandHandler("pais", pais))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("✅ Bot Alexander iniciado correctamente.")
    app.run_polling()

if __name__ == "__main__":
    main()
