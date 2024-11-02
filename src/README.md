**Introduction** 

This repository has an outline of design/architecture of how to evolve or refactor the existing system
, to make it maintainable, scalable, adaptable for more use cases to be added in the future. And make the data flow linear and less confusing (can be reasoned why data flows from one direction to the other)
The design choices are explained as we go through each layer of the data processing system.
1. The codebase is not an implementation, rather it is just an outline of how to implement things, in the lakehouse architecture which I introduced in the existing design or seperation of concerns.
2. The CI/CD is not considered but touched on it, with the idea of workflows and how the images/applications are deployed.

**Architecture explanation**

![](../../../Desktop/Screenshot 2024-11-01 at 10.22.26.png)

We have multiple layers here as opposed to the current system design - which are outlined with dashes. The main objective is to 
1. Reduce the workload on the SQL server
2. Bring the data processing, OLAP queries and data modeling to the lakehouse
3. Version control the OLAP/OLTP process with tools like DBT(seperate codebase) or delta tables (with materialised views) or managed cloud solutions(like aws athena) for better code versioning, testing, readability.
4. Have all the raw events and modeled data in the data lake again for scaling and maintainability and use raw events for backfilling/further analysis.
5. Only use the SQL server as backend to the UI and for dashboarding.
6. There is an aspect of streaming or low latency pipelines which is touched but not elaborately designed.
7. Make the pipelines easy to backfill and make it idempotent.

All of these managed tools tools/tech used are AWS/GCP based which also can be translated to Azure (tools work similarly except that there might be minor changes with few implementation details changing)

Further explanation of the design in detail.

**Lakehouse Architecture**

Acts as a core component of the data architecture, the main reason for choosing this design is to have better governance, make the system scale for data heavy workloads, code maintainability, adapt to new use cases and versioning.

1. This acts as main entry point for all raw events bringing them into the data lake for hot storage (S3 like blob storage)
and cold storage for future processing/archiving(tools like glacier).
2. The raw events are date partitioned by date or any other attribute for better manageability.
3. These raw events are transformed/modelled to create fact and dimensions and stored in parquet format on tables such as delta tables by Databricks or Iceberg for versioning/cataloging/ACID complaince, reporting and analytical processing.
The reason to choose the storage data format and modelling here is to reduce the load on the transactional processing engines like SQL server (which might work poorly for analytical processing and might scale but at the cost of increase in cloud cost)
All of the data processing is implemented in the spark/EMR/Databricks platform, these are managed solutions for running spark in python or java, the reason for choosing them is the ability to scale, support and to reduce ops. 
EMR/Dataproc are cost effective but might require more ops, but Databricks provides a seamless solution with various tools in all aspect of data lifecycle.
4. The data is pulled in to the data lake through a pull mechanism from Python or Java jobs deployed in solutions like AWS batch (fetches from other third party REST APIs and tables) or through solutions like Fivetran (having integrations for various tools to bring data into the datalake),
the latter is a set and forget kind of tool with less ops but with more integrations with other system with low ops.
5. All of these jobs are scheduled through Airflow/prefect, hourly or daily depending on the need and makes the system/lake idempotent

![](../../../Desktop/Screenshot 2024-11-01 at 10.22.06.png)

**Serving Layer**

The Analytics VM is replaced with DBT or can be managed by materialised views in databricks.
1. This makes easy to run the analytical queries/modeling of the OLAP queries on the transformed delta table
2. Which can be used for ad hoc querying/dashboarding/version control and create the stream of analytics engineering which data analysts can consume/operate with.
3. And finally only the required datasets or facts are sent to SQL server for backend to reduce the load.
4. Tools such as Tableau or PowerBI can used and can be powered by the Databricks/Iceberg transformed tables and SQLserver for adhoc report generation

Now we have separated the OLAP and OLTP queries. The SQL servers and other data pipelines can also act as an input for the data lake, the OLAP queries are scheduled through Airflow and finally the OLTP queries can be version controlled with SQL queries.
The load on SQL server is greatly reduced and OLAP queries are effectively run because of the modelling and data storage considered optimally and have control over the cost of the cloud tools.
Later Data governance/cataloging is something which can be considered in the future.

The speed layer can act as an input for the transformed table by ingesting events from Kafka messaging service and prcessing them through streaming engines
and finally store them, since we choose data formats such as Delta tables/Iceberg tables it can work effeciently for both batch and streaming use cases.

**Requirements**

To run these scripts locally we need to have these below requirements. But as I said this is just a structure.
1. Python 3.10.0 (I just chose it since I used this version recently)
2. I did that by installing, pyenv, pyenv-virtualenv and then
commands: 

`%pyenv install 3.10.0`

`%pyenv virtualenv 3.10 trasnferroom_activity`

3. Run the below commands,

`echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc`

`echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
`

`echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
`

`echo 'eval "$(pyenv init -)"' >> ~/.zshrc
`

`echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
`

``source ~/.zshrc`
``

`%pyenv activate transferroom_activity
`

``%pip install -r requirements.txt`
``

or on bash
4. To run tests locally install **"Make"** by brew install make if on Mac or apt-get install -y make
5. And then add the python path : `export PYTHONPATH="/transferrrom_activity:$PYTHONPATH"`
6. To run the tests run make test or pytest tests/
7. To run the main program run `spark-submit src/app/modeling_application.py`

**Explanation**

1. The project has an app folder which is the main entry point of the script
2. There is a models foldr, where all the schemas are placed (It is always better to provide schemas explicitely)
3. The transformations folder has implementation of all the methods the main script calls, I have separated and parameterised the modules so we can test them easily.
4. resources folder has files or might contain configs in future if needed for various environments to be used in the script and also has the output folder for this activity.
5. There is a Makefile which can be used to run commands in CI to install dependancies and make a checking for the test to pass before deploying
6. I did not create a deployment mechanism, but the commands I provide below can be added to a bash script or in a Dockerfile to be deployed.
7. I have used Pyspark as the engine so that even if there is change in size of data or running engine (either EMR or databricks etc) we can deploy the script and run by tweaking few parameters like partition and different sources and sinks.

**Things not considered**
1. The CD part is not considered since I felt currently all these commands can be run locally for testing
2. If the project evolves we can create a Dockerfile with all the commands I mentioned above and can be deployed as an docker image for EMR or databricks engine.

The makefile can be used for CI and can be used in github worflow for deployment as well.