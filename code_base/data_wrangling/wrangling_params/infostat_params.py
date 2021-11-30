
from code_base.data_wrangling.groupings.group_eurostat_data import GroupByAgeSexLocation, GroupBySexLocation


class InfostatWranglingParams:

    GROUP_DATA_BY_POPULATION = {
        'asl': GroupByAgeSexLocation,
        'sl': GroupBySexLocation
    }