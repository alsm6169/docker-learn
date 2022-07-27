import os
from datetime import datetime

from airflow.decorators import dag, task  # DAG and task decorators for interfacing with the TaskFlow API
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule  # Used to change how an Operator is triggered
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


@dag(
    # This defines how often your DAG will run, or the schedule by which your DAG runs. In this case, this DAG
    # will run daily
    schedule_interval='0 23 * * *',
    # This DAG is set to run for the first time on January 1, 2021. Best practice is to use a static
    # start_date. Subsequent DAG runs are instantiated based on scheduler_interval
    start_date=datetime(2022, 1, 1),
    # When catchup=False, your DAG will only run for the latest schedule_interval. In this case, this means
    # that tasks will not be run between January 1, 2021 and 30 mins ago. When turned on, this DAG's first
    # run will be for the next 30 mins, per the schedule_interval
    catchup=False,
    default_view='graph',
    default_args={
        'retries': 2,  # If a task fails, it will retry 2 times.
    },
    tags=['market data loader'])  # If set, this tag is shown in the DAG view of the Airflow UI
def load_market_data():
    # DummyOperator placeholder for first task
    begin = EmptyOperator(task_id='begin')

    @task()
    def check_env_var():
        print(f'os.getcwd(): {os.getcwd()}')
        print(os.listdir(os.getcwd()))
        print(f'APP_INPUT_DIR: {os.getenv("APP_INPUT_DIR")}')
        print(f'APP_OUTPUT_DIR: {os.getenv("APP_OUTPUT_DIR")}')
        print(f'MYSQL_DATABASE: {os.getenv("MYSQL_DATABASE")}')
        print(f'MYSQL_USER: {os.getenv("MYSQL_USER")}')
        print(f'MYSQL_PASSWORD: {os.getenv("MYSQL_PASSWORD")}')
        print(f'MYSQL_DB_PORT: {os.getenv("MYSQL_DB_PORT")}')
        return os.getcwd(), os.listdir(os.getcwd())

    pre_step = DockerOperator(
        task_id='test_dockeroperator',
        image='alpine',
        api_version='auto',
        command='/bin/touch /output/run_docker_touch.txt',
        auto_remove=True,
        # below is example of not hard-coded path
        mounts=[
            Mount(source='/Users/anirudh/Documents/Python/GitHub/docker-learn/docker007/output',
                  target='/output',
                  type='bind'),
        ],
        mount_tmp_dir=False,
        docker_url='tcp://docker-proxy:2375',
        network_mode='bridge'
    )

    eod_price_file = DockerOperator(
        task_id='eod_price_file',
        image='eod_price',
        api_version='auto',
        command='python eod_price.py ACN -b 15 -f out.csv',
        mounts=[
            Mount(source=os.getenv("APP_OUTPUT_DIR"),
                  target='/app_base/output',
                  type='bind'),
        ],
        auto_remove=True,
        mount_tmp_dir=False,
        docker_url='tcp://docker-proxy:2375',
        network_mode='bridge'
    )

    eod_price_db = DockerOperator(
        task_id='eod_price_db',
        image='eod_price',
        api_version='auto',
        command='python eod_price.py AAPL -b 10 -d',
        environment={
            'MYSQL_DATABASE': os.getenv("MYSQL_DATABASE"),
            'MYSQL_USER': os.getenv('MYSQL_USER'),
            'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
            'MYSQL_DB_PORT': os.getenv('MYSQL_DB_PORT')
        },
        auto_remove=True,
        mount_tmp_dir=False,
        docker_url='tcp://docker-proxy:2375',
        network_mode='bridge'
    )

    @task(task_id='last_msg', retries=3)
    def end_msg():
        print('Docker command executed successfully')
        return str('Docker command executed successfully')

    # Last task will only trigger if no previous task failed
    end = EmptyOperator(task_id='end', trigger_rule=TriggerRule.NONE_FAILED)

    begin >> check_env_var() >> pre_step >> eod_price_file >> eod_price_db >> end_msg() >> end


dag = load_market_data()
