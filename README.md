```python
# Utilities
  crossdomain()
  jsonify_error_handler(error)
﫧 find_geoid(geoid, acs=None)
  before_request()
  get_acs_name(acs_slug)
﫧 convert_row(row)

# Geographies
  compute_profile_item_levels(geoid)
  geo_search()
  geo_tiles(sumlevel, zoom, x, y)
  geo_lookup(release, geoid)
  geo_parent(release, geoid)

# Tables (and/or columns)
  format_table_search_result(obj, obj_type, release)
  table_search()
  tabulation_details(tabulation_id)
table_details(table_id)
table_details_with_release(release, table_id)
table_geo_comparison_rowcount(table_id)

# Data
  download_specified_data(*args, **kwargs)
  _download_specified_data(acs)
﫧 show_specified_geo_data(release)
show_specified_data(acs)
get_variables_for_data(acs)
data_compare_geographies_within_parent(acs, table_id)
  get_data_fallback(table_ids, geoids, acs=None)

  healthcheck()
  robots_txt()
  index()
```
