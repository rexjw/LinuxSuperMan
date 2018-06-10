from pathlib import Path

import logging
_l = logging.getLogger('pipeline')


class Pipeline:
    def __init__(self, conf=None, data_dir=None, force=False):
        self._conf = conf
        self._data_dir = data_dir
        self._force = not not force

        self._ctx = None
        self._task_class_list = []

    def append_task(self, task_class, force=None):
        self._task_class_list.append((task_class, not not force))
        _l.debug(task_class)

    def execute(self):
        data_path = Path(self._data_dir)
        result, c = True, 0
        for (task_class, force) in self._task_class_list:
            _i = data_path / ("_%d" % c)
            _o = data_path / ("_%d" % (c+1))
            _l.debug(_i)
            _l.debug(_o)
            task = task_class(_i, _o, force or self._force)
            _l.debug(task)
            result = task.execute()
            if result is True:
                c += 1
            else:
                break
        pass



