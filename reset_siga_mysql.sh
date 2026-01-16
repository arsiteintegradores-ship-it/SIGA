#!/usr/bin/env bash
set -euo pipefail

DB_NAME="${DB_NAME:-siga_db}"
DB_USER="${DB_USER:-siga_user}"
DB_PASS="${DB_PASS:-Siga2026*Segura}"

MYSQL_HOST="${MYSQL_HOST:-localhost}"
MYSQL_PORT="${MYSQL_PORT:-3306}"

MYSQL_ADMIN_USER="${MYSQL_ADMIN_USER:-root}"
MYSQL_ADMIN_PASS="${MYSQL_ADMIN_PASS:-}"  # si lo dejas vacío, te lo pedirá

mysql_admin() {
  if [[ -n "${MYSQL_ADMIN_PASS}" ]]; then
    mysql -h "${MYSQL_HOST}" -P "${MYSQL_PORT}" -u "${MYSQL_ADMIN_USER}" -p"${MYSQL_ADMIN_PASS}"
  else
    mysql -h "${MYSQL_HOST}" -P "${MYSQL_PORT}" -u "${MYSQL_ADMIN_USER}" -p
  fi
}

echo "⚠️  ATENCIÓN: Esto borrará COMPLETAMENTE la BD '${DB_NAME}' y la recreará desde cero."
echo

mysql_admin <<SQL
DROP DATABASE IF EXISTS \`${DB_NAME}\`;

CREATE DATABASE \`${DB_NAME}\`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

DROP USER IF EXISTS '${DB_USER}'@'localhost';
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;

USE \`${DB_NAME}\`;
SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE ganado_productor (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  apellido_paterno VARCHAR(120) NULL,
  apellido_materno VARCHAR(120) NULL,
  direccion VARCHAR(180) NULL,
  telefono VARCHAR(25) NULL,
  email VARCHAR(100) NULL,
  activo BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_productor_nombre (nombre, apellido_paterno, apellido_materno)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_finca (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL UNIQUE,
  ubicacion VARCHAR(180) NULL,
  hectareas DECIMAL(10,2) NULL,
  propietario VARCHAR(120) NULL,
  telefono VARCHAR(25) NULL,
  activo BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_upp (
  id INT AUTO_INCREMENT PRIMARY KEY,
  finca_id INT NOT NULL,
  productor_id INT NOT NULL,
  clave VARCHAR(30) NULL UNIQUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_upp_finca (finca_id),
  KEY idx_upp_productor (productor_id),
  CONSTRAINT fk_ganado_upp_finca FOREIGN KEY (finca_id) REFERENCES ganado_finca(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ganado_upp_productor FOREIGN KEY (productor_id) REFERENCES ganado_productor(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_color (
  id INT AUTO_INCREMENT PRIMARY KEY,
  color VARCHAR(120) NOT NULL UNIQUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_raza (
  id INT AUTO_INCREMENT PRIMARY KEY,
  raza VARCHAR(120) NOT NULL UNIQUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_registro (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_madre VARCHAR(120) NULL,
  id_padre VARCHAR(120) NULL,
  id_abuelo VARCHAR(120) NULL,
  id_abuela VARCHAR(120) NULL,
  id_bovino VARCHAR(120) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_registro_bovino (id_bovino)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_lote (
  id INT AUTO_INCREMENT PRIMARY KEY,
  finca_id INT NOT NULL,
  nombre VARCHAR(80) NOT NULL,
  descripcion VARCHAR(200) NULL,
  activo BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_lote_finca_nombre (finca_id, nombre),
  KEY idx_lote_finca (finca_id),
  CONSTRAINT fk_ganado_lote_finca FOREIGN KEY (finca_id) REFERENCES ganado_finca(id)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ganado_animal (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_interno VARCHAR(50) NULL UNIQUE,
  id_siniga VARCHAR(50) NULL UNIQUE,
  nombre_bov VARCHAR(80) NULL,
  fecha_nacimiento DATE NULL,
  peso_nacimiento DECIMAL(6,2) NULL,
  peso_destete DECIMAL(6,2) NULL,
  productor_id INT NULL,
  upp_id INT NULL,
  color_id INT NULL,
  raza_id INT NULL,
  registro_id INT NULL,
  sexo ENUM('M','H') NOT NULL,
  padre_id INT NULL,
  madre_id INT NULL,
  finca_id INT NOT NULL,
  lote_id INT NULL,
  estado ENUM('ACTIVO','VENDIDO','MUERTO','BAJA') NOT NULL DEFAULT 'ACTIVO',
  notas TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY idx_animal_finca (finca_id),
  KEY idx_animal_lote (lote_id),
  KEY idx_animal_raza (raza_id),
  KEY idx_animal_padre (padre_id),
  KEY idx_animal_madre (madre_id),
  CONSTRAINT fk_ganado_animal_productor FOREIGN KEY (productor_id) REFERENCES ganado_productor(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_upp FOREIGN KEY (upp_id) REFERENCES ganado_upp(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_color FOREIGN KEY (color_id) REFERENCES ganado_color(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_raza FOREIGN KEY (raza_id) REFERENCES ganado_raza(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_registro FOREIGN KEY (registro_id) REFERENCES ganado_registro(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_finca FOREIGN KEY (finca_id) REFERENCES ganado_finca(id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ganado_animal_lote FOREIGN KEY (lote_id) REFERENCES ganado_lote(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_padre FOREIGN KEY (padre_id) REFERENCES ganado_animal(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_ganado_animal_madre FOREIGN KEY (madre_id) REFERENCES ganado_animal(id)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS=1;
SQL

echo "✅ Listo: se borró todo y se recreó '${DB_NAME}' desde cero."
