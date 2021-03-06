--determine linked places
-- places with label tag
UPDATE osm_polygon p
  SET linked_osm_id = r.member_id
FROM osm_relation_member r
WHERE r.member_type = 0
      AND r.role = 'label'
      AND p.osm_id = r.osm_id;

-- places with admin_centre tag
UPDATE osm_polygon p
  SET linked_osm_id = r.member_id
FROM osm_relation_member r
  WHERE r.member_type = 0
        AND (r.role = 'admin_centre' OR r.role = 'admin_center')
        AND p.name = r.name
        AND p.osm_id = r.osm_id
        AND p.linked_osm_id IS NULL;

--tag linked places
UPDATE osm_point p
  SET linked = TRUE
FROM osm_point po
WHERE po.osm_id IN (SELECT linked_osm_id FROM osm_polygon WHERE linked_osm_id IS NOT NULL)
      AND po.osm_id = p.osm_id;

CREATE INDEX IF NOT EXISTS idx_osm_point_linked_false ON osm_point(linked) WHERE linked IS FALSE;
