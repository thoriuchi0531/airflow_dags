from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

venv = 'production'
github_dir = '~/Documents/github/'
root_dir = '{github_dir}adagio_backtest/adagio_backtest/'.format(github_dir=github_dir)
default_args = {
    'owner': 'thoriuchi0531',
    'depends_on_start': True,
    'start_date': datetime(2018, 1, 1, 6, 0),
    'email': ['thoriuchi0531@gmail.com'],
    'email_on_failure': ['thoriuchi0531@gmail.com'],
    'email_on_retry': ['thoriuchi0531@gmail.com'],
    'retries': 0,
}

dag = DAG('daily_backtest_update',
          default_args=default_args,
          schedule_interval='25 4 * * *',
          catchup=False)

task_fx = BashOperator(
    task_id='save_fx_rates',
    bash_command='source activate {venv}; '
                 'cd {root_dir};'
                 'python save_fx_rates.py'
        .format(venv=venv, root_dir=root_dir),
    dag=dag
)

task_cash = BashOperator(
    task_id='save_cash_returns',
    bash_command='source activate {venv};'
                 'cd {root_dir};'
                 'python save_cash_returns.py'
        .format(venv=venv, root_dir=root_dir),
    dag=dag
)

task_longonly = BashOperator(
    task_id='run_longonly',
    bash_command='source activate {venv};'
                 'cd {root_dir};'
                 'python run_longonly.py'
        .format(venv=venv, root_dir=root_dir),
    dag=dag
)

task_longonly.set_upstream(task_fx)
