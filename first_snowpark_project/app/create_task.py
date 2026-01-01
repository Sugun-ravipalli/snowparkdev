from snowflake.core import Root
from snowflake.snowpark import Session
import snowflake.connector
from datetime import timedelta
from snowflake.core.task import Task, StoredProcedureCall
import procedures
from snowflake.core.task.dagv1 import DAG, DAGTask, DAGOperation, CreateMode

# Create a Snowpark session with custom package uploads enabled
session = Session.builder.getOrCreate()
session.custom_package_usage_config = {"enabled": True}
print("connected to snowflake with custom package uploads enabled")

# Get root object from session
root = Root(session)
print("got root object")

#create task definition

my_task = Task("my_task",StoredProcedureCall(procedures.hello_procedure,args= ["sugun"],\
            stage_location="@dev_deployment"), warehouse="COMPUTE_WH", schedule = timedelta(hours=1))

tasks = root.databases["DEMO_DB"].schemas["PUBLIC"].tasks

#tasks.create(my_task)

with DAG("my_dag", schedule=timedelta(days=1)) as dag:
    task1 = DAGTask("hello_task", StoredProcedureCall(procedures.hello_procedure,args= ["sugun"],\
                                                      packages=["snowflake-snowpark-python"],imports=["@dev_deployment/my_snowpark_project/app.zip"],\
                                                       stage_location="@dev_deployment"), warehouse="COMPUTE_WH")
    task2 = DAGTask("Test_task", StoredProcedureCall(procedures.test_procedure,\
                                                     packages=["snowflake-snowpark-python"],imports=["@dev_deployment/my_snowpark_project/app.zip"],\
                                                          stage_location="@dev_deployment"), warehouse="COMPUTE_WH")
    task3 = DAGTask("Test_task3", StoredProcedureCall(procedures.test_procedure_two,\
                                                        packages=["snowflake-snowpark-python"],imports=["@dev_deployment/my_snowpark_project/app.zip"],\
                                                            stage_location="@dev_deployment"), warehouse="COMPUTE_WH")
    task4 = DAGTask("Test_task4", StoredProcedureCall(procedures.test_procedure,\
                                                     packages=["snowflake-snowpark-python"],imports=["@dev_deployment/my_snowpark_project/app.zip"],\
                                                          stage_location="@dev_deployment"), warehouse="COMPUTE_WH")
    
    task1 >> task2 >> [task3, task4]  # Define dependencies

    schema = root.databases["DEMO_DB"].schemas["PUBLIC"]
    dag_op = DAGOperation(schema)
    dag_op.deploy(dag,CreateMode.or_replace)