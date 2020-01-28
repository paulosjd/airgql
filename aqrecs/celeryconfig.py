#
# broker_url = 'amqp://127.0.0.1:5672'
#
# result_backend = 'redis://localhost:6379/0'
#
# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']
# timezone = 'Europe/London'
# enable_utc = True
#
# celery_default_queue = 'pyratest'
# celery_default_exchange = 'pyratest'
# celery_default_exchange_type = 'direct'
# celery_default_routing_key = 'pyratest'
#
# imports = ('pyratest.tasks.orders_report', 'pyratest.tasks.notifier_task')
#
# celery_routes = {
#     'mytask1': {'queue': 'test_queue_name_for_task'},
#     'account_task': {'queue': 'low_priority'},
#     'mytask3': {'queue': 'low_priority'},
#     'notifier_task': {'queue': 'low_priority'}
# }
#
