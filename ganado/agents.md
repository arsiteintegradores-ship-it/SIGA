# Reglas para Codex - SIGA (Django + MySQL)

- No cambiar `managed = False` ni `db_table` sin pedirlo explícitamente.
- Preferir propiedades `@property` para campos calculados (edad, etapa).
- En exports (Excel/PDF): nunca escribir tuplas; convertir a texto.
- Antes de finalizar: correr `python manage.py check` y, si aplica, `python manage.py runserver` (ver que no truene).
- Mantener código claro y listo para copiar/pegar.
- Si hay riesgo de integridad (FK RESTRICT), preferir "desactivar" (campo activo) en lugar de borrar.
