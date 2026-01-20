#!/usr/bin/env bash
set -euo pipefail

# =========================
# Configuración
# =========================
BRANCH_EXPECTED="siga-v1.1.2"
REMOTE="origin"
DEFAULT_MESSAGE="Corregido Admin/Excel: fecha nacimiento dd/mm/yyyy + mascara"

# =========================
# Helpers
# =========================
die() { echo "ERROR: $*" >&2; exit 1; }

# =========================
# Validaciones iniciales
# =========================
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "No estás dentro de un repositorio Git."

current_branch="$(git branch --show-current)"
if [[ "$current_branch" != "$BRANCH_EXPECTED" ]]; then
  echo "Estás en la rama: $current_branch"
  echo "Este script está pensado para: $BRANCH_EXPECTED"
  echo "Cámbiate con: git checkout $BRANCH_EXPECTED"
  exit 1
fi

echo "✅ Rama actual: $current_branch"
echo

# =========================
# Mostrar cambios
# =========================
echo "=== git status ==="
git status
echo

# Si no hay cambios, salir limpio
if git diff --quiet && git diff --cached --quiet; then
  echo "No hay cambios por commitear. ✅"
else
  echo "=== Resumen de cambios (git diff --stat) ==="
  git diff --stat
  echo

  # =========================
  # Stage automático (solo archivos relevantes si existen)
  # =========================
  files_to_add=()

  if [[ -f "ganado/admin.py" ]]; then
    files_to_add+=("ganado/admin.py")
  fi

  if [[ -f "ganado/static/ganado/js/date_mask.js" ]]; then
    files_to_add+=("ganado/static/ganado/js/date_mask.js")
  fi

  if [[ "${#files_to_add[@]}" -eq 0 ]]; then
    echo "No encontré archivos esperados (ganado/admin.py o date_mask.js). Haré 'git add -A' para incluir todo."
    git add -A
  else
    echo "Agregando archivos:"
    for f in "${files_to_add[@]}"; do
      echo " - $f"
    done
    git add "${files_to_add[@]}"
  fi

  echo
  echo "=== Cambios staged ==="
  git diff --cached --stat
  echo

  # Mensaje de commit (puedes pasar uno como argumento)
  commit_msg="${1:-$DEFAULT_MESSAGE}"

  # Si no hay nada staged, no comitear
  if git diff --cached --quiet; then
    echo "No hay cambios staged para commit. ✅"
  else
    echo "Creando commit con mensaje: $commit_msg"
    git commit -m "$commit_msg"
    echo "✅ Commit creado."
  fi
fi

echo
echo "=== Verificando upstream de la rama ==="
if git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' >/dev/null 2>&1; then
  upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}')"
  echo "Upstream actual: $upstream"
else
  echo "No hay upstream configurado. Configurando a $REMOTE/$BRANCH_EXPECTED ..."
  git branch --set-upstream-to="$REMOTE/$BRANCH_EXPECTED" "$BRANCH_EXPECTED" 2>/dev/null || true
fi

echo
echo "=== Push de la rama ==="
git push -u "$REMOTE" "$BRANCH_EXPECTED"
echo "✅ Rama enviada a $REMOTE/$BRANCH_EXPECTED"
echo

# =========================
# Tag estable (auto-incremento)
# =========================
echo "=== Tag estable (opcional pero recomendado) ==="
# Base tag: v1.1.2.X
base="v1.1.2"
n=1
while git rev-parse -q --verify "refs/tags/${base}.${n}" >/dev/null; do
  n=$((n+1))
done
new_tag="${base}.${n}"

echo "Creando tag: $new_tag"
git tag "$new_tag"
git push "$REMOTE" "$new_tag"
echo "✅ Tag publicado: $new_tag"

echo
echo "✅ Listo. Estado final:"
git --no-pager log --oneline --decorate -n 5
