#!/bin/bash
set -e

FECHA=$(date +"%Y-%m-%d %H:%M")

echo "🔍 Revisando cambios..."
git status

echo "➕ Agregando cambios (excepto guardar_dia.sh)..."
git add . ":!guardar_dia.sh"

# Si no hay nada staged, no hace commit
if git diff --cached --quiet; then
  echo "✅ No hay cambios reales que guardar (solo el script o nada). Buen descanso 😴"
  exit 0
fi

echo "💾 Creando commit..."
git commit -m "Respaldo automático del día $FECHA"

echo "🚀 Enviando a GitHub..."
git push origin dev

echo "✅ Trabajo guardado correctamente. Buen descanso 😴"
