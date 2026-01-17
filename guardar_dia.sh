#!/bin/bash

# Fecha y hora para el mensaje de commit
FECHA=$(date +"%Y-%m-%d %H:%M")

echo "🔍 Verificando cambios..."
git status

echo "➕ Agregando cambios..."
git add .

echo "💾 Creando commit..."
git commit -m "Respaldo automático del día $FECHA"

echo "🚀 Enviando a GitHub..."
git push origin dev

echo "✅ Trabajo guardado correctamente. Buen descanso 😴"
