from pathlib import Path
import shutil

import logging
_l = logging.getLogger('task')


class Task(object):
    def __init__(self, in_path: Path, out_path: Path, force=False):
        self._i_path = in_path
        self._o_path = out_path
        self._force = force

    def execute(self):
        return False


class PrepareManFiles(Task):
    def __init__(self, i_path, o_path, force=False):
        super().__init__(i_path, o_path, force)

    def execute(self):
        if self._o_path.exists():
            if self._o_path.is_dir():
                if self._force:
                    _l.warning("FORCE RE-EXECUTE! Remove target directory. (%s)" % self._o_path.name)
                    shutil.rmtree(self._o_path, ignore_errors=True)

                else:
                    if (self._o_path / '_DONE').exists():
                        _l.info("Already Done!")
                        return True

            else:
                raise Exception("Target directory already exists and is not a directory! (%s)" % self._o_path)

        self._o_path.mkdir(exist_ok=True)

        for manx_path in sorted(self._i_path.glob('man*')):
            manx = manx_path.name
            for manf in sorted(manx_path.glob("*.%s" % manx[-1])):
                if manf.stat().st_size < 128:
                    if manf.read_text().startswith(".so "):
                        _l.warning("xxx> %s" % manf)
                        continue
                out = self._o_path / ("%s_%s" % (manx, manf.name))
                _l.debug("%s ==> %s" % (manf, out))
                shutil.copy(manf, out)

        return False


class SimpleTask(Task):
    def __init__(self, i_path, o_path, force):
        super().__init__(i_path, o_path, force)

    def execute(self):
        pass
