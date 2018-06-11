from pathlib import Path
import shutil

import logging
_l = logging.getLogger('task')


class Task(object):

    MAGIC_FILE_DONE = '_DONE'

    def __init__(self, in_path: Path, out_path: Path, force=False, name=None):
        self._i_path = in_path
        self._o_path = out_path
        self._name = name or self.__class__.__name__
        self._force = force

        _l.info("Create task %s: %s --> %s" % (self._name, self._i_path.name, self._o_path.name))

    def _check_output_dir(self):
        """
        :return: True or False
        """
        if self._o_path.exists():
            if self._o_path.is_dir():
                if self._force:
                    _l.warning("FORCE RE-EXECUTE! Remove target directory. (%s)" % self._o_path.name)
                    shutil.rmtree(self._o_path, ignore_errors=True)

                else:
                    if (self._o_path / self.MAGIC_FILE_DONE).exists():
                        _l.info("Already Done! (%s)" % self._name)
                        return True

            else:
                raise Exception("Target directory already exists and is not a directory! (%s)" % self._o_path)

        self._o_path.mkdir(exist_ok=True)
        return None

    def _done(self):
        (self._o_path / self.MAGIC_FILE_DONE).touch()

    def execute(self):
        return False


class PrepareManFiles(Task):
    def __init__(self, i_path, o_path, force=False):
        super().__init__(i_path, o_path, force)

    def execute(self):
        result = self._check_output_dir()
        if result is not None:
            return result

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

        self._done()

        return False


class SimpleTask(Task):
    def __init__(self, i_path, o_path, force):
        super().__init__(i_path, o_path, force)

    def execute(self):
        result = self._check_output_dir()
        if result is not None:
            return result

        for i_file in sorted(self._i_path.glob('man*')):
            _l.debug("==> %s" % i_file)
            o_file = self._o_path / i_file.name
            result = self._on_file(i_file, o_file)
            if result is not True:
                break

        if result is True:
            self._done()

    def _on_file(self, i_file: Path, o_file: Path):
        return False


class PlainManTask(SimpleTask):
    def __init__(self, i_path, o_path, force):
        super().__init__(i_path, o_path, force)

    def _done(self):
        pass

    def _on_file(self, i_file, o_file):
        with i_file.open() as i_f, o_file.open(mode='w') as o_f:
            buff = ""

            for line in i_f:
                if line.startswith('.\\"') or line.startswith('.TH'):
                    continue

                elif line.startswith('.SH COLOPHON'):
                    if len(buff):
                        o_f.write(buff)
                        o_f.write('\n')
                    break

                elif line.startswith('.SH'):
                    if len(buff):
                        o_f.write(buff)
                        o_f.write('\n')
                        buff = ""
                    continue

                else:
                    pass

                line = line.strip()
                if len(line):
                    buff += line
                    if buff[-1] in '.:':
                        o_f.write(buff)
                        o_f.write('\n')
                        buff = ""
                    else:
                        buff += ' '

        return False
