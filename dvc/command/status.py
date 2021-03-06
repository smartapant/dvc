from dvc.command.data_sync import CmdDataBase


class CmdDataStatus(CmdDataBase):
    STATUS_LEN = 10
    STATUS_INDENT = '\t'

    def _normalize(self, s):
        s += ':'
        assert len(s) < self.STATUS_LEN
        return s + (self.STATUS_LEN - len(s))*' '

    def _show(self, status, indent=0):
        ind = indent * self.STATUS_INDENT

        for key, value in status.items():
            if isinstance(value, dict):
                self.project.logger.info('{}{}'.format(ind, key))
                self._show(value, indent+1)
            else:
                msg = '{}{}{}'.format(ind, self._normalize(value), key)
                self.project.logger.info(msg)

    def do_run(self, target=None):
        indent = 1 if self.args.cloud else 0
        try:
            st = self.project.status(target=target,
                                     jobs=self.args.jobs,
                                     cloud=self.args.cloud,
                                     show_checksums=self.args.show_checksums,
                                     remote=self.args.remote)
            if st:
                self._show(st, indent)
            else:
                self.project.logger.info("Nothing to reproduce. "
                                         "Pipeline is up to date.")
        except Exception as exc:
            self.project.logger.error('Failed to obtain data status', exc)
            return 1
        return 0
