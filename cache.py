from celery import Celery, Task

celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

class BaseTask(Task):
    """BaseTask child with useful extra functionalities"""
    abstract = True

    # def __call__(self, *args, **kwargs):
    #     Task.__call__(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        print("CALLED!")
        return super(BaseTask, self).__call__(*args, **kwargs)

    def get_desc(self):
        """Returns useful informations on the task
        :return: Object containing useful info concerning the task (id,name,status,info)
        """
        task_id = self.request.id
        rv = self.AsyncResult(task_id)

        # try:
        #     status = rv.state
        # except AttributeError:
        #     status = None
        # try:
        #     info = rv.info
        # except AttributeError:
        #     info = None

        
        status = rv.state
        
        
        info = rv.info
        

        return {
            'id': task_id,
            'name': self.name,
            'status': status,
            'info': info
        }

    def update_progress(self, title=None, progress=None, total=None):
        """Helper function to easily update metadata in a formatted way
        :param title:The title of the current step in the task
        :param progress: The current step count of the task
        :param total: The current scale (from 0 to total) on which is based the progress
        """
        # We fetched the previously saved meta state and overwrite with the given
        # new meta state
        result = self.AsyncResult(self.request.id)
        current_meta = result.info if result.state == 'PROGRESS' else {'title': '', 'progress': 'unknown', 'total': 100}
        meta = {
            'title': title or current_meta['title'],
            'progress': progress or current_meta['progress'],
            'total': total or current_meta['total']
        }
        # logger.debug(meta)
        self.update_state(state='PROGRESS', meta=meta)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """Sends a socketio update_task message when task finishes"""
        super().after_return(status, retval, task_id, args, kwargs, einfo)
        

    # def on_failure(self, exc, task_id, args, kwargs, einfo):
    #     logger.info(retval)

    def on_success(self, retval, task_id, args, kwargs):
        print(retval)

    def update_state(self, task_id=None, state=None, meta=None):
        """Sends a socketio update_task message when task state is updated"""
        super().update_state(task_id, state, meta)
        
# we monkey-patch the celery default task to use the previously defined as default
# this requires to call celery from this module
celery.Task = BaseTask
