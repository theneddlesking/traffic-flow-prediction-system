from sources import sources

from cache import default_cache


# get all locations

locations = default_cache.site_controller.get_locations()

# get all location names

location_names = [location.name for location in locations]

print(len(location_names))
print(len(set(location_names)))

# find duplicates

duplicates = [name for name in location_names if location_names.count(name) > 1]

# HIGH_ST NE of CHARLES_ST is duplicated, but for different locations
print(duplicates)

# sources

sources = sources

# get all location names from sources

location_names = [source.location_name for source in sources]

print(len(location_names))
print(len(set(location_names)))

# diff

diff = set(location_names) - set(location_names)

print(diff)
