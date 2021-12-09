from pathlib import Path
import stat


def is_under(path: Path, parent: Path) -> bool:
    try:
        _ = path.relative_to(parent)
        return True
    except ValueError:
        return False


class Walker:
    def __init__(self, root: Path) -> None:
        self._walk(root.resolve())

    def _walk(self, directory: Path) -> None:
        for path in directory.iterdir():
            if not path.is_symlink():
                if path.is_dir():
                    self.act_on_directory(path)
                    self._walk(path)

                elif path.is_file():
                    self.act_on_file(path)

    def act_on_file(self, path: Path) -> None:
        file_stat = path.stat()

        # File gets ug+rw and g=u
        mode = file_stat.st_mode
        mode |= stat.S_IRUSR | stat.S_IWUSR
        mode |= (mode & stat.S_IRWXU) >> 3
        path.chmod(mode)

        print(f"File\t{path}\tug+rw,g=u")

    def act_on_directory(self, directory: Path) -> None:
        # Directory gets ug+wx
        mode = directory.stat().st_mode
        mode |= stat.S_IWUSR | stat.S_IXUSR | stat.S_IWGRP | stat.S_IXGRP
        directory.chmod(mode)

        print(f"Directory\t{directory}\tug+wx")
