# import time
#
# import requests
#
# from airgql.tasks.celery_app import celery_app
#
#
# class NotifierTask(celery_app.Task):
#     """ Task that sends notification on completion """
#
#     def after_return(self, status, retval, task_id, args, kwargs, einfo):
#         """ Handler called after the task returns; return value ignored """
#         url = 'http://localhost:3000/notify'
#         print(f'Task after_return method clientid kwargs: {kwargs["clientid"]}')
#         data = {'clientid': kwargs['clientid'], 'result': retval}
#         requests.post(url, data=data)
#
#
# @celery_app.task(base=NotifierTask)
# def notifier_task(clientid=None):
#     """ Simulates some slow computation """
#     time.sleep(7)
#     return 42
