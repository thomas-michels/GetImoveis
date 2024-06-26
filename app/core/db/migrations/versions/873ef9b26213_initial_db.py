"""initial-db

Revision ID: 873ef9b26213
Revises: 
Create Date: 2023-08-09 23:21:12.250870

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '873ef9b26213'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"""         

CREATE TABLE companies (
	id serial4 NOT NULL,
	name varchar(50) NOT NULL,
	CONSTRAINT company_pk PRIMARY KEY (id)
);

CREATE TABLE neighborhoods (
	id serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	population int4 NULL,
	houses int4 NULL,
	area numeric(10, 5) NULL,
	CONSTRAINT neighborhood_pk PRIMARY KEY (id),
	CONSTRAINT neighborhood_un UNIQUE (name)
);

CREATE TABLE streets (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	neighborhood_id int4 NOT NULL,
	zip_code varchar NULL,
	flood_quota numeric NULL,
	latitude varchar(20) NULL,
	longitude varchar(20) NULL,
	CONSTRAINT street_pk PRIMARY KEY (id),
	CONSTRAINT streets_un UNIQUE (name, zip_code),
	CONSTRAINT street_fk FOREIGN KEY (neighborhood_id) REFERENCES neighborhoods(id)
);
CREATE INDEX streets_name_idx ON streets USING btree (name);
CREATE INDEX streets_zip_code_idx ON streets USING btree (zip_code);

CREATE TABLE modalities (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	CONSTRAINT modality_pk PRIMARY KEY (id)
);

CREATE TABLE properties (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	code int8 NOT NULL,
	title varchar(255) NULL,
	price double precision NOT NULL,
	description varchar NULL,
	neighborhood_id int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	rooms int2 NOT NULL,
	bathrooms int2 NOT NULL,
	"size" numeric NOT NULL,
	parking_space int2 NOT NULL,
	modality_id int4 NOT NULL,
	image_url varchar NOT NULL,
	property_url varchar NOT NULL,
	"type" varchar NOT NULL,
	street_id int4 NULL,
	"number" varchar(20) NULL,
	is_active bool NOT NULL DEFAULT true,
	CONSTRAINT property_pk PRIMARY KEY (id),
	CONSTRAINT property_unique UNIQUE (company_id, code),
	CONSTRAINT properties_fk FOREIGN KEY (neighborhood_id) REFERENCES neighborhoods(id),
	CONSTRAINT property_fk FOREIGN KEY (company_id) REFERENCES companies(id),
	CONSTRAINT property_modality_fk FOREIGN KEY (modality_id) REFERENCES modalities(id),
	CONSTRAINT property_street_fk FOREIGN KEY (street_id) REFERENCES streets(id)
);

CREATE TABLE property_histories (
	id serial4 NOT NULL,
	property_id int4 NOT NULL,
	price double precision NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT property_histories_pk PRIMARY KEY (id),
	CONSTRAINT property_histories_fk FOREIGN KEY (property_id) REFERENCES properties(id)
);

CREATE TABLE events (
	id uuid NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	sent_to varchar(50) NOT NULL,
	payload jsonb NOT NULL,
	origin varchar(50) NOT NULL,
	CONSTRAINT events_pk PRIMARY KEY (id, origin, sent_to)
);

""")


def downgrade() -> None:
    pass
