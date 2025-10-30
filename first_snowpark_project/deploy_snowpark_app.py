import sys
import os
import yaml

directory_path = sys.argv[1]
os.chdir(f"{directory_path}")

#make sure all 6 snowflake account env variables are set
#SnowCLI access the password directly from the SNOWFLAKE_PASSWORD env variable

os.system(f"snow snowpark build")
os.system(f"snow snowpark deploy --replace --temporary-connection --account=$SNOWFLAKE_ACCOUNT --user=$SNOWFLAKE_USER --role=$SNOWFLAKE_ROLE --warehouse=$SNOWFLAKE_WAREHOUSE --database=$SNOWFLAKE_DATABASE --schema=$SNOWFLAKE_SCHEMA")