import os
import pytest

from osmnames.database.functions import exec_sql_from_file
from osmnames.prepare_data.prepare_housenumbers import set_street_attributes_by_street_relation_members


@pytest.fixture(scope="function")
def schema(engine):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    exec_sql_from_file('../fixtures/test_prepare_imported_data.sql.dump', cwd=current_directory)


def test_street_id_and_name_set_if_street_in_relation_exists(session, schema, tables):
    session.add(tables.osm_housenumber(id=1, osm_id=1111))
    session.add(tables.osm_relation(osm_id=-9999, type="associatedStreet"))
    session.add(tables.osm_relation_member(osm_id=-9999, member_id=1111, role="house"))
    session.add(tables.osm_relation_member(osm_id=-9999, member_id=1337, role="street"))
    session.add(tables.osm_linestring(osm_id=1337, name="Ruetistrasse"))

    session.commit()

    set_street_attributes_by_street_relation_members()

    assert session.query(tables.osm_housenumber).get(1).street_id == 1337
    assert str(session.query(tables.osm_housenumber).get(1).street) == "Ruetistrasse"


def test_street_id_correctly_set_if_linestring_is_merged(session, schema, tables):
    session.add(tables.osm_housenumber(id=1, osm_id=1111))
    session.add(tables.osm_relation(osm_id=-9999, type="associatedStreet"))
    session.add(tables.osm_relation_member(osm_id=-9999, member_id=1111, role="house"))
    session.add(tables.osm_relation_member(osm_id=-9999, member_id=1337, role="street"))
    session.add(tables.osm_linestring(osm_id=1337, merged_into=42, name="Ruetistrasse"))

    session.commit()

    set_street_attributes_by_street_relation_members()

    assert session.query(tables.osm_housenumber).get(1).street_id == 42
    assert str(session.query(tables.osm_housenumber).get(1).street) == "Ruetistrasse"
