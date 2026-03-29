from hale_hub.outlet_interface import get_outlets


class _HomeStatsCollection:

    def get_formatted_home_stats(self):
        """Return current outlet states for API responses."""
        formatted_home_stats = dict()

        outlets = get_outlets()
        outlets_key = 'Outlets'
        formatted_home_stats[outlets_key] = list()
        for outlet in outlets:
            if not outlet.state:
                outlet_state_string = "Off"
            else:
                outlet_state_string = "On"
            outlet_string = '{}: {}'.format(outlet.name, outlet_state_string)
            formatted_home_stats[outlets_key].append(outlet_string)

        return formatted_home_stats


# Expose these functions
_home_stats = _HomeStatsCollection()
get_formatted_home_stats = _home_stats.get_formatted_home_stats
